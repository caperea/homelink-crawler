from django.db import models

class District(models.Model):
    hlid = models.CharField(max_length=4, unique=True, null=False)
    desc = models.CharField(max_length=8)

class Subdistrict(models.Model):
    hlid = models.CharField(max_length=8, unique=True, null=False)
    dist = models.ForeignKey(District)
    desc = models.CharField(max_length=16)
    updated = models.BooleanField(default=False)

class Community(models.Model):
    hlid = models.CharField(max_length=64, unique=True)
    desc = models.CharField(max_length=32, null=True)
    addr = models.CharField(max_length=128, null=True)
    detail = models.CharField(max_length=255, null=True)
    time_added = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

class RealEstate(models.Model):
    hlid = models.CharField(max_length=64, unique=True, null=False)
    subdist = models.ForeignKey(Subdistrict)
    desc = models.CharField(max_length=255, null=True)
    community = models.ForeignKey(Community, null=True)
    nbedrm = models.IntegerField(null=True)
    nlvnrm = models.IntegerField(null=True)
    area = models.FloatField(null=True)
    price = models.FloatField(null=True)
    facing = models.CharField(max_length=8, null=True)
    in_sale = models.BooleanField(default=True)
    duty_free = models.BooleanField(default=False)
    edu_district = models.BooleanField(default=False)
    updated = models.BooleanField(default=False)
    time_added = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

class EstateZoning(models.Model):
    estate = models.ForeignKey(RealEstate)
    subdist = models.ForeignKey(Subdistrict)
    time_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('estate', 'subdist')
