"""
Filename: admin.py
Author: Kacper Raubo
Creation date: 03/08/2023

Admin configuration for the AccountTier and Image models.

This file defines admin views for the AccountTier and Image models, which allow
administrators to view and edit instances of these models through the Django admin site.
"""

from django.contrib import admin
from .models import AccountTier, Image

@admin.register(AccountTier)
class AccountTierAdmin(admin.ModelAdmin):
    """
    Admin configuration for the AccountTierAdmin model.
    """

    list_display = ['name', 'thumbnail_size_1', 'thumbnail_size_2', 'link_to_original', 'link_expiration_time']
    search_fields = ['name']

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Image model.
    """

    list_display = ('id', 'title', 'owner', 'thumbnail_1', 'thumbnail_2', 'image')
