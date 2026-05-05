from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Student
from .serializer import StudentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

# Create your views here.

@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    if not username or not password or not email:
        return Response({"success": False, "error": "All fields are required"}, status= status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({"success": False, "error": "username already exists"}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username,
                                    password=password,
                                    email=email)
    user.save()
    return Response({"success": True, "message": "user created successfully"}, status=status.HTTP_201_CREATED)
                        







@api_view(['POST']) 
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'success': True,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status = status.HTTP_200_OK)
        
    return Response({"success": False, "error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def student_api(request):
    if request.method == 'GET':
        students = Student.objects.all()

        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 5))

        start = (page - 1) * limit
        end = start + limit

        students = students[start:end]

        serializer = StudentSerializer(students, many=True)
        return Response({"success": True, "data": serializer.data}, status = status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT','PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def student(request, id):
    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        return Response({"success": False, "error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
    

    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = StudentSerializer(student, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        student.delete()
        return Response({"success": True, "message": "Student deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PATCH':
        serializer = StudentSerializer(student, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)