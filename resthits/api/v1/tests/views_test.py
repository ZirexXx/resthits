from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Artist, Hit
from django.urls import reverse


class HitListCreateViewTest(APITestCase):
    def setUp(self):
        self.artist = Artist.objects.create(
            first_name="Dawid",
            last_name="Podsiadlo"
        )
        self.hit_data = {
            "title": "Małomiasteczkowy",
            "artist_id": self.artist.id
        }
        self.url = reverse('hit-list-create')

    def test_get_hits(self):
        Hit.objects.create(
            title="Małomiasteczkowy",
            artist_id=self.artist,
            title_url="malomiasteczkowy-dawid-podsiadlo"
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_hit(self):
        response = self.client.post(self.url, self.hit_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Hit.objects.count(), 1)
        self.assertEqual(Hit.objects.first().title, "Małomiasteczkowy")


class HitRetrieveUpdateDestroyViewTest(APITestCase):
    def setUp(self):
        self.artist = Artist.objects.create(
            first_name="Dawid",
            last_name="Podsiadlo"
        )
        self.hit = Hit.objects.create(
            title="Malomiasteczkowy",
            artist_id=self.artist,
            title_url="malomiasteczkowy-dawid-podsiadlo"
        )
        self.url = reverse(
            'hit-detail',
            kwargs={'title_url': self.hit.title_url}
        )

    def test_get_hit(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.hit.title)

    def test_update_hit(self):
        updated_data = {"title": "Nieznajomy", "artist_id": self.artist.id}
        response = self.client.put(self.url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.hit.refresh_from_db()
        self.assertEqual(self.hit.title, "Nieznajomy")

    def test_delete_hit(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Hit.objects.count(), 0)


class ArtistListCreateViewTest(APITestCase):
    def setUp(self):
        self.artist_data = {"first_name": "Dawid", "last_name": "Podsiadlo"}
        self.url = reverse('artist-list-create')

    def test_get_artists(self):
        Artist.objects.create(**self.artist_data)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_artist(self):
        response = self.client.post(self.url, self.artist_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Artist.objects.count(), 1)
        self.assertEqual(Artist.objects.first().first_name, "Dawid")


class ArtistRetrieveUpdateDestroyViewTest(APITestCase):
    def setUp(self):
        self.artist = Artist.objects.create(
            first_name="Dawid",
            last_name="Podsiadlo"
        )
        self.url = reverse('artist-detail', kwargs={'pk': self.artist.pk})

    def test_get_artist(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], self.artist.first_name)

    def test_delete_artist(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Artist.objects.count(), 0)
