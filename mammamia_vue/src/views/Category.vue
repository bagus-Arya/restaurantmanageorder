<template>
    <div class="container">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h2 class="is-size-2 has-text-centered">
                    {{ category.name }}
                </h2>
            </div>
            <ProductBox
            v-for="product in category.products"
            v-bind:key="product.id"
            v-bind:product="product" />
        </div>
    </div>
</template>


<script>
import axios from 'axios'
import {toast} from 'bulma-toast'
import ProductBox from '../components/ProductBox.vue'

export default {
    name:'Category',
    data(){
        return{
            category:{
                products: []
            }
        }
    },
    components:{
        ProductBox
    },
    mounted(){
        this.getCategory()
    },
    watch:{
        $route(to, from){
            if(to.name == 'Category'){
                this.getCategory()
            }
        }
    },
    methods:{
        async getCategory(){
            const categorySlug = this.$route.params.category_slug
            const token = localStorage.getItem('token')
            const decodeValueTkn = atob(token);
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+decodeValueTkn
            };
            this.$store.commit('setIsLoading', true)
            await axios
                .get(`/api/v1/products/${categorySlug}/`, {headers})
                .then(response => {
                    this.category = response.data
                    document.title =  this.category.name +' | mammamia'
                })
                .catch(error => {
                     if (this.$store.state.isAuthenticated === true) {
                        toast({
                            message: 'No Data Found',
                            type: 'is-danger',
                            dismissible: true,
                            pauseOnHover: true,
                            duration:2000,
                            position: 'bottom-right'
                        })
                    }else{
                        toast({
                            message: 'Login Dulu Ya',
                            type: 'is-danger',
                            dismissible: true,
                            pauseOnHover: true,
                            duration:2000,
                            position: 'center'
                        })
                    }
                })
            this.$store.commit('setIsLoading', false)
        }
    }
}
</script>

