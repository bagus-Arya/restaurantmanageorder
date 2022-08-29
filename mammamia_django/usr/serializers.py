from rest_framework import serializers
from .models import Pesanan, Profile, Pesanan_History, Detail_Pesanan_History,StoreStatus
from product.models import Product

# all product
class ProductMostOrderedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'get_absolute_url', 'description',
                  'price','size','get_thumbnail','stok')

# update product stok
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('stok',)

# get Store Status Value
class StoreStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreStatus
        fields = ('id', 'isOpen')

# get data user
class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = ('user_id', 'username', 'nama_depan', 'nama_belakang', 'jenis_kelamin', 'hp', 'alamat')

# create data user profile
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

# CRUD PESANAN
# create pesanan 
class PesananPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pesanan
        fields = '__all__'

# get pesanan 
class PesananSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='product.name', read_only=True)
    id_pesanan = serializers.IntegerField(source='product.id', read_only=True)
    stok = serializers.IntegerField(source='product.stok', read_only=True)
    price = serializers.IntegerField(source='product.price', read_only=True)
    get_absolute_url = serializers.CharField(source='product.get_absolute_url', read_only=True)

    class Meta:
        model = Pesanan
        fields = ('id', 'id_pesanan', 'user_id','price_toping','quantity','note_customer','toping_id','name', 'price', 'get_absolute_url', 'stok')

# CRUD HISTORY PESANAN
# create history pesanan
class PesananHistoryPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pesanan_History
        fields = '__all__'

# update history pesanan is_history
class PesananHistoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pesanan_History
        fields = ('is_history',)

# update history pesanan is_checkOut
class PesananHistoryUpdateCheckOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pesanan_History
        fields = ('is_checkout','detail_id_pesanan')

# get history pesanan
class PesananHistorySerializer(serializers.ModelSerializer):
    name_history = serializers.CharField(source='product_history.name', read_only=True)
    size = serializers.CharField(source='product_history.size', read_only=True)
    get_thumbnail = serializers.CharField(source='product_history.get_thumbnail', read_only=True)
    id_pesanan_history = serializers.IntegerField(source='product_history.id', read_only=True)
    stok = serializers.IntegerField(source='product_history.stok', read_only=True)
    price_history = serializers.IntegerField(source='product_history.price', read_only=True)
    metode_pesanan = serializers.CharField(source='detail_id_pesanan.metode_pesanan', read_only=True)
    get_absolute_url_history = serializers.CharField(source='product_history.get_absolute_url', read_only=True)

    class Meta:
        model = Pesanan_History
        fields = ('id', 'id_pesanan_history','size','metode_pesanan','get_thumbnail','user_id_history','price_toping','note_customer','toping_id','stok','quantity_history', 'name_history', 'price_history', 'get_absolute_url_history')

# get most ordered
class MostOrderedSerializer(serializers.ModelSerializer):
    name_history = serializers.CharField(source='product_history.name', read_only=True)
    id_product_history = serializers.IntegerField(source='product_history.id', read_only=True)
    price_history = serializers.IntegerField(source='product_history.price', read_only=True)
    size = serializers.CharField(source='product_history.size', read_only=True)
    get_absolute_url_history = serializers.CharField(source='product_history.get_absolute_url', read_only=True)
    get_thumbnail_history = serializers.CharField(source='product_history.get_thumbnail', read_only=True)
    description_history = serializers.CharField(source='product_history.description', read_only=True)

    class Meta:
        model = Pesanan_History
        fields = ('id', 'id_product_history','description_history','size','name_history', 'price_history','quantity_history','get_absolute_url_history', 'get_thumbnail_history')

# get checkout pesanan
class PesananCheckoutSerializer(serializers.ModelSerializer):
    name_history = serializers.CharField(source='product_history.name', read_only=True)
    id_pesanan_history = serializers.IntegerField(source='product_history.id', read_only=True)
    price_history = serializers.CharField(source='product_history.price', read_only=True)
    get_absolute_url_history = serializers.CharField(source='product_history.get_absolute_url', read_only=True)

    class Meta:
        model = Pesanan_History
        fields = ('id', 'id_pesanan_history', 'user_id_history', 'quantity_history', 'name_history', 'price_history', 'detail_id_pesanan_id','get_absolute_url_history')

# get all pesanan (user profile)
class PesananUserSerializer(serializers.ModelSerializer):
    name_history = serializers.CharField(source='product_history.name', read_only=True)
    status_bayar = serializers.CharField(source='detail_id_pesanan.status_bayar', read_only=True)
    is_delivered = serializers.CharField(source='detail_id_pesanan.is_delivered', read_only=True)
    is_ready = serializers.CharField(source='detail_id_pesanan.is_ready', read_only=True)
    metode_pesanan = serializers.CharField(source='detail_id_pesanan.metode_pesanan', read_only=True)
    id_pesanan_history = serializers.IntegerField(source='product_history.id', read_only=True)
    price_history = serializers.IntegerField(source='product_history.price', read_only=True)
    get_absolute_url_history = serializers.CharField(source='product_history.get_absolute_url', read_only=True)

    class Meta:
        model = Pesanan_History
        fields = ('id', 'id_pesanan_history','date_added_history','is_delivered','toping_id','price_toping','note_customer','metode_pesanan','is_ready','status_bayar','user_id_history', 'quantity_history', 'name_history', 'price_history', 'detail_id_pesanan_id','get_absolute_url_history')

# get detail history pesanan (admin)
class PesananHistoryAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail_Pesanan_History
        fields = ('id_detail_pesanan','lokasi_pengiriman','is_ready','is_delivered','kode_unik','metode_bayar', 'metode_pesanan', 'is_processed', 'is_checkout', 'status_bayar', 'biaya_ongkir', 'date_detail_pesanan')

# update status bayar (admin)
class DetailStatusBayarAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail_Pesanan_History
        fields = ('is_processed', 'status_bayar')

# update status pesanan (admin) 
class DetailStatusPesananAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail_Pesanan_History
        fields = ('is_ready',)

# update status kirim (admin) 
class DetailStatusKirimAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail_Pesanan_History
        fields = ('is_delivered',)

# update status stok (admin) 
class UpdateStatusStokSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pesanan_History
        fields = ('is_stokUpdated',)

# get history pesanan (admin)
class PesananHistoryAdminByIdSerializer(serializers.ModelSerializer):
    hp = serializers.CharField(source='user_id_history.hp', read_only=True)
    name_depan_user = serializers.CharField(source='user_id_history.nama_depan', read_only=True)
    username = serializers.CharField(source='user_id_history.user.username', read_only=True)
    name_history = serializers.CharField(source='product_history.name', read_only=True)
    stok = serializers.IntegerField(source='product_history.stok', read_only=True)
    id_product_history = serializers.IntegerField(source='product_history.id', read_only=True)
    price_history = serializers.IntegerField(source='product_history.price', read_only=True)
    
    class Meta:
        model = Pesanan_History
        fields = ('id','id_product_history','hp','toping_id','price_toping','note_customer','is_stokUpdated','stok','username','name_depan_user','user_id_history', 'quantity_history', 'name_history', 'price_history')

# check unique ID
class PesananHistoryUserCheckIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pesanan_History
        fields = ('id',)

# CRUD DETAIL HISTORY PESANAN
# create detail history pesanan
class DetailPesananHistoryPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail_Pesanan_History
        fields = '__all__'