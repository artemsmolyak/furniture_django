

from django.db import models
from django.utils import timezone



class StatusCatalog(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name



class Order(models.Model):

    id = models.AutoField(primary_key=True)

    date_created = models.DateTimeField(default=timezone.now)

    surname = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255)

    status = models.ForeignKey(StatusCatalog, models.SET_NULL, blank=True, null=True)

    details = models.TextField()


    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return self.name + " " + self.surname + ": " + self.details




class RequiredOperation(models.Model):
    idOrder = models.IntegerField()
    idOperation = models.IntegerField()
    idWorker = models.IntegerField()




class DillerCatalog(models.Model):
    date_created = models.DateTimeField
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    def __str__(self):
        return self.name



class MaterialCatalog(models.Model):
    date_created = models.DateTimeField
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name




class RequiredMaterial(models.Model):

    id = models.AutoField(primary_key=True)

    idOrder = models.ForeignKey(Order, models.SET_NULL, blank=True, null=True)

    idMaterial = models.ForeignKey(MaterialCatalog, models.SET_NULL, blank=True, null=True)

    count = models.IntegerField()




class OperationCatalog(models.Model):
    date_created = models.DateTimeField
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PositionCatalog(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class WorkerCatalog(models.Model):
    date_created = models.DateTimeField

    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255)

    position = models.ManyToManyField(PositionCatalog)

    def __str__(self):
        return self.name + " " + self.patronymic





class Storage(models.Model):
    date_created = models.DateTimeField
    name = models.CharField(max_length=255)
    count = models.IntegerField()

    def __str__(self):
        return self.name



