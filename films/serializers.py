from rest_framework import serializers

from .models import Film, Review, Rating, Actor


class FilterReviewListSerializer(serializers.ListSerializer):
    '''Фильтр комментариев, только parent'''
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    '''Вывод рекурсивно children'''
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ActorSerializer(serializers.ModelSerializer):
    '''Вывод списка актеров и режиссеров'''
    class Meta:
        model = Actor
        fields = ("id", "name", "image")


class ActorDetailSerializer(serializers.ModelSerializer):
    '''Вывод полного описания актеров и режиссеров'''
    class Meta:
        model = Actor
        fields = "__all__"


class FilmListSerializer(serializers.ModelSerializer):
    '''Список фильмов'''
    rating_user = serializers.BooleanField()
    middle_star = serializers.IntegerField()

    class Meta:
        model = Film
        fields = ("id", "title", "tagline", "category", "rating_user", "middle_star", "poster")


class ReviewCreateSerializer(serializers.ModelSerializer):
    '''Добавление отзыва к фильму'''

    class Meta:
        model = Review
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    '''Вывод отзывов'''
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ("id", "name", "text", "children")

class FilmDetailSerializer(serializers.ModelSerializer):
    '''Полное описание фильмов'''
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = ActorSerializer(read_only=True, many=True)
    actors = ActorSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    review = ReviewSerializer(many=True)

    class Meta:
        model = Film
        exclude = ("draft", )

class CreateRatingSerializer(serializers.ModelSerializer):
    '''Добавление рейтинга пользователем'''
    class Meta:
        model = Rating
        fields = ("star", "movie")

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get("star")}
        )
        return rating