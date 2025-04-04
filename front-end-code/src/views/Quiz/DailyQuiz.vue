<template>
    <div class="container">
        <h1 class="title">DAILY QUIZ | {{ logged_in_user }}</h1>

        <div v-if="current_view === 'instructions'">
            <div class="instruction-box"> 
                <p> This is your daily training session. </p>
                <p> 1: Start with practicing 10 road signs to warm up. </p>
                <p> 2: Proceed with regular 10 multiple choice questions. </p>
                <p> 3: 3 Hazard Perception clips to practice on. </p>
            </div>

            <div class="buttons">
                <button @click="next_page('dashboard')">Back</button>
                <button @click="init_multiple_choice()">Start</button>
            </div>
        </div>

        <div v-if="current_view === 'road_sign'">

        </div>

        <div v-if="current_view === 'multiple_choice'">

        </div>

        <div v-if="current_view === 'hazard_perception'">

        </div>

        <p v-if="message.error" class="error-message">{{ message.error }}</p>
        <p v-if="message.success" class="success-message">{{ message.success }}</p>
    </div>
</template>
  
<script>
import toastr from 'toastr';
const images = require.context('@/assets/questions/.', false, /\.(jpg|jpeg|png)$/);
export default {
    // Page member variables and methods:
    name: "dailyquiz",
    data() {
        return {
            current_view: 'instructions', // State of quiz page

            // 10 Road Sign Questions

            // 10 Multiple Choice Questions

            // 3 Hazard Perception Clips

            logged_in_user: this.$store.state.currentUser,
            message: { error: "", success: "" },
        };
    },
    methods: {
        toggle_view(view) {
            // Reset state
            this.message.error = "";
            this.message.success = "";
            this.state.current_view = view;
        },
        async add_achievement(name) {
            // Add achievement to user's achievements and notify on the UI.
            this.achievements.push(name)

            // Update database
            const input = { 'id': user_stats.id, 'updates': { 'achievements': this.achievements } }
            const update = await this.azure_function("PUT", "/user/update/info", input)
            if (update) {
                this.$store.commit("setCurrentAchievements", this.achievements);
                this.message.success = 'Achievements update Successful!'

                const options = { "closeButton": true, "debug": false, "newestOnTop": true, "progressBar": true,
                "positionClass": "toast-top-right", "preventDuplicates": true, "onclick": null, "showDuration": "300",
                "hideDuration": "1000", "timeOut": "5000", "extendedTimeOut": "1000", "showEasing": "swing",
                "hideEasing": "linear", "showMethod": "fadeIn","hideMethod": "fadeOut"}

                toastr.success('"' + `/${name}` + '""',"Achievement Unlocked:", options)
            }
        },
        async azure_function(function_type, function_route, json_doc) {
            console.log(function_route);
            // Call Azure function with request
            try {
                const url = process.env.VUE_APP_BACKEND_URL + function_route + '?code=' + process.env.VUE_APP_MASTER_KEY
                
                if (function_type === "GET") {
                    const response = await fetch( url, { method: function_type, headers: { "Content-Type": "application/json"} });
                    const API_reply = await response.json();
                    console.log("Result: " + JSON.stringify(API_reply.result));
                    return API_reply
                } else {
                    const response = await fetch( url, { method: function_type, headers: { "Content-Type": "application/json"},body: JSON.stringify(json_doc)});
                    const API_reply = await response.json();
                    console.log("Result: " + JSON.stringify(API_reply.result));
                    return API_reply
                }

            } catch (error) {
                console.error("Error:", error);
                this.message.error = "An API error occurred. Please try again later.";
            }
        },
        next_page(page) {
            console.log("/" + page);
            this.$router.push(`/${page}`);
        }
    },
};
</script>

<style lang="scss" scoped>
.instruction-box {
  background-color: #f9f9f9;
  border-left: 5px solid #007bff;
  padding: 10px;
  margin: 10px 0;
  font-size: 14px;
  color: #333;
  border-radius: 5px;
}
</style>