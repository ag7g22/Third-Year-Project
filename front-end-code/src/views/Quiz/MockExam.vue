<template>
    <div class="container">

        <div v-if="current_view === 'instructions'">
            <h1 class="title">MOCK EXAM | {{ logged_in_user }}</h1>
            <div class="instruction-box"> 
                <p> These tests are timed, like the actual exam. </p>
                <p> The exam is split into two sections; Multiple choice and Hazard Perception. </p>
                <p> 1: 50 multiple questions selected at random. </p>
                <p> 2: 14 video clips containing developing hazards. </p>
                <p> You have 1 hour to answer the multiple choice, and each clip is a minute long. </p>
            </div>

            <div class="buttons">
                <button @click="next_page('dashboard')">Back</button>
                <button @click="init_questions()">Start</button>
            </div>
        </div>

        <div v-if="current_view === 'multiple_choice'">
            <h1 class="title">MOCK EXAM | {{ logged_in_user }}</h1>
            <div v-if="timer_finished" class="overlay">
                <div class="overlay-content" @click.stop>
                    <p>You've ran out of time.</p>
                    <button @click="terminate_mock_exam()">End Exam</button>
                    <button @click="toggle_view('hazard_perception')">Next</button>
                </div>
            </div>

            <h2>{{ formattedTime }}</h2>
            <button @click="terminate_mock_exam()">End Exam</button>
        </div>

        <div v-if="current_view === 'hazard_perception'">
            <div v-if="too_many_clicks" class="overlay">
                <div class="overlay-content" @click.stop>
                    <p>You've clicked too many times.</p>
                    <button @click="toggle_view('score')">Next</button>
                </div>
            </div>

            <button @click="terminate_mock_exam()">End Exam</button>
        </div>

        <div v-if="current_view === 'score'">
            <button @click="terminate_mock_exam()">End Exam</button>
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
    name: "mockexam",
    data() {
        return {
            current_view: 'instructions', // State of quiz page

            // Timer
            timeLeft: 60 * 60, // 60 minutes in seconds
            timer: null,
            timer_finished: false,

            // Multiple Choice Questions
            questions: [], // {question, topic, image, correct_answer, options, selected_ans, flagged}
            current_Q: 0, // Question pointer
            scores_1: 0, // Score for questions

            // Images
            images: images.keys().map(image => images(image)),
            image: "",

            // Hazard Perception Clips
            clips: [], // {name, x, y, time}
            current_C: 0, // Clip pointer
            scores_2: 0, // Scores for clips

            // Clicking the video
            click_x: 0,
            click_y: 0,
            click_time: 0,
            click_history: [],
            clicks: [],
            too_many_clicks: false,

            feedback: [],
            // {question, correct_ans, selected_ans, image}

            logged_in_user: this.$store.state.currentUser,
            message: { error: "", success: "" },
        };
    },
    methods: {
        toggle_view(view) {
            // Reset state
            this.message = { error: "", success: "" };
            this.current_view = view;
        },
        async init_questions() {
            // Set up the questions
            this.message = { error: "", success: "" };
            this.message.success = 'LOADING QUESTIONS ...';

            // Fetch the multiple choice questions:
            const input = { 'No_of_Qs': 50, 'username': this.logged_in_user };
            const quiz = await this.azure_function('POST', '/question/get/quiz', input);
            if (quiz.result) {
                // Populate the questions list, and add a flag to them and remove explanation attr.
                this.questions = quiz.msg;
                this.questions.forEach(item => {
                    item.flagged = false;
                    delete item.explanation;
                });
                this.init_clips();
            } else {
                this.message.error = quiz.msg || 'LOADING QUIZ FAILED.'
            }
        },
        async init_clips() {
            // Set up the clips
            this.message = { error: "", success: "" };
            this.message.success = 'SELECTING HAZARD PERCEPTION CLIPS';

            // Fetch the 14 clips:
            const dictList = [
                {name: 'Urban Driving 1', x: 370, y: 270, time: 15.25}, {name: 'Urban Driving 2', x: 540, y: 270, time: 18.00}, {name: 'Urban Driving 3', x: 410, y: 260, time: 29.00}, {name: 'Urban Driving 4', x: 415, y: 260, time: 37.60}, {name: 'Urban Driving 5', x: 350, y: 260, time: 29.00}, {name: 'Rural Driving 1', x: 490, y: 220, time: 47.00},
                {name: 'Rural Driving 2', x: 250, y: 250, time: 31.00}, {name: 'Rural Driving 3', x: 395, y: 230, time: 17.50}, {name: 'Rural Driving 4', x: 450, y: 290, time: 13.45}, {name: 'Rural Driving 5', x: 295, y: 240, time: 37.85}, {name: 'Bigger Roads 1', x: 415, y: 250, time: 13.90}, {name: 'Bigger Roads 2', x: 425, y: 240, time: 14.55},
                {name: 'Bigger Roads 3', x: 510, y: 260, time: 26.30}, {name: 'Bigger Roads 4', x: 500, y: 245, time: 21.45}, {name: 'Motorways 1', x: 25, y: 190, time: 2.55}, {name: 'Motorways 2', x: 320, y: 250, time: 25.45}, {name: 'Motorways 3', x: 690, y: 290, time: 30.20}, {name: 'Tricky Conditions 1', x: 110, y: 250, time: 17.10},
                {name: 'Tricky Conditions 2', x: 515, y: 240, time: 31.80}, {name: 'Tricky Conditions 3', x: 280, y: 254, time: 33.45}, {name: 'Tricky Conditions 4', x: 325, y: 235, time: 22.70}, {name: 'Tricky Conditions 5', x: 320, y: 255, time: 24.00}
            ];
            // Shuffle and select random clips
            this.clips = dictList
                .sort(() => 0.5 - Math.random())  // Randomly shuffle
                .slice(0, 14);           // Select the first 14 clips
            
            this.message.success = 'LOADING HAZARD PERCEPTION CLIPS';
            this.clips.forEach(async item => {
                const input = {'filename': item.name + ".mp4"};
                const video = await this.azure_function('POST', '/question/get/video', input);
                if (video.result) {
                    // Set the playing video
                    item.url = video.msg;
                    console.log(video.msg);
                }
            });
            this.message.success = 'LOADING SUCCESS';
            this.toggle_view('multiple_choice');
            this.startTimer();
        },
        startTimer() {
            this.timer = setInterval(() => {
                if (this.timeLeft > 0) {
                    this.timeLeft--;
                } else {
                    clearInterval(this.timer);
                    this.timer_finished = true;
                }
            }, 1000);
        },
        add_image() {
            // Library of images
            let question_image = this.questions[this.currentQuestion].image
            if (question_image !== 'n/a') {
                this.image = this.images.filter((image, index) => images.keys()[index].includes(question_image))[0];
            }
        },
        async terminate_mock_exam() {
            // Reset states
            this.timeLeft = 60 * 60; // 60 minutes in seconds
            this.timer = null;
            this.questions = [];
            this.current_Q = 0;
            this.scores_1 = 0;
            this.timer_finished = false;
            this.image = "";
            this.clips = [];
            this.current_C = 0;
            this.scores_2 = 0;
            this.click_x = 0;
            this.click_y = 0;
            this.click_time = 0;
            this.click_history = [];
            this.clicks = [];
            this.too_many_clicks = false;
            this.feedback = [];
            this.message = { error: "", success: "" };
            this.toggle_view('instructions');
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
    computed: {
    formattedTime() {
      const minutes = String(Math.floor(this.timeLeft / 60)).padStart(2, '0');
      const seconds = String(this.timeLeft % 60).padStart(2, '0');
      return `${minutes}:${seconds}`;
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

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7); /* Semi-transparent background */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

/* Centered box but slightly above the middle */
.overlay-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  width: 80%;
  max-width: 400px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}

</style>