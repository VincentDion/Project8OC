from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    brand = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    nutrition_grade = models.CharField(max_length=1)
    picture = models.URLField()
    nutrition_image = models.URLField()
    url = models.URLField()


    def __str__(self):
        return self.name

class UserFavorite(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

