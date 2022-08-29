from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from .serializers import UserSerializer,PesananSerializer,UpdateStatusStokSerializer,MostOrderedSerializer,ProductMostOrderedSerializer,PesananUserSerializer,PesananHistoryUpdateCheckOutSerializer,PesananHistoryUpdateSerializer,ProductSerializer,DetailStatusKirimAdminSerializer,DetailStatusPesananAdminSerializer,UserDetailSerializer,PesananHistoryUserCheckIdSerializer,PesananCheckoutSerializer,DetailStatusBayarAdminSerializer,StoreStatusSerializer,PesananHistoryAdminSerializer,PesananHistorySerializer, PesananHistoryPostSerializer, PesananPostSerializer,DetailPesananHistoryPostSerializer,PesananHistoryAdminByIdSerializer
from django.http import Http404
from django.db.models import Q
import datetime
import zoneinfo
from django.utils import timezone
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from .models import Pesanan,Profile,Pesanan_History,StoreStatus,Detail_Pesanan_History
from product.models import Product
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User
from django.db.models import Count
# Create your views here.
# new code apriori algorithm not ready
import numpy as np
import pandas as pd
import json
from mlxtend.frequent_patterns import apriori, association_rules

class AprioriData(generics.CreateAPIView):
    def get(self, format=None):
        pesananH = Pesanan_History.objects.filter(is_checkout='1')
        serializer = PesananHistorySerializer(pesananH, many=True)
        return Response(serializer.data)

# new code

class GetUser(APIView):
    def get_object(self, user_ids):
        try:
            return Profile.objects.filter(user_id=user_ids)
        except Profile.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, user_ids, format=None):
        user = self.get_object(user_ids)
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)

class GetStoreStatus(generics.CreateAPIView):
    def get(self, format=None):
        storestatus = StoreStatus.objects.all()
        serializer = StoreStatusSerializer(storestatus, many=True)
        return Response(serializer.data)

class TokenAdminView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        uname = request.data['username']
        filterIsAdmin = User.objects.filter(username=uname).filter(is_superuser='1')
        if not filterIsAdmin:
            serializer.is_valid(raise_exception=True)
            data = {
                'status': 'Anda Dilarang Masuk'
            }
            return Response(data)
        else:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            custom_response = {
                'auth_token': token.key,
                'user_id': user.id
            }
            return Response(custom_response, status=status.HTTP_201_CREATED)

class TokenUserView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            custom_response = {
                'auth_token': token.key,
                'user_id': user.id
            }
            return Response(custom_response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# get most ordered product not ready
class AllProductsList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductMostOrderedSerializer(products, many=True)
        return Response(serializer.data)

# All Cart List byUser id
class CartLists(APIView):
    def get_object(self, user_ids):
        try:
            return Pesanan.objects.filter(user_id=user_ids)
        except Pesanan.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, user_ids, format=None):
        pesananU = self.get_object(user_ids)
        serializer = PesananSerializer(pesananU, many=True)
        return Response(serializer.data)

# Get All Cart List History ID 
class HistoryCartListsId(generics.CreateAPIView):
    def get(self, format=None):
        categorys = Pesanan_History.objects.all()
        serializer = PesananHistoryUserCheckIdSerializer(categorys, many=True)
        return Response(serializer.data)
        
# All history cart list done (user profile)
class HistoryCartListsDone(APIView):
    def get_object(self, user_ids):
        try:
            return Pesanan_History.objects.filter(user_id_history=user_ids).filter(is_checkout='1').filter(is_history='0')
        except Pesanan_History.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, user_ids, format=None):
        pesananH = self.get_object(user_ids)
        serializer = PesananUserSerializer(pesananH, many=True)
        return Response(serializer.data)

# All riwayat cart list done (user profile) 
class RiwayatCartListsDone(APIView):
    def get_object(self, user_ids):
        try:
            return Pesanan_History.objects.filter(user_id_history=user_ids).filter(is_checkout='1').filter(is_history='1')
        except Pesanan_History.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, user_ids, format=None):
        pesananH = self.get_object(user_ids)
        serializer = PesananUserSerializer(pesananH, many=True)
        return Response(serializer.data)

# All history cart list (user)
class HistoryCartLists(APIView):
    def get_object(self, user_ids):
        try:
            return Pesanan_History.objects.filter(user_id_history=user_ids).filter(is_checkout='0')
        except Pesanan_History.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, user_ids, format=None):
        pesananH = self.get_object(user_ids)
        serializer = PesananHistorySerializer(pesananH, many=True)
        return Response(serializer.data)

# Detail check out (user)
class DetailCheckOutCartLists(APIView):
    def get_object(self,fk):
        try:
            return Detail_Pesanan_History.objects.filter(id_detail_pesanan=fk)
        except Detail_Pesanan_History.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, fk,format=None):
        detail = self.get_object(fk)
        serializer = PesananHistoryAdminSerializer(detail, many=True)
        return Response(serializer.data)

# All riwayat cart list (Admin)
class RiwayatCartListsAdmin(generics.CreateAPIView):
    def post(self, request, format=None):
        today = request.data.get('datestrs', '')
        pesananH = Detail_Pesanan_History.objects.filter(is_ready='1').filter(date_detail_pesanan__istartswith=today)
        serializer = PesananHistoryAdminSerializer(pesananH, many=True)
        return Response(serializer.data)

    def get(self, format=None):
        pesananH = Detail_Pesanan_History.objects.filter(is_ready='1')
        serializer = PesananHistoryAdminSerializer(pesananH, many=True)
        return Response(serializer.data)

# All PickUp list (Admin)
class PickUpListsAdmin(generics.CreateAPIView):
    def get(self, format=None):
        today = timezone.localtime(timezone.now()).strftime('%Y-%m-%d')
        pesananH = Detail_Pesanan_History.objects.filter(metode_pesanan='Pick-up').filter(is_processed='1').filter(date_detail_pesanan__istartswith=today)
        serializer = PesananHistoryAdminSerializer(pesananH, many=True)
        return Response(serializer.data)

# All Delivery list (Admin)
class DeliveryListsAdmin(generics.CreateAPIView):
    def get(self, format=None):
        today = timezone.localtime(timezone.now()).strftime('%Y-%m-%d')
        pesananH = Detail_Pesanan_History.objects.filter(metode_pesanan='Delivery').filter(is_processed='1').filter(date_detail_pesanan__istartswith=today)
        serializer = PesananHistoryAdminSerializer(pesananH, many=True)
        return Response(serializer.data)

# All detail history cart list (Admin)
class HistoryCartListsAdmin(generics.CreateAPIView):
    def get(self, format=None):
        today = timezone.localtime(timezone.now()).strftime('%Y-%m-%d')
        print(zoneinfo.available_timezones())
        pesananH = Detail_Pesanan_History.objects.filter(is_processed='0').filter(date_detail_pesanan__istartswith=today)
        serializer = PesananHistoryAdminSerializer(pesananH, many=True)
        return Response(serializer.data)

# *statistik All history cart list (Admin) 
class StatistikAllUserOrderLists(generics.CreateAPIView):
    def post(self, request, format=None):
        find = request.data.get('datestrs', '')
        pesananH = Pesanan_History.objects.filter(is_checkout='1').filter(date_added_history__istartswith=find)
        serializer = PesananHistorySerializer(pesananH, many=True)
        return Response(serializer.data)

    def get(self, format=None):
        pesananH = Pesanan_History.objects.filter(is_checkout='1')
        serializer = PesananHistorySerializer(pesananH, many=True)
        return Response(serializer.data)

# All Most Ordered Product 
class MostOrderedProduct(generics.CreateAPIView):
    def post(self, request, format=None):
        pesananH = Pesanan_History.objects.filter(is_checkout='1')
        serializer = MostOrderedSerializer(pesananH, many=True)
        return Response(serializer.data)

    def get(self, format=None):
        pesananH = Pesanan_History.objects.filter(is_checkout='1')
        serializer = MostOrderedSerializer(pesananH, many=True)
        return Response(serializer.data)

# All history cart list by ID (Admin)
class HistoryCartListsAdminById(APIView):
    def get_object(self, fk):
        try:
            return Pesanan_History.objects.filter(detail_id_pesanan_id=fk).filter(is_checkout='1')
        except Pesanan_History.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, fk, format=None):
        pesananD = self.get_object(fk)
        serializer = PesananHistoryAdminByIdSerializer(pesananD, many=True)
        return Response(serializer.data)

class UserDetailCreate(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserDetailSerializer

# update data history cart
class CartHistory(APIView):
    def get_object(self, obj_id):
        try:
            return Pesanan_History.objects.get(id=obj_id)
        except Pesanan_History.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        b = request.data['id']
        d = b.split(',')
        instances = []
        for c in d :
            idp = int(c)
            is_checkout = request.data['is_checkout']
            detail_id_pesanan = request.data['detail_id_pesanan_id']
            obj = self.get_object(idp)
            obj.is_checkout = is_checkout
            obj.detail_id_pesanan_id = detail_id_pesanan
            obj.save()
            instances.append(obj)
        serializer = PesananHistoryUpdateCheckOutSerializer(instances, many=True)
        return Response(serializer.data)

# update data history cart is_history
class CartHistoryAdmin(APIView):
    def get_object(self, obj_id):
        try:
            return Pesanan_History.objects.get(id=obj_id)
        except Pesanan_History.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        b = request.data['id']
        d = b.split(',')
        instances = []
        for c in d :
            idp = int(c)
            is_history = request.data['is_history']
            obj = self.get_object(idp)
            obj.is_history = is_history
            obj.save()
            instances.append(obj)
        serializer = PesananHistoryUpdateSerializer(instances, many=True)
        return Response(serializer.data)

# update data stok produk not ready
class UpdateProductStok(APIView):
    def get_object(self, obj_id):
        try:
            return Product.objects.get(id=obj_id)
        except Product.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        b = request.data['idP']
        s = request.data['ustok']
        d = b.split(',')
        p = s.split(',')
        instances = []
        for c in d :
            idp = int(c)
            obj = self.get_object(idp)
            for u in p :
                obj.stok = int(u)
                obj.save()
                instances.append(obj)
                print(obj)
                print(obj.stok)
        serializer = ProductSerializer(instances, many=True)
        return Response(serializer.data)

# delete cart user bulk
class DeleteCartBulk(APIView):
    def get_object(self, obj_id):
        try:
            return Pesanan.objects.get(id=obj_id)
        except Pesanan.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        b = request.data['id']
        d = b.split(',')
        instances = []
        for c in d :
            idp = int(c)
            obj = self.get_object(idp)
            obj.delete()
            instances.append(obj)
        serializer = PesananSerializer(instances, many=True)
        return Response(serializer.data)

# delete product 
@api_view(['DELETE'])
def delete_product(request, pk, format=None):
    snippetHistory = Pesanan_History.objects.filter(detail_id_pesanan_id=pk).filter(is_checkout='0')
    snippetHistory.delete()
    snippet = Product.objects.get(id=pk)
    snippet.delete()
    snippetPesanan = Pesanan.objects.get(id=pk)
    snippetPesanan.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# delete cart
@api_view(['DELETE'])
def delete_cart(request, pk, format=None):
    snippet = Pesanan.objects.get(id=pk)
    snippetHistory = Pesanan_History.objects.get(id=pk)
    snippet.delete()
    snippetHistory.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# post UpdateUserDetail
@api_view(['PUT'])
def update_user_detail(request, userId):
    try:
        model = Profile.objects.get(user_id=userId)
    except:
        return Response('Cannot Update Data')
    if request.method == 'PUT':
        serializer = UserSerializer(model, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# post new data Pesanan History With Detail Lokasi (Checkout)
@api_view(['POST'])
def post_cartHistory(request):
    if request.method == 'POST':
        serializer = PesananHistoryPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# post new data detail Pesanan History
@api_view(['POST'])
def post_detailHistory(request):
    if request.method == 'POST':
        serializer = DetailPesananHistoryPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_cart_history(request, cart_ids):
    try:
        model = Pesanan_History.objects.get(id=cart_ids)
    except:
        return Response('Not Found')
    if request.method == 'PUT':
        serializer = PesananHistorySerializer(model, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# update stok
@api_view(['PUT'])
def update_stok(request, fk):
    try:
        model = Product.objects.get(id=fk)
    except:
        return Response('Not Found')
    if request.method == 'PUT':
        serializer = ProductSerializer(model, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# update status stok
@api_view(['PUT'])
def update_status_stok(request, fk):
    try:
        model = Pesanan_History.objects.get(id=fk)
    except:
        return Response('Not Found')
    if request.method == 'PUT':
        serializer = UpdateStatusStokSerializer(model, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# post new data Pesanan (Cart)
@api_view(['POST'])
def post_cart(request):
    if request.method == 'POST':
        serializer = PesananPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# update status bayar 
@api_view(['PUT'])
def update_status_bayar(request, fk):
    try:
        model = Detail_Pesanan_History.objects.get(id_detail_pesanan=fk)
    except:
        return Response('Not Found')
    if request.method == 'PUT':
        serializer = DetailStatusBayarAdminSerializer(model, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# update status pesanan 
@api_view(['PUT'])
def update_status_pesanan(request, fk):
    try:
        model = Detail_Pesanan_History.objects.get(id_detail_pesanan=fk)
    except:
        return Response('Not Found')
    if request.method == 'PUT':
        serializer = DetailStatusPesananAdminSerializer(model, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# update status kirim 
@api_view(['PUT'])
def update_status_kirim(request, fk):
    try:
        model = Detail_Pesanan_History.objects.get(id_detail_pesanan=fk)
    except:
        return Response('Not Found')
    if request.method == 'PUT':
        serializer = DetailStatusKirimAdminSerializer(model, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# update cart
@api_view(['PUT'])
def update_cart(request, cart_ids):
    try:
        model = Pesanan.objects.get(id=cart_ids)
    except:
        return Response('Not Found')
    if request.method == 'PUT':
        serializer = PesananSerializer(model, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# update status restauran
@api_view(['PUT'])
def update_status_restauran(request):
    try:
        model = StoreStatus.objects.filter(id='1').first()
    except:
        return Response('Not Found')
    if request.method == 'PUT':
        serializer = StoreStatusSerializer(model, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)