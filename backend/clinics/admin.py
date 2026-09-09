from django.contrib import admin

from .models import AllowedHospitalDomain, Clinic, NurseAssignment, NurseProfile

@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone_number')
    search_fields = ('name', 'address', 'phone_number')

@admin.register(NurseProfile)
class NurseProfileAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'registration_type', 'nmc_pin')
    list_filter = ('registration_type',)
    search_fields = ('user__email', 'qualifications')

    fieldsets = (
        (None, {'fields': ('user', 'registration_type', 'qualifications')}),
    )

    @admin.display(description='Email')
    def user_email(self, obj):
        return obj.user.email if obj.user else obj.user_id

    @admin.display(description='NMC PIN/AIN')
    def nmc_pin(self, obj):
        return obj.user.nmc_pin if obj.user and obj.user.nmc_pin else '-'

@admin.register(AllowedHospitalDomain)
class AllowedHospitalDomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'hospital', 'created_at')
    search_fields = ('domain', 'hospital')

@admin.register(NurseAssignment)
class NurseAssignmentAdmin(admin.ModelAdmin):
    list_display = ('nurse', 'clinic')
    search_fields = ('nurse__username', 'clinic__name')