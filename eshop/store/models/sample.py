from django.db import models


class Sample(models.Model):
    title = models.CharField(max_length=50)
    rate = models.IntegerField(default=0)
    percent = models.IntegerField(default=0)
    image = models.ImageField(upload_to='sample/')

    @staticmethod
    def get_all_sample():
        return Sample.objects.all()

    def __str__(self):
        return self.title