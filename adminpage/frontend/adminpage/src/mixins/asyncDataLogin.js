export default {
    data () {
        return {
            asyncDataLogin_readys: this.asyncDataLogin_ready()
        }
    },
    methods: {
      asyncDataLogin_ready() {
        const token = localStorage.getItem('token')
            if (token) {
                return true
            } else {
                this.$router.push({name:'LoginPage'})
            }
        }
    }
}