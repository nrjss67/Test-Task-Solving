from datetime import datetime
from time import timezone
from rest_framework import serializers
import pytz

from social_media_service.models import Hashtag, Like, Post
from social_media_service.tasks import async_schedule_create_post


class HashtagCustomField(serializers.ListField):
    child = serializers.CharField()

    def to_representation(self, value):
        if isinstance(value, list):
            return [item for item in value]

    def to_internal_value(self, data):
        if not isinstance(data, list):
            raise serializers.ValidationError("Хештеги повинні бути списком")
        return [Hashtag.objects.get_or_create(name=item)[0] for item in data]


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ["id", "user"]


class LikeCreateSerializer(LikeSerializer):

    class Meta:
        model = Like
        fields = ["id"]

    def create(self, validated_data):
        post = self.context["post"]
        user = self.context["user"]
        like = Like.objects.create(user=user, post=post)
        return like


class LikeDeleteSerializer(LikeSerializer):

    class Meta:
        model = Like
        fields = ["id"]


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "image",
            "content",
            "hashtags",
            "count_of_likes",
            "likes",
            "created_at",
            "updated_at",
        ]

    def get_likes(self, obj):
        return LikeSerializer(obj.likes.all(), many=True).data


class PostHashtagsSerializer(PostSerializer):

    class Meta:
        model = Hashtag
        fields = ["id", "name"]


class PostCreateSerializer(PostSerializer):
    hashtags = HashtagCustomField()

    class Meta:
        model = Post
        fields = ["id", "image", "content", "hashtags", "created_at", "updated_at"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        hashtags = validated_data.pop("hashtags")

        post = Post.objects.create(**validated_data)
        post.hashtags.set(hashtags)
        post.save()

        return post


class PostScheduleResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    scheduled_time = serializers.DateTimeField()
    content = serializers.CharField()
    hashtags = HashtagCustomField()


class PostScheduleCreateSerializer(serializers.Serializer):
    scheduled_time = serializers.DateTimeField()
    hashtags = HashtagCustomField(required=False)
    image = serializers.ImageField(required=False, allow_null=True)
    content = serializers.CharField()

    class Meta:
        model = Post
        fields = ["image", "content", "hashtags", "scheduled_time"]

    def create(self, validated_data):
        user = self.context["request"].user.id
        hashtags = [hashtag.name for hashtag in validated_data.get("hashtags", [])]
        scheduled_time = validated_data["scheduled_time"]

        if isinstance(scheduled_time, str):
            scheduled_time = datetime.fromisoformat(
                scheduled_time.replace("Z", "+00:00")
            )

        # Створюємо таску напряму
        task = async_schedule_create_post.apply_async(
            kwargs={
                "user": user,
                "image": validated_data.get("image"),
                "content": validated_data["content"],
                "hashtags": hashtags,
            },
            eta=scheduled_time,
        )

        respons_data = {
            "scheduled_time": scheduled_time,
            "content": validated_data["content"],
            "hashtags": hashtags,
        }
        return PostScheduleResponseSerializer(respons_data).data
