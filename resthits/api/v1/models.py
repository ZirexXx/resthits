from django.db import models
from simple_history.models import HistoricalRecords


class Artist(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.first_name} {self.last_name}"


class Hit(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    artist_id = models.ForeignKey(
        Artist,
        on_delete=models.DO_NOTHING,
        related_name='hits'
    )
    title_url = models.CharField(max_length=1024, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        msg = f"{self.artist_id.first_name}"
        msg += f" {self.artist_id.last_name}"
        msg += f" - {self.title}"
        return msg
