from django import template
from datetime import datetime
from bs4 import BeautifulSoup
register = template.Library()

@register.filter(name='safe_text')
def safe_text(value):
    soup=BeautifulSoup(value, 'html.parser')
    return soup.text

@register.filter
def days_until(date):
    # hour, minute, second, microsecond
    delta = datetime.now().timestamp() - datetime.timestamp(date)
    # delta = int(delta // 1000*60)
    delta = int(delta//60)
    if delta < 60: return str(delta) + " phút"
    delta = int(delta // 60)
    if delta < 24: return str(delta) + " giờ"
    delta = int(delta // 24)
    if delta < 7: return str(delta) + " ngày"
    delta = int(delta // 7)
    if delta < 10: return str(delta) + " tuần"
    delta = int(delta // 4)
    return str(delta) + " tháng"