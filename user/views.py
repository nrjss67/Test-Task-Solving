from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from rest_framework.decorators import action


from social_media_service.permissions import DeleteUpdateOnlyOwner
from user.serializers import (
    ProfileFollowUnfollowSerializer,
    UserSerializer,
    ProfileSerializer,
)
from user.models import Profile


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "user": serializer.data,
                    "token": str(RefreshToken.for_user(user).access_token),
                    "refresh_token": str(RefreshToken.for_user(user)),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_serializer_class(self):
        if self.action == "follow":
            return ProfileFollowUnfollowSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ["follow", "unfollow"]:
            return [IsAuthenticated]
        if self.action in ["destroy", "update"]:
            return [DeleteUpdateOnlyOwner]
        return super().get_permissions()

    @action(detail=True, methods=["post"], url_path="follow")
    def follow(self, request, *args, **kwargs):
        profile = self.get_object()
        user = request.user
        profile.user.followers.add(user)
        return Response({"message": "Followed successfully"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="unfollow")
    def unfollow(self, request, *args, **kwargs):
        profile = self.get_object()
        user = request.user
        profile.user.followers.remove(user)
        return Response(
            {"message": "Unfollowed successfully"}, status=status.HTTP_200_OK
        )
