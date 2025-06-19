from django.contrib import admin
from .models import UserProfile, Machine, Maintenance, Complaint, Reference

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__username', 'role')

class MachineAdmin(admin.ModelAdmin):
    list_display = ('factory_number', 'model_ref', 'shipment_date')
    search_fields = ('factory_number', 'model_ref', 'engine_model_ref')
    list_filter = ('shipment_date',)

class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('machine', 'maintenance_type_ref', 'maintenance_date', 'service_company_ref')
    search_fields = ('machine__factory_number', 'maintenance_type_ref', 'service_company_ref')
    list_filter = ('maintenance_date',)

class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('machine', 'failure_node_ref', 'claim_date', 'service_company_ref')
    search_fields = ('machine__factory_number', 'failure_node_ref', 'service_company_ref')
    list_filter = ('claim_date',)


class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('entity_name', 'name', 'description')
    search_fields = ('entity_name', 'name')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Machine, MachineAdmin)
admin.site.register(Maintenance, MaintenanceAdmin)
admin.site.register(Complaint, ComplaintAdmin)
admin.site.register(Reference,ReferenceAdmin)
