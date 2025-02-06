import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const state = {
    user: '',
}

export default new Vuex.Store({
    state,
    mutations: {
        setUser(state, user) {
            state.user = user
        },
    },
})