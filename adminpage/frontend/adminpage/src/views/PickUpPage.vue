<template>
    <div class="container-fluid">
        <div class="main-content columns is-fullheight">
            <SidebarAdmins/>  
            <div class="container mgv-medium mx-5">
                <h1 class="title">Pick Up :</h1>
                <div class="box column is-12 is-1-mobile is-0-tablet mt-2 ml-1">
                    <div class="columns mb-1 mt-1 ml-1 mr-1">
                        <div v-if="this.itemsD > 0" class="column is-4">
                            <div class="box">
                                <div v-for="itema in items"
                                    v-bind:key="itema.id">
                                    <p>
                                        #{{itema.id_detail_pesanan}} <span class="is-pulled-right">{{dateTime(itema.date_detail_pesanan)}} <br> <p class="is-pulled-right">{{relativeTime(itema.date_detail_pesanan)}}</p></span> <br><br>
                                        <strong>{{itema.metode_pesanan}}<span> | {{itema.metode_bayar}}</span> </strong><br>
                                        Lokasi : {{itema.lokasi_pengiriman}}<br>
                                        Ongkir : Rp. {{formatPrices(itema.biaya_ongkir)}}<br>
                                        Berita Acara : {{itema.kode_unik}}<br>
                                        Status Bayar : <strong style="color:#E76F51;">{{itema.status_bayar}}</strong><br>
                                        Status Pesanan : <strong style="color:#E76F51;" v-if="itema.is_ready == 0" >Sedang dikerjakan</strong> <strong style="color:#E76F51;" v-else >Selesai dikerjakan</strong><br>
                                    </p>
                                    <div class="buttons are-small">
                                        <button v-if="itema.is_ready == 0" @click='getModalDetailPesananHistory(itema.id_detail_pesanan)' class="button is-primary mt-1 mx-1 modal-button is-fullwidth is-medium is-responsive">Update Status Pesanan</button>
                                        <button v-else class="button is-primary mt-1 mx-1 modal-button is-fullwidth is-medium is-responsive" disabled>Update Status Pesanan</button>
                                    </div>
                                    <hr>
                                </div>
                            </div>
                        </div>
                        <p v-else>Opps! belum ada pesanan nih hari ini</p>
                    </div>
                </div>
                <!-- modal start -->
                <div class="modal" v-bind:class="{ 'is-active': isShowModal }">
                    <div class="modal-background" v-on:click="isShowModal = false"></div>
                    <div class="modal-card">
                        <header class="modal-card-head">
                            <p class="modal-card-title">Apakah semua pesanan sudah selesai dikerjakan?</p>
                            <button class="delete" aria-label="close" v-on:click="isShowModal = false"></button>
                        </header>
                        <section v-if="cartTotalLength" class="modal-card-body">
                            <p class="is-pulled-right">Total : Rp.{{formatPrices(total)}}</p>
                            Nama pelanggan:<h6 style="color:#2A9D8F;"> {{this.nama_user}} | {{this.no_hp}}</h6> 
                            <table class="table is-fullwidth">
                                <thead>
                                    <tr>
                                        <th>Product</th>
                                        <th>Price</th>
                                        <th>Quantity</th>
                                        <th>Sisa Stok</th>
                                        <th>Total</th>
                                        <th>Aksi</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="item in itemsDetail"
                                        v-bind:key="item.id">
                                        <td>{{item.name_history}}</td>
                                        <td>Rp. {{formatPrices(item.price_history)}}</td>
                                        <td>{{item.quantity_history}} item(s)</td>
                                        <td v-if="item.is_stokUpdated == 0">{{item.stok - item.quantity_history}} item(s)</td>
                                        <td v-else>{{item.stok}} item(s)</td>
                                        <td>Rp. {{formatPrices(item.price_history*item.quantity_history)}}</td> 
                                        <td v-if="item.is_stokUpdated == 0"><button class="button is-primary" @click="updateStoks(item); updateStokStatus(item)">Update Stok</button></td> 
                                        <td v-else><button class="button is-primary" disabled>Updated</button></td> 
                                    </tr>
                                </tbody>
                            </table>
                        </section>
                        <footer class="modal-card-foot">
                            <input type="hidden" v-model="itemId" disabled/>
                            <input type="hidden" v-model="itemIdProduct" disabled/>
                            <input type="hidden" v-model="sisaStok" disabled/>
                            <button class="button is-primary" @click='updateStatusPesanan(this.modal_id_pesanan); updateHistoryCart();'>Iya, Sudah!</button>
                            <button class="button is-danger" v-on:click="isShowModal = false">Batal</button>
                        </footer>
                    </div>
                </div>
                <!-- modal end -->
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
            itemId: [],
            itemIdProduct: [],
            sisaStok: [],
            itemsD: '',
            itemsDetail: [],
            displays:'block',
            isShowModal:false,
            nama_user:'',
            modal_id_pesanan:'',
            no_hp:'',
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
                return acc += curVal.price_history * curVal.quantity_history
            },0);
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
        relativeTime(value) {
            return moment(value).startOf('hour').fromNow(); 
        },
        formatPrices(harga) {
            var hargas = parseInt(harga)
            var hargat = formatPrice(hargas);
            return hargat;
        },
        async getAllCartLists(){
            const token = localStorage.getItem('token')
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+token
            };
            this.$store.commit('setIsLoading', true)
            await axios.get('/api/v1/usr/transaksi-user-pickup-lists/', {headers})
                .then(response => {
                    this.items = response.data
                    this.itemsD = parseInt(JSON.stringify(response.data.length))
                })
                .catch(error => {console.log(error)})
            this.$store.commit('setIsLoading', false)
        },
        async updateStoks(item){
            const token = localStorage.getItem('token')
            const idproduk = item.id_product_history
            const updatestok = item.stok - item.quantity_history
            const updateStok = JSON.stringify({
                stok: updatestok
            });
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+token
            };
            await axios
                .put(`/api/v1/usr/product-update-stok/${idproduk}`, updateStok, {headers})
                .then(response=>{
                    if (response) {
                        toast({
                            message: 'Stok Berhasil Di perbaharui',
                            type: 'is-success',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 5000,
                            position: 'top-right',
                        })
                    } else{
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
        async updateStokStatus(item){
            const token = localStorage.getItem('token')
            const id = item.id
            const updateStatusStok = JSON.stringify({
                is_stokUpdated: 1
            });
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+token
            };
            await axios
                .put(`/api/v1/usr/update-status-stok/${id}`, updateStatusStok, {headers})
                .then(response=>{
                    if (response) {
                        this.$router.go()
                    } else{
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
        async updateStok(){
            const token = localStorage.getItem('token')
            const updateStok = JSON.stringify({
                idP: this.itemIdProduct.slice(0, -1),
                ustok: this.sisaStok.slice(0, -1),
            });
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+token
            };
            await axios
                .put(`/api/v1/usr/product-update-stok`, updateStok, {headers})
                .then(response=>{
                    if (response) {
                        toast({
                            message: 'Stok Berhasil Di perbaharui',
                            type: 'is-success',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 5000,
                            position: 'top-right',
                        })
                        this.clicked = true
                    } else{
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
        async getModalDetailPesananHistory(id_pesanan){
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
                    this.isShowModal = true
                    this.modal_id_pesanan = id_pesanan
                    if (response.data) {
                        let ids = "";
                        for (ids in response.data) {
                            const dts = response.data[ids].id;
                            const dtP = response.data[ids].id_product_history;
                            const dtstok = response.data[ids].stok - response.data[ids].quantity_history
                            this.itemId += parseInt(dts)+","
                            this.itemIdProduct += parseInt(dtP)+","
                            this.sisaStok += parseInt(dtstok)+","
                        }
                    }
                })
                .catch(error => {console.log(error)})
            this.$store.commit('setIsLoading', false)
        },
        async updateStatusPesanan(id_pesanan){
            const token = localStorage.getItem('token')
            const updateStatusPesanan = JSON.stringify({
                is_ready: 1,
            });
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+token
            };
            this.$store.commit('setIsLoading', true)
            await axios.put(`/api/v1/usr/update-status-pesanan/${id_pesanan}`,updateStatusPesanan, {headers})
                .then(response => {
                    if (response) {
                        toast({
                            message: 'Status Pesanan Berhasil Di Perbaharui',
                            type: 'is-success',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 5000,
                            position: 'top-right',
                        })
                        this.$router.go()
                    } else{
                        toast({
                            message: 'Gagal Mengupdate Data',
                            type: 'is-danger',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 5000,
                            position: 'top-right',
                        })
                        this.$router.go()
                    }
                })
                .catch(error => {console.log(error)})
            this.$store.commit('setIsLoading', false)
        },
        async updateHistoryCart(){
            const token = localStorage.getItem('token')
            const checkoutStore = JSON.stringify({
                id: this.itemId.slice(0, -1),
                is_history: 1, // checkout history
            });
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+token
            };
                await axios
                    .put(`/api/v1/usr/update-history-cart`, checkoutStore, {headers})
                    .then(response=>{
                        this.$router.go()
                        return response
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