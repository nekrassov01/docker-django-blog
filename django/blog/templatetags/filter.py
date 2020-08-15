from django import template
import unicodedata

register = template.Library()

""" 汎用タグ | ペイジャーでクエリを保持 """
@register.simple_tag
def replace_url(request, field, value):
    url_dict = request.GET.copy()
    url_dict[field] = str(value)
    return url_dict.urlencode()

""" 汎用フィルタ | 半角全角を区別してTRUNCATE """
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