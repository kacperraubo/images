"""
Filename: models.py
Author: Kacper Raubo
Creation date: 03/08/2023

Models for image uploads and retrieval.

This file defines two models: `AccountTier` and `Image`. 
"""

from PIL import Image as PILImage
from datetime import timedelta
import io

from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from .utils import generate_expiring_link


class AccountTier(models.Model):
    """
    Model representing a pricing tier for image uploads and retrieval.

    This model represents a pricing tier that users can subscribe to in order
    to upload and retrieve images. Each account tier has a name, thumbnail sizes,
    the ability to retrieve the original image file, and the ability to generate
    expiring links to the original file.

    The default account tiers are `Basic`, `Premium`, and `Enterprise`, each with
    different capabilities for image uploads and retrieval. Admin users can create
    additional account tiers with custom capabilities.

    This model is used to associate each image with an account tier, which determines
    the capabilities of the user when retrieving the image.
    """

    name = models.CharField(max_length=100, unique=True)
    thumbnail_size_1 = models.PositiveIntegerField(null=True, blank=True)
    thumbnail_size_2 = models.PositiveIntegerField(null=True, blank=True)
    link_to_original = models.BooleanField(default=False)
    link_expiration_time = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    """
    Model representing an uploaded image.

    This model represents an uploaded image, which is associated with an
    authenticated user and an account tier. Each image has a thumbnail image
    at two different sizes, as well as a link to the original image file.

    When an image is uploaded, the system generates the thumbnail images and
    the link to the original image file. Users with different account tiers
    have different capabilities for retrieving the thumbnail images and the
    original file, as well as the ability to generate expiring links to the
    original file.

    This model is used to represent the uploaded image and its associated metadata.
    """
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')
    account_tier = models.ForeignKey(AccountTier, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    thumbnail_1 = models.ImageField(upload_to='thumbnails/')
    thumbnail_2 = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    link_to_original = models.URLField(null=True, blank=True)
    link_expiration_time = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # create thumbnail 1
        image = PILImage.open(self.image.path)
        image.thumbnail((self.account_tier.thumbnail_size_1, self.account_tier.thumbnail_size_1))
        thumbnail_1_io = io.BytesIO()
        image.save(thumbnail_1_io, 'JPEG')
        thumbnail_1_io.seek(0)
        self.thumbnail_1.save(self.image.name, ContentFile(thumbnail_1_io.read()), save=False)

        # create thumbnail 2 (if applicable)
        if self.account_tier.thumbnail_size_2:
            image = PILImage.open(self.image.path)
            image.thumbnail((self.account_tier.thumbnail_size_2, self.account_tier.thumbnail_size_2))
            thumbnail_2_io = io.BytesIO()
            image.save(thumbnail_2_io, 'JPEG')
            thumbnail_2_io.seek(0)
            self.thumbnail_2.save(self.image.name, ContentFile(thumbnail_2_io.read()), save=False)

        # create link to original (if applicable)
        if self.account_tier.link_to_original:
            self.link_to_original = self.image.url

        # create expiring link (if applicable)
        if self.account_tier.link_expiration_time:
            expiration_time = self.account_tier.link_expiration_time
            expiration_datetime = self.created_at + timedelta(seconds=expiration_time)
            self.link_expiration_time = expiration_datetime
            self.link_to_original = generate_expiring_link(self.image.url, expiration_time)

        super().save(*args, **kwargs)