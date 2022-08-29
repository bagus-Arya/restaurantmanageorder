<template>
    <div class="mb-5">
        <div class="box column is-12 is-1-mobile is-0-tablet mt-2 ml-1">
            <div class="box columns">
                <div class="column">
                    <form @submit.prevent='categoryForm'>
                        <h1 class="title">Tambahkan Kategori Produk:</h1>
                        <div class="field">
                            <div class="control">
                                <label for="">Nama Kategori</label>
                                <input class="input is-large" type="text" v-model="cName" autofocus="">
                            </div>
                        </div>
                        <div class="field">
                            <div class="control">
                                <input class="input" type="hidden" v-model="slug" disabled/>
                            </div>
                        </div>
                        <button class="button is-block is-danger is-large is-fullwidth">Tambah Data</button>
                    </form>
                    <br>
                    <list-category/>
                </div>
                <div class="column">
                    <post-topping/>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import {toast} from 'bulma-toast'
import { makeSlug } from '@/utils/slugmaker'
import ListCategory from '@/components/ListCategory'
import PostTopping from '@/components/PostTopping'

export default {
    data(){
        return{
            cName:''
        }
    },
    components:{
        ListCategory,
        PostTopping
    },
    mounted(){
        document.title = 'Input Product'+' | admin mammamia'
    },
    computed: {
        slug: function() {
            var slug = makeSlug(this.cName);
            return slug;
        }
    },
    watch:{
        cName(){
            this.cName = this.cName.charAt(0).toUpperCase() + this.cName.slice(1)
        }
    },
    methods:{
        async categoryForm(){
            const categoryData = JSON.stringify({
                name : this.cName,
                slug : this.slug
            });
            const token = localStorage.getItem('token')
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+token
            };
                await axios
                    .post('/api/v1/category/post', categoryData, {headers})
                    .then(response=>{
                        if (!response) {
                            toast({
                                message: 'Gagal Membuat Kategori',
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
                                message: 'Kategori Berhasil Dibuat',
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
                                message: 'Gagal Membuat Kategori',
                                type: 'is-danger',
                                dismissible: true,
                                pauseOnHover: true,
                                duration: 5000,
                                position: 'top-right',
                            })
                        }
                    });
        },
    }
}
</script>

<style lang="scss">
@import '~bulma/css/bulma.css';
</style>