 <template>
    <div class="mb-5 mt-5">
        <h1 class="title">List Produk:</h1>
        <div class="box column is-12 is-1-mobile is-0-tablet mt-2 ml-1">
            <table class="table is-fullwidth">
                <thead>
                    <tr>
                        <th>Kategori</th>
                        <th>Nama Produk</th>
                        <th>Ukuran</th>
                        <th>Stok</th>
                        <th>Harga</th>
                        <th>Gambar</th>
                        <th>Deskripsi</th>
                        <th>Aksi</th>
                    </tr>
                </thead>
                
                <tbody>
                    <tr
                        v-for="item in latestProducts"
                        v-bind:key="item.id"
                    >   
                        <td class="has-text-left">{{item.category_name}}</td>
                        <td class="has-text-left">{{item.name}}</td>
                        <td>{{item.size}}</td>
                        <td>{{item.stok}} item(s)</td>
                        <td>Rp. {{formatPrices(item.price)}}</td>
                        <td><img :src="item.get_thumbnail" alt="thumbnail" width="75" height="75"></td>
                        <td class="has-text-left">
                            {{ readMore(item.description) }}
                            <span>
                                <button v-if="this.displays == 'block'" class="button is-danger is-inverted"
                                    @click="closeToping">
                                    <span>Tutup</span>
                                </button>
                                <button v-else class="button is-danger is-inverted"
                                    @click="showToping">
                                    <span>...Selengkapnya</span>
                                </button>
                            </span>
                        </td>
                        <td>
                            <button class="button is-success is-outlined is-rounded is-small mx-2"
                            @click="setEditClicked(item.id)">
                                <span class="icon">
                                    <i class="fa fa-edit"></i>
                                </span>
                            </button>
                            <button class="button is-danger is-outlined is-rounded is-small"
                            @click="removeProduct(item)">
                                <span class="icon">
                                    <i class="fa fa-times"></i>
                                </span>
                            </button>
                        </td>
                    </tr> 
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import {toast} from 'bulma-toast'
import { formatPrice } from '@/utils/slugmaker'

export default {
    data(){
        return{
            latestProducts: [],
            displays:'none',
        }
    },
    mounted(){
        document.title = 'Input Product'+' | admin mammamia'
    },
    created(){
        this.getLatestProducts()
    },
    methods: {
        formatPrices(harga) {
            var hargas = parseInt(harga)
            var hargat = formatPrice(hargas);
            return hargat;
        },
        readMore(str) {
            const noLength = 4
            const stringStr = str.split(', ')
            const desc = str.trim().split(', ',4)
            console.log("asd->"+stringStr.length)
            
            if(stringStr.length > noLength){
                if(this.displays == 'block'){
                    return str
                }
                return String(desc)
            }else{
                return str
            }
            // if(this.displays == 'block'){
            //     return String(str)
            // }else{
            //     return String(desc.split(/[.,!,?]/))
            // }
        },
        showToping() {
            this.displays='block'; 
        },
        closeToping() {
            this.displays='none'; 
        },
        async getLatestProducts(){
            const token = localStorage.getItem('token')
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+token
            };
            this.$store.commit('setIsLoading', true)
            await axios.get('/api/v1/all-products/', {headers})
                .then(response => {this.latestProducts = response.data})
                .catch(error => {console.log(error)})
            this.$store.commit('setIsLoading', false)
        },
        async removeProduct(item){
            const token = localStorage.getItem('token')
            var id_product = parseInt(item.id)
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+token
            };
            await axios.delete(`/api/v1/usr/product-delete/${id_product}`,{headers})
                .then(response => {
                    if (response) {
                        toast({
                            message: 'Produk Berhasil Dihapus',
                            type: 'is-success',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 5000,
                            position: 'top-right',
                        })
                        this.$router.go()
                    }else{
                        toast({
                            message: 'Produk Gagal Dihapus',
                            type: 'is-success',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 5000,
                            position: 'top-right',
                        })
                        this.$router.go()
                    }
                });
        },
        setEditClicked(item){
            this.$store.commit('setEditClickeds', item)
        },
    }
}
</script>

<style lang="scss">
@import '~bulma/css/bulma.css';
table, td, th {
    text-align:center;
    width: 2%;
    padding:2px;
}
</style>