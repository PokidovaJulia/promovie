from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = format_suffix_patterns([
    path("film/", views.FilmViewSet.as_view({'get': 'list'})),
    path("film/<int:pk>", views.FilmViewSet.as_view({'get': 'retrieve'})),
    path("review/", views.ReviewCreateViewSet.as_view({'post': 'create'})),
    path("rating/", views.AddStarRatingViewSet.as_view({'post': 'create'})),
    path("actors/", views.ActorViewSet.as_view({'get': 'list'})),
    path("actors/<int:pk>", views.ActorViewSet.as_view({'get': 'retrieve'})),
])

# urlpatterns = [
#     path("film/", views.FilmListView.as_view()),
#     path("film/<int:pk>", views.FilmDetailView.as_view()),
#     path("review/", views.ReviewCreateView.as_view()),
#     path("rating/", views.AddStarRatingView.as_view()),
#     path("actors/", views.ActorListView.as_view()),
#     path("actors/<int:pk>", views.ActorDetailView.as_view()),
# ]