from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from social_media_service.models import Post
from social_media_service.permissions import DeleteUpdateOnlyOwner
from social_media_service.serializers import (
    LikeCreateSerializer,
    LikeDeleteSerializer,
    PostCreateSerializer,
    PostScheduleCreateSerializer,
    PostSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return PostCreateSerializer
        if self.action == "like":
            return LikeCreateSerializer
        if self.action == "unlike":
            return LikeDeleteSerializer
        if self.action == "schedule":
            return PostScheduleCreateSerializer
        return PostSerializer

    def get_permissions(self):
        if self.action in ["create", "schedule", "like", "unlike"]:
            return [IsAuthenticated]
        if self.action in ["update", "destroy"]:
            return [DeleteUpdateOnlyOwner]
        return super().get_permissions()

    def get_queryset(self):
        queryset = Post.objects.all()
        hashtag = self.request.query_params.get("hashtag")
        username = self.request.query_params.get("user")

        if self.action == "list":
            queryset = queryset.filter(user__in=self.request.user.following.all())

        if username:
            queryset = queryset.filter(user__username=username)
        if hashtag:
            queryset = queryset.filter(hashtags__name=hashtag)

        return queryset

    @action(detail=True, methods=["post"], url_path="add-hashtags")
    def add_hashtags(self, request, pk=None):
        post = self.get_object()
        serializer = self.get_serializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="like")
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if post.likes.filter(user=user).exists():
            return Response({"error": "Ти вже поставив лайк цьому посту"})

        context = {"post": post, "user": user}
        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="unlike")
    def unlike(self, request, pk=None):
        post = self.get_object()
        like = post.likes.filter(user=request.user).first()

        if not like:
            return Response({"error": "Ти ще не поставив лайк цьому посту"})

        like.delete()
        return Response({"message": "Лайк успішно видалено"})

    @action(detail=False, methods=["post"], url_path="schedule")
    def schedule(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
