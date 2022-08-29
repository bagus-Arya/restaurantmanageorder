<template>
    <div class="container">
        <div class="page-cart">
            <!-- <div class="column is-12 box mb-3" v-bind:style="{ display: computedNone }" > -->
            <div class="column is-12 box mb-3" >
                <div>
                    <l-map
                    v-model="maps.zoom"
                    :zoom.sync="maps.zoom"
                    :center="maps.center"
                    :max-zoom="19"
                    style="height: 435px; width: auto;"
                    >
                    <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
                    <l-control-layers />
                        <l-marker
                            :key="markers.id"
                            :visible="markers.visible"
                            :draggable="markers.draggable"
                            :lat-lng="markers.position"
                            :icon="markers.icon"
                            @click="getAddress"
                        >
                        <l-tooltip :content="markers.tooltip" />
                    </l-marker>

                    <l-marker :lat-lng="icons.mmLocation">
                        <l-icon
                        :icon-size="iconSize"
                        :icon-url="iconUrl">
                        </l-icon>
                        <l-tooltip :content="icons.tooltip" />
                    </l-marker>
                    </l-map>
                </div>
            </div>
            <div class="column is-12 mb-3">
                <h1 class="title">Checkout</h1>
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
                    <p v-else>You don't have anything in your cart</p>
                </div>
                <div class="column box">
                    <div class="control mb-2">
                            <div class="column">
                                <template v-if="v$.md_order.$error">
                                    <span style="color:#E76F51;">*Metode pesanan wajib dipilih</span><br>
                                </template>
                                <template v-if="v$.md_payment.$error">
                                    <span style="color:#E76F51;">*Metode bayar wajib dipilih</span><br>
                                </template>
                                <template v-if="v$.alamatKirim.$error">
                                    <span style="color:#E76F51;">*Silahkan geser & klik Icon lokasi pada Maps untuk menentukan lokasi</span><br>
                                </template>
                                <template v-if="v$.no_hp.$error">
                                    <span v-if="this.no_hp == ''" style="color:#E76F51;">*Nomor Handphone wajib diisi</span>
                                    <span v-if="v$.no_hp.maxLength" style="color:#E76F51;"> *Max 13 Karakter</span>
                                </template>
                            </div>
                        <div class="columns is-mobile">
                            <div class="column">
                                <h6>Metode Pesanan</h6>
                                <div class="select">
                                    <select class="is-hovered" @change="showMaps">
                                        <option>-- Pilih Metode --</option>
                                        <option value="Pick-up">Pick-Up</option>
                                        <option value="Delivery">Delivery</option>
                                    </select>
                                </div>
                            </div>
                            <div class="column">
                                <h6>Metode Bayar</h6>
                                <div class="select">
                                    <select class="is-hovered" @change="choosePayment">
                                        <option>-- Pilih Metode --</option>
                                        <option value="Cash">Cash</option>
                                        <option value="Transfer">Transfer</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="control mb-2">
                        <h6>Nomor Handphone</h6>
                        <input v-bind:value="no_hp"
                            v-on:input="no_hp = $event.target.value"
                            class="input" type="text">
                    </div>
                    <div class="control mb-2">
                        <h6>Alamat</h6>
                        <textarea type="text" class="textarea" v-model="alamatKirim" col="50" disabled> </textarea>
                    </div>
                        <h6 v-if="this.kilometer == 0">Ongkos Kirim ( 0 Km)</h6>
                        <h6 v-else>Ongkos Kirim ( {{this.kilometer}} Km)</h6>
                    <div class="field has-addons mt-2">
                            <div class="control">
                                <input v-if="this.distance == 0" type="text" class="input" v-model="distances" disabled/>
                                <input v-else type="text" class="input" v-model="distance" disabled/>
                            </div>
                            <div class="control">
                                <button v-if="(this.md_order == 'Delivery') && (this.freearea == 'freearea') || (this.freearea == 'insidedps')" class="button is-primary" @click="getDistance">Cek Ongkir</button>
                                <button v-else-if="this.md_order == 'Pick-up'" class="button is-primary" disabled>Cek Ongkir</button>
                                <button v-else class="button is-primary" disabled>Cek Ongkir</button>
                            </div>
                    </div>
                    <h2 class="subtitle">
                        Summary
                    </h2>
                    <strong>Rp. {{ formatPrices(total) }}</strong>
                    <input type="hidden" v-model="total" disabled/>
                    <input type="hidden" v-model="kdBayar" disabled/>
                    <input type="hidden" v-model="id_detail_random" disabled/>
                    <input type="hidden" v-model="itemHistory" disabled/>
                    <input type="hidden" v-model="idusr" disabled/>
                    <hr>
                    
                    <button v-if="$store.state.IS_CEKONGKIR == false" class="button is-primary" disabled>Bayar Sekarang ({{cartTotalLength}}) item(s)</button>
                    <button v-else @click.prevent='validateForms();' class="button is-primary">Bayar Sekarang ({{cartTotalLength}}) item(s)</button>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import axios from 'axios'
import { formatPrice } from '@/utils/function'
import {toast} from 'bulma-toast'
import {
  LMap,
  LIcon,
  LTileLayer,
  LMarker,
  LTooltip,
  LControlLayers,
  LPopup,
  LCircle,
  LPolygon,
} from "@vue-leaflet/vue-leaflet";
import "leaflet/dist/leaflet.css";
import { calculate, kd_bayar, randomChar } from '@/utils/function'
import useValidate from "@vuelidate/core";
import { required, maxLength } from "@vuelidate/validators";

export default {
    components:{
        LMap,
        LIcon,
        LTileLayer,
        LMarker,
        LControlLayers,
        LTooltip,
        LPopup,
        LCircle,
        LPolygon,
    },
    validations() {
        return {
            md_order: { required },
            md_payment: { required },
            alamatKirim: { required },
            no_hp: { required, maxLength:maxLength(13) }
        };
    },
    data(){
        return{
            v$: useValidate(),
            items: [],
            itemHistory: [],
            alamatKirim: '', 
            distance: '',
            distances: '',
            ids: '',
            idusr: '',
            no_hp: '',
            kilometer: '',
            md_order:'',
            id_detail_random:'',
            md_payment:'',
            kdBayar:'',
            kdBayar:'',
            freearea:'',
            displays:'none',
            acc:'',
            url:'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            attribution:
                '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
            icons:{
                iconWidth: 60,
                iconHeight: 50,
                tooltip: 'Lokasi Mammamia Renon',
                mmLocation:{ lat:-8.674267, lng:115.226320 },
            },
            userLocation: { lat: '', lng: ''},
            maps: {
                center: [-8.67309677934738, 115.22660597200628],
                zoom: 15,
            },
            markers: {
                id: 'm1',
                position: { lat:-8.672844915233407, lng:115.22173117482454 },
                tooltip: 'Klik untuk atur lokasi tujuan',
                draggable: true,
                visible: true,
            },     
        }
    },
    mounted(){
        this.getUserDetail()
        document.title = 'Checkout'+ ' | Mammamia Renon'
    },
    computed:{
        iconUrl() {
            return '/img/logo_mammamia.f3779587.png';
        },
        iconSize() {
            return [this.icons.iconWidth, this.icons.iconHeight];
        },
        cartTotalLength(){
            return this.items.reduce((acc, curVal) =>{
                return acc += parseInt(curVal.quantity_history)
            },0)
        },
        total: function() {
            var total2 = this.items.reduce((acc, curVal) =>{
                return acc += curVal.price_history * curVal.quantity_history + parseInt(curVal.price_toping)
            },0);
            var total = calculate(this.distance, total2);
            return total;
        },
        computedNone: function () {
            return this.displays;
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
            await axios.get(`/api/v1/usr/history-cart-lists/${decodeValueId}/`, {headers})
                .then(response => {
                    this.items = response.data
                    var kdByr = kd_bayar(1);
                    this.kdBayar = parseInt(kdByr);
                    this.id_detail_random = randomChar(8);
                    let ids = "";
                    for (ids in response.data) {
                        if ( response.data.hasOwnProperty(ids) ) {
                            const dts = response.data[ids].id;
                            this.itemHistory += parseInt(dts)+","
                        }
                    }
                })
                .catch(error => {console.log(error)})
            this.$store.commit('setIsLoading', false)
        },
        // Menggunakan data dummy untuk menghemat API QUOTA REQ
        async getDistance(){
            const APP_KEY = "5b3ce3597851110001cf624888a5e141273b4b1480c92c80963df51e"
            const START = this.userLocation.lng+','+this.userLocation.lat
            const END = 115.23905794252643+','+-8.688198990795224
            // const END = this.icons.mmLocation.lng+','+this.icons.mmLocation.lat
            const headers = { 
                'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8'
            }
            await axios
            .get('https://api.openrouteservice.org/v2/directions/driving-car?api_key='+APP_KEY+'&start='+START+'&end='+END, {headers})
            .then(response => {
                const perMeter = response.data.features[0].properties.summary.distance
                var hasil = Math.round(perMeter / 1000) * 1000
                this.kilometer = hasil / 1000
                if (hasil >= 2900) { // round 8000 km max
                    this.distance = (hasil) * 4 // Rp.4000/km
                    this.$store.commit('setButtonCekOngkir', true)
                } else {
                    this.distance = 0
                    this.distances = "Gratis Ongkir"
                    this.$store.commit('setButtonCekOngkir', true)
                }
            })
            .catch(error => {console.log(error)})
        },
        validateForms(){
            this.v$.$validate() 
            if (!this.v$.$error) { 
                this.postDetailHistoryCart(); 
                this.updateHistoryCart(); 
                this.updateProfile(); 
                this.removeFromCart(); 
            } else {
                toast({
                    message: 'Gagal Divalidasi',
                    type: 'is-danger',
                    dismissible: true,
                    pauseOnHover: true,
                    duration: 2000,
                    position: 'center',
                })
            }
            console.log(this.v$)
        },
        async postDetailHistoryCart(){
            const token = localStorage.getItem('token')
            const decodeValue = atob(token)
            const checkoutStore = JSON.stringify({
                lokasi_pengiriman: this.alamatKirim?this.alamatKirim:'none',
                kode_unik: this.kdBayar?this.kdBayar:0,
                metode_pesanan: this.md_order,
                metode_bayar: this.md_payment,
                is_checkout: 1, // indicates checkout 
                biaya_ongkir: parseInt(this.distance)?parseInt(this.distance):0,
                id_detail_pesanan: parseInt(this.id_detail_random)
            });
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+decodeValue
            };
            await axios
                .post(`/api/v1/usr/detail-history-store/`, checkoutStore, {headers})
                .then(response=>{
                    this.$router.push('/review-cart')
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
        async updateHistoryCart(){
            const token = localStorage.getItem('token')
            const uids = localStorage.getItem('uid')
            const decodeValue = atob(token)
            const decodeValueuIds = atob(uids)
            const checkoutStore = JSON.stringify({
                id: this.itemHistory.slice(0, -1),
                is_checkout: 1, // checkout history
                // is_history: 1, // checkout history
                detail_id_pesanan_id: this.id_detail_random
            });
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+decodeValue
            };
            await axios
                .put(`/api/v1/usr/update-history-cart/${decodeValueuIds}/`, checkoutStore, {headers})
                .then(response=>{
                    this.$router.push('/review-cart')
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
        async getUserDetail(){
            const token = localStorage.getItem('token')
            const uIds = localStorage.getItem('uid')
            const decodeValueTkn = atob(token);
            const decodeValueId = atob(uIds);
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+decodeValueTkn
            };
            await axios.get(`/api/v1/usrs/${decodeValueId}/`, {headers})
                .then(response => {
                        if (response.data[0]) {
                            this.idusr = response.data[0].user_id; 
                            this.no_hp = response.data[0].hp; 
                        }
                    })
                .catch(error => {console.log(error)})

        },
        async updateProfile(){
            const token = localStorage.getItem('token')
            const decodeValue = atob(token)
            const decodeValueuIds = this.idusr
            const checkoutStore = {
                hp: this.no_hp,
            };
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+decodeValue
            };
                await axios
                    .put(`/api/v1/usr/update/${decodeValueuIds}/`, checkoutStore, {headers})
                    .then(response=>{
                        this.$router.push('/review-cart')
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
        // parsing const datas ke python
        // supaya tidak kelihatan API_KEY 
        async getDistancePython(){
            const headers = { 
                'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8'
            }
            const datas = { 
                START : "-8.674267,115.226320",
                END : "-8.672844915233407,115.22173117482454"
            }
            await axios
            .get('/api/v1/location/distance/', {datas})
            .then(response => {
                console.log(response)
            })
            .catch(error => {console.log(error)})
        },
        async getAddress(e) {
            this.userLocation.lat = e.latlng.lat
            this.userLocation.lng = e.latlng.lng
            try {
                const lat = this.userLocation.lat;
                const lng = this.userLocation.lng;
                const result = await fetch(
                `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lng}`
                );
                const body = await result.json();
                if (result.status === 200) {
                    console.log(lat+","+lng) // After click the marker -8.685905849425838,115.21619796752931
                    console.log("body -> "+ JSON.stringify(body))
                    this.alamatKirim = body.display_name
                    this.$store.commit('setButtonCartClick')

                    if(body.address.city == "Denpasar"){
                        if(body.address.village == "Renon"){
                            this.freearea = "freearea";
                            toast({
                                message: 'Area Free Delivery',
                                type: 'is-success',
                                dismissible: true,
                                pauseOnHover: true,
                                duration: 3000,
                                position: 'center',
                            })
                        } else {
                            this.freearea = "insidedps";
                            toast({
                                message: 'Area Delivery',
                                type: 'is-warning',
                                dismissible: true,
                                pauseOnHover: true,
                                duration: 3000,
                                position: 'center',
                            })
                        }
                    }else{
                        this.freearea = "outsidedps";
                        toast({
                            message: 'Bukan Area Delivery',
                            type: 'is-warning',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 3000,
                            position: 'center',
                        })
                        this.$router.go()
                    }
                  
                }
            } catch (e) {
                console.error("Reverse Geocode Error->", e);
            }    
        },
        async removeFromCart(){
            const token = localStorage.getItem('token')
            const uids = localStorage.getItem('uid')
            const decodeValue = atob(token)
            const decodeValueuIds = atob(uids)
            const deleteCart = JSON.stringify({
                id: this.itemHistory.slice(0, -1),
            });
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization': 'Token '+decodeValue
            };
            await axios.post('/api/v1/usr/delete-cart-bulk/', deleteCart,{headers})
                .then(response => {
                    if (response) {
                        this.$router.go()
                    } else{
                        toast({
                            message: 'Maaf terjadi kesalahan',
                            type: 'is-warning',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 3000,
                            position: 'center',
                        })
                    }
                });
        },
        showMaps(e){
            let d = "Delivery";
            let p = "Pick-up";
            if (e.target.value == d) {
                // this.displays='block';
                this.alamatKirim=" ";
                this.distances=" ";
                toast({
                    message: 'Silahkan geser & klik Icon berwarna Biru pada maps',
                    type: 'is-warning',
                    dismissible: true,
                    pauseOnHover: true,
                    duration: 3000,
                    position: 'center',
                })
                this.$store.commit('setButtonCekOngkir', false)
            } else if(e.target.value == p){
                // this.displays='none';
                this.alamatKirim="Jalan Tukad Jinah No.5 Renon ( Lokasi MammaMia Renon )";
                this.distances=0;
                this.distance=0;
                this.$store.commit('setButtonCekOngkir', true)
            }
            this.md_order = e.target.value;
        },
        choosePayment(e){
            this.md_payment = e.target.value;
        }
    },
}
</script>

