

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

    nameOrder =  models.CharField(max_length=255)
    nameContract = models.CharField(max_length=255)

    fio = models.CharField(max_length=255)

    status = models.ForeignKey(StatusCatalog, blank=False, null=False, on_delete=models.PROTECT)

    address = models.CharField(max_length=255)

    phone = models.CharField(max_length=11)

    trelloLink = models.CharField(max_length=255)

    details = models.TextField()

    cost = models.IntegerField(blank=True, null=True, default = 0)

    prepayment = models.IntegerField(blank=True, null=True, default = 0 )


    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return self.nameContract + ". " + self.nameOrder + ". " + self.details


class PositionCatalog(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class WorkerCatalog(models.Model):

    #idWorker = models.CharField(max_length=36, blank=True, unique=False, default=uuid.uuid4)

    date_created = models.DateTimeField

    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255)

    position = models.ManyToManyField(PositionCatalog)

    def save(self, *args, **kwargs):
        super(WorkerCatalog, self).save(*args, **kwargs)

    def __str__(self):
        return self.surname  + " " +  self.name + " " + self.patronymic



# class TypeOperationCatalog(models.Model):
#     date_created = models.DateTimeField
#
#     name = models.CharField(max_length=255)
#
#     def __str__(self):
#         return self.name




# class OperationCatalog(models.Model):
#     date_created = models.DateTimeField
#
#     name = models.CharField(max_length=255)
#     #idTypeOperation = models.ForeignKey(TypeOperationCatalog, blank=False, null=False, on_delete=models.PROTECT)
#
#
#     def __str__(self):
#         return self.name



# class RequiredOperation(models.Model):
#
#     id = models.AutoField(primary_key=True)
#
#     idOrder = models.ForeignKey(Order, blank=False, null=False, on_delete=models.PROTECT)
#
#     idOperation =  models.ForeignKey(OperationCatalog,  blank=False, null=False, on_delete=models.PROTECT)
#     idWorker = models.ForeignKey(WorkerCatalog, blank=False, null=False, on_delete=models.PROTECT)
#
#     cost = models.IntegerField()
#
#     def save(self, *args, **kwargs):
#         super(RequiredOperation, self).save(*args, **kwargs)




class OperationProjectCatalog(models.Model):
    date_created = models.DateTimeField

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class RequiredOperationProject(models.Model):

    id = models.AutoField(primary_key=True)

    idOrder = models.ForeignKey(Order, blank=False, null=False, on_delete=models.CASCADE)

    idOperation =  models.ForeignKey(OperationProjectCatalog,  blank=False, null=False, on_delete=models.PROTECT)
    idWorker = models.ForeignKey(WorkerCatalog, blank=False, null=False, on_delete=models.PROTECT)

    cost = models.IntegerField(blank=False, null=False)

    isDone = models.BooleanField(default=False)

    isDoneDate = models.DateField(null=True, blank = True)

    def save(self, *args, **kwargs):
        super(RequiredOperationProject, self).save(*args, **kwargs)



class OperationManufactoryCatalog(models.Model):
    date_created = models.DateTimeField

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class RequiredOperationManufactory(models.Model):
    id = models.AutoField(primary_key=True)

    idOrder = models.ForeignKey(Order, blank=False, null=False, on_delete=models.CASCADE)

    idOperation = models.ForeignKey(OperationManufactoryCatalog, blank=False, null=False, on_delete=models.PROTECT)
    idWorker = models.ForeignKey(WorkerCatalog, blank=False, null=False, on_delete=models.PROTECT)

    cost = models.IntegerField(blank=False, null=False)

    isDone = models.BooleanField(default=False)

    isDoneDate = models.DateField(null=True, blank = True)

    def save(self, *args, **kwargs):
        super(RequiredOperationManufactory, self).save(*args, **kwargs)



class OperationContractorCatalog(models.Model):
    date_created = models.DateTimeField

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class RequiredOperationContractor(models.Model):

    id = models.AutoField(primary_key=True)

    idOrder = models.ForeignKey(Order, blank=False, null=False, on_delete=models.CASCADE)

    idOperation = models.ForeignKey(OperationContractorCatalog, blank=False, null=False, on_delete=models.PROTECT)
    idWorker = models.ForeignKey(WorkerCatalog, blank=False, null=False, on_delete=models.PROTECT)

    cost = models.IntegerField(blank=False, null=False)

    isDone = models.BooleanField(default=False)

    isDoneDate = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super(RequiredOperationContractor, self).save(*args, **kwargs)




class DillerCatalog(models.Model):

    date_created = models.DateTimeField

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=11)

    def __str__(self):
        return self.name



class MaterialTypeCatalog(models.Model):

    name = models.CharField(max_length=255)


class MaterialCategoryCatalog(models.Model):

    name = models.CharField(max_length=255)


class MaterialCatalog(models.Model):

    date_created = models.DateTimeField
    name = models.CharField(max_length=255)

    type = models.ForeignKey(MaterialTypeCatalog, blank=False, null=False, on_delete=models.PROTECT)
    category = models.ForeignKey(MaterialCategoryCatalog, blank=False, null=False, on_delete=models.PROTECT)

    def __str__(self):
        return self.name



class RequiredMaterial(models.Model):

    id = models.AutoField(primary_key=True)

    idOrder = models.ForeignKey(Order, blank=False, null=False, on_delete=models.CASCADE)

    idMaterial = models.ForeignKey(MaterialCatalog, blank=False, null=False, on_delete=models.PROTECT)

    count = models.IntegerField()

    def save(self, *args, **kwargs):
        super(RequiredMaterial, self).save(*args, **kwargs)








class Storage(models.Model):

    date_created = models.DateTimeField

    idMaterial = models.ForeignKey(MaterialCatalog, models.SET_NULL, blank=True, null=True)
    count = models.IntegerField()





