<template>
    <div class="container">
        <div class="questionnaire">
            <!-- LOADING SCREEN FOR FEEDBACK -->
            <div v-if="state.current_view === 'loading'" class="quiz-result">
                <h1>Loading ...</h1>
            </div>
            <!-- ACTUAL FEEDBACK PAGE -->
            <div v-if="state.current_view === 'feedback'">
                <h2>Feedback {{ current_Q + 1 }} of {{ state.feedback.length }}</h2>
                <div class="progress-bar">
                    <div class="progress-fill" :style="{ width: progressBarWidth + '%' }"></div>
                </div>
                <div class="question-container">
                    <div class="question-text">
                        <h1>{{ state.feedback[current_Q].question }}</h1>
                    </div>
                    <div class="question-image" v-if="input[current_Q].image !== 'n/a'">
                        <img :src="image" alt="Question Image">
                    </div>
                </div>
                <div class="feedback-box">
                    <div class="answer-row">
                        <p class="incorrect">{{ input[current_Q].selected }}❌</p>
                        <p class="correct">{{ input[current_Q].correct }}✔️</p>
                    </div>
                    <div class="feedback-text">
                        <h3>{{ state.feedback[current_Q].feedback }}</h3>
                    </div>
                </div>
                <div class="game-buttons">
                    <button 
                        class="game-button" @click="prev_feedback()" 
                        :disabled="current_Q === 0">Previous
                    </button>
                    <button 
                        class="game-button" @click="next_feedback()" 
                        :disabled="current_Q === state.feedback.length - 1">Next
                    </button>
                    <button 
                        class="game-button" @click="next_page('dashboard')"
                        :disabled="current_Q < state.feedback.length - 1">Finish
                    </button>
                </div>
            </div>
        </div>
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
                const { image, explanation, ...rest } = item; // Destructure to remove the 'author' property
                return rest; // Return the rest of the object
            });
            console.log(new_input);
            
            try {
                const feedback = await this.azure_function('POST', '/question/get/feedback', {incorrect_answers: new_input});
                if (feedback.result) {
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
            } catch (error) {
                console.log('Unable to generate, using the explanation as a substitute feedback.');
                this.state.feedback = this.input.map(({ image, explanation, ...rest }) => ({
                    feedback: explanation,
                    ...rest
                }));
                this.add_image();
                this.toggle_view('feedback');
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
    computed: {
        progressBarWidth() {
        return (this.current_Q / (this.state.feedback.length - 1)) * 100;
    }
  },
};
</script>

<style lang="scss" scoped>
.feedback-box {
    color: #ffffff;
    background-color: black;
    border: 2px solid #f3af59;
    width: 100%;
    max-width: 1400px;
    height: 180px;
    padding: 20px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 10px;
}

.answer-row {
    font-size: 1.1rem;
    display: flex;
    justify-content: space-between;
    gap: 40px;
}

.feedback-box p.correct {
    color: #5bd45f;
}

.feedback-box p.incorrect {
    color: #e34242;
}

.feedback-text {
    padding-top: 10px;
}

h1 {
    color: white;
}

</style>