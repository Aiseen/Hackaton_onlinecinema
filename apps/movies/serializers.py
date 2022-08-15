from rest_framework import serializers

from apps.movies.models import Category, Image, Film, Review, Rating

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print(representation)
        return representation


class ReviewSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    class Meta:
        model = Review
        fields = '__all__'



class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'


class FilmSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    images = ImageSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Film
        fields = '__all__'

    def create(self, validated_data):
        requests = self.context.get('request')
        images = requests.FILES
        film = Film.objects.create(**validated_data)
        print(images)

        for image in images.getlist('images'):
            Image.objects.create(film=film, image=image)

        return film

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes'] = instance.likes.filter(like=True).count()
        representation['favourits'] = instance.favourits.filter(favourite=True).count()
        rating_result = 0
        for rating in instance.ratings.all():
            rating_result += int(rating.rating)
        try:
            representation['rating'] = rating_result / instance.ratings.all().count()
        except ZeroDivisionError:
            pass
        return representation



class RatingSerializer(serializers.ModelSerializer):


    class Meta:
        model = Rating
        fields = ['rating']

    rating = serializers.IntegerField(required=True,min_value=1,max_value=5)
    def create(self, validated_data):
        print(validated_data)
        validated_data['owner'] = self.context.get('request').user
        validated_data['film_id'] = self.context.get('film_id')
        return super().create(validated_data)



