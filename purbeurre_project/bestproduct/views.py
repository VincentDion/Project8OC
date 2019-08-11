from django.shortcuts import render
from django.http import HttpResponse

import requests

from .models import Product


def index(request):
    return render(request, 'bestproduct/index.html')

def detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    context = {
        'image' : product.picture,
        'name' : product.name,
        'product' : product
    }
    return render(request, 'bestproduct/detail.html', context)


def replace(request):
    query = request.GET.get('query')
    # if not query:
    #    message = "Aucun produit n'est demandé"

    
    products = Product.objects.filter(name__icontains=query)

    """
    Il faut prévoir comment gérer les erreurs, genre pas de produit ou pas de query
    L'ancienne version avec message = en http ne fonctionne plus, cf commentaires
    """

    # if not products.exists():
    #     message = "Misère de misère, nous n'avons trouvé aucun résultat !"
    # else:
    choice = products[0]
    substitutes = Product.objects.filter(category=choice.category, nutrition_grade__lt=choice.nutrition_grade).order_by("nutrition_grade")[:6]
    context = {
        'name' : choice.name,
        'image' : choice.picture,
        'substitutes' : substitutes,
    }

    return render(request, 'bestproduct/replace.html', context)


        # substitutes = ["<li>{}</li>".format(product.name) for product in substitutes]
        # message = """
        #     Nous avons trouvé les produits correspondant à votre requête ! Les voici :
        #     <ul>{}</ul>
        #     Pour rappel, le produit à remplacer est : {}
        # """.format(" ".join(substitutes), choice.name)

    # return HttpResponse(message)
