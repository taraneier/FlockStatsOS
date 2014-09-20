# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Dailysummary(models.Model):
    daily_id = models.IntegerField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    meantempm = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    meantempi = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    meandewptm = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    meandewpti = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    meanwindspdm = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    meanwindspdi = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    meanwdire = models.CharField(max_length=45, blank=True)
    meanwdird = models.CharField(max_length=45, blank=True)
    humidity = models.IntegerField(blank=True, null=True)
    maxtempm = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    maxtempi = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    mintempm = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    mintempi = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    maxhumidity = models.IntegerField(blank=True, null=True)
    minhumidity = models.IntegerField(blank=True, null=True)
    maxdewptm = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    maxdewpti = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    mindewptm = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    mindewpti = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    maxpressurem = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    maxpressurei = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    minpressurem = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    minpressurei = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    maxwspdm = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    maxwspdi = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    precipm = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    precipi = models.DecimalField(max_digits=2, decimal_places=2, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'dailysummary'

class Observation(models.Model):
    observation_id = models.IntegerField(primary_key=True)
    date = models.DateTimeField()
    tempm = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    tempi = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    dewptm = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    dewpti = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    hum = models.IntegerField(blank=True, null=True)
    wspdm = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    wspdi = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    wgustm = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    wgusti = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    pressurem = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    pressurei = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    windchillm = models.IntegerField(blank=True, null=True)
    windchilli = models.IntegerField(blank=True, null=True)
    heatindexm = models.IntegerField(blank=True, null=True)
    heatindexi = models.IntegerField(blank=True, null=True)
    precip_ratem = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    precip_ratei = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    precip_totalm = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    precip_totali = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    solarradiation = models.CharField(max_length=45, blank=True)
    uv = models.CharField(db_column='UV', max_length=45, blank=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'observation'
