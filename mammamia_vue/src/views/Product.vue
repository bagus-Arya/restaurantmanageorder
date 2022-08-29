<template>
    <div class="page-product">
        <div class="columns is-multiline">
            <div class="column is-4 is-offset-2">
                <figure class="image mb-6">
                    <img :src="product.get_thumbnail" alt="thumbnail" width="75" height="75">
                </figure>
                <h1 class="title">{{ product.name}}</h1>
                <p>{{product.description}}</p>
            </div>
            <div class="box column is-4">
                <h2 class="subtitle"><b>Informasi</b></h2>
                <p>Size: <strong>{{product.size}}</strong></p>
                <p>Harga: <strong>Rp.{{formatPrices(product.price)}}</strong></p>

                <p v-if="checkedToping != ''">Toping: Rp.{{ formatPrices(sum) }} </p>

                <button v-if="this.displays == 'block'" class="button is-danger is-inverted"
                    @click="closeToping">
                    <span class="icon">
                        <i class="fa fa-pencil"></i>
                    </span>
                    <span>Tambah Topping</span>
                </button>

                <button v-else class="button is-danger is-inverted"
                    @click="showToping">
                    <span class="icon">
                        <i class="fa fa-pencil"></i>
                    </span>
                    <span>Tambah Topping</span>
                </button>

                <div v-if="$store.state.isAuthenticated === true" v-bind:style="{ display: computedNone }">
                    <div class="field">
                        <div class="control">
                            <div class="table-container">
                                <table class="table is-narrow">
                                    <thead>
                                        <tr class="has-text-left">
                                            <th></th>
                                            <th>Nama Topping</th>
                                            <th>Ukuran</th>
                                            <th>Harga</th>
                                            <th>Keterangan</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr
                                            class="has-text-left"
                                            v-for="item in toppingLists.lists"
                                            v-bind:key="item.id"
                                        >   
                                            <td>
                                                <input type="checkbox" v-bind:id="item.id" v-bind:value="item.name" v-model="checkedToping" @change="addChecked(item.price,$event)" >
                                            </td>
                                            <td>{{item.name}}</td>
                                            <td>{{item.size}}</td>
                                            <td>Rp.{{formatPrices(item.price)}}</td>
                                            <td>{{item.note}}</td>
                                        </tr> 
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                    <div class="field">
                        <div class="control">
                            <label for="">Catatan</label>
                            <textarea class="textarea" v-model="notes"></textarea>
                        </div>
                    </div>
                </div>

                <div v-if="$store.state.isAuthenticated === true" class="field has-addons mt-1">
                    <div class="field has-addons">
                        <div class="control">
                            <input type="number" class="input" min="1" v-model="quantity">
                        </div>
                        <div class="control">
                            <input v-bind:value="productID"
                                v-on:input="productID = $event.target.value"
                                type="hidden" class="input">
                            <input type="hidden" v-model="randomId"/>
                            <button v-if="(parseInt(product.stok) < 5) || (this.quantity > (parseInt(product.stok) - 1))" class="button is-block is-danger" disabled>Stok Habis</button>
                            <button v-else class="button is-block is-danger" @click.prevent='addToCartDB(); addToCartHistoryDB()'>Tambah ke Keranjang</button>
                        </div>
                    </div>  
                </div>
                <div v-if="$store.state.isAuthenticated === false" class="field has-addons mt-6">
                    <div class="control">
                        <a class="button is-dark" @click="toLogin">Login dulu yaa!</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

 <script>
 import axios from 'axios'
 import {toast} from 'bulma-toast'
 import { kd_bayar, formatPrice } from '@/utils/function'

 export default {
    name: 'Product',
    data(){
        return{
            product:'',
            productID:null,
            quantity:1,
            user_id:'',
            randomId:'',
            notes:'',
            sum:'',
            sums: [],
            checkedToping: [],
            displays:'none',
            idCartHistorys:[],
            toppingLists: {
                lists: []
            },
        }
    },
    beforeCreate(){
        this.$store.dispatch('getAllCartHistoryIdLists')
    },
    created(){
        this.getAllToppingLists()
    },
    mounted(){
        this.getProduct()
        document.title = 'Produk'+ ' | mammamia'
    },
    computed:{
        computedNone: function () {
            return this.displays;
        }
    },
    methods:{
        formatPrices(harga) {
            var hargas = parseInt(harga)
            var hargat = formatPrice(hargas);
            return hargat;
        },
        async getAllToppingLists(){
            const token = localStorage.getItem('token')
            const decodeValueTkn = atob(token)
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+decodeValueTkn
            };
            await axios.get(`/api/v1/topping/lists/`, {headers})
                .then(response => {
                        this.toppingLists.lists = response.data
                    })
                .catch(error => {console.log("asdfasasgasd")})
        },
        async getProduct(){
             // loading bar
            this.$store.commit('setIsLoading', true)
            const category_slug = this.$route.params.category_slug
            const product_slug = this.$route.params.product_slug
            const token = localStorage.getItem('token')
            const uIds = localStorage.getItem('uid')
            const decodeValueTkn = atob(token)
            const decodeValueId = atob(uIds)
            var randomId = kd_bayar(3)
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+decodeValueTkn
            };
             await axios
                .get(`/api/v1/products/${category_slug}/${product_slug}`,{headers})
                .then(response => {
                    this.product = response.data
                    this.productID = response.data.id
                    this.randomId = parseInt(randomId)
                    this.idCartHistorys = JSON.stringify(this.$store.getters.isIdCartHistory)
                    var stringify = JSON.parse(this.idCartHistorys);
                    for (var i = 0; i < stringify.length; i++) {
                        const dataid = stringify[i]['id']
                        if (this.randomId == dataid) {
                            this.$router.go()
                        } else {
                            this.randomId = parseInt(randomId)
                        }
                    }
                    document.title = this.product.name + ' | mammammia'
                })
                .catch(error => {console.log(error)})
             this.$store.commit('setIsLoading', false)

        },
        async addToCartDB(){
            if (isNaN(this.quantity) || this.quantity < 1){
                this.quantity = 1
            }
            const token = localStorage.getItem('token')
            const uids = localStorage.getItem('uid')
            const decodeValue = atob(token)
            const decodeValueuIds = atob(uids)
            const cartStore = JSON.stringify({
                id: this.randomId,
                product: this.productID,
                quantity: this.quantity,
                toping_id: this.checkedToping.toString()?this.checkedToping.toString():"-",
                price_toping: this.sum?this.sum:"0",
                note_customer: this.notes?this.notes:"-",
                user_id: decodeValueuIds
            });
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+decodeValue
            };
            console.log("Store = "+cartStore)
                await axios
                    .post('/api/v1/usr/cart-store/', cartStore, {headers})
                    .then(response=>{
                        if (!response) {
                            toast({
                                message: 'Data Sudah Ada',
                                type: 'is-danger',
                                dismissible: true,
                                pauseOnHover: true,
                                duration: 5000,
                                position: 'top-right',
                            })
                            
                        } else {
                            toast({
                                message: 'Berhasil Ditambah Ke Keranjang',
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
        },
        async addToCartHistoryDB(){
            if (isNaN(this.quantity) || this.quantity < 1){
                this.quantity = 1
            }
            const token = localStorage.getItem('token')
            const uids = localStorage.getItem('uid')
            const decodeValue = atob(token)
            const decodeValueuIds = atob(uids)
            const cartHitoryStore = JSON.stringify({
                id: this.randomId,
                product_history: this.productID,
                quantity_history: this.quantity,
                toping_id: this.checkedToping.toString()?this.checkedToping.toString():"-",
                price_toping: this.sum?this.sum:"0",
                note_customer: this.notes?this.notes:"-",
                user_id_history: decodeValueuIds
            });
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+decodeValue
            };
                await axios
                    .post(`/api/v1/usr/cart-history-store/`, cartHitoryStore, {headers})
                    .then(response=>{
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
        },
        toLogin() {
            this.$router.push({name:'Login'})
        },
        showToping(e) {
            this.displays='block'; 
        },
        closeToping(e) {
            this.displays='none'; 
        },
        addChecked: function(prices,e) {
            const a = e.target.checked
            const c = parseInt(prices)
            if ( a == true) {
                this.sums.push(c);
                const i = 0;
                const sumToping = this.sums.reduce(
                    (a, b) => a + b,
                    i
                );
                this.sum = sumToping
            }else{
                const sumTotal =  this.sums.filter(function(el) {
                    return el != c;
                });
                this.sums = sumTotal
                this.sum = sumTotal
            }
        }
    }
 }
 </script>
