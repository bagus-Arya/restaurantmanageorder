<template>
    <div v-if="asyncDataLogin_readys">
        <div class="container-fluid">
            <div class="main-content columns is-fullheight">
                <SidebarAdmins/>  
                <post-product/>
            </div>
            <AppFooter/>
        </div>
    </div>
</template>

<script>
import SidebarAdmins from '@/components/SideBarAdmin'
import AppFooter from '@/components/AppFooter'
import PostProduct from '@/components/PostProduct'
import asyncDataLogin from '@/mixins/asyncDataLogin'

export default {
    mixins: [asyncDataLogin],
    components: {
      SidebarAdmins,
      AppFooter,
      PostProduct
    },
}
</script>

<style lang="scss">
@import '~bulma/css/bulma.css';

</style>