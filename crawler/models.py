from django.db import models

class District(models.Model):
    hlid = models.CharField(max_length=4, unique=True, null=False)
    desc = models.CharField(max_length=8)

class Subdistrict(models.Model):
    hlid = models.CharField(max_length=8, unique=True, null=False)
    dist = models.ForeignKey(District)
    desc = models.CharField(max_length=16)
    updated = models.BooleanField(default=False)

class Listing(models.Model):
    hlid = models.CharField(max_length=64, unique=True, null=False)
    subdist = models.ForeignKey(Subdistrict)
    updated = models.BooleanField(default=False)
    time_added = models.DateTimeField(auto_now_add=True)

class Community(models.Model):
    name = models.CharField(max_length=64)
    dist = models.ForeignKey(Subdistrict)
    addr = models.CharField(max_length=128)
    link = models.CharField(max_length=64, unique=True)
    desc = models.CharField(max_length=255, null=True)
    time_added = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

class RealEstate(models.Model):
    hlid = models.ForeignKey(Listing)
    desc = models.CharField(max_length=255)
    community = models.ForeignKey(Community)
    nbedrm = models.IntegerField()
    nlvnrm = models.IntegerField()
    area = models.FloatField()
    price = models.FloatField()
    facing = models.CharField(max_length=8)
    in_sale = models.BooleanField(default=False)
    duty_free = models.BooleanField(default=False)
    edu_district = models.BooleanField(default=False)
    time_added = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
