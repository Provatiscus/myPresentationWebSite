from django.contrib import admin
from .models import CarMake, CarModel,Certificate
# from .models import related models


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5


# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    model = CarModel
    #

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    model = CarMake
    inlines = [CarModelInline]

class CertificateAdmin(admin.ModelAdmin):
    model = Certificate



# Register models here
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(Certificate, CertificateAdmin)
