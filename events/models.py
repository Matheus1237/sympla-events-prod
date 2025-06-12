from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ImportLog(BaseModel):
    class Status(models.TextChoices):
        SUCCESS = "SUCCESS", _("Success")
        ERROR = "ERROR", _("Error")

    status = models.CharField(max_length=10, choices=Status.choices)
    imported_count = models.IntegerField(default=0)
    error_message = models.TextField(null=True, blank=True)
    version = models.IntegerField()

    class Meta:
        ordering = ["-created_at"]


class Venue(BaseModel):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    sympla_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name} - {self.city}"

    class Meta:
        ordering = ["name"]


class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]


class Event(BaseModel):
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="events")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="events")
    sympla_id = models.CharField(max_length=100, unique=True)
    import_version = models.ForeignKey(ImportLog, on_delete=models.CASCADE, related_name="events")
    raw_data = models.JSONField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-start_date"]
        indexes = [
            models.Index(fields=["sympla_id"]),
            models.Index(fields=["start_date"]),
        ]
