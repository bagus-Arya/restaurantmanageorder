<template>
    <tr>
        <td><router-link :to="item.get_absolute_url">{{item.name}}</router-link></td>
        <td>Rp. {{formatPrices(item.price)}}</td>
        <td>
            {{item.quantity}}
            <a v-if="item.quantity == 1"><i class="fa fa-minus mx-2"></i></a>
            <a v-else @click="decrementQuantity(item);updateCart(item);updateCartHistory(item);"><i class="fa fa-minus mx-2"></i></a>
            <a v-if="(parseInt(item.stok) < 5) || (item.quantity > (parseInt(item.stok) - 2))">Stok Habis</a>
            <a v-else @click="incrementQuantity(item);updateCart(item);updateCartHistory(item);"><i class="fa fa-plus"></i></a>
        </td>

        <!-- toFixed itu untuk remove decimal berlebih -->
        <td>{{item.toping_id}}</td> 
        <td>{{item.note_customer}}</td> 
        <td>Rp. {{formatPrices(getItemTotal(item) + parseInt(item.price_toping))}}</td> 
        <td><button class="delete" @click="removeFromCart(item)"></button></td>
    </tr> 
</template>


<script>
import axios from 'axios'
import { formatPrice } from '@/utils/function'

export default {
    name: 'CartItem',
    props:{
        initialItem : Object
    },
    data(){
        return{
            item: this.initialItem,
            qty:'',
            id_pesanan:'',
        }
    },
    methods:{
        formatPrices(harga) {
            var hargas = parseInt(harga)
            var hargat = formatPrice(hargas);
            return hargat;
        },
        getItemTotal(item){
            return item.quantity * item.price
        },
        decrementQuantity(item){
            item.quantity -= 1
        },
        incrementQuantity(item){
            item.quantity ++
        },
        updateCart(item){
            const token = localStorage.getItem('token')
            const uids = localStorage.getItem('uid')
            const decodeValue = atob(token)
            const id_pesanan = item.id
            const qty = item.quantity
            const decodeValueuIds = atob(uids)
            const cartHitoryStore = JSON.stringify({
                quantity: qty,
                user_id: decodeValueuIds,
                id: id_pesanan
            });
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+decodeValue
            };
            axios
                .put(`/api/v1/usr/cart-update/${id_pesanan}/`, cartHitoryStore, {headers})
                .then(response=>{
                    console.log(response)
                    this.$router.go()
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
        async updateCartHistory(item){
            const token = localStorage.getItem('token')
            const uids = localStorage.getItem('uid')
            const decodeValue = atob(token)
            const id_pesanan = item.id
            const qty = item.quantity
            const decodeValueuIds = atob(uids)
            const cartHitoryStore = JSON.stringify({
                quantity_history: qty,
                user_id_history: decodeValueuIds,
                id: id_pesanan
            });
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+decodeValue
            };
            await axios
                .put(`/api/v1/usr/cart-update-history/${id_pesanan}/`, cartHitoryStore, {headers})
                .then(response=>{
                    console.log(response)
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
        async removeFromCart(item){
            const token = localStorage.getItem('token')
            const decodeValue = atob(token)
            var id_cart = parseInt(item.id)
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+decodeValue
            };
            await axios.delete(`/api/v1/usr/cart-delete/${id_cart}`,{headers})
                .then(response => {
                    console.log(response)
                    this.$router.go()
                });
        }
    }
    
}
</script>


