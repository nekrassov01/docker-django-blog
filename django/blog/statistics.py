"""
開発初期段階では、サイトレポートをVIEWに直書きしていた
パフォーマンス改善のため、バッチ処理に変更
このVIEWは今は使われていないが、一応残しておく
"""

from django.conf import settings
from django.db.models import Q, Count
from django.db.models.functions import TruncMonth
from django.utils import html
from .models import Post, Category, Tag
from datetime import datetime
from collections import Counter
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *
import itertools

""" データ可視化 """
def statistics(request):
    label = 'データ可視化'

    """
    基本のクエリセット
    """

    """ queryset | 公開されている記事一覧 """
    published_post = Post.objects.select_related('category').prefetch_related('tag').filter(is_public=True).order_by('published_at', 'created_at', 'updated_at')

    """ queryset | （紐づく記事が）公開されているカテゴリ一覧 """
    published_category = Category.objects.filter(post__is_public=True).order_by('index')

    """ queryset | （紐づく記事が）公開されているタグ一覧 """
    published_tag = Tag.objects.filter(post__is_public=True).order_by('name')

    """
    カテゴリを基準とした集計
    """

    """ list | カテゴリ一覧からカテゴリ名のリストを作る """
    category_list = list(published_category.distinct().values_list('name', flat=True))

    """ list | カテゴリ一覧からカテゴリ別記事数のリストを作る """
    category_post_list = list(published_category.annotate(count=Count('post')).values_list('count', flat=True))

    """ list | カテゴリ一覧からカテゴリ別タグ数のリストを作る """
    category_tag_list = list(published_category.annotate(count=Count('tag', filter=Q(tag__post__is_public=True), distinct=True)).values_list('count', flat=True))

    """ dict | カテゴリ別記事数の辞書を作る """    
    category_post_dict = dict(zip(category_list, category_post_list))

    """ dict | カテゴリ別タグ数の辞書を作る """    
    category_tag_dict = dict(zip(category_list, category_tag_list))

    """
    タグを基準とした集計
    """

    """ list | タグ一覧からタグ名のリストを作る """
    tag_list = list(published_tag.distinct().values_list('name', flat=True))

    """ list | タグ一覧からタグ別記事数のリストを作る """
    tag_post_list = list(published_tag.annotate(count=Count('post')).values_list('count', flat=True))

    """ dict | タグ別記事数の辞書を作る 順番は記事数降順にする """
    tag_post_dict = dict(zip(tag_list, tag_post_list))
    tag_post_dict = sorted(tag_post_dict.items(), reverse=True, key=lambda x:x[1])
    tag_post_dict = dict(tag_post_dict)

    """ タグが多すぎる場合の「その他」化 """    
    tag_post_dict_length = len(tag_post_dict)
    display_length = 20
    enable_length = display_length - 1
    if enable_length < 0:
        enable_length = 0 
    if tag_post_dict_length > enable_length:
        dif_length = tag_post_dict_length - enable_length
        if dif_length != 1:
            key_list = list(tag_post_dict.keys())[:enable_length]
            value_list = list(tag_post_dict.values())[:enable_length]
            others_value = sum(list(tag_post_dict.values())[-dif_length:])
            tag_post_dict = dict(zip(key_list, value_list))
            tag_post_dict['その他'] = others_value

    """
    投稿年月を基準とした集計
    """

    """ list | 投稿年月リストを作る """
    month_list = sorted(list(set(map(lambda date: date.strftime('%Y-%m'), list(published_post.values_list('published_at', flat=True))))))

    """ list | 年月リスト、カテゴリリスト、記事数リストを各々作る """
    """ warn | ループでSQLが多重発行されるため、より良い方法の模索が必要 """
    list1, list2, list3 = [], [], []
    for date, category in itertools.product(month_list, category_list):
        yyyy, mm = date.split('-')
        month_post_count = published_post.filter(published_at__year=yyyy, published_at__month=mm).filter(category__name=category).annotate(count=Count('pk')).count()
        list1.append(date)
        list2.append(category)
        list3.append(month_post_count)

    """ list | 年月リスト、カテゴリリスト、記事数リストを一つのリストにまとめる """
    month_post_list = list(set(zip(list1, list2, list3)))

    """
    ワードクラウドのための形態素解析 前処理
    """

    """ 直近のタイトルと説明とテキスト本文を抽出しクレンジング """
    post_count = 30
    post_titles = list(published_post.values_list('title', flat=True))[:post_count]
    post_titles = ' '.join(post_titles).split()
    post_descriptions = list(published_post.values_list('description', flat=True))[:post_count]
    post_descriptions = ' '.join(post_descriptions).split()
    post_texts = list(map(lambda lfc: lfc.replace('\r\n', '\n').replace('\r', '\n').replace('\n', ' '), list(published_post.values_list('text', flat=True))))[:post_count]
    post_texts = html.strip_tags(''.join(post_texts)).split()
    tokens = ' '.join(post_descriptions + post_titles + post_texts)

    """
    janome 形態素解析でワードクラウド生成用の辞書を作る
    """
    
    """ 形態素解析のためのアナライザを定義 """
    udic_path = settings.JANOME_DICTIONARY_PATH
    char_filters = [UnicodeNormalizeCharFilter(), RegexReplaceCharFilter('\,', '')]
    tokenizer = Tokenizer(udic=udic_path, udic_type='simpledic', udic_enc='utf8')
    token_filters = [CompoundNounFilter(), POSKeepFilter(['名詞']), LowerCaseFilter(), TokenCountFilter()]
    analyzer = Analyzer(char_filters, tokenizer, token_filters)

    """ dict | 単語リストから辞書を作る """
    word_dict = dict(analyzer.analyze(tokens))

    """ レンダリング """
    return render(request, 'blog/blog_single_graph.html', {
        'label': label, 
        'category_list': category_list, 
        'category_post_dict': category_post_dict, 
        'category_tag_dict': category_tag_dict, 
        'tag_post_dict': tag_post_dict, 
        'month_list': month_list, 
        'month_post_list': month_post_list, 
        'word_dict': word_dict, 
    })