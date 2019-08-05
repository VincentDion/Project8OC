# from django.shortcuts import render
import requests

from django.http import HttpResponse

from .models import Product

def index(request):
    # request products (category for now, query later versions)
    products = Product.objects.filter(category="jus-de-fruits").order_by('nutrition_grade')[:12]

    formatted_products = ["<li>{}</li>".format(product.name) for product in products]
    message = """<ul>{}</ul>""".format("\n".join(formatted_products))
    return HttpResponse(message)


# def listing(request):
#     users = ["<li>{}</li>".format(user['name']) for user in USERS]
#     message = """<ul>{}</ul>""".format("\n".join(users))
#     return HttpResponse(message)


def detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    message = "Le produit est {}, de la marque {}. Sa note nutritive est {}.".format(product.name, product.brand, product.nutrition_grade)
    return HttpResponse(message)


def search(request):
    query = request.GET.get('query')
    if not query:
        message = "Aucun produit n'est demandé"

    else:
        products = Product.objects.filter(name__icontains=query)

        if not products.exists():
            message = "Misère de misère, nous n'avons trouvé aucun résultat !"
        else:
            products = ["<li>{}</li>".format(product.name) for product in products]
            message = """
                Nous avons trouvé les produits correspondant à votre requête ! Les voici :
                <ul>{}</ul>
            """.format("</li><li>".join(products))

    return HttpResponse(message)
