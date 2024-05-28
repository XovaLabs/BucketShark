from django.urls import reverse
from django.conf import settings

def map():
    map = {
        "authenticated": {
        'Home': reverse('home'),
        'Log out': reverse('logout'),
        'Ontime Payment': reverse('add_onetime_payment'),
        'Repeated Payment': reverse('add_repeated_payment'),
        'Summary': reverse('summary'),
    },
        "unauthenticated": {
            "Home": reverse('home')
        }
    }
def get_uni_acess_links(request):

    #  TODO: Logout button should be only visible if logged in. log in button should be visible if not logged in.
    #   The payment views should only be visible if the user is currently logged in.
    #   If the user is not logged they should only see home and login.
    uni_access_links_dict = {

        'Home': reverse('home'),
        'Log out': reverse('logout'),
        'Ontime Payment': reverse('add_onetime_payment'),
        'Repeated Payment': reverse('add_repeated_payment'),
        'Summary': reverse('summary'),
    }

    return {'u_links': uni_access_links_dict}
