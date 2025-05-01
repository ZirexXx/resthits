from django.test import TestCase
from ..models import Hit, Artist


class ArtistModelTest(TestCase):
    def setUp(self):
        self.artist = Artist.objects.create(
            first_name="Dawid",
            last_name="Podsiadlo"
        )

    def test_artist_creation(self):
        self.assertIsInstance(self.artist, Artist)
        self.assertEqual(self.artist.first_name, "Dawid")
        self.assertEqual(self.artist.last_name, "Podsiadlo")

    def test_artist_str(self):
        self.assertEqual(
            str(self.artist), f"{self.artist.id} - Dawid Podsiadlo"
        )


class HitModelTest(TestCase):
    def setUp(self):
        self.artist = Artist.objects.create(
            first_name="Dawid",
            last_name="Podsiadlo"
        )
        self.hit = Hit.objects.create(
            title="Malomiasteczkowy",
            artist_id=self.artist,
            title_url="malomiasteczkowy-dawid-podsiadlo",
        )

    def test_hit_creation(self):
        self.assertIsInstance(self.hit, Hit)
        self.assertEqual(self.hit.title, "Malomiasteczkowy")
        self.assertEqual(self.hit.artist_id, self.artist)
        self.assertEqual(
            self.hit.title_url,
            "malomiasteczkowy-dawid-podsiadlo"
        )

    def test_hit_str(self):
        self.assertEqual(
            str(self.hit), "Dawid Podsiadlo - Malomiasteczkowy"
        )

    def test_hit_artist_relationship(self):
        self.assertEqual(self.artist.hits.count(), 1)
        self.assertEqual(self.artist.hits.first(), self.hit)
