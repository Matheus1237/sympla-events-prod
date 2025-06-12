from rest_framework import serializers

from events.models import Category, Event, ImportLog, Venue


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ["id", "name", "city", "sympla_id"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ImportLogSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M")
    
    class Meta:
        model = ImportLog
        fields = ["id", "status", "imported_count", "error_message", "version", "created_at"]


class EventSerializer(serializers.ModelSerializer):
    venue = VenueSerializer()
    category = CategorySerializer()
    import_version = serializers.IntegerField(source="import_version.version")
    start_date = serializers.DateTimeField(format="%d/%m/%Y %H:%M")
    created_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M")
    updated_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M")

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "start_date",
            "venue",
            "category",
            "sympla_id",
            "import_version",
            "created_at",
            "updated_at",
        ] 