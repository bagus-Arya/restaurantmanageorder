<template>
    <div class="container-fluid">
        <div class="main-content columns is-fullheight">
            <SidebarAdmins/>  
            <div class="container mgv-medium mx-5">
                <h1 class="title">Riwayat</h1>
                <div class="box column is-12 is-1-mobile is-0-tablet mt-2 ml-1">
                    <div class=" mb-1 mt-1 ml-1 mr-1">
                        <div class="is-5">

                            <div class="box">
                                <div class="select ml-5">
                                    <select class="is-hovered" @change="chooseDay">
                                        <option
                                            :key="daysArray"
                                            v-for="daysArray in days"
                                            :value="daysArray"
                                            >
                                            {{ daysArray }}
                                        </option>
                                    </select>
                                </div>
                                <div class="select mx-1">
                                    <select class="is-hovered" @change="chooseMonth">
                                        <option
                                            :key="monthArray"
                                            v-for="monthArray in months"
                                            :value="monthArray"
                                            >
                                            {{ monthArray }}
                                        </option>
                                    </select>
                                </div>
                                <div class="select">
                                    <select class="is-hovered" @change="chooseYear">
                                        <option
                                            :key="yearArray"
                                            v-for="yearArray in years"
                                            :value="yearArray"
                                            >
                                            {{ yearArray }}
                                        </option>
                                    </select>
                                </div>
                                <button type="submit" v-if="this.clicked === false" @click="cariData" class="button mt-2 is-fullwidth is-responsive" :class="{ 'is-primary': true, 'is-loading': loading, 'clicked': clicked }">Cari</button>
                                <button type="submit" v-else @click="resetPage" class="button is-fullwidth mt-2 is-responsive" :class="{ 'is-primary': true, 'is-loading': loading, 'clicked': clicked }">Reset Data</button>
                            </div>

                            <div class="box box-pesanan">
                                <div v-if="cartTotalLength">
                                    <div class="card-content">
                                        <div class="content">
                                            <p class="is-pulled-right">Total : Rp.{{formatPrices(total)}}</p>
                                            Nama pelanggan:<h6 style="color:#2A9D8F;"> {{this.nama_user}} | {{this.no_hp}}</h6> 
                                            <table class="table is-fullwidth">
                                                <thead>
                                                    <tr>
                                                        <th>Product</th>
                                                        <th>Price</th>
                                                        <th>Quantity</th>
                                                        <th>Toping</th>
                                                        <th>Note</th>
                                                        <th>Total</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    <tr v-for="item in itemsDetail"
                                                        v-bind:key="item.id">
                                                        <td>{{item.name_history}}</td>
                                                        <td>Rp. {{formatPrices(item.price_history)}}</td>
                                                        <td>{{item.quantity_history}} item(s)</td>
                                                        <td>{{item.toping_id}} (Rp.{{formatPrices(item.price_toping)}})</td>
                                                        <td>{{item.note_customer}}</td>
                                                        <td>Rp. {{formatPrices((item.price_history * item.quantity_history)+parseInt(item.price_toping))}}</td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div v-if="this.clicked === false">
                                <div class="box" v-if="this.itemsDetail !== null">
                                    <div v-for="itema in items"
                                        v-bind:key="itema.id">
                                        <p>
                                            #{{itema.id_detail_pesanan}} <span class="is-pulled-right">{{dateTime(itema.date_detail_pesanan)}} <br> <p class="is-pulled-right">{{relativeTime(itema.date_detail_pesanan)}}</p></span> <br><br>
                                            <strong>{{itema.metode_pesanan}}<span> | {{itema.metode_bayar}}</span> </strong><br>
                                            Lokasi : {{itema.lokasi_pengiriman}}<br>
                                            Ongkir : {{itema.biaya_ongkir}}<br>
                                            Berita Acara : {{itema.kode_unik}}<br>
                                            Status Bayar : <strong style="color:#2A9D8F;">{{itema.status_bayar}}</strong><br>
                                        </p>
                                        <div class="buttons are-small is-pulled-right">
                                            <button @click='getDetailPesananHistory(itema.id_detail_pesanan)' class="button mt-1 mx-1" :class="{ 'is-primary': true }">Lihat Pesanan</button>
                                        </div>
                                        <hr>
                                        <br>
                                    </div>
                                </div>
                                <p v-else>Opps! belum ada pesanan nih</p>
                            </div>

                            <div v-else>
                                <div class="box">
                                    <div v-for="itema in searchitems"
                                        v-bind:key="itema.id">
                                        <p>
                                            #{{itema.id_detail_pesanan}} <span class="is-pulled-right">{{dateTime(itema.date_detail_pesanan)}} <br> <p class="is-pulled-right">{{relativeTime(itema.date_detail_pesanan)}}</p></span> <br><br>
                                            <strong>{{itema.metode_pesanan}}<span> | {{itema.metode_bayar}}</span> </strong><br>
                                            Lokasi : {{itema.lokasi_pengiriman}}<br>
                                            Ongkir : {{itema.biaya_ongkir}}<br>
                                            Berita Acara : {{itema.kode_unik}}<br>
                                            Status Bayar : <strong style="color:#2A9D8F;">{{itema.status_bayar}}</strong><br>
                                        </p>
                                        <div class="buttons are-small is-pulled-right">
                                            <button @click='getDetailPesananHistory(itema.id_detail_pesanan)' class="button mt-1 mx-1" :class="{ 'is-primary': true }">Lihat Pesanan</button>
                                        </div>
                                        <hr>
                                        <br>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <AppFooter/>
    </div>
</template>

<script>
import axios from 'axios'
import { formatPrice } from '@/utils/slugmaker'
import SidebarAdmins from '@/components/SideBarAdmin'
import AppFooter from '@/components/AppFooter'
import moment from 'moment'
import {toast} from 'bulma-toast'

export default {
    components: {
        SidebarAdmins,
        AppFooter
    },
    data(){
        return{
            items: [],
            searchitems: [],
            years: [],
            months: ["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"],
            days: [
                    "01","02","03","04","05","06","07","08","09","10","11","12",
                    "13","14","15","16","17","18","19","20","21","22","23","24",
                    "25","26","27","28","29","30","31"
                ],
            itemsDetail: [],
            nama_user:'',
            no_hp:'',
            i_month:'',
            searchitemfail:'',
            i_year:'',
            i_day:'',
            loading:false,
            clicked:false,
            search_data:'',
            berita_acara:'',
        }
    },
    computed:{
        cartTotalLength(){
            return this.itemsDetail.reduce((acc, curVal) =>{
                return acc += parseInt(curVal.quantity_history)
            },0)
        },
        total: function() {
            return this.itemsDetail.reduce((acc, curVal) =>{
                return acc += (curVal.price_history * curVal.quantity_history)+ parseInt(curVal.price_toping)
            },0);
        },
    },
    watch:{
        clicked(){
            if (this.clicked === true) {
                this.postDetailPesananHistory(this.search_data)
            } 
        }
    },
    created(){
        this.getAllCartLists()
    },
    methods:{
        dateTime(value) {
            return moment(value).format('LLL');
        },
        relativeTime(value) {
            return moment(value).startOf('hour').fromNow(); 
        },
        formatPrices(harga) {
            var hargas = parseInt(harga)
            var hargat = formatPrice(hargas);
            return hargat;
        },
        chooseYear(e) {
            this.i_year = e.target.value
        },
        chooseDay(e) {
            this.i_day = e.target.value
        },
        chooseMonth(e) {
            this.i_month = e.target.value
        },
        resetPage() {
            this.$router.go()
        },
        cariData() {
            if (this.i_month == "Januari") {
                const jan = this.i_month.replace("Januari", "01")
                this.search_data = this.i_year+'-'+jan+'-'+this.i_day
            }else if(this.i_month == "Februari"){
                const feb = this.i_month.replace("Februari", "02")
                this.search_data = this.i_year+'-'+feb+'-'+this.i_day
            }else if(this.i_month == "Maret"){
                const mar = this.i_month.replace("Maret", "03")
                this.search_data = this.i_year+'-'+mar+'-'+this.i_day
            }else if(this.i_month == "April"){
                const apr = this.i_month.replace("April", "04")
                this.search_data = this.i_year+'-'+apr+'-'+this.i_day
            }else if(this.i_month == "Mei"){
                const mei = this.i_month.replace("Mei", "05")
                this.search_data = this.i_year+'-'+mei+'-'+this.i_day
            }else if(this.i_month == "Juni"){
                const jun = this.i_month.replace("Juni", "06")
                this.search_data = this.i_year+'-'+jun+'-'+this.i_day
            }else if(this.i_month == "Juli"){
                const jul = this.i_month.replace("Juli", "07")
                this.search_data = this.i_year+'-'+jul+'-'+this.i_day
            }else if(this.i_month == "Agustus"){
                const aug = this.i_month.replace("Agustus", "08")
                this.search_data = this.i_year+'-'+aug+'-'+this.i_day
            }else if(this.i_month == "September"){
                const sep = this.i_month.replace("September", "09")
                this.search_data = this.i_year+'-'+sep+'-'+this.i_day
            }else if(this.i_month == "Oktober"){
                const oct = this.i_month.replace("Oktober", "10")
                this.search_data = this.i_year+'-'+oct+'-'+this.i_day
            }else if(this.i_month == "November"){
                const nov = this.i_month.replace("November", "11")
                this.search_data = this.i_year+'-'+nov+'-'+this.i_day
            }else if(this.i_month == "Desember"){
                const des = this.i_month.replace("Desember", "12")
                this.search_data = this.i_year+'-'+des+'-'+this.i_day
            }
            this.loading = true;
            this.clicked = true;
        },
        async getAllCartLists(){
            const token = localStorage.getItem('token')
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+token
            };
            this.$store.commit('setIsLoading', true)
            await axios.get('/api/v1/usr/riwayat-user-cart-lists/', {headers})
                .then(response => {
                    this.items = response.data
                    const tahunsekarang = (new Date()).getFullYear();
                    const range = (start, stop, step) => Array.from({ length: (stop - start) / step + 1}, (_, i) => start + (i * step));
                    const year = range(tahunsekarang, tahunsekarang - 10, -1); 
                    this.years = year;
                })
                .catch(error => {console.log(error)})
            this.$store.commit('setIsLoading', false)
        },
        async getDetailPesananHistory(id_pesanan){
            const token = localStorage.getItem('token')
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+token
            };
            this.$store.commit('setIsLoading', true)
            await axios.get(`/api/v1/usr/history-user-cart-lists/${id_pesanan}`, {headers})
                .then(response => {
                    this.itemsDetail = response.data
                    this.nama_user = response.data[0].name_depan_user?response.data[0].name_depan_user:response.data[0].username;
                    this.no_hp = response.data[0].hp?response.data[0].hp:'-';
                })
                .catch(error => {
                    console.log(error)
                    this.$router.go()
                })
            this.$store.commit('setIsLoading', false)
        },
        async postDetailPesananHistory(datestr){
            const token = localStorage.getItem('token')
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+token
            };
            const postDetailPesananHistorys = JSON.stringify({
                datestrs: datestr,
            });
            console.log(postDetailPesananHistorys)
            this.$store.commit('setIsLoading', true)
            await axios.post('/api/v1/usr/find-riwayat-user-cart-lists', postDetailPesananHistorys,{headers})
                .then(response => {
                    this.searchitems = response.data
                    this.searchitemfail = parseInt(JSON.stringify(response.data.length))
                    if (this.searchitemfail == 0) {
                        toast({
                            message: 'Data Tidak Dapat Ditemukan',
                            type: 'is-warning',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 5000,
                            position: 'top-right',
                        })
                        this.$router.go()
                    }
                    this.nama_user = response.data[0].name_depan_user?response.data[0].name_depan_user:response.data[0].username;
                    this.no_hp = response.data[0].hp?response.data[0].hp:'-';
                    this.loading = false;
                })
                .catch(error => {
                    console.log(error)
                    this.$router.go()
                })
            this.$store.commit('setIsLoading', false)
        }
    }
}
</script>

<style lang="scss">
@import '~bulma/css/bulma.css';

  .box-pesanan {
    position: sticky;
    display: inline-block;
    vertical-align: top;
    max-height: 50vh;
    overflow-y: auto;
    top: 0;
    bottom: 0;
    padding: 30px;
  }
</style>