<template>
    <div class="columns is-mobile">
        <div class="column is-4 is-offset-4">
            <h1 style="color:#E76F51;" class="is-size-4"><center>Daftar</center></h1>
            <form @submit.prevent='submitForm'>
                <div class="field">
                    <label style="color:#E76F51;" for="">Nama Pengguna</label>
                    <div class="control">
                        <input type="text" class="input" v-model="username">
                    </div>
                </div>
                <div class="field">
                    <label style="color:#E76F51;" for="">Password</label>
                    <div class="control">
                        <input type="password" class="input" v-model="password">
                    </div>
                </div>
                <div class="field">
                    <label style="color:#E76F51;" for="">Re-enter Password</label>
                    <div class="control">
                        <input type="password" class="input" v-model="password2">
                    </div>
                </div>
                <div class="notification is-danger" v-if="errors.length">
                    <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                    
                </div>
                <div class="field is-grouped is-grouped-centered">
                    <p class="control">
                        <button class="button is-primary">Daftar</button>
                    </p>
                    <p class="control">
                        <button @click='toHome' class="button is-primary">Home</button>
                    </p>
                </div>
                <hr>
                Sudah punya akun? <router-link to='/log-in'>Login</router-link> 
            </form>
        </div>
    </div>
</template>


<script>
import axios from 'axios'
import {toast} from 'bulma-toast'
export default {
    name: 'Signup',
    data(){
        return{
            username: '',
            password: '',
            password2: '',
            errors: [],

        }
    },
    watch:{
        username(newVal){
            this.username = this.username.toLowerCase()
        }
    },
    methods:{
        async submitForm(){
            // reset error
            this.errors = []

            // validate
            if(this.username === ''){
                this.errors.push('Nama Pengguna Wajib Diisi')
            }
            if(this.password === ''){
                this.errors.push('Password Wajib Diisi')
            }
            if(this.password != this.password2){
                this.errors.push('Password Tidak Cocok')
            }
            // if no errors
            if(!this.errors.length){
                const formData = {
                    username : this.username,
                    password : this.password

                }
                await axios
                    .post('/api/v1/users/', formData)
                    .then(response=>{
                        if (!response) {
                            const a = JSON.parse(JSON.stringify(response))
                            console.log(a)
                            toast({
                                message: 'Password Harus Unik',
                                type: 'is-warning',
                                dismissible: true,
                                pauseOnHover: true,
                                duration: 5000,
                                position: 'top-right',
                            }) 
                            this.$router.go()
                        }else{
                            toast({
                                message: 'Akun anda berhasil dibuat!',
                                type: 'is-success',
                                dismissible: true,
                                pauseOnHover: true,
                                duration: 5000,
                                position: 'top-right',
                            }) 
                        }
                    })
                    .catch(error=> {
                        if (error.response) {
                        // The request was made and the server responded with a status code
                        // that falls out of the range of 2xx
                        console.log(error.response.data);
                        console.log(error.response.status);
                        console.log(error.response.headers);
                        } else if (error.request) {
                        // The request was made but no response was received
                        // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
                        // http.ClientRequest in node.js
                        console.log(error.request);
                        } else {
                        // Something happened in setting up the request that triggered an Error
                        console.log('Error', error.message);
                        }
                        toast({
                            message: 'Username Harus Unik',
                            type: 'is-warning',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 5000,
                            position: 'top-right',
                        }) 
                        this.$router.go()
                        console.log(error.config);
                        // this.errors.push('Silahkan Buat Password yang Unik')
                        // const a = JSON.parse(JSON.stringify(error))
                        // console.log(a)
                    })
            }
        },
        toHome(){
            this.$router.push({name:'Home'})
        }
    },
    
    
}
</script>
