# from django.shortcuts import render
import requests

from django.http import HttpResponse

from .models import USERS

def index(request):
    message = "Salut tout le monde !"
    return HttpResponse(message)

def listing(request):
    users = ["<li>{}</li>".format(user['name']) for user in USERS]
    message = """<ul>{}</ul>""".format("\n".join(users))
    return HttpResponse(message)

def detail(request, user_id):
    id = int(user_id)
    user = USERS[id]
    pizza = " ".join([pizza['name'] for pizza in user['pizza']])
    message = "Le client est {}. Il a commandé une {}".format(user['name'], pizza)
    return HttpResponse(message)

def search(request):
    query = request.GET.get('query')
    if not query:
        message = "Aucun utilisateur n'est demandé"
    else:
        users = [
            user for user in USERS
            if query in " ".join(product['name'] for product in user['pizza'])
        ]

        if len(users) == 0:
            message = "Misère de misère, nous n'avons trouvé aucun résultat !"
        else:
            users = ["<li>{}</li>".format(user['name']) for user in users]
            message = """
                Nous avons trouvé les utilisateurs correspondant à votre requête ! Les voici :
                <ul>
                    {}
                </ul>
            """.format("</li><li>".join(users))

    return HttpResponse(message)