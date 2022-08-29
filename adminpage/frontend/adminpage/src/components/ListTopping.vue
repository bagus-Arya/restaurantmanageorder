<template>
    <div class="mb-5">
        <h1 class="title">List Topping:</h1>
        <div class="box column is-12 is-1-mobile is-0-tablet mt-2 ml-1">
            <table class="table is-fullwidth">
                <thead>
                    <tr class="has-text-left">
                        <th>Nama Topping</th>
                        <th>Ukuran</th>
                        <th>Harga</th>
                        <th>Keterangan</th>
                        <th>Aksi</th>
                    </tr>
                </thead>
                <tbody>
                    <tr
                        class="has-text-left"
                        v-for="item in toppingLists.lists"
                        v-bind:key="item.id"
                    >   
                        <td>{{item.name}}</td>
                        <td>{{item.size}}</td>
                        <td>Rp.{{formatPrices(item.price)}}</td>
                        <td>{{item.note}}</td>
                        <td>
                            <button class="button is-danger is-outlined is-rounded is-small"
                            @click="removeTopping(item)">
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
import { formatPrice } from '@/utils/slugmaker'

export default {
    data(){
        return{
            toppingLists: {
                lists: []
            },
        }
    },
    mounted(){
        document.title = 'Input Product'+' | admin mammamia'
    },
    created(){
        this.getAllToppingLists()
    },
    methods: {
        formatPrices(harga) {
            var hargas = parseInt(harga)
            var hargat = formatPrice(hargas);
            return hargat;
        },
        async getAllToppingLists(){
            const token = localStorage.getItem('token')
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+token
            };
            await axios.get('/api/v1/topping/lists/', {headers})
                .then(response => {
                        this.toppingLists.lists = response.data
                    })
                .catch(error => {console.log(error)})
        },
        async removeTopping(item){
            const token = localStorage.getItem('token')
            var id_topping = parseInt(item.id)
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+token
            };
            await axios.delete(`/api/v1/topping-delete/${id_topping}`,{headers})
                .then(response => {
                    if (response) {
                        this.$router.go()
                    }
                });
        }
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