from django.contrib import admin
from django.utils.html import format_html

from .models import Clinic, NurseAssignment, NurseProfile

@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone_number')
    search_fields = ('name', 'address', 'phone_number')

@admin.register(NurseProfile)
class NurseProfileAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'registration_type', 'nmc_pin', 'license_status', 'license_preview')
    list_filter = ('license_status', 'registration_type')
    search_fields = ('user__email', 'qualifications')
    readonly_fields = ('license_preview',)
    actions = ('approve_license', 'reject_license')

    fieldsets = (
        (None, {'fields': ('user', 'registration_type', 'qualifications')}),
        ('NMC License', {'fields': ('license_file', 'license_status', 'license_review_note', 'license_preview')}),
        ('AI OCR Result', {'fields': ('license_extracted',)}),
    )

    @admin.display(description='Email')
    def user_email(self, obj):
        return obj.user.email if obj.user else obj.user_id

    @admin.display(description='NMC PIN/AIN')
    def nmc_pin(self, obj):
        return obj.user.nmc_pin if obj.user and obj.user.nmc_pin else '-'

    @admin.display(description='License')
    def license_preview(self, obj):
        if not obj.license_file:
            return 'No file uploaded'
        url = f'/api/users/license-files/{obj.license_file.name}/'
        ext = obj.license_file.name.lower().rsplit('.', 1)[-1]
        if ext in ('jpg', 'jpeg', 'png', 'webp', 'heic'):
            return format_html(
                '<a href="{0}" target="_blank"><img src="{0}" style="max-height:140px;border:1px solid #ccc;border-radius:4px"/></a>',
                url,
            )
        return format_html('<a href="{0}" target="_blank">Download license (PDF)</a>', url)

    @admin.action(description='Approve selected licenses')
    def approve_license(self, request, queryset):
        updated = queryset.update(license_status='APPROVED', license_review_note='Approved by admin review.')
        self.message_user(request, f'{updated} license(s) approved.')

    @admin.action(description='Reject selected licenses')
    def reject_license(self, request, queryset):
        updated = queryset.update(license_status='REJECTED', license_review_note='Rejected by admin review.')
        self.message_user(request, f'{updated} license(s) rejected.')

@admin.register(NurseAssignment)
class NurseAssignmentAdmin(admin.ModelAdmin):
    list_display = ('nurse', 'clinic')
    search_fields = ('nurse__username', 'clinic__name')