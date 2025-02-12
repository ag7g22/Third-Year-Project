import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const state = {
    currentUser: '', // Current logged in user
    currentPassword: '', // Current password of the logged in user
    currentStats: { id: 'n/a', streak: 0, daily_training_score: 0, training_completion_date: 'n/a'} // Current stats of the logged in user
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

        setCurrentStats(state, stats) {
            state.currentStats = stats
        }
    },
})