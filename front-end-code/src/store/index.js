import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const state = {
    currentUser: '',
    currentPassword: '',
}

export default new Vuex.Store({
    // Vuex for vue states, to be saved and referenced later.
    state,
    mutations: {
        setCurrentUser(state, user) {
            state.currentUser = user
        },

        setCurrentPassword(state, password) {
            state.currentPassword = password
        },
    },
})