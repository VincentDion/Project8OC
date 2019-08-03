# from django.db import models

PRODUCTS = {
    'pizza-napolitaine' : {'name': 'Pizza napolitaine'},
    'pizza-quat-fromages' : {'name' : 'Pizza 4 fromages'},
    'pizza-mexicaine' : {'name' : 'pizza mexicaine'},
}

USERS = [
    {'name': 'Vincent', 'pizza': [PRODUCTS['pizza-napolitaine']]},
    {'name': 'Axel', 'pizza': [PRODUCTS['pizza-quat-fromages']]},
    {'name': 'Camille', 'pizza': [PRODUCTS['pizza-mexicaine'], PRODUCTS['pizza-napolitaine']]}
]


"""
class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    brand = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    nutrition_grade = models.CharField(max_length=1)
    picture = models.URLField()
    nutrition_image = models.URLField()
    url = models.URLField()
"""