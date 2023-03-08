"""
Filename: tests.py
Author: Kacper Raubo
Creation date: 03/08/2023

This module provides tests for the Image and AccountTier models and their
corresponding API views. 

These tests include both unit tests for the models themselves, as well
as integration tests for the corresponding API views.
"""

import io
import os
from PIL import Image as PILImage
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import AccountTier, Image
from .serializers import AccountTierSerializer, ImageSerializer


class AccountTierTests(TestCase):
    """
    Test suite for the AccountTier model and API views.

    The AccountTier model represents a pricing tier that users can subscribe to,
    and the API views provide endpoints for creating new pricing tiers,
    retrieving lists of pricing tiers, and retrieving individual pricing tiers.

    These tests cover both the model and API views to ensure that the system
    is working as expected.
    """

    def setUp(self):
        self.basic_tier = AccountTier.objects.create(
            name='Basic',
            thumbnail_size_1=200,
            thumbnail_size_2=None,
            link_to_original=False,
            link_expiration_time=None
        )
        self.premium_tier = AccountTier.objects.create(
            name='Premium',
            thumbnail_size_1=200,
            thumbnail_size_2=400,
            link_to_original=True,
            link_expiration_time=None
        )
        self.enterprise_tier = AccountTier.objects.create(
            name='Enterprise',
            thumbnail_size_1=200,
            thumbnail_size_2=400,
            link_to_original=True,
            link_expiration_time=600
        )

    def test_account_tier_serializer(self):
        basic_tier = AccountTier.objects.get(name='Basic')
        serialized_tier = AccountTierSerializer(basic_tier)
        expected_data = {
            'id': basic_tier.id,
            'name': 'Basic',
            'thumbnail_size_1': 200,
            'thumbnail_size_2': None,
            'link_to_original': False,
            'link_expiration_time': None
        }
        self.assertEqual(serialized_tier.data, expected_data)


class ImageTests(TestCase):
    """
    Test suite for the Image model and API views.

    The Image model represents an uploaded image, and the API views provide endpoints
    for uploading new images, retrieving lists of images, and retrieving individual images.

    These tests cover both the model and API views to ensure that the system is working as expected.
    """

    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.basic_tier = AccountTier.objects.create(
            name='Basic',
            thumbnail_size_1=200,
            thumbnail_size_2=None,
            link_to_original=False,
            link_expiration_time=None
        )
        self.premium_tier = AccountTier.objects.create(
            name='Premium',
            thumbnail_size_1=200,
            thumbnail_size_2=400,
            link_to_original=True,
            link_expiration_time=None
        )
        self.enterprise_tier = AccountTier.objects.create(
            name='Enterprise',
            thumbnail_size_1=200,
            thumbnail_size_2=400,
            link_to_original=True,
            link_expiration_time=600
        )

    def test_image_upload(self):
        # authenticate user1
        self.client.login(username='user1', password='password')
        user1_account_tier = AccountTier.objects.get(name='Basic')

        # upload an image as user1
        image_file = io.BytesIO()
        image = PILImage.new('RGB', (100, 100), color='red')
        image.save(image_file, 'png')
        image_file.name = 'test_image.png'
        image_file.seek(0)
        response = self.client.post('/images/', {'image': image_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Image.objects.count(), 1)
        image = Image.objects.first()
        expected_thumbnail_1_url = f'http://testserver{image.thumbnail_1.url}'
        expected_data = {
            'id': image.id,
            'user': self.user1.id,
            'image': f'http://testserver{image.image.url}',
            'thumbnail_1': expected_thumbnail_1_url
        }
        self.assertEqual(response.data, expected_data)
        self.assertEqual(image.user, self.user1)
        self.assertEqual(image.account_tier, user1_account_tier)
        self.assertTrue(image.image)
        self.assertTrue(image.thumbnail_1)
        self.assertIsNone(image.thumbnail_2)
        self.assertIsNone(image.link_to_original)
        self.assertIsNone(image.link_expiration_time)
        self.assertTrue(os.path.exists(image.image.path))
        self.assertTrue(os.path.exists(image.thumbnail_1.path))

        # authenticate user2
        self.client.logout()
        self.client.login(username='user2', password='password')
        user2_account_tier = AccountTier.objects.get(name='Premium')

        # upload an image as user2
        image_file = io.BytesIO()
        image = PILImage.new('RGB', (200, 200), color='blue')
        image.save(image_file, 'jpeg')
        image_file.name = 'test_image.jpg'
        image_file.seek(0)
        response = self.client.post('/images/', {'image': image_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Image.objects.count(), 2)
        image = Image.objects.last()
        expected_thumbnail_1_url = f'http://testserver{image.thumbnail_1.url}'
        expected_thumbnail_2_url = f'http://testserver{image.thumbnail_2.url}'
        expected_image_url = f'http://testserver{image.image.url}'
        expected_data = {
            'id': image.id,
            'user': self.user2.id,
            'image': expected_image_url,
            'thumbnail_1': expected_thumbnail_1_url,
            'thumbnail_2': expected_thumbnail_2_url,
            'link_to_original': expected_image_url
        }
        self.assertEqual(response.data, expected_data)
        self.assertEqual(image.user, self.user2)
        self.assertEqual(image.account_tier, user2_account_tier)
        self.assertTrue(image.image)
        self.assertTrue(image.thumbnail_1)
        self.assertTrue(image.thumbnail_2)
        self.assertEqual(image.link_to_original, expected_image_url)
        self.assertIsNone(image.link_expiration_time)
        self.assertTrue(os.path.exists(image.image.path))
        self.assertTrue(os.path.exists(image.thumbnail_1.path))
        self.assertTrue(os.path.exists(image.thumbnail_2.path))