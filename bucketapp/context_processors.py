from django.urls import reverse
from django.conf import settings


def get_links():
    links = {
        "authenticated": {
            'Home': reverse('home'),
            'Log out': reverse('logout'),
            'Onetime Payment': reverse('add_onetime_payment'),
            'Repeated Payment': reverse('add_repeated_payment'),
            'Summary': reverse('summary'),
        },
        "unauthenticated": {
            'Home': reverse('home'),
            'Log in': reverse('login'),
        }
    }
    return links


def get_uni_access_links(request):
    links = get_links()
    if request.user.is_authenticated:
        access_links = links["authenticated"]
    else:
        access_links = links["unauthenticated"]

    return {'u_links': access_links}
