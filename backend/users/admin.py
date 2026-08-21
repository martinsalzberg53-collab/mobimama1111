from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin panel for the email-based User model.
    """
    model = User
    
    # What to show in the main list of users
    list_display = ['email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']
    
    # Fields to show when *editing* an existing user
    # This is much more complete than the one you had.
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'role', 'clinic')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fields to show when *adding* a new user
    # This form will appear when you click "Add user"
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            # Use 'password' and 'password2' for the confirmation fields
            'fields': ('email', 'password', 'password2', 'first_name', 'last_name', 'role', 'is_staff', 'is_superuser')}
        ),
    )
    
    # Make the admin searchable by email and name
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    # These are needed for the email-based UserAdmin
    filter_horizontal = ()