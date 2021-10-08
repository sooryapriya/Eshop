from django import template
register = template.Library()


@register.filter(name='rupee')
def rupee(number):
    return "₹ "+str(number)

@register.filter(name='multiply')
def rupee(number, num1):
    return number * num1