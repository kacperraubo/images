"""
Filename: tests.py
Author: Kacper Raubo
Creation date: 03/08/2023

Provides API endpoints for uploading, retrieving, and listing images as well
as retrieving account tiers. 

All viewsets require JWT authentication and only authorized users can access
their own images. By default, images are uploaded with a `Basic` account tier,
which allows users to retrieve a 200px thumbnail of the image. Users with
`Premium` and `Enterprise` account tiers can retrieve larger thumbnails and
the original image file, as well as generate expiring links to the original file. 

Admin users can create additional account tiers with custom capabilities,
such as different thumbnail sizes, the ability to retrieve the original image
file, and the ability to generate expiring links to the original file. 

This module also defines several actions for retrieving specific data about
an image, including its thumbnails, links, and expiration time. 

"""

from datetime import timedelta, datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import AccountTier, Image
from .serializers import AccountTierSerializer, ImageSerializer
from rest_framework.decorators import authentication_classes
from rest_framework.permissions import IsAuthenticated
from images.jwt import JWTAuthentication


@authentication_classes([JWTAuthentication])
class AccountTierViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to retrieve account tiers.

    This viewset provides read-only endpoints for retrieving lists of account
    tiers and individual account tiers. The default account tiers are `Basic`,
    `Premium`, and `Enterprise`, each with different capabilities for image
    uploads and retrieval.

    Admin users can create additional account tiers with custom capabilities,
    such as different thumbnail sizes, the ability to retrieve the original
    image file, and the ability to generate expiring links to the original file.

    This viewset requires authentication, and only admin users can create new account tiers.
    """

    queryset = AccountTier.objects.all()
    serializer_class = AccountTierSerializer


@authentication_classes([JWTAuthentication])
class ImageViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    API endpoint that allows users to upload, retrieve, and list images.

    This viewset provides endpoints for creating new images, retrieving individual images, and retrieving
    lists of images. It also provides a custom `thumbnail` action for retrieving thumbnail images at specific sizes.

    By default, images are uploaded with a `Basic` account tier, which allows users to retrieve a 200px thumbnail
    of the image. Users with `Premium` and `Enterprise` account tiers can retrieve larger thumbnails and the original
    image file, as well as generate expiring links to the original file.

    This viewset requires authentication, and each image is associated with the authenticated user. Users can only
    retrieve or delete images that they have uploaded themselves.
    """

    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['user', 'created_at']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        user = self.request.user
        account_tier = user.account_tier
        data = serializer.validated_data

        # save the image
        image = data['image']
        instance = serializer.save(user=user)

        # create thumbnails based on user's account tier
        if account_tier.thumbnail_size_1:
            instance.thumbnail_1.save(
                f'thumbnail_1_{image.name}',
                image,
                save=False
            )
        if account_tier.thumbnail_size_2:
            instance.thumbnail_2.save(
                f'thumbnail_2_{image.name}',
                image,
                save=False
            )

        # save link to the original image if allowed by account tier
        if account_tier.link_to_original:
            instance.link = instance.image.url

        # save expiration time if allowed by account tier
        if account_tier.link_expiration_time:
            time_delta = timedelta(seconds=account_tier.link_expiration_time)
            instance.expiration_time = datetime.now() + time_delta

        instance.save()


@authentication_classes([JWTAuthentication])
class UserImageViewSet(generics.ListAPIView):
    """
    API endpoint that allows users to list their uploaded images.

    The endpoint requires JWT authentication, and only the user
    associated with the JWT token will be able to access their own images.

    If the user has a 'Basic' account tier, the API response will include
    links to 200px thumbnail images.

    If the user has a 'Premium' account tier, the API response will include
    links to 200px and 400px thumbnail images, as well as a link to the full-size image.

    If the user has an 'Enterprise' account tier, the API response will
    include links to 200px and 400px thumbnail images, as well as a link
    to the full-size image and an expiring link to the full-size image.
    """

    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Image.objects.filter(user=user)

    @action(detail=True, methods=['get'])
    def thumbnail_1(self, request, pk=None):
        image = self.get_object()
        if image.thumbnail_1:
            return Response({'thumbnail_1': image.thumbnail_1.url})
        return Response({'error': 'Thumbnail 1 not found.'})

    @action(detail=True, methods=['get'])
    def thumbnail_2(self, request, pk=None):
        image = self.get_object()
        if image.thumbnail_2:
            return Response({'thumbnail_2': image.thumbnail_2.url})
        return Response({'error': 'Thumbnail 2 not found.'})

    @action(detail=True, methods=['get'])
    def link(self, request, pk=None):
        image = self.get_object()
        if image.link:
            return Response({'link': image.link})
        return Response({'error': 'Link not found.'})

    @action(detail=True, methods=['get'])
    def expiration_time(self, request, pk=None):
        image = self.get_object()
        if image.expiration_time:
            return Response({'expiration_time': image.expiration_time})
        return Response({'error': 'Expiration time not found.'})
