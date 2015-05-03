from __future__ import division
from django.db import models
from django.db.models import Avg
from django.db import connection
from django.core.files import File
from PIL import Image as PImage
from django.contrib import admin
import os
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
        return Bird.objects.filter(flock = self.flock_id).exclude(active = 0).order_by('name')
    @property
    def eggs(self):
        return Egg.objects.filter(bird__flock = self.flock_id).order_by('finish')
    def bird_count(self):
        return self.birds.count()
    def egg_count(self):
        return self.eggs.count()
    def avg_weight(self):
        return round(self.eggs.aggregate(Avg('weight')).get('weight__avg'),2)
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
        # query = "select b.bird_id, b.name as Bird, count(1) as Eggs from egg e join bird b on e.bird_id = b.bird join _id where b.flock_id=%s group by Bird  order by Eggs desc limit 5"
        query = "select count(distinct(e.bird_id)) from egg e join bird b on b.bird_id = e.bird_id where b.flock_id=%s and finish >= curdate() - INTERVAL DAYOFWEEK(curdate())+1 DAY;"
        cursor.execute(query, [self.flock_id])
        return cursor.fetchall()

    def percent_day(self):
        cursor = connection.cursor()
        query = "select count(distinct(e.bird_id)) from egg e join bird b on b.bird_id = e.bird_id where b.flock_id=%s and finish >= DATE_ADD(CURDATE(), INTERVAL -1 DAY);"
        cursor.execute(query, [self.flock_id])
        return round(cursor.fetchall()[0][0] / self.bird_count() * 100, 0)

    def percent_week(self):
        cursor = connection.cursor()
        query = "select count(distinct(e.bird_id)) from egg e join bird b on b.bird_id = e.bird_id where b.flock_id=%s and finish >= DATE_ADD(CURDATE(), INTERVAL -7 DAY);"
        cursor.execute(query, [self.flock_id])
        return round(cursor.fetchall()[0][0] / self.bird_count() * 100, 0)

    def percent_month(self):
        cursor = connection.cursor()
        query = "select count(distinct(e.bird_id)) from egg e join bird b on b.bird_id = e.bird_id where b.flock_id=%s and finish >= DATE_ADD(CURDATE(), INTERVAL -30 DAY);"
        cursor.execute(query, [self.flock_id])
        return round(cursor.fetchall()[0][0] / self.bird_count() * 100, 0)

    def percent_quarter(self):
        cursor = connection.cursor()
        query = "select count(distinct(e.bird_id)) from egg e join bird b on b.bird_id = e.bird_id where b.flock_id=%s and finish >= DATE_ADD(CURDATE(), INTERVAL -90 DAY);"
        cursor.execute(query, [self.flock_id])
        return round(cursor.fetchall()[0][0] / self.bird_count() * 100, 0)

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
    death = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=1)

    def is_active(self):
        return bool(self.active)

    def breed_name(self):
        return self.breed.name;

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
    def last_egg(self):
        last_index = len(self.eggs) - 1
        print(last_index)
        if (last_index>-1):
            return self.eggs[last_index].finish

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

    def avatar(self):
        return Image.objects.filter(birds = self.bird_id).exclude(avatar = 0)[0]

    def __unicode__(self):
        return self.name
    class Meta:
        managed = False
        db_table = 'bird'



class Egg(models.Model):
    egg_id = models.AutoField(primary_key=True)
    bird = models.ForeignKey(Bird)
    site = models.ForeignKey(Site)
    weight = models.IntegerField(blank=True, null=True)
    start = models.DateTimeField(blank=False)
    finish = models.DateTimeField(blank=False)


    def __unicode__(self):
        import datetime
        return "#" + `self.egg_id` + ":" + self.bird.name + ":" + self.finish.strftime("%Y-%m-%d %H:%M")

    class Meta:
        managed = False
        db_table = 'egg'
        ordering = ['-egg_id']



# flock

# select
#     date(`finish`) as `Date`,
#     count(1) as `Total`,
#     sum(if(`e`.`bird_id` = 8, `weight`, 0)) as `Faith`,
#     sum(if(`e`.`bird_id` = 1, `weight`, 0)) as `Della`,
#     sum(if(`e`.`bird_id` = 2, `weight`, 0)) as `Ozzie`,
#     sum(if(`e`.`bird_id` = 11, `weight`, 0)) as `Ivy`,
#     sum(if(`e`.`bird_id` = 7, `weight`, 0)) as `Buffy`,
#     sum(if(`e`.`bird_id` = 4, `weight`, 0)) as `Barbara`,
#     sum(if(`e`.`bird_id` = 9, `weight`, 0)) as `Georgia`,
#     sum(if(`e`.`bird_id` = 12, `weight`, 0)) as `Winona`,
#     sum(if(`e`.`bird_id` = 10, `weight`, 0)) as `Mabel`,
#     sum(if(`e`.`bird_id` = 3, `weight`, 0)) as `Rosie`,
#     sum(if(`e`.`bird_id` = 5, `weight`, 0)) as `Sammy`,
#     sum(if(`e`.`bird_id` = 6, `weight`, 0)) as `Cappie`
#
# from
#     `egg` `e`
# group by `Date`
# order by `Date` desc
# ;


# select b.name as Bird, count(1) as Eggs from egg e join bird b on e.bird_id = b.bird_id  group by Bird  order by Eggs desc;
# select l.name as Site, count(1) as Eggs from egg e join site l  on e.site_id = l.site_id  group by Site  order by Eggs desc;
# select b.name as Bird, avg(weight) as Avg from egg e join bird b on e.bird_id = b.bird_id  group by Bird  order by Avg desc;
# select date(finish) as date, count(1) as eggs from egg group by date(finish) order by finish;
#
# bird
# select count(egg_id) from egg where bird_id=2;
# select avg(weight) from egg where bird_id=2;
# select finish as "Start", timestampdiff(day,finish,now()) as "Days Laying" from egg where bird_id=2 order by finish limit 1;
# select l.name as Site, count(1) as Eggs from egg e join site l  on e.site_id = l.site_id  where bird_id=2 group by Site  order by Eggs desc limit 1;

class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    image = models.FileField(upload_to="images/")
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    birds = models.ManyToManyField(Bird, blank=True)
    eggs = models.ManyToManyField(Egg, blank=True)
    thumbnail2 = models.ImageField(upload_to="images/", blank=True, null=True)
    thumbnail = models.ImageField(upload_to="images/", blank=True, null=True)
    avatar = models.BooleanField(default=0, blank=True)


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
        return """<a href="/static/media/%s"><img border="0" alt="" src="/static/media/%s" height="40" /></a>""" % ((self.image.name, self.thumbnail.name))

    thumbnail_link.allow_tags=True

    def size(self):
        return "%s x %s" % (self.width, self.height)

    def __unicode__(self):
        return self.image.name

    class Meta:
        managed = False
        db_table = 'image'

class ImageAdmin(admin.ModelAdmin):
    # search_fields = ["title"]
    list_display = ["__unicode__", "title", "thumbnail"]
    list_filter = ["birds", "eggs"]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()
