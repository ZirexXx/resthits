from django.urls import path
from .views import HitListCreateView, HitRetrieveUpdateDestroyView
from .views import ArtistListCreateView, ArtistRetrieveUpdateDestroyView
from .views import PopulateArtistsAndHitsView

urlpatterns = [
    path(
        route='hits/',
        view=HitListCreateView.as_view(),
        name='hit-list-create'
    ),
    path(
        route='hits/<str:title_url>/',
        view=HitRetrieveUpdateDestroyView.as_view(),
        name='hit-detail'
    ),
    path(
        route='artists/',
        view=ArtistListCreateView.as_view(),
        name='artist-list-create'
    ),
    path(
        route='artists/<int:pk>/',
        view=ArtistRetrieveUpdateDestroyView.as_view(),
        name='artist-detail',
    ),
    path(
        route='populate/',
        view=PopulateArtistsAndHitsView.as_view(),
        name='populate-artists-and-hits'
    )
]
