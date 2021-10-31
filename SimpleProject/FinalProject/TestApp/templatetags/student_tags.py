from django import template
from TestApp.models import Student

register = template.library()

@register.simple_tag()
def get_students():
    return Student.objects.all()