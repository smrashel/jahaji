from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

admin.site.site_title = "Jahaji"
admin.site.site_header = "Jahaji"
admin.site.index_title = "Administration"


# Register your models here.
@admin.register(District, Thana, Association, Companie)
@admin.register(VesselType, GoodsType, Vessel, Position, EducationLevel,
                MobileMoneyAccount, ShippingStaff, Ghat, GhatLabor)
class CompanieAdmin(ImportExportModelAdmin):
    pass


class ShipAdmin(ImportExportModelAdmin):
    pass


class ShippingStaffAdmin(ImportExportModelAdmin):
    pass
