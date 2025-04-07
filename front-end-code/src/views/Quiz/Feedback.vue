<template>
    <div class="p-6 bg-gray-100 rounded-2xl shadow-lg max-w-xl mx-auto">
        <h1 class="text-2xl font-bold text-gray-800">FEEDBACK | {{ logged_in_user }}</h1>

        <!-- LOADING SCREEN FOR FEEDBACK -->
        <div v-if="state.current_view === 'loading'">
            <p class="text-gray-500">LOADING FEEDBACK ...</p>
            <button @click="next_page('dashboard')">Finish</button>
        </div>

        <!-- ACTUAL FEEDBACK PAGE -->
        <div v-if="state.current_view === 'feedback'">
            <div class="feedback">
                <h2>{{ state.feedback[current_Q].question }}</h2>

                <div v-if="input[current_Q].image !== 'n/a'">
                    <img :src=image alt="Question Image">
                </div> 

                <p>YOU SELECTED: {{ input[current_Q].selected }}</p>
                <p>CORRECT ANSWER: {{ input[current_Q].correct }}</p>

                <h3>{{ state.feedback[current_Q].feedback }}</h3>

                <div class="mt-4 flex justify-between">
                    <button 
                        @click="prev_feedback()" 
                        class="px-4 py-2 rounded-lg text-white" 
                        :class="{ 'bg-gray-400': current_Q === 0, 'bg-blue-600 hover:bg-blue-700': current_Q > 0 }" 
                        :disabled="current_Q === 0"
                    >Previous</button>
                    <button 
                        @click="next_feedback()" 
                        class="px-4 py-2 rounded-lg text-white" 
                        :class="{ 'bg-gray-400': current_Q === state.feedback.length - 1, 'bg-blue-600 hover:bg-blue-700': current_Q < state.feedback.length - 1 }" 
                        :disabled="current_Q === state.feedback.length - 1"
                    >Next</button>
                </div>
            </div>
            <button @click="next_page('dashboard')">Finish</button>
        </div>

        <p v-if="message.error" class="mt-2 text-red-500">{{ message.error }}</p>
        <p v-if="message.success" class="mt-2 text-green-500">{{ message.success }}</p>
    </div>
</template>
  
<script>
import toastr from 'toastr';
const images = require.context('@/assets/questions/.', false, /\.(jpg|jpeg|png)$/);
export default {
    // Page member variables and methods:
    name: "feedback",
    mounted() {
        // Set up input to send to openai model
        this.input = this.$route.query.input || [];
        this.get_feedback();
    },
    data() {
        return {
            // The views and feedback:
            input: [], // Input for API
            state: { current_view: 'loading', feedback: []},
            current_Q: 0,

            // Images
            images: images.keys().map(image => images(image)),
            image: "",

            logged_in_user: this.$store.state.currentUser,
            message: { error: "", success: "" },
        };
    },
    methods: {
        toggle_view(view) {
            // Reset state
            this.message = { error: "", success: "" };
            this.state.current_view = view;
        },
        async get_feedback() {
            // Get feedback from API:
            const new_input = this.input.map(item => {
                const { image, ...rest } = item; // Destructure to remove the 'author' property
                return rest; // Return the rest of the object
            });

            console.log(new_input);

            const feedback = await this.azure_function('POST', '/question/get/feedback', {incorrect_answers: new_input});
            if (feedback.result) {
                this.message.success = 'Loading feedback successful!';
                this.state.feedback = JSON.parse(feedback.msg);

                console.log('Is array:', Array.isArray(this.state.feedback));
                console.log('Type:', typeof this.state.feedback);

                console.log(this.state.feedback);
                console.log(this.state.feedback[this.current_Q]);

                this.add_image();

                this.toggle_view('feedback');
            } else {
                this.message.error = feedback.msg || "Loading feedback failed."
            }
        },
        next_feedback() {
            this.current_Q++;
            this.add_image();
        },
        prev_feedback() {
            this.current_Q--;
            this.add_image();
        },
        add_image() {
            // Library of images
            let question_image = this.input[this.current_Q].image
            if (question_image !== 'n/a') {
                this.image = this.images.filter((image, index) => images.keys()[index].includes(question_image))[0];
            }
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
            this.input = [];
            this.state = { current_view: 'loading', feedback: []};
            this.current_Q = 0;
            this.image = "";
            this.message = { error: "", success: "" };
            console.log("/" + page);
            this.$router.push(`/${page}`);
        }
    },
};
</script>

<style lang="scss" scoped>
img {
  max-width: 300px; /* Limits the width to 200px */
  max-height: 200px; /* Limits the height to 100px */
  width: auto; /* Maintain aspect ratio */
  height: auto; /* Maintain aspect ratio */
}

.feedback {
  text-align: center;
  max-width: 600px;
  margin: auto;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  background: #f9f9f9;
}
</style>