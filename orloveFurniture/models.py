

from django.db import models
from django.utils import timezone
import uuid



class StatusCatalog(models.Model):
    name = models.CharField(max_length=255)
    orderliness = models.IntegerField()

    def __str__(self):
        return self.name



class Order(models.Model):

    idOrder = models.CharField(max_length=36, blank=True, unique=False, default=uuid.uuid4)

    date_created = models.DateTimeField(default=timezone.now)

    surname = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255)

    status = models.ForeignKey(StatusCatalog, models.SET_NULL, blank=True, null=True)

    address = models.CharField(max_length=255)

    phone = models.CharField(max_length=11)

    details = models.TextField()


    cost = models.IntegerField(blank=True, null=True, default = 0)

    prepayment = models.IntegerField(blank=True, null=True, default = 0 )


    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return self.name + " " + self.surname + ": " + self.details


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



class OperationCatalog(models.Model):
    date_created = models.DateTimeField
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name



class RequiredOperation(models.Model):

    id = models.AutoField(primary_key=True)

    idOrder = models.ForeignKey(Order, models.SET_NULL, blank=True, null=True)

    idOperation =  models.ForeignKey(OperationCatalog,  blank=False, null=False)
    idWorker = models.ForeignKey(WorkerCatalog, blank=False, null=False)
    cost = models.IntegerField()



class DillerCatalog(models.Model):

    date_created = models.DateTimeField

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=11)

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

    idMaterial = models.ForeignKey(MaterialCatalog, blank=False, null=False)

    count = models.IntegerField()






class Storage(models.Model):

    date_created = models.DateTimeField

    idMaterial = models.ForeignKey(MaterialCatalog, models.SET_NULL, blank=True, null=True)
    count = models.IntegerField()





