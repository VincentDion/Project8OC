import requests

from django.core.management.base import BaseCommand, CommandError
from django.db.utils import DataError, IntegrityError
from bestproduct.models import Product

# More info : https://docs.djangoproject.com/fr/2.2/howto/custom-management-commands/

class Command(BaseCommand):
    help = 'Fill the database with products from pre-set categories'

    CATEGORIES = [
        'fromages-a-tartiner', 'jus-d-orange', 
        'jus-de-pamplemousse', 'jus-de-raisin',
        'jus-de-pomme', 'jus-multifruits', 'cremes-fraiches',
        'biscuits-aperitifs', 'confitures-d-abricot', 'confitures-de-fruits-rouges',
        'pates-a-tartiner-au-chocolat', 'beurres', 'huiles-d-olive'
    ]


    def fill_db(self):

        for category in self.CATEGORIES:

            research_url = 'https://fr.openfoodfacts.org/cgi/search.pl?tagtype_0=categories\
&tag_contains_0=contains&tag_0=%s&sort_by=unique_scans_n&page_size=500&action=process&json=1' \
                           % (category)
                
            r = requests.get(url=research_url)
            data_dict = r.json()
            products = data_dict['products']

            for product in products:
                try:
                    name = product["product_name_fr"]
                    brand = product["brands"]
                    nutrition_grade = product["nutrition_grade_fr"]
                    url = product["url"]
                    picture = product['image_front_url']
                    nutrition_image = product["image_nutrition_url"]

                    Product.objects.create(name=name, category=category, brand=brand, nutrition_grade=nutrition_grade, 
                        url=url, picture=picture, nutrition_image=nutrition_image)

                except KeyError: 
                    pass

                except DataError:
                    pass

                except IntegrityError:
                    pass

    def handle(self, *args, **options):
        self.fill_db()
