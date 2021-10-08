import datetime
from django.db import models
from.customer import Customer
from.product import Product


class Orders(models.Model):
    orderstatus = (("PENDING", "Pending"), ("ON PROCESS", "ON Process"), ("DELIEVERED", "Delieverd"),
                   ("ORDER PLACED", "Order Placed"),
                   ("COMPLETED PROCESSING", "Completed Processing"),
                   ("ON TRANSIT", "On Transit"),
                   ("CANCELLED", "Cancelled"))
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    name = models.CharField(max_length=30, default='')
    email = models.EmailField(default='')
    mobnumber = models.CharField(max_length=10, default='')
    city = models.CharField(max_length=25, default='')
    state = models.CharField(max_length=15, default='')
    zip = models.CharField(max_length=6, default='')
    address = models.CharField(max_length=60, default='')
    date = models.DateField(default=datetime.datetime.today)
    status = models.CharField(max_length=30, choices=orderstatus)

    def __str__(self):
        return self.name

    def place_order(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Orders.\
            objects\
            .filter(customer=customer_id)\
            .order_by('-date')
