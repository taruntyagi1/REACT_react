from django.shortcuts import render,HttpResponse
from accounts.models import User
from product.models import *
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login
import datetime 
import json
import jwt
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from product.serializer import *
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.utils.translation import gettext as _
# Create your views here.
def merge_carts(user,session_cart):
    user_cart = user.cart
    for item in session_cart:
        user_cart.add(item)
    user_cart.save()

@csrf_exempt
def add_to_cart(request,product_id,user_id):
        
       
        user = User.objects.get(id = user_id)
        product = Product.objects.get(id= product_id)
        # variant = Variant.objects.get(id=variant_id)
        price = request.POST.get('price')
        cart , created = Cart.objects.get_or_create(user = user)
        

        cart_item , created = cartitem.objects.get_or_create(cart = cart , product = product ,price = price)
       
        if created:
            cart_item.quantity = 1
            cart_item.save()
            return HttpResponse(cart_item)
        else:
            cart_item.quantity += 1
            cart_item.save()

        return HttpResponse(cart_item)
            
        
@csrf_exempt
@api_view(['POST'])
def login_view(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    user = authenticate(email = email,password = password)
    if user is not None:
        payload = {
            'id' : user.id,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key = 'jwt',value=token,httponly=True)
        response.data = {
            'token' : token
        }
        return response
    else:
        return JsonResponse({
            'message' : 'invalid'
        })


class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = Userserializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            user = authenticate(email=email, password=password)

            if user:
                
                    if user.is_active:
                        token, created = Token.objects.get_or_create(user=user)
                        return Response({'token': token.key,
                        'email' : user.email,
                        'id' : user.id,
                        'username' : user.username},status=status.HTTP_200_OK)
                    else:
                        content = {'detail': _('User account not active.')}
                        return Response(content,
                                        status=status.HTTP_401_UNAUTHORIZED)
                
            else:
                content = {'detail':
                           _('Unable to login with provided credentials.')}
                return Response(content, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
            

       


        
        
class ProductView(APIView):
    def get(self,reuqest):
        product = Product.objects.filter(is_active = True)
        serializer = productSerializer(product,many = True).data
        return Response(serializer,status=status.HTTP_200_OK)

