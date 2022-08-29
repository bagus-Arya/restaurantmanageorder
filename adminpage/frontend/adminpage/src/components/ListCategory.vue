<template>
    <div class="mb-5">
        <h1 class="title">List Kategori:</h1>
        <div class="box column is-12 is-1-mobile is-0-tablet mt-2 ml-1">
            <table class="table is-fullwidth">
                <thead>
                    <tr class="has-text-left">
                        <th>Nama Kategori</th>
                        <th>Aksi</th>
                    </tr>
                </thead>
                <tbody>
                    <tr
                        class="has-text-left"
                        v-for="item in categoryList.lists"
                        v-bind:key="item.id"
                    >   
                        <td>{{item.name}}</td>
                        <td>
                            <button class="button is-danger is-outlined is-rounded is-small"
                            @click="removeCategory(item)">
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

export default {
    data(){
        return{
            categoryList: {
                lists: []
            },
        }
    },
    mounted(){
        document.title = 'Input Product'+' | admin mammamia'
    },
    created(){
        this.getAllCategoryLists()
    },
    methods: {
        async getAllCategoryLists(){
            const token = localStorage.getItem('token')
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+token
            };
            await axios.get('/api/v1/category/lists/', {headers})
                .then(response => {
                        this.categoryList.lists = response.data
                    })
                .catch(error => {console.log(error)})
        },
        async removeCategory(item){
            const token = localStorage.getItem('token')
            var id_category = parseInt(item.id)
            const headers = { 
                'Content-Type': 'application/json',
                'Authorization':'Token '+token
            };
            await axios.delete(`/api/v1/category-delete/${id_category}`,{headers})
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