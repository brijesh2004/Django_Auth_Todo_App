from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework import status
from .serializers import RegisterSerializer , LoginSerializer , TodoSerializer
# Create your views here.
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .models import TodoModel
from django.utils.timezone import now

class UserRegisterView(APIView):
    permission_classes = []
    def post(self , request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if not serializer.is_valid():
            return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        print("user" , user)
        token , _ = Token.objects.get_or_create(user=user)
        response = Response({
            "data":serializer.data , 
            "message":"User created successfully",
            'token':str(token)
        })
        response.set_cookie(key='token', value=str(token) , httponly=True ,samesite='None' , secure=True)

        return response
    

class UserLoginView(APIView):
    permission_classes = []

    def post(self , request):
        data = request.data 
        print("data" , data)
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=serializer.data['username'] , password=serializer.data['password'])
        if not user:
            return Response({"error":"Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        token , _ = Token.objects.get_or_create(user=user)
        response = Response({
            "data":serializer.data , 
            "message":"User logged in successfully",
            'token':str(token)
        })
        response.set_cookie(key='token', value=str(token) , httponly=True ,samesite='None' , secure=True)   
        return response


class TodoListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self , request):
        todos = request.user.todos.all()
        serializer = TodoSerializer(todos , many=True)
        return Response({"data":serializer.data , "message":"Todo list fetched successfully"}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TodoSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"data": serializer.data, "message": "Todo created successfully"}, status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        todo_id = request.GET.get('id')
        if not todo_id:
           return Response({"error": "Todo ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    
        try:
           todo = request.user.todos.get(id=todo_id)
           todo.delete()
           return Response({"message": "Todo deleted successfully"}, status=status.HTTP_200_OK)
        except TodoModel.DoesNotExist:
           return Response({"error": "Todo not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def patch(self, request):
        todo_id = request.GET.get('id')
        if not todo_id:
           return Response({"error": "Todo ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
           todo = request.user.todos.get(id=todo_id)
        except TodoModel.DoesNotExist:
           return Response({"error": "Todo not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['updated_at'] = now() 

        serializer = TodoSerializer(todo, data=data, partial=True)
        if not serializer.is_valid():
           return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()  
        return Response({"data": serializer.data, "message": "Todo updated successfully"}, status=status.HTTP_200_OK)


