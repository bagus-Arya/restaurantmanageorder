from django.db import models
from product.models import Product
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    nama_depan = models.TextField(max_length=20, blank=True)
    nama_belakang = models.TextField(max_length=20, blank=True)
    jenis_kelamin = models.TextField(max_length=15, blank=True)
    hp = models.CharField(max_length=13, blank=True)
    alamat = models.CharField(max_length=30, blank=True)

# Create store tutup toko
class StoreStatus(models.Model):
    isOpen = models.CharField(max_length=5, default="1")
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('isOpen',)

    def __str__(self):
        return self.isOpen

# Create store pesanan model 
class Pesanan(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, default="")
    product = models.ForeignKey(
    Product, related_name='pesanans', on_delete=models.CASCADE, null=True)
    quantity = models.CharField(max_length=10)
    user_id = models.CharField(max_length=10)
    toping_id = models.CharField(max_length=100, null=True)
    note_customer = models.CharField(max_length=255, null=True)
    price_toping = models.DecimalField(max_digits=10, decimal_places=2, default="0", blank=True, null=True)
    date_added = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-date_added',)

# Create store pesanan history model 
class Pesanan_History(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, default="")
    product_history = models.ForeignKey(
    Product, related_name='pesananHistory', on_delete=models.CASCADE, null=True)
    quantity_history = models.IntegerField(default="0")
    user_id_history = models.ForeignKey('Profile',on_delete=models.CASCADE, null=True)
    is_checkout = models.IntegerField(default="0")
    is_history = models.IntegerField(default="0")
    toping_id = models.CharField(max_length=100, null=True)
    note_customer = models.CharField(max_length=255, null=True)
    price_toping = models.DecimalField(max_digits=10, decimal_places=2, default="0", blank=True, null=True)
    is_stokUpdated = models.IntegerField(default="0")
    detail_id_pesanan = models.ForeignKey('Detail_Pesanan_History',on_delete=models.CASCADE, null=True)
    date_added_history = models.DateTimeField(default=timezone.now)
    class Meta:
        ordering = ('-date_added_history',)

# Create store detail pesanan history model 
class Detail_Pesanan_History(models.Model):
    id_detail_pesanan = models.IntegerField(primary_key=True, unique=True, default="")
    lokasi_pengiriman = models.CharField(max_length=225, null=True)
    kode_unik = models.IntegerField()
    metode_bayar = models.CharField(max_length=10, null=True)
    metode_pesanan = models.CharField(max_length=15,null=True)
    is_processed = models.IntegerField(default="0")
    is_delivered = models.IntegerField(default="0")
    is_ready = models.IntegerField(default="0")
    is_checkout = models.IntegerField(default="0")
    status_bayar = models.CharField(max_length=20, default="Belum bayar")
    biaya_ongkir = models.IntegerField(default="0")
    date_detail_pesanan = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-date_detail_pesanan',)