from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions

from .models import *
from .serializers import *
from .permissions import HasUserAPIKey


class usersListView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        data = User.objects.all()

        serializer = UserSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class usersDetailView(APIView):
    permission_classes = [HasUserAPIKey]

    def get(self, request, user_id, *args, **kwargs):
        key = request.META["HTTP_AUTHORIZATION"].split()[1]
        api_key = UserAPIKey.objects.get_from_key(key)
        user = User.objects.get(api_key=api_key)

        serializer = UserSerializer(user, context={'request': request}, many=False)

        if user.id == int(user_id):
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user_id, *args, **kwargs):
        key = request.META["HTTP_AUTHORIZATION"].split()[1]
        api_key = UserAPIKey.objects.get_from_key(key)

        try:
            user_edit = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(api_key=api_key)

        serializer = UserSerializer(user_edit, data=request.data,context={'request': request})
        
        if user.id == int(user_id):
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id, *args, **kwargs):
        key = request.META["HTTP_AUTHORIZATION"].split()[1]
        api_key = UserAPIKey.objects.get_from_key(key)

        try:
            user_del = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        user = User.objects.get(api_key=api_key)

        if user.id == int(user_id):
            user_del.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class userAdminDetailView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, user_id, *args, **kwargs):
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user, context={'request': request}, many=False)
        return Response(serializer.data)

    def put(self, request, user_id, *args, **kwargs):
        try:
            user_edit = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user_edit, data=request.data,context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id, *args, **kwargs):
        try:
            user_del = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user_del.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)