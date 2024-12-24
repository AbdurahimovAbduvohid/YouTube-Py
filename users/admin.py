from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'surname', 'is_staff')
    search_fields = ('email', 'name', 'surname')
    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
