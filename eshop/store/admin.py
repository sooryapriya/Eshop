from django.contrib import admin
from.models.product import Product
from.models.category import Category
from.models.customer import Customer
from.models.sample import Sample
from.models.orders import Orders

class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'discount', 'category']


class AdminCategory(admin.ModelAdmin):
    list_display = ['name']


class AdminCustomer(admin.ModelAdmin):
    list_display = ['name', 'email', 'mobnumber', 'state', 'city', 'zip']


class AdminSample(admin.ModelAdmin):
    list_display = ['title', 'rate', 'percent']


class AdminOrders(admin.ModelAdmin):
    list_display = ['customer', 'product', 'quantity', 'price', 'date', 'status', 'address', 'city', 'state', 'zip', 'mobnumber', 'email']


# Register your models here.


admin.site.register(Product, AdminProduct)
admin.site.register(Category, AdminCategory)
admin.site.register(Customer, AdminCustomer)
admin.site.register(Sample, AdminSample)
admin.site.register(Orders, AdminOrders)
# Register your models here.
