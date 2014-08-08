__author__ = 'tneier'


from django.contrib import admin
from birds.models import Image, Egg, Bird, Breed, Site, Flock

class ImageAdmin(admin.ModelAdmin):
    list_display = ("title","thumbnail_link")
    list_filter = ["birds"]

# Register your models here.
admin.site.register(Egg)
admin.site.register(Bird)
admin.site.register(Breed)
admin.site.register(Site)
admin.site.register(Flock)
admin.site.register(Image, ImageAdmin)

