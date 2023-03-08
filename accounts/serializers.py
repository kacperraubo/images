"""
Filename: serializers.py
Author: Kacper Raubo
Creation date: 03/08/2023

The serializers module is used to transform Django models into Python data
types that can be easily rendered into JSON or XML format. This file defines
two serializers: ImageSerializer and AccountTierSerializer, which are used
to serialize the Image and AccountTier models, respectively.
"""

from rest_framework import serializers
from .models import Image, AccountTier

class ImageSerializer(serializers.ModelSerializer):
    """
    It includes read-only fields for the thumbnail images and link to original,
    which are created automatically when the model is saved. These fields are
    not included in the request payload when uploading a new image, but they
    are included in the response payload when retrieving a list of images. 
    """

    thumbnail_1 = serializers.ImageField(read_only=True)
    thumbnail_2 = serializers.ImageField(read_only=True)
    link_to_original = serializers.URLField(read_only=True)

    class Meta:
        model = Image
        fields = ['id', 'user', 'image', 'thumbnail_1', 'thumbnail_2', 'link_to_original']

class AccountTierSerializer(serializers.ModelSerializer):
    """
    Includes all fields of the AccountTier model, but it may perform formatting
    or data transformations to ensure that the response is consistent and well-formatted.
    """
    
    class Meta:
        model = AccountTier
        fields = ['id', 'name', 'thumbnail_size_1', 'thumbnail_size_2', 'link_to_original', 'link_expiration_time']
