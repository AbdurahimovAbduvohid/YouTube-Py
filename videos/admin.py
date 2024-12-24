from django.contrib import admin
from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'created_at', 'is_active')
    list_filter = ('created_at', 'is_active')
    search_fields = ('title', 'description')
    actions = ['mark_active', 'mark_inactive']

    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected videos have been moved to active status.")

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request,
                          "Selected videos have been moved to inactive status.")

    mark_active.short_description = "Active"
    mark_inactive.short_description = "Inactive"
