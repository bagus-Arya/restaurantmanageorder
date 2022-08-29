<template>
    <div class="container">
        <div class="page-cart">
            <div class="column is-12 mb-3">
                <h1 class="title">Keranjang</h1>
            </div>
            <div class="columns is-1-mobile is-0-tablet">
                <div class="column is-8 box mx-3">
                    <table class="table is-fullwidth" v-if="cartTotalLength">
                        <thead>
                            <tr>
                                <th>Product</th>
                                <th>Price</th>
                                <th>Quantity</th>
                                <th>Toping</th>
                                <th>Catatan</th>
                                <th>Total</th>
                            </tr>
                        </thead>
                        <tbody>
                            <CartItem
                                v-for="item in items"
                                v-bind:key="item.id"
                                v-bind:initialItem="item"
                            />
                        </tbody>
                    </table>
                    <p v-else>Belum ada barang belanjaan nih!</p>
                </div>
                <div class="column box">
                    <h2 class="subtitle">
                        Ringkasan Belanja
                    </h2>
                    Total harga : <strong>Rp. {{ formatPrices(total) }} </strong>
                    <hr>
                    <button v-if="cartTotalLength" @click.prevent='toCheckOut' class="button is-primary">Beli ({{cartTotalLength}})</button>
                    <button v-else class="button is-primary" disabled>Beli ({{cartTotalLength}})</button>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import axios from 'axios'
import CartItem from '@/components/CartItem.vue'
import { calculate, kd_bayar, formatPrice } from '@/utils/function'

export default {
    components:{
        CartItem
    },
    data(){
        return{
            items: [],
        }
    },
    mounted(){
        document.title = 'Keranjang'+ ' | Mammamia Renon'
    },
    computed:{
        cartTotalLength(){
            return this.items.reduce((acc, curVal) =>{
                return acc += parseInt(curVal.quantity)
            },0)
        },
        total: function() {
            var total = this.items.reduce((acc, curVal) =>{
                return acc += curVal.price * curVal.quantity + parseInt(curVal.price_toping)
            },0);
            return total;
        }
    },
    created(){
        this.getAllCartLists()
    },
    methods:{ 
        formatPrices(harga) {
            var hargas = parseInt(harga)
            var hargat = formatPrice(hargas);
            return hargat;
        },
        async getAllCartLists(){
            const token = localStorage.getItem('token')
            const uIds = localStorage.getItem('uid')
            const decodeValueTkn = atob(token);
            const decodeValueId = atob(uIds);
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+decodeValueTkn
            };
            this.$store.commit('setIsLoading', true)
            await axios.get(`/api/v1/usr/cart-lists/${decodeValueId}/`, {headers})
                .then(response => {
                    this.items = response.data
                })
                .catch(error => {console.log(error)})
            this.$store.commit('setIsLoading', false)
        },
        toCheckOut(){
            this.$router.push({name:'CheckOut'})
        },
    },
}
</script>