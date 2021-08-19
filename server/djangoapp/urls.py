from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view

    # path for contact us view

    # path for registration

    # path for login

    # path for logout

    path(route='index.html', view=views.index, name='index'),
    path(route='about.html', view=views.about, name='about'),
    path(route='contact.html', view=views.contact, name='contact'),
    path(route='test.html', view=views.test, name='contact'),
    path(route='login.html', view=views.login_request, name='login_request'),
    path(route='logout.html', view=views.logout_request, name='login_request'),
    path(route='signup.html', view=views.registration_request, name='registration_request'),
    path(route='', view=views.get_dealerships, name='index'),
    path(route='by_id', view=views.get_dealerships_by_id, name='index'),
    path(route='by_state', view=views.get_dealerships_by_state, name='get_dealerships_by_state'),
    path(route='dealerships.html', view=views.dealerships, name='dealerships'),
    path(route='dealerships_by_id.html', view=views.get_dealerships_by_id_from_mongoDB, name='dealerships_by_id_from_mongo'),
    path(route='dealerships_by_state.html', view=views.get_dealerships_by_state_from_mongoDB, name='dealerships_by_state_from_mongo'),

    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
