from django.contrib import admin

from birds.models import Egg
from birds.models import Bird
from birds.models import Breed
from birds.models import Site
from birds.models import Flock


class EggAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'site', 'weight')
    list_editable = ('site', 'weight')
    list_filter = ('bird', 'finish')

    class Media:
        js = ('js/admin.js',)

# Register your models here.
admin.site.register(Egg, EggAdmin)
admin.site.register(Bird)
admin.site.register(Breed)
admin.site.register(Site)
admin.site.register(Flock)


