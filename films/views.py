from django.db import models
from rest_framework import generics, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import Film, Actor, Review
from .serializers import (
    FilmListSerializer,
    FilmDetailSerializer,
    ReviewCreateSerializer,
    CreateRatingSerializer,
    ActorSerializer,
    ActorDetailSerializer,
)
from .service import get_client_ip, FilmFilter, PaginationFilm


class FilmViewSet(viewsets.ReadOnlyModelViewSet):
    '''Вывод списка фильмов'''
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilmFilter
    pagination_class = PaginationFilm

    def get_queryset(self):
        films = Film.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return films

    def get_serializer_class(self):
        if self.action == 'list':
            return FilmListSerializer
        elif self.action == "retrieve":
            return FilmDetailSerializer


class ReviewCreateViewSet(viewsets.ModelViewSet):
    '''Добавление отзыва к фильму'''
    serializer_class = ReviewCreateSerializer


class AddStarRatingViewSet(viewsets.ModelViewSet):
    '''Добавление рейтинга к фильму'''
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorViewSet(viewsets.ReadOnlyModelViewSet):
    '''Вывод актеров или режиссеров'''
    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ActorSerializer
        elif self.action == "retrieve":
            return ActorDetailSerializer




# class FilmListView(generics.ListAPIView):
#     '''Вывод списка фильмов'''
#     serializer_class = FilmListSerializer
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = FilmFilter
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_queryset(self):
#         films = Film.objects.filter(draft=False).annotate(
#             rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request)))
#         ).annotate(
#             middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
#         )
#         return films
#
#
# class FilmDetailView(generics.RetrieveAPIView):
#     '''Вывод полного описания фильмов'''
#     queryset = Film.objects.filter(draft=False)
#     serializer_class = FilmDetailSerializer
#
# class ReviewCreateView(generics.CreateAPIView):
#     '''Добавление отзыва к фильму'''
#     serializer_class = ReviewCreateSerializer
#
#
# class AddStarRatingView(generics.CreateAPIView):
#     '''Добавление рейтинга фильму'''
#     serializer_class = CreateRatingSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(ip=get_client_ip(self.request))
#
#
# class ActorListView(generics.ListAPIView):
#     '''Вывод списка актеров или режиссеров'''
#     queryset = Actor.objects.all()
#     serializer_class = ActorSerializer
#
#
# class ActorDetailView(generics.RetrieveAPIView):
#     '''Вывод полного описания актеров или режиссеров'''
#     queryset = Actor.objects.all()
#     serializer_class = ActorDetailSerializer