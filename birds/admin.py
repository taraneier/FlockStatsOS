from django.contrib import admin

from birds.models import Egg
from birds.models import Bird
from birds.models import Breed
from birds.models import Site
from birds.models import Flock


# class EggAdmin(admin.ModelAdmin):
    # ordering = ['-egg_id']

# Register your models here.
admin.site.register(Egg)
admin.site.register(Bird)
admin.site.register(Breed)
admin.site.register(Site)
admin.site.register(Flock)


