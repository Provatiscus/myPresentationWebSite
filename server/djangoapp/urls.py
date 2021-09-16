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
    path(route='contact', view=views.contact, name='contact'),
    path(route='login', view=views.login_request, name='login_request'),
    path(route='logout', view=views.logout_request, name='login_request'),
    path(route='signup', view=views.registration_request, name='registration_request'),
    path(route='', view=views.general, name='index'),
    path(route='resumee', view=views.resumee, name='resumee'),
    path(route='gallery', view=views.gallery, name='resumee'),
    path(route='certificates', view=views.certificates, name='resumee'),
    path(route='comments', view=views.comments, name='comments'),
    path(route='delete_comment', view=views.delete_comment, name='delete_comment'),
    path(route='fibromyalgia', view=views.fibromyalgia, name='delete_comment'),

    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
