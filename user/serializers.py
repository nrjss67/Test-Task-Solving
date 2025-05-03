from rest_framework import serializers, mixins

from user.models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    profile_picture = serializers.ImageField(required=False)
    followers_count = serializers.IntegerField(read_only=True, source="followers.count")
    following_count = serializers.IntegerField(read_only=True, source="following.count")
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "profile_picture",
            "bio",
            "followers_count",
            "followers",
            "following_count",
            "following",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        profile = Profile.objects.create(**validated_data)
        return profile

    def get_followers(self, obj):
        return UserSerializer(obj.get_followers, many=True).data

    def get_following(self, obj):
        return UserSerializer(obj.get_following, many=True).data


class ProfileFollowUnfollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id"]
