from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required
from django.contrib import messages

import requests

from .models import Product, UserFavorite
from .forms import UserRegisterForm

def index(request):
    return render(request, 'bestproduct/index.html')

def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
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


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Votre compte a bien été créé')
            """ On voit pas ce message, ça revient directement au menu, il faudrait pouvoir montrer
            à l'utilisateur que ça a bien fonctionné, si possible en le renvoyant à la page login plutôt"""
            return redirect('bestproduct:index')
    else:
        form = UserRegisterForm()
        
    return render(request, 'bestproduct/register.html', {'form': form})


 
@login_required
def profile(request):
    return render(request, 'bestproduct/profile.html')


@login_required
def favorite(request):

    user = request.user
    fav = Product.objects.filter(userfavorite__user_name=user.id)
    if fav:
        product = Product.objects.filter(pk__in=fav)
    else:
        product = []

    return render(request, 'bestproduct/favorite.html', {'favorite': product})


