import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const state = {
    currentUser: '', // Current logged in user
    currentPassword: '', // Current password of the logged in user
    currentRank: { level: 'n/a', exp: 0, exp_threshold: 0 }, // Current rank of the logged user
    currentStats: { id: 'n/a', streak: 0, daily_training_score: 0, training_completion_date: 'n/a'}, // Current stats of the logged in user
    currentAchievements: [], // The achievements of the logged in user.
    currentRecentCatScores: {"Driving Off": [], "Urban Driving": [], "Rural Driving": [], "Bigger Roads": [], "Motorways": [], "Tricky Conditions": [], "Breakdowns": []},
    currentSocialLists: {friends: [], friend_requests: []}, // Friends and friend requests of the current user
    currentLeaderboards: {public: [], friends: []}, // Public and friend leaderbaords
    currentClientSocket: null // Socket of connected client
}

export default new Vuex.Store({
    // Vuex for vue states, to be saved and referenced later.
    state,
    mutations: {
        setCurrentUser(state, user) {
            state.currentUser = user;
        },

        setCurrentPassword(state, password) {
            state.currentPassword = password;
        },

        setCurrentRank(state, rank) {
            state.currentRank = rank;
        },

        setCurrentStats(state, stats) {
            state.currentStats = stats;
        },

        setCurrentAchievements(state, achievements) {
            state.currentAchievements = achievements;
        },

        setCurrentRecentCatScores(state, recentCatScores) {
            state.currentRecentCatScores = recentCatScores
        },

        setCurrentSocialLists(state, lists) {
            state.currentSocialLists = lists;
        },

        setCurrentLeaderboards(state, leaderboards) {
            state.currentLeaderboards = leaderboards;
        },

        setCurrentClientSocket(state, clientSocket) {
            state.currentClientSocket = clientSocket;
        }
    },
})