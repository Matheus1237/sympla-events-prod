from django.contrib import admin
from django.utils.html import format_html

from events.models import Category, Event, ImportLog, Venue


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ["name", "city", "sympla_id", "created_at"]
    search_fields = ["name", "city", "sympla_id"]
    list_filter = ["city"]
    ordering = ["name"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(ImportLog)
class ImportLogAdmin(admin.ModelAdmin):
    list_display = ["version", "status", "imported_count", "created_at"]
    list_filter = ["status"]
    readonly_fields = ["version", "status", "imported_count", "error_message", "created_at"]
    ordering = ["-created_at"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["name", "start_date", "venue_display", "category", "import_version", "created_at"]
    list_filter = ["category", "venue__city", "start_date"]
    search_fields = ["name", "venue__name", "venue__city", "category__name"]
    readonly_fields = ["sympla_id", "raw_data", "import_version"]
    ordering = ["-start_date"]

    def venue_display(self, obj):
        return format_html(f"{obj.venue.name}<br><small>{obj.venue.city}</small>")
    venue_display.short_description = "Venue"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
