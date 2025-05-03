from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

from social_media_service.models import Post, Hashtag


@shared_task()
def async_schedule_create_post(user, image, content, hashtags):
    try:
        user = get_user_model().objects.get(id=user)

        post = Post.objects.create(
            user=user,
            image=image,
            content=content,
        )

        hashtag_objects = []
        for tag_name in hashtags:
            tag, _ = Hashtag.objects.get_or_create(name=tag_name)
            hashtag_objects.append(tag)

        post.hashtags.set(hashtag_objects)
        post.save()

        print(f"Post created successfully with id {post.id}")
        return post.id

    except Exception as e:
        raise e
