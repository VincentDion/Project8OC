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


def detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    message = "Le produit est {}, de la marque {}. Sa note nutritive est {}.".format(product.name, product.brand, product.nutrition_grade)
    return HttpResponse(message)


def replace(request):
    query = request.GET.get('query')
    if not query:
        message = "Aucun produit n'est demandé"

    else:
        products = Product.objects.filter(name__icontains=query)

        """
        La solution d'Elia ne me convient pas, concrètement il applique une méthode first() mais qui modifie la nature de l'objet
        Je préfère plutôt prendre le premier item de la liste => product = products[0], quitte à informer l'utilisateur qu'il y a un 
        grand nombre de résultat et qu'il serait peut-être plus pertinent de préciser sa recherche.
        On cherche ensuite un substitut sur le seul produit conservé.

        Il faudra aussi résoudre le fait qu'il faille le nom exact du produit, il faudrait quelque chose de plus intuitif 
        (peut être plusieurs couches de filtre, genre cherche tous les produits contenant jus, puis parmi eux ts ceux contenant orange)
        => Vite très chiant à coder, comment savoir le nombre de filtre, il doit y avoir un moyen plus simple à voir dans la doc.

        """

    if not products.exists():
        message = "Misère de misère, nous n'avons trouvé aucun résultat !"
    else:
        choice = products[0]
        substitutes = Product.objects.filter(category=choice.category, nutrition_grade__lt=choice.nutrition_grade).order_by("nutrition_grade")
        substitutes = ["<li>{}</li>".format(product.name) for product in substitutes]
        message = """
            Nous avons trouvé les produits correspondant à votre requête ! Les voici :
            <ul>{}</ul>
            Pour rappel, le produit à remplacer est : {}
        """.format(" ".join(substitutes), choice.name)

    return HttpResponse(message)
