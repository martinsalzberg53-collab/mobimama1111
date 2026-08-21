from django.contrib import admin

# Register your models here.

from .models import Tip

@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'is_approved', 'created_at')
    list_filter = ('category', 'is_approved', 'author')
    search_fields = ('title', 'content')
    
    # This makes the author field read-only in the admin panel
    # because we will set it automatically.
    readonly_fields = ('author', 'created_at')

    def save_model(self, request, obj, form, change):
        """
        When creating a new tip in the admin panel,
        set the author to the currently logged-in user.
        """
        if not obj.pk:  # This means the object is being created (pk is 'primary key')
            obj.author = request.user
        super().save_model(request, obj, form, change)