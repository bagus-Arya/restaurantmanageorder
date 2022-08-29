<template>
    <div class="container">
        <div class="box column is-12 is-1-mobile is-0-tablet">
            <AppNavAkun/>
            <hr>
            <form>
                <div class="columns">
                    <div class="column">
                        <div class="field">
                            <div class="control">
                                <label for="">Nama Pengguna</label>
                                <input type="hidden" 
                                    v-bind:value="ids"
                                    v-on:input="ids = $event.target.value">
                                <input v-bind:value="userMe.username"
                                    v-on:input="username = $event.target.value"
                                    class="input is-large" type="text" disabled>
                            </div>
                        </div>
                        <div class="field">
                            <div class="control">
                                <label for="">Nama Depan</label>
                                <input  v-bind:value="nama_depan"
                                    v-on:input="nama_depan = $event.target.value"
                                    class="input is-large" 
                                    type="text" 
                                    autofocus="">
                            </div>
                        </div>
                        <div class="field">
                            <div class="control">
                                <label for="">Nomor Hp</label>
                                <input v-bind:value="hp"
                                    v-on:input="hp = $event.target.value"
                                    class="input is-large" type="text" autofocus="">
                            </div>
                        </div>
                    </div>
                    <div class="column">
                        <div class="field">
                            <div class="control">
                                <label for="">Nama Belakang</label>
                                <input v-bind:value="nama_belakang"
                                    v-on:input="nama_belakang = $event.target.value"
                                    class="input is-large" type="text" autofocus="">
                            </div>
                        </div>
                        <div class="field">
                            <div class="control">
                                <label for="">Jenis Kelamin</label>
                                <input v-bind:value="jenis_kelamin"
                                    v-on:input="jenis_kelamin = $event.target.value"  
                                    class="input is-large" type="text" autofocus="">
                            </div>
                        </div>
                        <div class="field">
                            <div class="control">
                                <label for="">Alamat</label>
                                <textarea 
                                    v-bind:value="alamat"
                                    v-on:input="alamat = $event.target.value"
                                    class="textarea" cols="75" rows="2"></textarea>
                            </div>
                        </div>
                    </div>
                </div>
                <button v-if="ids" class="button is-block is-danger is-large is-fullwidth" type="submit" @click.prevent='updateUserDetail'>Update Data</button>
                <button v-else class="button is-block is-danger is-large is-fullwidth" type="submit" @click.prevent='postUserDetail'>Simpan Data</button>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import {toast} from 'bulma-toast'
import AppNavAkun from '@/components/AppNavAkun'

export default {
    name: 'MyAccount',
    components: {
        AppNavAkun,
    },
    data(){
        return{
            user_detail:{},
            userMe:{},
            ids:null, 
            username:null, 
            nama_depan:null,
            nama_belakang:null,
            jenis_kelamin:null,
            hp:null,
            alamat:null,
        }
    },
    mounted(){
        this.getUserDetail()
        this.getUserMe()
        
        document.title = 'Akun'+ ' | Mammamia Renon'
    },
    created(){
        this.getUserDetail()
    },
    methods:{
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
                    this.user_detail = response.data;
                        if (response.data[0]) {
                            this.ids = response.data[0].user_id; 
                            this.username = response.data[0].username; 
                            this.nama_depan = response.data[0].nama_depan;
                            this.nama_belakang = response.data[0].nama_belakang;
                            this.jenis_kelamin = response.data[0].jenis_kelamin;
                            this.hp = response.data[0].hp;
                            this.alamat = response.data[0].alamat;
                        }
                    })
                .catch(error => {console.log(error)})

        },
        async getUserMe(){
            const token = localStorage.getItem('token')
            const decodeValueTkn = atob(token);
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+decodeValueTkn
            };
            await axios
            .get('/api/v1/users/me', {headers})
            .then(response =>{ 
                this.userMe = response.data
            }).catch(error => {console.log(error)})

        },
        async updateUserDetail(){
            const token = localStorage.getItem('token')
            const uIds = localStorage.getItem('uid')
            const decodeValueTkn = atob(token);
            const decodeValueId = atob(uIds);
            const dtId = this.ids;
            const userDetail = {
                user:decodeValueId, 
                id:this.ids, 
                nama_depan:this.nama_depan,
                nama_belakang:this.nama_belakang,
                jenis_kelamin:this.jenis_kelamin,
                hp:this.hp,
                alamat:this.alamat,
            };
            console.log(JSON.stringify(userDetail))
            const headers = { 
                'accept': 'application/json',
                'Authorization':'Token '+decodeValueTkn,
            };
                await axios
                    .put(`/api/v1/usr/update/${dtId}/`, userDetail, {headers})
                    .then(response=>{
                        if (!response) {
                            toast({
                                message: 'Galat',
                                type: 'is-danger',
                                dismissible: true,
                                pauseOnHover: true,
                                duration: 5000,
                                position: 'top-right',
                            })
                            return response
                        } else {
                            toast({
                                message: 'Data Berhasil Diperbaharui',
                                type: 'is-success',
                                dismissible: true,
                                pauseOnHover: true,
                                duration: 5000,
                                position: 'top-right',
                            })
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
                            this.errors.push('Something went wrong, please try again')
                            console.log(JSON.stringify(error))
                        }
                    });
        },
        async postUserDetail(){
            const token = localStorage.getItem('token')
            const uIds = localStorage.getItem('uid')
            const decodeValueTkn = atob(token);
            const decodeValueId = atob(uIds);
            const dtId = this.ids;
            const userDetail = {
                user:decodeValueId, 
                id:this.ids, 
                nama_depan:this.nama_depan,
                nama_belakang:this.nama_belakang,
                jenis_kelamin:this.jenis_kelamin,
                hp:this.hp,
                alamat:this.alamat,
            };
            console.log(JSON.stringify(userDetail))
            const headers = { 
                'accept': 'application/json',
                'Authorization':'Token '+decodeValueTkn,
            };
                await axios
                    .post('/api/v1/usr/post-detail/', userDetail, {headers})
                    .then(response=>{
                        if (!response) {
                            toast({
                                message: 'Galat',
                                type: 'is-danger',
                                dismissible: true,
                                pauseOnHover: true,
                                duration: 5000,
                                position: 'top-right',
                            })
                            return response
                        } else {
                            toast({
                                message: 'Data Berhasil Diperbaharui',
                                type: 'is-success',
                                dismissible: true,
                                pauseOnHover: true,
                                duration: 5000,
                                position: 'top-right',
                            })
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
                            this.errors.push('Something went wrong, please try again')
                            console.log(JSON.stringify(error))
                        }
                    });
        },
    },
}
</script>
