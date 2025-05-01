from rest_framework import serializers
from django.utils.text import slugify
from django.utils import timezone
from .models import Hit, Artist


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = [
            'id',
            'first_name',
            'last_name',
            'created_at'
        ]
        read_only_fields = [
            'id',
            'created_at'
        ]

    def create(self, validated_data):
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        now = timezone.now()

        artist = Artist.objects.create(
            first_name=first_name,
            last_name=last_name,
            created_at=now
        )
        return artist

    def delete(self, instance):
        instance.delete()
        return instance


class HitSerializer(serializers.ModelSerializer):
    artist_id = serializers.PrimaryKeyRelatedField(
        queryset=Artist.objects.all()
    )

    class Meta:
        model = Hit
        fields = [
            'id',
            'title',
            'artist_id',
            'title_url',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'title_url',
            'created_at',
            'updated_at'
        ]

    def create(self, validated_data):
        title = validated_data['title']
        artist = validated_data['artist_id']
        now = timezone.now()

        artist_name = f"{artist.first_name}-{artist.last_name}"
        raw_slug = f"{title}-{artist_name}-{now.strftime('%Y%m%d%H%M%S')}"
        generated_slug = slugify(raw_slug)

        hit = Hit.objects.create(
            title=title,
            artist_id=artist,
            title_url=generated_slug,
            created_at=now,
            updated_at=now
        )
        return hit

    def update(self, instance, validated_data):
        instance.title = validated_data.get(
            'title',
            instance.title
        )
        instance.artist_id = validated_data.get(
            'artist_id',
            instance.artist_id
        )

        if 'title' in validated_data:
            artist_name = f"{instance.artist_id.first_name}"
            artist_name += f"-{instance.artist_id.last_name}"
            raw_slug = f"{instance.title}-{artist_name}"
            raw_slug += f"-{instance.created_at.strftime('%Y%m%d%H%M%S')}"
            instance.title_url = slugify(raw_slug)

        instance.updated_at = timezone.now()

        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        return instance
