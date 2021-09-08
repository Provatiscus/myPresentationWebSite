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

    path(route='general', view=views.general, name='general'),
    path(route='about', view=views.about, name='about'),
    path(route='contact', view=views.contact, name='contact'),
    path(route='test', view=views.test, name='contact'),
    path(route='login', view=views.login_request, name='login_request'),
    path(route='logout', view=views.logout_request, name='login_request'),
    path(route='signup', view=views.registration_request, name='registration_request'),
    path(route='', view=views.general, name='index'),
    path(route='by_id', view=views.get_dealerships_by_id, name='index'),
    path(route='by_state', view=views.get_dealerships_by_state, name='get_dealerships_by_state'),
    path(route='dealerships', view=views.dealerships, name='dealerships'),
    path(route='dealer_details', view=views.get_dealer_details, name='reviews_by_id'),
    path(route='post_review', view=views.add_review, name='post_review'),
    path(route='resumee', view=views.resumee, name='resumee'),
    path(route='gallery', view=views.gallery, name='resumee'),
    path(route='certificates', view=views.certificates, name='resumee'),
    path(route='minigame', view=views.minigame, name='minigame'),

    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
