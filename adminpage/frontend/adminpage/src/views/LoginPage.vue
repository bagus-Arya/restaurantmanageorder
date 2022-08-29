<template>
    <div class="hero is-fullheight is-info">
        <div class="hero-body">
            <div class="container has-text-centered">
                <div class="column is-8 is-offset-2">
                    <h3 class="title has-text-white">
                        Admin Mamma Mia Renon
                    </h3>
                    <hr class="login-hr">
                    <p class="subtitle has-text-white">We Serve An Authentic Food</p>
                    <div class="box columns is-1-mobile is-0-tablet is-3-desktop">
                        <div class="column">
                            <img src="@/assets/logo_mammamia.png" alt="logo-mammamia" style="width:195px;"/>
                        </div>
                        <div class="column">
                            <form @submit.prevent='loginForm'>
                                <div class="field">
                                    <div class="control">
                                        <input class="input is-large" type="text" placeholder="Username" autofocus="" v-model="username"/>
                                    </div>
                                </div>

                                <div class="field">
                                    <div class="control">
                                        <input class="input is-large" type="password" placeholder="Password" autofocus="" v-model="password"/>
                                    </div>
                                </div>
                                <button class="button is-block is-danger is-large is-fullwidth is-responsive">Login</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>
  
</template>

<script>
import axios from 'axios'
import {toast} from 'bulma-toast'

export default {
    data(){
        return{
            username: '',
            password: ''
        }
    },
    mounted(){
        document.title = 'Admin | Login'
    },
    methods:{
        async loginForm(){
            axios.defaults.headers.common['Authorization'] = ''
            localStorage.removeItem('token')
            const formData = {
                username : this.username,
                password : this.password
            }
            await axios
                .post('/api/v1/usr/admin-login/', formData)
                .then(response =>{
                    if (response.data.status) {
                        toast({
                            message: response.data.status,
                            type: 'is-danger',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 5000,
                            position: 'center',
                        })
                        this.$router.go() 
                    } else {
                        const token = response.data.auth_token
                        const dataActive = {
                            isActivateIndex : true,
                            isActivateStatistik : false,
                            isActivateTransaksi : false,
                            isActivateRiwayat : false
                        }
                        this.$store.commit('setIndex', dataActive)
                        this.$store.commit('setToken', token)
                        axios.defaults.headers.common['Authorization'] = 'Token '+token
                        localStorage.setItem('token', token)
                            toast({
                                message: 'Berhasil Masuk',
                                type: 'is-success',
                                dismissible: true,
                                pauseOnHover: true,
                                duration: 5000,
                                position: 'top-right',
                            })
                        const toPath = this.$route.query.to || '/index'
                        this.$router.push(toPath)
                    }
                })
                .catch(error => {
                    if (error) {
                        toast({
                            message: 'Username atau Password Salah',
                            type: 'is-danger',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 5000,
                            position: 'top-right',
                        })
                        this.$router.go() 
                    }
                })  
        },
    }
    
}
</script>

<style>

</style>
