from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.contrib.auth.models import User
from .models import Product, UserFavorite
from .forms import UserRegisterForm, ChangeMailForm


def index(request):
    """ Display main page of website """
    return render(request, 'bestproduct/index.html')


def detail(request, product_id):
    """ Display information on one product """
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'image': product.picture,
        'name': product.name,
        'product': product
    }
    return render(request, 'bestproduct/detail.html', context)


def replace(request):
    """
    Display list of products with better nutritive score than one searched
    by user
    """
    query = request.GET.get('query')

    # Use of icontains to increase the chance of finding a result
    products = Product.objects.filter(name__icontains=query)

    if len(products) > 0:
        choice = products[0]

        substitutes_list = Product.objects.filter(
                            category=choice.category,
                            nutrition_grade__lt=choice.nutrition_grade
                            ).order_by("nutrition_grade")[:6]
        
        context = {
            'id': choice.id,
            'name': choice.name,
            'image': choice.picture,
            'substitutes': substitutes_list,
        }

        return render(request, 'bestproduct/replace.html', context)

    else:
        # Warning for no product found and redirection to index
        messages.warning(request,
                         "Nous n'avons pas trouvé de produit correspondant")
        return redirect('bestproduct:index')


@login_required(login_url='/login')
def favorite(request):
    """ Display list of favorite products for connected user """
    user = request.user
    users_favorites_list = Product.objects.filter(
                                    userfavorite__user_name=user.id)
    if len(users_favorites_list) > 0:
        favorites_list = Product.objects.filter(pk__in=users_favorites_list).order_by('id')
    else:
        favorites_list = []

    page = request.GET.get('page', 1)
    paginator = Paginator(favorites_list, 6)
    try:
        favorites = paginator.page(page)
    except PageNotAnInteger:
        favorites = paginator.page(1)
    except EmptyPage:
        favorites = paginator.page(paginator.num_pages)

    return render(request, 'bestproduct/favorite.html',
                  {'favorites': favorites})


def register(request):
    """ Display of register page """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request,
                             'Votre inscription est un succès, vous pouvez \
                             désormais vous connecter')
            return redirect('bestproduct:login')
    else:
        form = UserRegisterForm()

    return render(request, 'bestproduct/register.html', {'form': form})


@login_required(login_url='/login')
def profile(request):
    """ Display of profile page, only if user is logged in """
    user = request.user
    return render(request, 'bestproduct/profile.html', {'email':user.email})


@login_required(login_url='/login')
def add_favorite(request, product_id):
    """ Function for adding a favorite product from the replace page """
    try:
        UserFavorite.objects.get(user_name_id=request.user.id,
                                 product_id=(product_id))
        messages.warning(request, 'Ce produit est déjà dans vos favoris')
        return redirect(request.META.get('HTTP_REFERER'))
    except ObjectDoesNotExist:
        UserFavorite.objects.create(user_name_id=request.user.id,
                                    product_id=(product_id))
        messages.success(request, 'Le produit a été ajouté à vos favoris')
        return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/login')
def del_favorite(request, product_id):
    try:
        UserFavorite.objects.get(user_name_id=request.user.id,
                                 product_id=(product_id))
        delete = UserFavorite.objects.get(user_name_id=request.user.id,
                                          product_id=(product_id))
        delete.delete()
        messages.success(request, 'Le produit a été retiré de vos favoris')
        #return redirect(request.META.get('HTTP_REFERER'))
        return redirect('bestproduct:favorite')
    except ObjectDoesNotExist:
        messages.warning(request, 'Le produit ne figure pas dans vos favoris')
        return redirect('bestproduct:favorite')


@login_required(login_url='/login')
def mail_change(request):
    """ Change of user's email adresse """

    if request.method == 'POST':
        form = ChangeMailForm(request.POST)
        if form.is_valid():
            change = User.objects.get(email=request.user.email)
            change.email = form.cleaned_data.get('email')
            change.save()

            # cleaned data : https://docs.djangoproject.com/fr/2.1/ref/forms/api/#django.forms.Form.cleaned_data

            messages.success(request,
                             'Votre adresse a été modifiée')
            return redirect('bestproduct:profile')
    else:
        form = ChangeMailForm()

    return render(request, 'bestproduct/mail_change.html', {'form': form})

def legal_notice(request):
    """ Display of Legal Notice page """
    return render(request, 'bestproduct/legal_notice.html')


"""
Web and documentation ressources :

Django messages :
-> https://docs.djangoproject.com/fr/2.2/ref/contrib/messages/

Django register view :
-> https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html

Django Decorators :
-> https://docs.djangoproject.com/fr/2.2/topics/auth/default/

More info on the request.user :
-> https://stackoverflow.com/questions/17312831/what-does-request-user-refer-to-in-django
"""
