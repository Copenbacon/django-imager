from django.db import models
from imager_profile.models import ImagerProfile


class Photo(models.Model):
    user_id = models.ForeignKey(ImagerProfile, related_name="photo")
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    date_uploaded = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateTimeField()
    PUBLISHED = [
        (1, 'Private'),
        (2, 'Shared'),
        (3, 'Public')
    ]
    published = models.SmallIntegerField(
        choices=PUBLISHED,
        default=1
    )
    albums = models.ManyToManyField(
        'Album',
        related_name='photos',
        blank=True)
    image = models.ImageField(upload_to='images')


class Album(models.Model):
    user_id = models.ForeignKey(ImagerProfile, related_name="album")
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField()
    PUBLISHED = [
        (1, 'Private'),
        (2, 'Shared'),
        (3, 'Public')
    ]
    published = models.SmallIntegerField(
        choices=PUBLISHED,
        default=1
    )
    photos = models.ManyToManyField(
        "Photo",
        related_name="albums",
        symmetrical=False)
    cover = models.ImageField(upload_to='images')
