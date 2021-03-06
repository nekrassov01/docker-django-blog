from django import template
import re
import unicodedata

register = template.Library()

"""
汎用タグ | ペイジャーでクエリを保持
"""
@register.simple_tag
def replace_url(request, field, value):
    url_dict = request.GET.copy()
    url_dict[field] = str(value)
    return url_dict.urlencode()

"""
汎用タグ | モデルの verbose_name をテンプレートで使う
"""
@register.simple_tag
def verbose_name(value):
    if hasattr(value, 'model'):
        value = value.model
    return value._meta.verbose_name.title()

"""
汎用フィルタ | 半角全角を区別してTRUNCATE
"""
@register.filter
def truncatechars_ja(text, arg):
    count = 0
    result = []
    for char in text:
        if unicodedata.east_asian_width(char) in 'FWA':
            count += 2
        else:
            count += 1
        result.append(char)
        if count > arg:
            result[-2:] = ['','…']
            break
    return ''.join(result)

"""
汎用フィルタ | 全角文字と半角英字の間に半角スペースを挿入する
  - 句読点の直後の半角英数字記号にはスペースを挿入しない
  - 数字のみの場合はスペースを挿入しない
  - <>"'と文字の間にはスペースを挿入しない
"""
@register.filter
def set_text_spacing(text):
    text = re.sub(r"([0-9]*[!#-&(-/:-;=?-~][0-9]*)([^ -~\W+])", r"\1 \2", text)
    text = re.sub(r"([^ -~\W+])([0-9]*[!#-&(-/:-;=?-~][0-9]*)", r"\1 \2", text)
    return text
