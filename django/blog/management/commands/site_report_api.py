from django.conf import settings
from django.db.models import Q, Count
from django.utils import html
from blog.models import Post, Category, Tag
from datetime import datetime
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *
import csv
import re
import itertools

"""
集計の基準となるクエリセット
"""
# queryset | 公開されている記事一覧
published_post = Post.objects.select_related('category').prefetch_related('tag').filter(is_public=True).order_by('published_at', 'created_at', 'updated_at')

# queryset | （紐づく記事が）公開されているカテゴリ一覧
published_category = Category.objects.filter(post__is_public=True).order_by('index')

# queryset | （紐づく記事が）公開されているタグ一覧
published_tag = Tag.objects.filter(post__is_public=True).order_by('slug')

"""
集計の基準となるリスト
"""
# list | カテゴリ一覧からカテゴリ名のリストを作る
category_list = list(published_category.distinct().values_list('name', flat=True))

# list | タグ一覧からタグ名のリストを作る
tag_list = list(published_tag.distinct().values_list('name', flat=True))

# list | 投稿年月リストを作る
month_list = sorted(list(set(map(lambda date: date.strftime('%Y-%m'), list(published_post.values_list('published_at', flat=True))))))

"""
自作 Reporting API | 1.カテゴリ別記事数
"""
def get_category_post_dict():

    # list | カテゴリ一覧からカテゴリ別記事数のリストを作る
    category_post_list = list(published_category.annotate(count=Count('post')).values_list('count', flat=True))

    # dict | カテゴリ別記事数の辞書を作る
    category_post_dict = dict(zip(category_list, category_post_list))

    for key, value in category_post_dict.items():
        yield key, value

"""
自作 Reporting API | 2.カテゴリ別タグ数
"""
def get_category_tag_dict():

    # list | カテゴリ一覧からカテゴリ別タグ数のリストを作る
    category_tag_list = list(published_category.annotate(count=Count('tag', filter=Q(tag__post__is_public=True), distinct=True)).values_list('count', flat=True))

    # dict | カテゴリ別タグ数の辞書を作る
    category_tag_dict = dict(zip(category_list, category_tag_list))

    for key, value in category_tag_dict.items():
        yield key, value

"""
自作 Reporting API | 3.タグ別記事数
"""
def get_tag_post_dict():

    """ list | タグ一覧からタグ別記事数のリストを作る """
    tag_post_list = list(published_tag.annotate(count=Count('post')).values_list('count', flat=True))

    # dict | タグ別記事数の辞書を作る 順番は記事数降順にする
    tag_post_dict = dict(zip(tag_list, tag_post_list))
    tag_post_dict = sorted(tag_post_dict.items(), reverse=True, key=lambda x:x[1])
    tag_post_dict = dict(tag_post_dict)

    # タグが多すぎる場合の「その他」化    
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

    for key, value in tag_post_dict.items():
        yield key, value

"""
自作 Reporting API | 4.月別記事数
"""
def get_month_post_list():

    # list | 年月リスト、カテゴリリスト、記事数リストを各々作る
    # warn | ループでSQLが多重発行されるため、より良い方法の模索が必要
    list1, list2, list3 = [], [], []
    for date, category in itertools.product(month_list, category_list):
        yyyy, mm = date.split('-')
        month_post_count = published_post.filter(published_at__year=yyyy, published_at__month=mm).filter(category__name=category).annotate(count=Count('pk')).count()
        list1.append(date)
        list2.append(category)
        list3.append(month_post_count)

    # list | 年月リスト、カテゴリリスト、記事数リストを一つのリストにまとめる
    month_post_list = list(set(zip(list1, list2, list3)))

    for date, category, month_post_count in month_post_list:
        yield date, category, month_post_count

"""
自作 Reporting API | 5.ワードクラウド
"""
def get_word_dict():

    # 直近のタイトルと説明とテキスト本文を抽出しクレンジング
    post_count = 30
    post_titles = list(published_post.values_list('title', flat=True))[:post_count]
    post_titles = ' '.join(post_titles).split()
    post_descriptions = list(published_post.values_list('description', flat=True))[:post_count]
    post_descriptions = ' '.join(post_descriptions).split()
    post_texts = list(map(lambda lfc: lfc.replace('\r\n', '\n').replace('\r', '\n').replace('\n', ' '), list(published_post.values_list('text', flat=True))))[:post_count]
    post_texts = html.strip_tags(''.join(post_texts)).split()
    tokens = ' '.join(post_descriptions + post_titles + post_texts)

    #  シノニム一覧から内容を1行ずつ取り出して行数分の RegexReplaceCharFilter を生成
    def set_synonym_filters(path, filters):
        synonym_list = []
        with open(path, mode='r', encoding='utf-8') as f:
            synonym_list = [row.strip() for row in f.readlines()]
        for synonym in synonym_list:
            from_word = str(synonym.split(',')[0])
            to_word = str(synonym.split(',')[1])
            filters.append(RegexReplaceCharFilter(from_word, to_word))

    # ひらがな・カタカナ・英数字で1文字の単語を除去するクラス
    class OneCharacterRemoveFilter(TokenFilter):
        def apply(self, tokens):
            for token in tokens:
                if re.match('^[あ-んア-ンa-zA-Z0-9ー]$', token.surface):
                    continue
                yield token

    # 数字と記号のみの単語を除去するクラス
    class OnlyNumericOrSymbolicRemoveFilter(TokenFilter):
        def apply(self, tokens):
            for token in tokens:
                if re.match('^[0-9!-/:-@¥[-`{-~]*$', token.surface):
                    continue
                yield token

    # ストップワードを除去するクラス
    class StopWordRemoveFilter(TokenFilter):
        def __init__(self):
            stopwords_path = settings.JANOME_STOPWORDS_PATH
            stopwords = []
            with open(stopwords_path, mode='r', encoding='utf-8') as f:
                self.stopwords = [row.strip() for row in f.readlines()]
        def apply(self, tokens):
            for token in tokens:
                if token.surface in self.stopwords:
                    continue
                yield token

    # 形態素解析のためのアナライザを定義
    udic_path = settings.JANOME_DICTIONARY_PATH
    synonym_path = settings.JANOME_SYNONYM_PATH
    char_filters = [UnicodeNormalizeCharFilter()]
    set_synonym_filters(synonym_path, char_filters)
    tokenizer = Tokenizer(udic=udic_path, udic_type='simpledic', udic_enc='utf8')
    token_filters = [POSKeepFilter(['名詞']), OneCharacterRemoveFilter(), OnlyNumericOrSymbolicRemoveFilter(), StopWordRemoveFilter(), TokenCountFilter()]
    analyzer = Analyzer(char_filters, tokenizer, token_filters)

    # dict | 単語リストから辞書を作る
    word_dict = dict(analyzer.analyze(tokens))

    for key, value in word_dict.items():
        yield key, value

if __name__ == '__main__':
    for key, value in get_category_post_dict():
        print(key, value)
    for key, value in get_category_tag_dict():
        print(key, value)
    for key, value in get_tag_post_dict():
        print(key, value)
    for date, category, month_post_count in get_month_post_list():
        print(date, category, month_post_count)
    for key, value in get_word_dict():
        print(key, value)