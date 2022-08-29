<template>
    <div class="container mgv-medium mx-5">
        <post-category/>
        <post-topping/>
        <div v-if="$store.state.editBtn === false">
        <h1 class="title">Tambahkan Produk Anda:</h1>
        <div class="box column is-12 is-1-mobile is-0-tablet mt-2 ml-1">
            <form @submit.prevent='productForm' enctype="multipart/form-data">
                <div class="columns">
                    <div class="column">
                        <div class="field">
                            <div class="control">
                                <label for="">Nama Produk</label>
                                <input class="input is-large" v-model="pName" type="text"  autofocus="">
                                <input class="input is-large" v-model="slug" type="hidden" autofocus="" disabled>
                            </div>
                        </div>
                        <div class="field">
                            <label for="">Kategori</label>
                            <div class="select is-danger is-medium is-fullwidth">
                                <select @change="cats">
                                    <option selected>-- Pilih Kategori --</option>
                                    <option v-for="item in categoryList.lists" 
                                        :key="item.id" 
                                        :value="item.id"
                                    >{{item.name}}</option>
                                </select>
                            </div>
                        </div>
                        <div class="field">
                            <label for="">Harga Rp. {{hargas}}</label>
                            <p class="control has-icons-left mt-2">
                                <input class="input is-large" v-model="harga" type="number" autofocus="">
                                <span class="icon is-small is-left">
                                    Rp
                                </span>
                            </p>
                        </div>
                        <div class="field">
                            <label for="">Gambar</label>
                            <div class="control">
                                <img :src="prview" v-if="prview" width="150" height="150">
                                <div class="file is-primary has-name mt-3">
                                    <label class="file-label">
                                        <input
                                            type="file" 
                                            accept="image/jpg,image/jpeg,image/x-png"
                                            class="file-input"
                                            @change="setImage"
                                            multiple
                                            required
                                            oninvalid="this.setCustomValidity('Gambar Wajib Diisi')"
                                            oninput="this.setCustomValidity('')"
                                        />
                                        <span class="file-cta">
                                        <span class="file-icon">
                                            <i class="fa fa-upload"></i>
                                        </span>
                                        <span class="file-label">
                                            Masukkan Gambar...
                                        </span>
                                        </span>
                                        <span v-if="this.fileName" class="file-name">
                                            {{this.fileName}}
                                        </span>
                                    </label>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="column">
                        <div class="field">
                            <div class="control">
                                <label for="">Deskripsi</label>
                                <textarea class="textarea" v-model="descs" cols="65" rows="4"></textarea>
                            </div>
                        </div>
                        <div class="field">
                            <div class="control">
                                <label for="">Stok Produk</label>
                                <input class="input is-large" v-model="stoks" type="number" autofocus="">
                            </div>
                        </div>
                        <div class="field">
                            <label for="">Ukuran</label>
                            <div class="select is-medium is-fullwidth">
                                <select @change="ukurans">
                                    <option value="-">-</option>
                                    <option value="S">S</option>
                                    <option value="L">L</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
                <template v-if="v$.harga.$error">
                    <span v-if="this.harga == ''" style="color:#E76F51;">*Harga wajib diisi</span>
                    <span v-if="v$.harga.minLength" style="color:#E76F51;"> *Max 4 Karakter</span>
                </template>
                <template v-if="v$.descs.$error">
                    <span style="color:#E76F51;">*Deskripsi wajib diisi</span><br>
                </template>
                <template v-if="v$.pName.$error">
                    <span style="color:#E76F51;">*Nama produk wajib diisi</span><br>
                </template>
                <template v-if="v$.id_category.$error">
                    <span style="color:#E76F51;">*Kategori wajib dipilih</span><br>
                </template>
                <template v-if="v$.stoks.$error">
                    <span v-if="this.stoks == ''" style="color:#E76F51;">*Stok wajib diisi</span>
                    <span v-if="v$.stoks.maxValue" style="color:#E76F51;"> *Max 100</span>
                </template>
                <button class="button is-block is-danger is-large is-fullwidth">Tambah Data</button>
            </form>
        </div>
        </div>
        <div v-if="$store.state.editBtn === true">
        <h1 class="title">Update Produk Anda: <span class="is-pulled-right"> <button class="button is-primary" @click="back()">Kembali</button> </span></h1>
        <div class="box column is-12 is-1-mobile is-0-tablet mt-2 ml-1" id="productEdit">
            <form @submit.prevent='updateProductForm' enctype="multipart/form-data">
                <div class="columns">
                    <div class="column">
                        <div class="field">
                            <div class="control">
                                <label for="">Nama Produk {{this.getProduct.name}}</label>
                                <input class="input is-large" 
                                    v-bind:value="getProduct.name"
                                    v-on:input="getProduct.name = $event.target.value" 
                                    type="text"  
                                    autofocus="">
                                <input class="input is-large" v-model="slugEdit" type="hidden" autofocus="" disabled>
                            </div>
                        </div>
                        <div class="field">
                            <label for="">Kategori</label>
                            <div class="select is-danger is-medium is-fullwidth">
                                <select @change="cats_update">
                                    <option selected>{{getProduct.category_name}}</option>
                                    <option v-for="item in categoryList.lists" 
                                        :key="item.id" 
                                        :value="item.id"
                                    >{{item.name}}</option>
                                </select>
                            </div>
                        </div>
                        <div class="field">
                            <label for="">Harga Rp. {{hargasUpdate}}</label>
                            <p class="control has-icons-left mt-2">
                                <input class="input is-large"     
                                    v-bind:value="getProduct.price"
                                    v-on:input="getProduct.price = $event.target.value" 
                                    type="number" autofocus="">
                                <span class="icon is-small is-left">
                                    Rp
                                </span>
                            </p>
                        </div>
                        <div class="field">
                            <label for="">Gambar</label>
                            <div class="control">
                                <img :src="getProduct.newprview" v-bind:style="{ display: computedNone }" alt="thumbnail" width="150" height="150">
                                <img :src="newImgPrview" v-bind:style="{ display: computedNew }" alt="thumbnail" width="150" height="150">
                                <div class="file is-primary has-name mt-3">
                                    <label class="file-label">
                                        <input
                                            type="file" 
                                            accept="image/*"
                                            class="file-input"
                                            @change="setEditImage"
                                            multiple
                                        />
                                        <span class="file-cta">
                                        <span class="file-icon">
                                            <i class="fa fa-upload"></i>
                                        </span>
                                        <span @click="changePic" class="file-label">
                                            Masukkan Gambar...
                                        </span>
                                        </span>
                                        <span v-if="this.fileNameEdit" class="file-name">
                                            {{this.fileNameEdit}}
                                        </span>
                                    </label>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="column">
                        <div class="field">
                            <div class="control">
                                <label for="">Deskripsi</label>
                                <textarea
                                    class="textarea"      
                                    v-bind:value="getProduct.description"
                                    v-on:input="getProduct.description = $event.target.value" 
                                    cols="65" rows="4"></textarea>
                            </div>
                        </div>
                        <div class="field">
                            <div class="control">
                                <label for="">Stok Produk</label>
                                <input class="input is-large" 
                                    v-bind:value="getProduct.stoks"
                                    v-on:input="getProduct.stoks = $event.target.value"  
                                    type="number" autofocus="">
                            </div>
                        </div>
                        <div class="field">
                            <label for="">Ukuran</label>
                            <div class="select is-medium is-fullwidth">
                                <select @change="ukurans_update">
                                    <option selected>{{getProduct.sizez}}</option>
                                    <option value="-">-</option>
                                    <option value="S">S</option>
                                    <option value="L">L</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
                <button class="button is-block is-danger is-large is-fullwidth">Update Data</button>
            </form>
        </div>
        </div>

        <list-product/>
    </div>
</template>

<script>
import axios from 'axios'
import {toast} from 'bulma-toast'
import PostCategory from '@/components/PostCategory'
import ListProduct from '@/components/ListProduct'
import { makeSlug, formatPrice } from '@/utils/slugmaker'
import useValidate from "@vuelidate/core";
import { required, maxValue, minLength } from "@vuelidate/validators";

export default {
    validations() {
        return {
            harga: { required, minLength:minLength(4) },
            descs: { required },
            pName: { required },
            id_category: { required },
            stoks: { required, maxValue:maxValue(100) }
        };
    },
    data(){
        return{
            v$: useValidate(),
            categoryList: {
                lists: []
            },
            pName:'', // nama product
            descs:'',
            harga: '',
            getProduct: {
                id: null,
                name: null,
                sizez: null,
                price: null,
                description: null,
                category_name: null,
                stoks: null,
                newprview: null,
                thumbnailGambarEdit: '',
                gambarEdit: '',
                category_old_id: '',
            },
            stoks: '',
            gambar: '',
            showImg: 'none',
            showNewImg: 'none',
            thumbnailGambar: '',
            fileNameEdit: '',
            fileName: '',
            prview: '',
            sizes: '',
            newImgPrview: '',
            inputGambar: false,
            id_category: '',
            id_category_update: '',
            sizes_update: ''
        }
    },
    components: {
        PostCategory,
        ListProduct
    },
    computed: {
        slug: function() {
            var slug = makeSlug(this.pName);
            return slug;
        },
        slugEdit: function() {
            var slug = makeSlug(this.getProduct.name);
            return slug;
        },
        hargasUpdate: function() {
            var hargat = formatPrice(this.getProduct.price);
            return hargat;
        },
        hargas: function() {
            var hargat = formatPrice(this.harga);
            return hargat;
        },
        computedNone: function () {
            return this.showImg;
        },
        computedNew: function () {
            return this.showNewImg;
        }
    },
    watch: {
        '$store.state.productId': function() {
            this.getProductById(this.$store.state.productId)
            this.scrollToTop()
        }
    },
    methods:{
        scrollToTop() {
            window.scrollTo({
                top: 955,
                behavior: 'smooth'
            });
        },
        back() {
            this.$router.go()
        },
        changePic() {
            this.inputGambar = true
        },
        async getAllCategoryLists(){
            const token = localStorage.getItem('token')
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+token
            };
            await axios.get('/api/v1/category/lists/', {headers})
                .then(response => {
                        this.categoryList.lists = response.data
                    })
                .catch(error => {console.log(error)})
        },
        async getProductById(product_id){
            const token = localStorage.getItem('token')
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+token
            };
            this.$store.commit('setIsLoading', true)
            await axios.get(`/api/v1/get-product-by-id/${product_id}`, {headers})
                .then(response => {
                    this.getProduct.name = response.data[0].name
                    this.getProduct.description = response.data[0].description
                    this.getProduct.category_name = response.data[0].category_name
                    this.getProduct.category_old_id = response.data[0].category_id
                    this.getProduct.id = response.data[0].id
                    this.getProduct.price = response.data[0].price
                    this.getProduct.sizez = response.data[0].size
                    this.getProduct.newprview = response.data[0].get_thumbnail
                    this.getProduct.stoks = formatPrice(response.data[0].stok)
                    this.showImg = 'block'
                    this.showNewImg = 'none'
                })
                .catch(error => {console.log(error)})
            this.$store.commit('setIsLoading', false)
        },
        async updateProductForm(){
            if ((this.getProduct.gambarEdit == '') || (this.getProduct.thumbnailGambarEdit == '')) {
                const productData = {
                    name : this.getProduct.name,
                    slug : this.getProduct.slugEdit,
                    description : this.getProduct.description,
                    price : this.getProduct.price,
                    size : this.sizes_update?this.sizes_update:this.getProduct.sizez,
                    category : this.id_category_update?this.id_category_update:this.getProduct.category_old_id,
                    stok : this.getProduct.stoks,
                };
                const token = localStorage.getItem('token')
                const headers = { 
                    'accept': 'application/json',
                    'Authorization':'Token '+token,
                    'content-type': 'application/json;multipart/form-data;boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW'
                };
                await axios
                    .put(`/api/v1/update-product-by-id-non-image/${this.getProduct.id}`, productData, {headers})
                    .then(response=>{
                        if (!response) {
                            toast({
                                message: 'Maaf terjadi kesalahan, silahkan cek/upload kembali data anda.',
                                type: 'is-danger',
                                dismissible: true,
                                pauseOnHover: true,
                                duration: 5000,
                                position: 'top-right',
                            })
                            this.$router.go()
                        } else {
                            toast({
                                message: 'Produk Berhasil Diupdate',
                                type: 'is-success',
                                dismissible: true,
                                pauseOnHover: true,
                                duration: 5000,
                                position: 'top-right',
                            })
                            this.$router.go()
                        }
                    })
                    .catch(error => {
                        if (error.response){
                            for (const property in error.response.data){
                                this.errors.push(`${property}: ${error.response.data[property]}`)
                            }
                            console.log(JSON.stringify(error.response.data))
                        }else if(error.message){
                            this.errors.push('Something went wrong, please try again')
                            console.log(JSON.stringify(error))
                        }
                    });
            } else {
                const productData = {
                    name : this.getProduct.name,
                    slug : this.getProduct.slugEdit,
                    description : this.getProduct.description,
                    price : this.getProduct.price,
                    size : this.sizes_update?this.sizes_update:this.getProduct.sizez,
                    category : this.id_category_update?this.id_category_update:this.getProduct.category_old_id,
                    stok : this.getProduct.stoks,
                    image: this.getProduct.gambarEdit,
                    thumbnail: this.getProduct.thumbnailGambarEdit
                };
                const token = localStorage.getItem('token')
                const headers = { 
                    'accept': 'application/json',
                    'Authorization':'Token '+token,
                    'content-type': 'application/json;multipart/form-data;boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW'
                };
                await axios
                    .put(`/api/v1/update-product-by-id/${this.getProduct.id}`, productData, {headers})
                    .then(response=>{
                        if (!response) {
                            toast({
                                message: 'Maaf terjadi kesalahan, silahkan cek/upload kembali data anda.',
                                type: 'is-danger',
                                dismissible: true,
                                pauseOnHover: true,
                                duration: 5000,
                                position: 'top-right',
                            })
                            
                        } else {
                            toast({
                                message: 'Produk Berhasil Diupdate',
                                type: 'is-success',
                                dismissible: true,
                                pauseOnHover: true,
                                duration: 5000,
                                position: 'top-right',
                            })
                            // this.$router.go()
                        }
                    })
                    .catch(error => {
                        if (error.response){
                            for (const property in error.response.data){
                                this.errors.push(`${property}: ${error.response.data[property]}`)
                            }
                            console.log(JSON.stringify(error.response.data))
                        }else if(error.message){
                            this.errors.push('Something went wrong, please try again')
                            console.log(JSON.stringify(error))
                        }
                    });
            }
        },
        async productForm(){
            this.v$.$validate() 
            if (!this.v$.$error) { 
                const productData = {
                    name : this.pName,
                    slug : this.slug,
                    description : this.descs,
                    price : this.harga,
                    size : this.sizes,
                    category : this.id_category,
                    stok : this.stoks,
                    image: this.gambar,
                    thumbnail: this.thumbnailGambar
                };
                const token = localStorage.getItem('token')
                const headers = { 
                    'accept': 'application/json',
                    'Authorization':'Token '+token,
                    'content-type': 'application/json;multipart/form-data;boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW'
                };
                await axios
                    .post('/api/v1/products/create', productData, {headers})
                    .then(response=>{
                        if (!response) {
                            toast({
                                message: 'Maaf terjadi kesalahan, silahkan cek/upload kembali data anda.',
                                type: 'is-danger',
                                dismissible: true,
                                pauseOnHover: true,
                                duration: 5000,
                                position: 'top-right',
                            })
                            this.$router.go()
                        } else {
                            toast({
                                message: 'Produk Berhasil Dibuat',
                                type: 'is-success',
                                dismissible: true,
                                pauseOnHover: true,
                                duration: 5000,
                                position: 'top-right',
                            })
                            this.$router.go()
                        }
                    })
                    .catch(error => {
                        if (error.response){
                            for (const property in error.response.data){
                                this.errors.push(`${property}: ${error.response.data[property]}`)
                            }
                            console.log(JSON.stringify(error.response.data))
                        }else if(error.message){
                            this.errors.push('Something went wrong, please try again')
                            console.log(JSON.stringify(error))
                        }
                    });
            }else{
                toast({
                    message: 'Gagal Divalidasi',
                    type: 'is-danger',
                    dismissible: true,
                    pauseOnHover: true,
                    duration: 2000,
                    position: 'center',
                })
            }
        },
        setImage(e) {
            const file = e.target.files[0]
            const reader = new FileReader()
                let rawImg;
                reader.onloadend = () => {
                rawImg = reader.result;
                    this.thumbnailGambar = rawImg
                    this.gambar = rawImg
                }
            reader.readAsDataURL(file);
            this.fileName = file.name
            this.prview = URL.createObjectURL(file)
        },
        setEditImage(e) {
            const file = e.target.files[0]
            const reader = new FileReader()
                let rawImg;
                reader.onloadend = () => {
                rawImg = reader.result;
                    this.getProduct.thumbnailGambarEdit = rawImg
                    this.getProduct.gambarEdit = rawImg
                }
            reader.readAsDataURL(file);
            this.showImg = 'none'
            this.showNewImg = 'block'
            this.fileNameEdit = file.name
            this.newImgPrview = URL.createObjectURL(file)
        },
        cats(e) {
            this.id_category = e.target.value
        },
        ukurans(e) {
            this.sizes = e.target.value
        },
        ukurans_update(e) {
            this.sizes_update = e.target.value
        },
        cats_update(e) {
            this.id_category_update = e.target.value
        },
    },
    created(){
        this.getAllCategoryLists()
    }
}
</script>

<style lang="scss">
@import '~bulma/css/bulma.css';
</style>