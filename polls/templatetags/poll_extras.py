from django import template
from jalali_date import date2jalali

register = template.Library()

@register.filter(name='show_jalali_date')
def show_jalali_date(value):
    return date2jalali(value)

@register.filter(name='three_digits_currency')
def three_digits_currency(value:int):
    return '{:,}'.format(value)+' تومان'

@register.filter(name='three_digits_currency2')
def three_digits_currency2(value:int):
    return '{:,}'.format(value)


@register.simple_tag
def moltiply(quantity,price,*args,**kwargs):
    return three_digits_currency(quantity * price)
@register.simple_tag(name='moltiply2')
def moltiply(quantity,price,*args,**kwargs):
    return three_digits_currency2(quantity * price)