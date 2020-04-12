from django.contrib import admin

# Register your models here.
from .models import Order,  Storage, RequiredMaterial, WorkerCatalog, PositionCatalog, MaterialCatalog, MaterialCategoryCatalog, MaterialTypeCatalog, DillerCatalog, StatusCatalog
from .models import RequiredOperationProject, RequiredOperationManufactory, RequiredOperationContractor
from .models import OperationContractorCatalog, OperationManufactoryCatalog, OperationProjectCatalog

admin.site.register(Order)
admin.site.register(Storage)

admin.site.register(RequiredOperationProject)
admin.site.register(RequiredOperationManufactory)
admin.site.register(RequiredOperationContractor)

admin.site.register(OperationProjectCatalog)
admin.site.register(OperationManufactoryCatalog)
admin.site.register(OperationContractorCatalog)


admin.site.register(RequiredMaterial)


admin.site.register(WorkerCatalog)
admin.site.register(PositionCatalog)

admin.site.register(MaterialCatalog)
admin.site.register(MaterialTypeCatalog)
admin.site.register(MaterialCategoryCatalog)

admin.site.register(DillerCatalog)
admin.site.register(StatusCatalog)