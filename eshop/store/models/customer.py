from django.db import models


class Customer(models.Model):
        name = models.CharField(max_length=30)
        email = models.EmailField()
        password = models.CharField(max_length=300)
        mobnumber = models.CharField(max_length=10)
        state = models.CharField(max_length=15)
        city = models.CharField(max_length=25)
        zip = models.CharField(max_length=6)

        def __str__(self):
                return self.name

        def register(self):
                self.save()

        @staticmethod
        def get_customer_by_email(email):
                try:
                        return Customer.objects.get(email=email)
                except:
                        return False

        def isExists(self):
                if Customer.objects.filter(email=self.email):
                        return True
                return False
