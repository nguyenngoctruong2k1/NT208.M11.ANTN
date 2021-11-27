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
    delta = datetime.now().date() - datetime.date(date)
    return delta.days