from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from django.utils.text import slugify
from django.utils import timezone
import random
from .serializers import HitSerializer, ArtistSerializer
from .models import Hit, Artist
from rest_framework.views import exception_handler


def conflict_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ValidationError) and \
            exc.get_codes() == {'detail': ['conflict']}:
        response.status_code = 409
    return response


class HitListCreateView(generics.ListCreateAPIView):
    serializer_class = HitSerializer

    def get_queryset(self):
        return Hit.objects.order_by('-created_at')[:20]

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        title = request.data.get('title')
        artist_id = request.data.get('artist_id')

        if Hit.objects.filter(title=title, artist_id=artist_id).exists():
            return Response(
                {"detail": "Hit already exists."},
                status=status.HTTP_409_CONFLICT
            )

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class HitRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HitSerializer
    lookup_field = 'title_url'

    def get_queryset(self):
        return Hit.objects.all()

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response

    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        return response

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return response


class ArtistListCreateView(generics.ListCreateAPIView):
    serializer_class = ArtistSerializer

    def get_queryset(self):
        return Artist.objects.all()

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        if Artist.objects.filter(
            first_name=first_name.strip(),
            last_name=last_name.strip()
        ).exists():
            return Response(
                {"detail": "Artist already exists."},
                status=status.HTTP_409_CONFLICT
            )

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArtistRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ArtistSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Artist.objects.all()

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return response


# FOR TESTING PURPOSES ONLY
class PopulateArtistsAndHitsView(APIView):
    def get(self, request):
        artist_data = [
            {"first_name": "David", "last_name": "Guetta"},
            {"first_name": "Justin", "last_name": "Timberlake"},
            {"first_name": "Ariana", "last_name": "Grande"}
        ]

        created_artists = []
        for data in artist_data:
            if Artist.objects.filter(
                first_name=data["first_name"],
                last_name=data["last_name"]
            ).exists():
                return Response(
                    {
                        "detail": f"Artist {data['first_name']} "
                                  f"{data['last_name']} already exists."
                    },
                    status=status.HTTP_409_CONFLICT
                )

            serializer = ArtistSerializer(data=data)
            if serializer.is_valid():
                artist = serializer.save()
                created_artists.append(artist)
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

        titles = [
            "Love Again", "Midnight City", "Back to You", "Sky High",
            "Electric Feel", "Lonely Night", "Firestorm", "Broken Wings",
            "Stay With Me", "Miracle", "Lost & Found", "Ocean Eyes",
            "Summer Jam", "Heartbeat", "Shivers", "Dreamscape",
            "On The Run", "Echoes", "Gravity", "Neon Light"
        ]
        random.shuffle(titles)

        hits_created = []
        now = timezone.now()

        for i, title in enumerate(titles):
            artist = created_artists[i % len(created_artists)]
            raw_slug = f"{title}-{artist.first_name}"
            raw_slug += f"-{artist.last_name}-{now.strftime('%Y%m%d%H%M%S')}"
            generated_slug = slugify(raw_slug)

            if Hit.objects.filter(title=title, artist_id=artist).exists():
                return Response(
                    {
                        "detail": f"Hit '{title}' by {artist.first_name} "
                                  f"{artist.last_name} already exists."
                    },
                    status=status.HTTP_409_CONFLICT
                )

            hit = Hit.objects.create(
                title=title,
                artist_id=artist,
                title_url=generated_slug,
                created_at=now,
                updated_at=now
            )
            hits_created.append(hit)

        return Response({
            "artists": ArtistSerializer(created_artists, many=True).data,
            "hits": HitSerializer(hits_created, many=True).data
        }, status=status.HTTP_201_CREATED)
