<template>
    <div class="container-fluid">
        <div class="main-content columns is-fullheight">
            <SidebarAdmins/>  
            <div class="container mgv-medium mx-5">
                <h1 class="title">Statistik Penjualan</h1>
                <div class="column is-12 is-1-mobile is-0-tablet ml-1">
                    <div class="box">
                        <div class="select">
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
                        <button type="submit" v-if="this.clicked === false" @click="cariData" class="button mx-2 is-responsive" :class="{ 'is-primary': true, 'is-loading': loading, 'clicked': clicked }">Cari</button>
                        <button type="submit" v-else @click="resetPage" class="button mx-2 is-responsive" :class="{ 'is-primary': true, 'is-loading': loading, 'clicked': clicked }">Reset Data</button>
                        <p class="is-pulled-right">Total Penjualan : Rp. {{formatPrices(total)}}</p><br><br>
                    </div>

                    <div class="box columns">
                        <div class="column">
                            <div class="box">
                                <h1 class="title">HotPick</h1>
                                <hr>
                                 <div class="columns"
                                    v-for="item in hotPick"
                                        v-bind:key="item.id"> 
                                    <div class="column">
                                            <h3 class="is-size-4">{{item.name_history}}</h3>
                                            <p class="is-size-6 has-text-grey">Rp. {{formatPrices(item.price_history)}}</p>
                                            <p class="is-size-6">Size: {{item.size}}</p>
                                            <p>Terjual: {{item.quantity_history}} item(s)</p>
                                    </div>
                                    <div class="column">
                                        <figure class="">
                                            <img :src="item.get_thumbnail" alt="thumbnail" width="150" height="150">
                                        </figure>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="column">
                            <div class="box">
                                <h1 class="title">Low Interest</h1> 
                                <hr>
                                <div class="columns"
                                    v-for="item in notInteresting"
                                        v-bind:key="item.id"> 
                                    <div class="column">
                                        <h3 class="is-size-4">{{item.name_history}}</h3>
                                        <p class="is-size-6 has-text-grey">Rp. {{formatPrices(item.price_history)}}</p>
                                        <p class="is-size-6">Size: {{item.size}}</p>
                                        <p>Terjual: {{item.quantity_history}} item(s)</p>
                                    </div>
                                    <div class="column">
                                        <figure class="">
                                            <img :src="item.get_thumbnail" alt="thumbnail">
                                        </figure>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="box">
                        <h1 class="title">Total Item ({{this.itemsDetails.length}})</h1>
                        <hr>
                        <table class="table is-fullwidth">
                            <thead>
                                <tr>
                                    <th>Product</th>
                                    <th>Price</th>
                                    <th>Quantity</th>
                                    <th>Total</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="item in itemsDetails"
                                    v-bind:key="item.id">
                                    <td>{{item.name_history}}</td>
                                    <td>Rp. {{formatPrices(item.price_history)}}</td>
                                    <td>{{item.quantity_history}} item(s)</td>
                                    <td>Rp. {{formatPrices((item.price_history * item.quantity_history))}}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    
                    <div class="box">
                        <h1 class="title">Delivery ({{this.aprioriData.length}})</h1>
                        <hr>
                        <table class="table is-fullwidth">
                            <thead>
                                <tr>
                                    <th>Product</th>
                                    <th>Price</th>
                                    <th>Quantity</th>
                                    <th>Total</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="item in aprioriData"
                                    v-bind:key="item.id">
                                    <td>{{item.name_history}}</td>
                                    <td>Rp. {{formatPrices(item.price_history)}}</td>
                                    <td>{{item.quantity_history}} item(s)</td>
                                    <td>Rp. {{formatPrices((item.price_history * item.quantity_history))}}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="box">
                        <h1 class="title">Pick-Up ({{this.aprioriDataPickUp.length}})</h1>
                        <hr>
                        <table class="table is-fullwidth">
                            <thead>
                                <tr>
                                    <th>Product</th>
                                    <th>Price</th>
                                    <th>Quantity</th>
                                    <th>Total</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="item in aprioriDataPickUp"
                                    v-bind:key="item.id">
                                    <td>{{item.name_history}}</td>
                                    <td>Rp. {{formatPrices(item.price_history)}}</td>
                                    <td>{{item.quantity_history}} item(s)</td>
                                    <td>Rp. {{formatPrices((item.price_history * item.quantity_history))}}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                </div>  
            </div>
        </div>
        <AppFooter/>
    </div>
</template>

<script>
import SidebarAdmins from '@/components/SideBarAdmin'
import AppFooter from '@/components/AppFooter'
import axios from 'axios'
import { formatPrice } from '@/utils/slugmaker'
import {toast} from 'bulma-toast'

export default {
    components: {
        SidebarAdmins,
        AppFooter
    },
    data(){
        return{
            itemsDetail: [],
            itemsDetails: {},
            aprioriData: {},
            hotPick: {},
            notInteresting: {},
            aprioriDataPickUp: {},
            years: [],
            months: ["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"],
            days: [
                    "01","02","03","04","05","06","07","08","09","10","11","12",
                    "13","14","15","16","17","18","19","20","21","22","23","24",
                    "25","26","27","28","29","30","31"
                ],
            i_month:'',
            i_year:'',
            i_day:'',
            search_data:'',
            loading:false,
            clicked:false,
        }
    },
    computed:{
        total: function() {
            return this.itemsDetail.reduce((acc, curVal) =>{
                return acc += (curVal.price_history * curVal.quantity_history) + parseInt(curVal.price_toping)

            },0);
        },
    },
    created(){
        this.getAllAprioriData(),
        this.getAllPesananHistory()
    },
    watch:{
        clicked(){
            if (this.clicked === true) {
                this.postDetailPesananHistory(this.search_data)
            } 
        }
    },
    methods:{
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
        async getAllPesananHistory(){
            const token = localStorage.getItem('token')
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+token
            };
            this.$store.commit('setIsLoading', true)
            await axios.get('/api/v1/usr/all-user-order-lists', {headers})
                .then(response => {
                    const datasd = response.data
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
                    this.itemsDetail = datasd
                    this.itemsDetails = result
                    const tahunsekarang = (new Date()).getFullYear();
                    const range = (start, stop, step) => Array.from({ length: (stop - start) / step + 1}, (_, i) => start + (i * step));
                    const year = range(tahunsekarang, tahunsekarang - 10, -1); 
                    this.years = year;
                })
                .catch(error => {
                    console.log(error)
                    this.$router.go()
                })
            this.$store.commit('setIsLoading', false)
        },
        async getAllAprioriData(){
            const token = localStorage.getItem('token')
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+token
            };
            this.$store.commit('setIsLoading', true)
            await axios.get('/api/v1/usr/apriori-data', {headers})
                .then(response => {
                    const datasd = response.data
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
                    const aprioriDatat =  result.filter(function(metode) {
                        return metode.metode_pesanan == "Delivery";
                    });
                    const aprioriDataPickUp =  result.filter(function(metode) {
                        return metode.metode_pesanan == "Pick-up";
                    });
                    // const sortLowest = arr => {
                    //     return arr.reduce((acc, val) => {
                    //         let a = 0;
                    //         while(a < arr.length && val < arr[a]){
                    //             a++;
                    //         }
                    //         acc.splice(a, 1, val);
                    //         return acc;
                    //     }, []);
                    // };
                    this.aprioriData = aprioriDatat
                    this.aprioriDataPickUp = aprioriDataPickUp
                    this.hotPick = result.sort(function(a, b) {
                        return b.quantity_history - a.quantity_history;
                    }).slice(0, 1)
                    this.notInteresting = result.sort(function(a, b) {
                        return a.quantity_history - b.quantity_history;
                    }).slice(0, 1)
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
            this.$store.commit('setIsLoading', true)
            await axios.post('/api/v1/usr/find-statistik-user-cart-lists', postDetailPesananHistorys,{headers})
                .then(response => {
                    const datasd = response.data
                    console.log(datasd)
                    const dataLength = parseInt(JSON.stringify(datasd.length))
                    if (dataLength == 0) {
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
                    this.itemsDetail = datasd
                    this.itemsDetails = result
                    const tahunsekarang = (new Date()).getFullYear();
                    const range = (start, stop, step) => Array.from({ length: (stop - start) / step + 1}, (_, i) => start + (i * step));
                    const year = range(tahunsekarang, tahunsekarang - 10, -1); 
                    this.years = year;
                    this.loading = false;
                })
                .catch(error => {console.log(error)})
            this.$store.commit('setIsLoading', false)
        }
    }
}
</script>

<style lang="scss">
@import '~bulma/css/bulma.css';

</style>