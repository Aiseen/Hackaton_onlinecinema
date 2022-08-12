from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.movies.models import Category, Film, Like, Review, Rating
from apps.movies.serializers import CategorySerializer, FilmSerializer, ReviewSerializer, RatingSerializer


class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class FilmView(ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    search_fields = ['name', 'description']
    ordering_fields = ['company']
    permission_classes = [IsAuthenticated]

    # @action(detail=False, methods=['GET'])
    # def my_films(self, request, pk=None):
    #     queryset = self.get_queryset()
    #     queryset = queryset.filter(owner=request.user)
    #     serializer = FilmSerializer(queryset, many=True)
    #     return Response(serializer.data, status=200)

    @action(methods=['POST'], detail=True)
    def like(self, request, pk, *args, **kwargs):
        try:

            like_object, _ = Like.objects.get_or_create(owner=request.user, film_id=pk)
            like_object.like = not like_object.like
            like_object.save()
            status = 'liked'

            if like_object.like:
                return Response({'status': status})
            status = 'unliked'
            return Response({'status': status})
        except:
            return Response('Такого фильма у нас нет')


    @action(methods=['POST'], detail=True)
    def rating(self,request,pk,*args,**kwargs):
        serializers = RatingSerializer(data=request.data, context={'film_id': pk, 'request': request})
        print(request.data)
        serializers.is_valid(raise_exception=True)

        serializers.save()
        return Response(request.data,status=201)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permissions = []
        elif self.action == 'like':
            permissions = [IsAuthenticated]
        else:
            permissions = [IsAuthenticated]

        return [p() for p in permissions]


class ReviewView(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

