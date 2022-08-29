<template>
    <div class="container">
        <div class="page-cart">
            <div v-if="this.metode_bayar === 'Transfer'" class="is-12 box mb-3 has-text-centered">
                <h3>Untuk memperlancar proses pemesanan makanan</h3>
                <h3>Segera lakukan pembayaran sekarang</h3>
                <hr>
                <div class="columns is-mobile">
                    <div class="column is-12">
                        <p> 
                            Debit<br>
                            Ayu Ratna | 651287917267581 | BCA
                        </p>
                    </div>
                </div>
            </div>
            <div class="column box">
                <div class="columns">
                    <div class="column">
                        <table class="tables is-large">
                            <tbody>
                                <tr>
                                    <td>Tanggal</td>
                                    <td>: {{dateTime(this.date_detail_pesanan)}}</td>
                                </tr>
                                <tr>
                                    <td>Alamat Tujuan</td>
                                    <td>: {{this.lokasi_pengiriman}}</td>
                                </tr>
                                <tr>
                                    <td>Metode Pemesanan</td>
                                    <td>: {{this.metode_pesanan}}</td>
                                </tr>
                                <tr>
                                    <td>Metode Bayar</td>
                                    <td>: {{this.metode_bayar}}</td>
                                </tr>
                                <tr>
                                    <td>Berita</td>
                                    <td>: {{this.kode_unik}} (*Wajib diisi saat Transfer)</td>
                                </tr>
                                <tr>
                                    <td>Ongkir</td>
                                    <td>: Rp. {{formatPrices(this.biaya_ongkir)}} </td>
                                </tr>
                                <tr>
                                    <td>Total Bayar</td>
                                    <td>: Rp. {{ formatPrices(total) }}</td>
                                </tr>
                                <tr>
                                    <td>Status Bayar</td>
                                    <td style="color:#E76F51;">: {{this.status_bayar}}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="column is-6">
                        <table class="table is-fullwidth">
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
                                <tr v-for="item in items"
                                    v-bind:key="item.id">
                                    <td><router-link :to="item.get_absolute_url_history">{{item.name_history}}</router-link></td>
                                    <td>Rp. {{formatPrices(item.price_history)}}</td>
                                    <td>{{item.quantity_history}} item(s)</td>
                                    <td>{{item.toping_id}}</td> 
                                    <td>{{item.note_customer}}</td> 
                                    <td>Rp. {{formatPrices(item.price_history*item.quantity_history + parseInt(item.price_toping))}}</td> 
                                </tr>
                            </tbody>
                        </table>
                        <input type="hidden"
                            v-bind:value="idDetail"
                            v-on:input="idDetail = $event.target.value" disabled>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import axios from 'axios'
import { formatPrice,calculate } from '@/utils/function'
import moment from 'moment'

export default {
   data(){
        return{
            items: [],
            detailItem: [],
            idDetail: '',
            metode_bayar: '',
            lokasi_pengiriman: '',
            metode_pesanan: '',
            metode_bayar: '',
            kode_unik: '',
            total: '',
            biaya_ongkir: '',
            date_detail_pesanan: '',
            status_bayar: '',
            id_detail_pesanan: ''
        }
    },
    watch: {
        idDetail(dataIn, oldData) {
            if (dataIn > -1) {
                this.getDetailCartLists()
                this.getAllCartLists()
            }
        }
    },
    created(){
        this.getAllCartLists()
    },
    computed:{
        total: function() {
            var total2 = this.items.reduce((acc, curVal) =>{
                return acc += curVal.price_history * curVal.quantity_history + parseInt(curVal.price_toping)
            },0);
            var total = calculate(this.biaya_ongkir, total2);
            return total;
        }
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
                    this.idDetail = response.data[0].detail_id_pesanan_id;
                    var dtArray = response.data.filter(function (el)
                        {
                            if (response.data[0].detail_id_pesanan_id == el.detail_id_pesanan_id) {
                                return response.data;
                            }
                        }
                    );this.items = dtArray;
                })
                .catch(error => {console.log(error)})
            this.$store.commit('setIsLoading', false)
        },
        async getDetailCartLists(){
            const token = localStorage.getItem('token')
            const uIds = localStorage.getItem('uid')
            const decodeValueTkn = atob(token);
            const decodeValueId = atob(uIds);
            const detail_id = this.idDetail;
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+decodeValueTkn
            };
            this.$store.commit('setIsLoading', true)
            await axios.get(`/api/v1/usr/detail-checkout-cart-lists/${detail_id}/`, {headers})
                .then(response => {
                    this.detailItem = response.data
                    this.metode_bayar = response.data[0].metode_bayar
                    this.lokasi_pengiriman = response.data[0].lokasi_pengiriman
                    this.metode_pesanan = response.data[0].metode_pesanan
                    this.metode_bayar = response.data[0].metode_bayar
                    this.kode_unik = response.data[0].kode_unik
                    this.status_bayar = response.data[0].status_bayar
                    this.id_detail_pesanan = response.data[0].id_detail_pesanan
                    this.date_detail_pesanan = response.data[0].date_detail_pesanan
                    this.biaya_ongkir = response.data[0].biaya_ongkir
                })
                .catch(error => {console.log(error)})
            this.$store.commit('setIsLoading', false)
        },
    }
}
</script>
<style lang="scss">
@import '~bulma/css/bulma.css';

.tables td {
    border: none
}

.tables th {
    border: none
}
</style>

