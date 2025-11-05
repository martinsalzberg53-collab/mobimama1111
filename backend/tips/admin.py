from django.contrib import admin

# Register your models here.

from .models import Tip

@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = ('title','category','author','is_approved')
    list_filter = ('category','is_approved')
    search_fields = ('title','content')
    