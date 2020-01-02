from django.contrib import admin

# Register your models here.
from .models import Order,  Storage, RequiredOperation, RequiredMaterial, WorkerCatalog, PositionCatalog, OperationCatalog, MaterialCatalog, DillerCatalog, StatusCatalog

admin.site.register(Order)
admin.site.register(Storage)
admin.site.register(RequiredOperation)
admin.site.register(RequiredMaterial)


admin.site.register(WorkerCatalog)
admin.site.register(PositionCatalog)
admin.site.register(OperationCatalog)
admin.site.register(MaterialCatalog)
admin.site.register(DillerCatalog)
admin.site.register(StatusCatalog)