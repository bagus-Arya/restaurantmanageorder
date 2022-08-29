<template>
    <div class="mb-5">
        <h1 class="title">Tambahkan Topping:</h1>
        <div class="column is-12 is-1-mobile is-0-tablet mt-2 ml-1">
            <div class="columns">
                <form @submit.prevent='toppingForm'>
                    <div class="field">
                        <div class="control">
                            <label for="">Nama Topping</label>
                            <input class="input is-large" type="text" v-model="cName" autofocus="">
                        </div>
                    </div>
                    <div class="columns ml-1 mr-1 mt-2">
                        <div class="field mr-1">
                            <label for="">Ukuran</label>
                            <div class="select is-medium is-fullwidth">
                                <select @change="ukurans">
                                    <option value="S">S</option>
                                    <option value="L">L</option>
                                </select>
                            </div>
                        </div>
                        <div class="field">
                            <label for="">Harga</label>
                            <p class="control has-icons-left">
                                <input class="input is-large"     
                                    v-model="price"
                                    type="number" autofocus="">
                                <span class="icon is-small is-left">
                                    Rp
                                </span>
                            </p>
                        </div>
                    </div>
                    <div class="field">
                        <div class="control">
                            <label for="">Keterangan</label>
                            <textarea class="textarea" v-model="descs" cols="65" rows="4"></textarea>
                        </div>
                    </div>
                    <button class="button is-block is-danger is-large is-fullwidth">Tambah Data</button>
                </form>
            </div>
        </div>
        <div class="column">
            <list-topping/>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import {toast} from 'bulma-toast'
import ListTopping from '@/components/ListTopping'

export default {
    data(){
        return{
            cName:'',
            descs:'',
            size:'',
            price:''
        }
    },
    components:{
        ListTopping
    },
    mounted(){
        document.title = 'Input Product'+' | admin mammamia'
    },
    methods:{
        async toppingForm(){
            const toppingData = JSON.stringify({
                name : this.cName,
                note : this.descs,
                size : this.size,
                price : this.price
            });
            const token = localStorage.getItem('token')
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+token
            };
                await axios
                    .post('/api/v1/topping/post', toppingData, {headers})
                    .then(response=>{
                        if (!response) {
                            toast({
                                message: 'Gagal Menambah Data Topping',
                                type: 'is-danger',
                                dismissible: true,
                                pauseOnHover: true,
                                duration: 5000,
                                position: 'top-right',
                            })
                            this.$router.go()
                            return response
                        } else {
                            toast({
                                message: 'Data Berhasil Disimpan',
                                type: 'is-success',
                                dismissible: true,
                                pauseOnHover: true,
                                duration: 5000,
                                position: 'top-right',
                            })
                            this.$router.go()
                            return response
                        }
                    })
                    .catch(error => {
                        if (error.response){
                            for (const property in error.response.data){
                                this.errors.push(`${property}: ${error.response.data[property]}`)
                            }
                            console.log(JSON.stringify(error.response.data))
                        }else if(error.message){
                            toast({
                                message: 'Gagal Membuat Topping',
                                type: 'is-danger',
                                dismissible: true,
                                pauseOnHover: true,
                                duration: 5000,
                                position: 'top-right',
                            })
                        }
                    });
        },
        ukurans(e) {
            this.size = e.target.value
        },
    }
}
</script>

<style lang="scss">
@import '~bulma/css/bulma.css';
</style>