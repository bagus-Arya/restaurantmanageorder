<template>
    <div class="page-log-in">
        <div class="column is-4 is-offset-4">
            <h1 class="title">Login</h1>
            <form @submit.prevent='submitForm'>
                <div class="field">
                    <label for="">Username</label>
                    <div class="control">
                        <input type="text" class="input" v-model="username">
                    </div>
                </div>
                <div class="field">
                    <label for="">Password</label>
                    <div class="control">
                        <input type="password" class="input" v-model="password">
                    </div>
                </div>
                <div class="notification is-danger" v-if="errors.length">
                    <p v-for="error in errors" v-bind:key="error">{{ error}}</p>
                </div>
                <div class="field">
                    <div class="control">
                        <button class="button is-dark">Log in</button>
                    </div>
                </div>
                <hr>
                or <router-link to='/sign-up'>Sign up</router-link> if you don't have an account

            </form>

        </div>
    </div>
    
</template>

<script>
import axios from 'axios'
export default {
    name:'Login',
    data(){
        return{
            username: '',
            password: '',
            errors: [],
        }
    },
    mounted(){
        document.title = 'Login | Mammamia'
    }
    
}
</script>
