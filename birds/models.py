from __future__ import division
from django.db import models
from django.db.models import Avg

from django.db import connection


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



# flock
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
