from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from .serializers import TodoSerializer, TodoCompleteSerializer
from todo.models import Todo
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


# we use csrf token for a security purpose, it protects django request from malicious code user can use on site
# if in API we dont have to concern about it that's why we put csrf_exempt
@csrf_exempt
def signup(request):
    if request.method == "POST":
        # here the user will send post request
        try:
            data = JSONParser().parse(request)
            # basically this will parse the user request into a JASON format dictionary
            user = User.objects.create_user(data['username'], password=data['password'])
            user.save()
            # status 201 means something has been created
            token = Token.objects.create(user=user)
            # generating token
            return JsonResponse({'token': str(token)}, status=201)
        except IntegrityError:
            # status 400 means bad request
            return JsonResponse({'error': 'Username is already take!'}, status=400)


@csrf_exempt
def login(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is None:
            return JsonResponse({'token': 'Could not login, Please check username and password'}, status=201)
        else:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status=200)


class TodoCompletedList(generics.ListAPIView):
    serializer_class = TodoSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user, dateCompleted__isnull=False).order_by('-dateCompleted')


class TodoListCreate(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user, dateCompleted__isnull=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)

    def delete(self, request, *args, **kwargs):
        todo = Todo.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if todo.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('Todo does not exists or already deleted')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TodoComplete(generics.UpdateAPIView):
    serializer_class = TodoCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user, dateCompleted__isnull=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # In the api if we press put then the system will insert a time to that todo
    def perform_update(self, serializer):
        serializer.instance.dateCompleted = timezone.now()
        serializer.save()
