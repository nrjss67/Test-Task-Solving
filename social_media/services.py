from uuid import uuid4


def picture_path(instance, filename):
    return f"media/{instance.__class__.__name__}/{instance.user.email}/{uuid4()}-{filename}"
