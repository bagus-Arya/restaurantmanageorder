from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Category, Topping
from .serializers import ProductSerializer,ToppingPostSerializer,ProductPostSerializer,ProductUpdateNonImageSerializer,ProductUpdateSerializer,ProductAdminSerializer,CategorySerializer,CategoryPostSerializer
from django.http import Http404
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework import status
import requests
import json
import http.client, urllib.parse
# Create your views here.


class LatestProductsList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()[:10]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class AllProductsList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductAdminSerializer(products, many=True)
        return Response(serializer.data)

class ProductDetail(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

# tampilkan data jarak lokasi
class LocationDistance(APIView):
    def get(self, request, format=None):
        url = 'https://api.openrouteservice.org/v2/directions/driving-car?api_key='
        key = "5b3ce3597851110001cf624888a5e141273b4b1480c92c80963df51e"
        headers = {
            'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        }
        call = requests.get(url+key+'&start=-8.674267,115.226320', headers=headers)
        res = call.getresponse()
        datas = res.read().decode('utf-8') #data http req
        data = json.loads(datas) #convert ke json
        print(request)
        return Response(data) #return by key 

# CRUD Source: https://medium.com/swlh/django-rest-framework-crud-with-drf-9a8756095c73
# category
# post new data
class CategoryCreate(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryPostSerializer

class ToppingCreate(generics.CreateAPIView):
    queryset = Topping.objects.all()
    serializer_class = ToppingPostSerializer


# list toping
class ToppingList(generics.CreateAPIView):
    def get(self, format=None):
        toppings = Topping.objects.all()
        serializer = ToppingPostSerializer(toppings, many=True)
        return Response(serializer.data)

# list category
class CategoryList(generics.CreateAPIView):
    def get(self, format=None):
        categorys = Category.objects.all()
        serializer = CategoryPostSerializer(categorys, many=True)
        return Response(serializer.data)
    
# tampilkan data berdasarkan kategori
class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
        
# product

class GetProductById(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.filter(id=pk)
        except Product.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)

# edit data
@api_view(['PUT'])
def update_product(request, pk):
    try:
        model = Product.objects.get(id=pk)
    except:
        return Response('Cannot Update Data')
    if request.method == 'PUT':
        serializer = ProductUpdateSerializer(model, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['PUT'])
def update_product_nonimage(request, pk):
    try:
        model = Product.objects.get(id=pk)
    except:
        return Response('Cannot Update Data')
    if request.method == 'PUT':
        serializer = ProductUpdateNonImageSerializer(model, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# delete data
class ProductDelete(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializers_class = ProductSerializer

@api_view(['POST'])
def post_product(request):
    if request.method == 'POST':
        serializer = ProductPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def search(request):
    # get the requested query
    query = request.data.get('query', '')

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({'products': []})

# delete category 
@api_view(['DELETE'])
def delete_category(request, pk, format=None):
    snippet = Category.objects.get(id=pk)
    snippet.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# delete topping 
@api_view(['DELETE'])
def delete_topping(request, pk, format=None):
    snippet = Topping.objects.get(id=pk)
    snippet.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
