<template>
    <div class="container">
        <div class="box column is-12 is-1-mobile is-0-tablet">
            <AppNavAkun/>
            <hr>
            <div class="columns mb-1 mt-1 ml-1 mr-1">
                <table class="table is-fullwidth">
                    <thead>
                        <tr>
                            <th>Tanggal</th>
                            <th>Product</th>
                            <th>Price</th>
                            <th>Quantity</th>
                            <th>Toping</th>
                            <th>Catatan</th>
                            <th>Metode Pesanan</th>
                            <th>Status Bayar</th>
                            <th>Status Pesanan</th>
                            <th>Status Delivery</th>
                            <th>Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="item in items"
                            v-bind:key="item.id">
                            <td>{{dateTime(item.date_added_history)}}</td>
                            <td><router-link :to="item.get_absolute_url_history">{{item.name_history}}</router-link></td>
                            <td>Rp. {{formatPrices(item.price_history)}}</td>
                            <td>{{item.quantity_history}} item(s)</td>
                            <td>{{item.toping_id?item.toping_id:"-"}}</td>
                            <td>{{item.note_customer?item.note_customer:"-"}}</td>
                            <td>{{item.metode_pesanan}}</td> 
                            <td>
                                <strong style="color:#2A9D8F;" v-if="item.status_bayar == 'Lunas'" >{{item.status_bayar}}</strong>
                                <strong style="color:#E76F51;" v-else >{{item.status_bayar}}</strong>
                            </td>
                            <td>
                                <strong style="color:#E76F51;" v-if="item.is_ready == 0" >Sedang dikerjakan</strong> 
                                <strong style="color:#2A9D8F;" v-else >Selesai</strong>
                            </td>
                            <td>
                                <strong v-if="item.is_delivered == 0" >-</strong>
                                <strong style="color:#E76F51;" v-else-if="item.is_delivered == 1" >Dalam Pengiriman</strong>
                                <strong style="color:#E76F51;" v-else-if="item.is_delivered == 2" >Diterima</strong>
                            </td>
                            <td>Rp. {{formatPrices(item.price_history*item.quantity_history+parseInt(item.price_toping))}}</td> 
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { formatPrice } from '@/utils/function'
import AppNavAkun from '@/components/AppNavAkun'
import moment from 'moment'

export default {
    name: 'PesananSaya',
    components: {
        AppNavAkun
    },
    data(){
        return{
            items: [],
        }
    },
    mounted(){      
        document.title = 'Pesanan Saya'+ ' | mammamia'
    },
    computed:{
        cartTotalLength(){
            return this.itemsDetail.reduce((acc, curVal) =>{
                return acc += parseInt(curVal.quantity_history)
            },0)
        },
        computedNone: function () {
            return this.displays;
        }
    },
    created(){
        this.getAllCartLists()
    },
    methods:{
        dateTime(value) {
            return moment(value).format('LLL');
        },
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
            await axios.get(`/api/v1/usr/history-done-user-cart-lists/${decodeValueId}`, {headers})
                .then(response => {
                    const dataItem = response.data;
                    const metodePesanan =  dataItem.filter(function(metode) {
                        return metode.metode_pesanan == "Pick-up";
                    });
                    this.items = metodePesanan
                })
                .catch(error => {console.log(error)})
            this.$store.commit('setIsLoading', false)
        },
    },
}
</script>