from django.contrib import admin
from .models import Certificate,  Comment
# from .models import related models


# Register your models here.

# CarModelInline class
class CommentInline(admin.StackedInline):
    model = Comment
    extra = 5


# CarModelAdmin class
class CommentAdmin(admin.ModelAdmin):
    model = Comment
    #

# CarMakeAdmin class with CarModelInline
# class UserAdmin(admin.ModelAdmin):
#     model = User
#     inlines = [CommentInline]

class CertificateAdmin(admin.ModelAdmin):
    model = Certificate


# Register models here
# admin.site.register(User, UserAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Certificate, CertificateAdmin)
