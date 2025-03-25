from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializer import UserSerializer,BlogPostSerializer
from rest_framework.response import Response
from rest_framework import status,permissions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from rest_framework import viewsets
from .models import Blog
from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from django .contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,logout as authlogout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
import jwt
import time
from django.conf import settings
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.

class RegisterApi(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        _data = request.data
        serializer = RegisterSerializer(data=_data)
        
        if not serializer.is_valid():
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save() 
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

def register_page(request):
    return render(request, 'registration.html')





class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Login the user (this sets the session if needed)
            login(request, user)

            # Generate JWT tokens
            access_token = str(AccessToken.for_user(user))
            refresh_token = str(RefreshToken.for_user(user))

            # Return tokens in the response
            return JsonResponse({
                'access_token': access_token,
                'refresh_token': refresh_token,
            })
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)




# Register API
class RegisterApi(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        _data = request.data
        serializer = RegisterSerializer(data=_data)
        
        if not serializer.is_valid():
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save() 
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

def register_page(request):
    return render(request, 'registration.html')


# Login API


def login_page(request):
    return render(request, 'login.html')



class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            access_token = str(AccessToken.for_user(user))
            refresh_token = str(RefreshToken.for_user(user))

            return JsonResponse({
                'access_token': access_token,
                'refresh_token': refresh_token,

               
            })
        else:
            return JsonResponse({'error':'Invalid credentials'}, status=400)




def blog_list(request):
    blogs = Blog.objects.all() 
    blogs_data = [{"id": e.id, "name": e.name, "email": e.email, "post": e.post} for e in blogs]
    return JsonResponse(blogs_data, safe=False)


def blogers_list(request):
    return render(request, 'employ_list.html')


def public(request):
    blog = Blog.objects.select_related("author").filter(status="published")
    paginator = Paginator(blog, 5)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'public.html', {"page_obj": page_obj})



def logout(request):
    authlogout(request)
    return redirect('login')



def index(request):
    return render(request, 'index.html')



def home(request):
    return render(request, 'header.html')





def login_page(request):
    
    return render(request, 'login.html')





class BlogListView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated] 
    def get(self, request, *args, **kwargs):
        
        token = request.headers.get('Authorization', None)
        print("Authorization Header:", token)  # Prints the token

        if token:
            print("Token is present in the header.")
        else:
            print("No token found in the header.")
        
       
        blogs = Blog.objects.filter(status="published").order_by('-created_at')
        
       
        paginator = Paginator(blogs, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        
        blog_data = [{
            "title": blog.title,
            "content": blog.content,
            "status": blog.status,
            "created_at": blog.created_at,
            "updated_at": blog.updated_at,
            "author": blog.author.username
        } for blog in page_obj]

      
        return Response({
            'blogs': blog_data,
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
        })

class BlogViewSet(viewsets.ModelViewSet):
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination  # Add pagination class

    def get_queryset(self):
        user = self.request.user
        status = self.request.query_params.get('status', None)
        queryset = Blog.objects.select_related('author').filter(author=user)
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            self.permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
        return super().get_permissions()
        

class IsOwnerOrReadOnly(permissions.BasePermission):
   
    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            return True
       
        return obj.author == request.user
        print (request.user)


def blog_list(request):
    
    blogs = Blog.objects.all() 
    blogs_data = [{"id": e.id, "name": e.name, "email": e.email, "post": e.post} for e in blogs]
    return JsonResponse(blogs_data, safe=False)

def blogers_list(request):
    
    return render(request, 'employ_list.html')

def public(request):
    blog = Blog.objects.select_related("author").filter(status = "published")
    paginator = Paginator(blog, 5)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'public.html',{"page_obj":page_obj})

def logout(request):
    authlogout(request)
    return redirect('login')




def index(request):
    
    return render(request, 'index.html')

def home(request):
    return render(request, 'header.html')








