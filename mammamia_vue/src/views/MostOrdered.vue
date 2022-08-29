<template>
    <div class="container">
        <div class="columns is-multiline">
            <div v-if="this.itemsDetails.length != 0" class="column is-12">
                <h2 class="is-size-2 has-text-centered">
                    Most Ordered
                </h2>
            </div>
            <div class="column is-3" 
                v-for="item in itemsDetails"
                v-bind:key="item.id">
                <div class="box">
                    <figure class="image mb-4">
                        <img :src="item.get_thumbnail_history" alt="thumbnail">
                    </figure>
                    <router-link v-bind:to="item.get_absolute_url_history" class="navbar-item">
                        <h3 class="is-size-4">{{item.name_history}}</h3>
                    </router-link>
                        <p class="is-size-6">Terjual: {{item.quantity_history}} item(s)</p>
                        <p class="is-size-6">Size: {{item.size}}</p>
                        <p class="is-size-6 has-text-grey">Rp. {{formatPrices(item.price_history)}}</p>
                    <router-link v-if="($store.state.IS_OPEN === true) && ($store.state.isAuthenticated === true)" v-bind:to="item.get_absolute_url_history" class="button is-primary mt-4 is-fullwidth">Pesan</router-link>
                    <router-link v-else to="#" class="button is-primary mt-4 is-fullwidth">Pesan</router-link>
                </div>
            </div>
            <div class="column is-12">
                <h2 class="is-size-2 has-text-centered">
                    All Products
                </h2>
                <button class="button is-primary is-rounded mx-2" 
                    v-for="item in categoryList.lists"
                    v-bind:key="item.id">{{item.name}}
                </button>
            </div>
            <ProductBox
                v-for="product in products"
                v-bind:key="product.id"
                v-bind:product="product" />
        </div>
    </div>
</template>


<script>
import axios from 'axios'
import {toast} from 'bulma-toast'
import ProductBox from '../components/ProductBox.vue'
import { formatPrice } from '@/utils/function'

export default {
    name:'MostOrdered',
    data(){
        return{
            products: [],
            itemsDetails: {},
            displays:'none',
            categoryList: {
                lists: []
            },
        }
    },
    components:{
        ProductBox
    },
    mounted(){
        this.getProduct(),
        this.getProductMost(),
        this.getAllCategoryLists()
    },
    watch:{
        $route(to, from){
            if(to.name == 'MostOrdered'){
                this.getProduct()
            }
        }
    },
    methods:{
        formatPrices(harga) {
            var hargas = parseInt(harga)
            var hargat = formatPrice(hargas);
            return hargat;
        },
        async getAllCategoryLists(){
            const token = localStorage.getItem('token')
            const decodeValueTkn = atob(token);
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+decodeValueTkn
            };
            await axios.get('/api/v1/category/lists/', {headers})
                .then(response => {
                        this.categoryList.lists = response.data
                    })
                .catch(error => {console.log(error)})
        },
        async getProduct(){
            const token = localStorage.getItem('token')
            const decodeValueTkn = atob(token);
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+decodeValueTkn
            };
            this.$store.commit('setIsLoading', true)
            await axios
                .get('/api/v1/products/all', {headers})
                .then(response => {
                    this.products = response.data
                    document.title = 'Most Ordered | mammamia'
                })
                .catch(error => {
                    console.log('here'+error)
                    toast({
                        message: 'No Data Found',
                        type: 'is-danger',
                        dismissible: true,
                        pauseOnHover: true,
                        duration:2000,
                        position: 'bottom-right',
                    })
                })

            this.$store.commit('setIsLoading', false)
             
        },
        async getProductMost(){
            const token = localStorage.getItem('token')
            const decodeValueTkn = atob(token);
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+decodeValueTkn
            };
            this.$store.commit('setIsLoading', true)
            await axios
                .get('/api/v1/products/most-ordered', {headers})
                .then(response => {
                    const datasd = response.data
                    const size = 4
                    var helper = {};
                    var result = datasd.reduce(function(r, o) {
                    var key = o.name_history;
                        if(!helper[key]) {
                            helper[key] = Object.assign({}, o); 
                            r.push(helper[key]);
                        } else {
                            helper[key].quantity_history += o.quantity_history;
                        }
                        return r;
                    }, []);
                    this.itemsDetails = result.sort(function(a, b) {
                        return b.quantity_history - a.quantity_history;
                    }).slice(0, size)
                    document.title = 'Most Ordered | mammamia'
                })
                .catch(error => {
                    console.log('here'+error)
                    toast({
                        message: 'No Data Found',
                        type: 'is-danger',
                        dismissible: true,
                        pauseOnHover: true,
                        duration:2000,
                        position: 'bottom-right',
                    })
                })

            this.$store.commit('setIsLoading', false)
             
        }
    }


}
</script>
<style scoped>
    .image{
        margin-top: -1.25 rem;
        margin-left:-1.25 rem;
        margin-bottom:-1.25 rem;
    }

</style>