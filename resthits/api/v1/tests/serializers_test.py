from django.test import TestCase
from ..models import Artist, Hit
from ..serializers import ArtistSerializer, HitSerializer


class ArtistSerializerTest(TestCase):
    def setUp(self):
        self.artist_data = {
            "first_name": "Dawid",
            "last_name": "Podsiadlo"
        }
        self.artist = Artist.objects.create(**self.artist_data)

    def test_artist_serializer_create(self):
        serializer = ArtistSerializer(data=self.artist_data)
        self.assertTrue(serializer.is_valid())
        artist = serializer.save()
        self.assertEqual(artist.first_name, self.artist_data["first_name"])
        self.assertEqual(artist.last_name, self.artist_data["last_name"])

    def test_artist_serializer_fields(self):
        serializer = ArtistSerializer(instance=self.artist)
        self.assertEqual(serializer.data["first_name"], self.artist.first_name)
        self.assertEqual(serializer.data["last_name"], self.artist.last_name)
        self.assertIn("created_at", serializer.data)


class HitSerializerTest(TestCase):
    def setUp(self):
        self.artist = Artist.objects.create(
            first_name="Dawid",
            last_name="Podsiadlo"
        )
        self.hit_data = {
            "title": "Malomiasteczkowy",
            "artist_id": self.artist.id
        }
        self.hit = Hit.objects.create(
            title="Malomiasteczkowy",
            artist_id=self.artist,
            title_url="malomiasteczkowy-dawid-podsiadlo"
        )

    def test_hit_serializer_create(self):
        serializer = HitSerializer(data=self.hit_data)
        self.assertTrue(serializer.is_valid())
        hit = serializer.save()
        self.assertEqual(hit.title, self.hit_data["title"])
        self.assertEqual(hit.artist_id, self.artist)
        self.assertTrue(
            hit.title_url.startswith("malomiasteczkowy-dawid-podsiadlo")
        )

    def test_hit_serializer_fields(self):
        serializer = HitSerializer(instance=self.hit)
        self.assertEqual(serializer.data["title"], self.hit.title)
        self.assertEqual(serializer.data["artist_id"], self.artist.id)
        self.assertEqual(serializer.data["title_url"], self.hit.title_url)
        self.assertIn("created_at", serializer.data)
        self.assertIn("updated_at", serializer.data)

    def test_hit_serializer_update(self):
        updated_data = {
            "title": "Nieznajomy",
            "artist_id": self.artist.id
        }
        serializer = HitSerializer(instance=self.hit, data=updated_data)
        self.assertTrue(serializer.is_valid())
        updated_hit = serializer.save()
        self.assertEqual(updated_hit.title, "Nieznajomy")
        self.assertTrue(
            updated_hit.title_url.startswith("nieznajomy-dawid-podsiadlo")
        )
