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

    path(route='fr/general', view=views.generalFR, name='generalFR'),
    path(route='fr/login', view=views.login_requestFR, name='login_requestFR'),
    path(route='fr/logout', view=views.logout_requestFR, name='logout_requestFR'),
    path(route='fr/signup', view=views.registration_requestFR, name='registration_requestFR'),
    path(route='fr', view=views.generalFR, name='indexFR'),
    path(route='fr/resumee', view=views.resumeeFR, name='resumeeFR'),
    path(route='fr/gallery', view=views.galleryFR, name='galleryFR'),
    path(route='fr/certificates', view=views.certificatesFR, name='certificatesFR'),
    path(route='fr/comments', view=views.commentsFR, name='commentsFR'),
    path(route='fr/delete_comment', view=views.delete_commentFR, name='delete_commentFR'),
    path(route='fr/fibromyalgia', view=views.fibromyalgiaFR, name='fibromyalgiaFR'),

    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
