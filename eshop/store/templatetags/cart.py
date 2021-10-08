from django import template
from math import floor
register = template.Library()


@register.filter(name='is_in_cart')
def is_in_cart(product, cart):
    keys = cart.keys()
    print(product, cart)
    for id in keys:
        print(id, product.id)
        print(type(id), type(product.id))
        if int(id) == product.id:
            return True
    return False;


@register.filter(name='cart_quantity')
def cart_quantity(product, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return cart.get(id)
    return 0;


@register.filter(name='price_discount')
def price_discount(product, cart):
    pdiscount = product.price - (product.price * product.discount/100)
    pdiscount = floor(pdiscount)
    return int(pdiscount)


@register.filter(name='price_total')
def price_total(product, cart):
    pdiscount = product.price - (product.price * product.discount / 100)
    pdiscount = floor(pdiscount)
    return int(pdiscount) * int(cart_quantity(product, cart))


@register.filter(name='price_amt')
def price_amt(products, cart):
    total = 0;
    for p in products:
        total += price_total(p, cart)
    return total