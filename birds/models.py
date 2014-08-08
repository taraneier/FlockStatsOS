from __future__ import division
from django.db import models
from django.db.models import Avg
from django.core.files import File
from PIL import Image as PImage
from django.contrib import admin
from django.db import connection
import os
# from settings import MEDIA_ROOT
from django.conf import settings
from tempfile import *



# Create your models here.
class Breed(models.Model):
    breed_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, blank=True)
    origin = models.CharField(max_length=45, blank=True)
    def __unicode__(self):
        return self.name
    class Meta:
        managed = False
        db_table = 'breed'


class Site(models.Model):
    site_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, blank=True)
    def __unicode__(self):
        return self.name
    class Meta:
        managed = False
        db_table = 'site'


class Flock(models.Model):
    flock_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, blank=True)
    @property
    def birds(self):
        return Bird.objects.filter(flock = self.flock_id).order_by('name')
    @property
    def eggs(self):
        return Egg.objects.filter(bird__flock = self.flock_id).order_by('finish')
    def bird_count(self):
        return self.birds.count()
    def egg_count(self):
        return self.eggs.count()
    def avg_weight(self):
        return self.eggs.aggregate(Avg('weight')).get('weight__avg')
    def days_laying(self):
        import datetime
        import pytz
        if (self.egg_count > 0):
            days_laying = (pytz.utc.localize(datetime.datetime.today())  - self.eggs[0].finish ).days + 1
            return days_laying
        else:
            return 0
    def eggs_per_day(self):
        return self.egg_count() / self.days_laying()
    def last_week(self):
        cursor = connection.cursor()
        query = "select date(finish) as date, count(1) as eggs, avg(weight) as avg from egg e join bird b on e.bird_id = b.bird_id where b.flock_id=%s group by date(finish) order by date desc limit 7"
        cursor.execute(query, [self.flock_id])
        return cursor.fetchall()
    def favorite_sites(self):
        cursor = connection.cursor()
        query = "select l.name as Site, count(1) as Eggs from egg e join site l  on e.site_id = l.site_id join bird b on e.bird_id = b.bird_id where b.flock_id=%s group by Site  order by Eggs desc limit 3"
        cursor.execute(query, [self.flock_id])
        return cursor.fetchall()
    def top_layers(self):
        cursor = connection.cursor()
        query = "select b.name as Bird, count(1) as Eggs from egg e join bird b on e.bird_id = b.bird_id where b.flock_id=%s group by Bird  order by Eggs desc limit 5"
        cursor.execute(query, [self.flock_id])
        return cursor.fetchall()

    def __unicode__(self):
        return self.name
    class Meta:
        managed = False
        db_table = 'flock'

class Bird(models.Model):
    bird_id = models.AutoField(primary_key=True)
    flock = models.ForeignKey(Flock)
    name = models.CharField(max_length=45, blank=True)
    breed = models.ForeignKey(Breed)
    hatched = models.DateTimeField(blank=True, null=True)
    @property
    def eggs(self):
        return  Egg.objects.filter(bird = self.bird_id).order_by('finish')
    @property
    def age(self):
        import datetime
        import pytz
        days_old = (pytz.utc.localize(datetime.datetime.today())  - self.hatched ).days
        weeks = int(days_old/7)
        days = days_old%7
        return `weeks` + " Weeks and " + `days` + " days old"
    @property
    def egg_count(self):
        return self.eggs.count()
    @property
    def avg_weight(self):
        return self.eggs.aggregate(Avg('weight')).get('weight__avg')
    @property
    def days_laying(self):
        import datetime
        import pytz
        if (self.egg_count > 0):
            days_laying = (pytz.utc.localize(datetime.datetime.today())  - self.eggs[0].finish ).days + 1
            return days_laying
        else:
            return 0
    def eggs_per_day(self):
        if(self.egg_count > 0):
            return "{:.0}".format(self.egg_count / self.days_laying)
        else:
            return 0;
    def favorite_site(self):
        cursor = connection.cursor()
        query = "select l.name as Site, count(1) as Eggs from egg e join site l  on e.site_id = l.site_id  where bird_id=%s group by Site  order by Eggs desc limit 1"
        cursor.execute(query, [self.bird_id])
        row = cursor.fetchone()
        if (row):
            return row[0]
        else:
            return ""

    def __unicode__(self):
        return self.name
    class Meta:
        managed = False
        db_table = 'bird'



class Egg(models.Model):
    egg_id = models.AutoField(primary_key=True)
    bird = models.ForeignKey(Bird)
    site = models.ForeignKey(Site)
    start = models.DateTimeField(blank=False)
    finish = models.DateTimeField(blank=False)
    weight = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        import datetime
        return "#" + `self.egg_id` + ":" + self.bird.name + ":" + self.finish.strftime("%Y-%m-%d %H:%M")

    class Meta:
        managed = False
        db_table = 'egg'
        ordering = ['-egg_id']

class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    image = models.FileField(upload_to="images/")
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    birds = models.ManyToManyField(Bird, blank=True)
    eggs  = models.ManyToManyField(Egg, blank=True)
    thumbnail2 = models.ImageField(upload_to="images/", blank=True, null=True)
    thumbnail = models.ImageField(upload_to="images/", blank=True, null=True)

    def save(self, *args, **kwargs):
        """Save image dimensions."""
        super(Image, self).save(*args, **kwargs)
        im = PImage.open(os.path.join(settings.MEDIA_ROOT, self.image.name))
        self.width, self.height = im.size
        super(Image, self).save(*args, ** kwargs)

        # large thumbnail
        fn, ext = os.path.splitext(self.image.name)
        im.thumbnail((128,128), PImage.ANTIALIAS)
        thumb_fn = fn + "-thumb2" + ext
        tf2 = NamedTemporaryFile()
        im.save(tf2.name, "JPEG")
        self.thumbnail2.save(thumb_fn, File(open(tf2.name)), save=False)
        tf2.close()

        # small thumbnail
        im.thumbnail((40,40), PImage.ANTIALIAS)
        thumb_fn = fn + "-thumb" + ext
        tf = NamedTemporaryFile()
        im.save(tf.name, "JPEG")
        self.thumbnail.save(thumb_fn, File(open(tf.name)), save=False)
        tf.close()

        super(Image, self).save(*args, ** kwargs)


    def thumbnail_link(self):
        return """<a href="/media/%s"><img border="0" alt="" src="/media/%s" height="40" /></a>""" % ((self.image.name, self.image.name))

    thumbnail_link.allow_tags=True

    def size(self):
        return "%s x %s" % (self.width, self.height)

    def __unicode__(self):
        return self.image.name

    # class Meta:
        # managed = False
        # db_table = 'image'

