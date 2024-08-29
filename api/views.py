from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

from .serializers import (
    ResultSerializer,
    UserSerializer, 
    ArticleSerializer, 
    MentorAppointmentSerializer,
    ContactSerializer, 
    MetaSerializer,
    CategorySerializer,
    EventSerializer,
    MentorSerializer,
)

from .models import (
    ResultModel, 
    UserModel, 
    ArticleModel, 
    ContactModel, 
    MentorAppointmentModel, 
    CategoryModel,
    EventModel,
    Meta,
    MentorModel
)


class MetaAPIView(APIView):
    def get(self, request, key):
        try:
            obj: Meta = Meta.objects.get(key=key.replace("$", "/"))
            return Response({"data": MetaSerializer(obj).data})
        except:
            return Response(f"Couldn't load {key.replace('$', '/')}")


class MentorView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = MentorSerializer
    parser_classes = [MultiPartParser, FormParser]
    
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        queryset = MentorModel.objects.all()

        if user_id:
            queryset = queryset.filter(id=user_id)

        status = self.request.query_params.get('status')
        
        if status:
            queryset = queryset.filter(status=status)

        return queryset
    
    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            user = get_object_or_404(MentorModel, id=kwargs['pk'])
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK) 

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        instance = MentorModel.objects.get(id=user_id)

        old_result_id = None
        if 'result' in request.data:
            old_result_id = instance.result

        excluded_fields  = None
        if not('photo' in request.data):
            excluded_fields = ['photo']

        serializer = UserSerializer(instance, excluded_fields=excluded_fields, partial=True)

        serializer_data = serializer.data
        serializer_data.update(request.data)

        serializer = UserSerializer(instance, data=serializer_data, excluded_fields=excluded_fields, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if old_result_id is not None:
            result_instance = ResultModel.objects.get(pk=old_result_id)
            result_instance.delete()
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "user was deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class UserView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, FormParser]
    
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        queryset = UserModel.objects.all()

        if user_id:
            queryset = queryset.filter(id=user_id)

        status = self.request.query_params.get('status')
        
        if status:
            queryset = queryset.filter(status=status)

        return queryset
    
    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            user = get_object_or_404(UserModel, id=kwargs['pk'])
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK) 

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        instance = UserModel.objects.get(id=user_id)

        old_result_id = None
        if 'result' in request.data:
            old_result_id = instance.result

        excluded_fields  = None
        if not('photo' in request.data):
            excluded_fields = ['photo']

        serializer = UserSerializer(instance, excluded_fields=excluded_fields, partial=True)

        serializer_data = serializer.data
        serializer_data.update(request.data)

        serializer = UserSerializer(instance, data=serializer_data, excluded_fields=excluded_fields, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if old_result_id is not None:
            result_instance = ResultModel.objects.get(pk=old_result_id)
            result_instance.delete()
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "user was deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class CategoryView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        category_id = self.request.query_params.get('category_id')

        if category_id:
            return CategoryModel.objects.filter(id=category_id)

        return CategoryModel.objects.all()
    
    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            article = get_object_or_404(CategoryModel, id=kwargs['pk'])
            serializer = self.get_serializer(article)
            return Response(serializer.data, status=status.HTTP_200_OK) 

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        category_id = kwargs.get('pk')
        instance = CategoryModel.objects.get(id=category_id)

        serializer = CategorySerializer(instance)

        serializer_data = serializer.data
        serializer_data.update(request.data)

        serializer = CategorySerializer(instance, data=serializer_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "category was deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ArticleView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        article_id = self.request.query_params.get('article_id')
        category_ids = self.request.query_params.getlist('category_id')
        title = self.request.query_params.get('title')

        queryset = ArticleModel.objects.all()

        if article_id:
            return queryset.filter(id=article_id)
        
        if category_ids:
            return queryset.filter(categories__id__in=category_ids)
        
        if title:
            return queryset.filter(title_en=title)

        return queryset
    
    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            article = get_object_or_404(ArticleModel, id=kwargs['pk'])
            serializer = self.get_serializer(article)
            return Response(serializer.data, status=status.HTTP_200_OK) 

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        article_id = kwargs.get('pk')
        instance = UserModel.objects.get(id=article_id)

        excluded_fields  = None
        if not('image' in request.data):
            excluded_fields = ['image']

        serializer = ArticleSerializer(instance, excluded_fields=excluded_fields, partial=True)

        serializer_data = serializer.data
        serializer_data.update(request.data)

        serializer = ArticleSerializer(instance, data=serializer_data, excluded_fields=excluded_fields, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "article was deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ContactView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = ContactSerializer

    def get_queryset(self):
        contact_id = self.request.query_params.get('contact_id')

        if contact_id:
            return ContactModel.objects.filter(id=contact_id)

        return ContactModel.objects.all()
    
    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            contact = get_object_or_404(ContactModel, id=kwargs['pk'])
            serializer = self.get_serializer(contact)
            return Response(serializer.data, status=status.HTTP_200_OK) 

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        contact_id = kwargs.get('pk')
        instance = ContactModel.objects.get(id=contact_id)

        serializer = ContactSerializer(instance)

        serializer_data = serializer.data
        serializer_data.update(request.data)

        serializer = ContactSerializer(instance, data=serializer_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()


    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "contact was deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class MentorAppointmentView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = MentorAppointmentSerializer

    def get_queryset(self):
        appointment_id = self.request.query_params.get('appointment_id')

        if appointment_id:
            return MentorAppointmentModel.objects.filter(id=appointment_id)

        return MentorAppointmentModel.objects.all()
    
    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            appointment = get_object_or_404(MentorAppointmentModel, id=kwargs['pk'])
            serializer = self.get_serializer(appointment)
            return Response(serializer.data, status=status.HTTP_200_OK) 

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        appointment_id = kwargs.get('pk')
        instance = MentorAppointmentModel.objects.get(id=appointment_id)

        serializer = MentorAppointmentSerializer(instance)

        serializer_data = serializer.data
        serializer_data.update(request.data)

        serializer = MentorAppointmentSerializer(instance, data=serializer_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Employee deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ResultView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = ResultSerializer

    def get_queryset(self):
        result_id = self.request.query_params.get('result_id')

        if result_id:
            return ResultModel.objects.filter(id=result_id)
        
        user_id = self.request.query_params.get('user_id')

        if user_id:
            return ResultModel.objects.filter(user_id=user_id)

        return ResultModel.objects.all()
    
    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            result = get_object_or_404(ResultModel, id=kwargs['pk'])
            serializer = self.get_serializer(result)
            return Response(serializer.data, status=status.HTTP_200_OK) 

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        result_id = kwargs.get('pk')
        instance = ResultModel.objects.get(id=result_id)

        serializer = ResultSerializer(instance)

        serializer_data = serializer.data
        serializer_data.update(request.data)

        serializer = ResultSerializer(instance, data=serializer_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "result was deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class EventView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        event_id = self.request.query_params.get('event_id')

        if event_id:
            return EventModel.objects.filter(id=event_id)

        return EventModel.objects.all()
    
    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            result = get_object_or_404(EventModel, id=kwargs['pk'])
            serializer = self.get_serializer(result)
            return Response(serializer.data, status=status.HTTP_200_OK) 

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        event_id = kwargs.get('pk')
        instance = EventModel.objects.get(id=event_id)

        excluded_fields  = None
        if not('image' in request.data):
            excluded_fields = ['image']

        serializer = EventSerializer(instance, excluded_fields=excluded_fields, partial=True)

        serializer_data = serializer.data
        serializer_data.update(request.data)

        serializer = EventSerializer(instance, data=serializer_data, excluded_fields=excluded_fields, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "event was deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_in(request, *args, **kwargs):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        user = UserModel.objects.filter(username=username)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            return Response({"message": "Authentication successful", "user_id": user.id}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Authentication failed"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({"message": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request, *args, **kwargs):
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        password = serializer.validated_data.get('password')
        
        user = serializer.save()
        user.set_password(password)
        user.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up_mentor(request, *args, **kwargs):
    serializer = MentorSerializer(data=request.data)
    
    if serializer.is_valid():
        password = serializer.validated_data.get('password')
        
        user = serializer.save()
        user.set_password(password)
        user.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
