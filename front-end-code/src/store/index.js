import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const state = {
    user: '',
}

export default new Vuex.Store({
    // Vuex for vue states, to be saved and referenced later.
    state,
    mutations: {
        setUser(state, user) {
            state.user = user
        },
    },
})