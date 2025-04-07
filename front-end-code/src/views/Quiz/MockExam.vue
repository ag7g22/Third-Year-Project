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
            <h1 class="title">MOCK EXAM | {{ formattedTime }}</h1>
            <div class="questionnaire">
                <p>Question {{ current_Q + 1 }} of {{ questions.length }}</p>

                <!-- Progress Bar -->
                <div class="progress-container">
                <div class="progress-bar" :style="{ width: progressBarWidth + '%' }"></div>
                </div>

                <h2>{{ questions[current_Q].question }}</h2>

                <div v-if="questions[current_Q].image !== 'n/a'">
                    <img :src=image alt="Question Image">
                </div>
                
                <button 
                    @click="toggle_flag"
                    :class="{ 'flagged': questions[current_Q].flagged }"
                    >
                    <span v-if="questions[current_Q].flagged">🚩 Unflag</span>
                    <span v-else>Flag</span>
                </button>

                <div class="options">
                    <button 
                    v-for="(option, index) in questions[current_Q].options"
                    :key="index"
                    :class="{
                        selected: questions[current_Q].selected_ans === option,
                    }"
                    @click="select_answer(option)"
                    >
                    {{ option }}
                    </button>
                </div>
                <button @click="terminate_mock_exam()">End Exam</button>
                <button v-if="current_Q !== 0" @click="prev_question()">Previous</button>
                <button v-if="questions[current_Q].selected_ans !== null" @click="next_question() && current_Q !== questions.length - 1">Next</button>
                <button v-if="current_Q === questions.length - 1 && questions[current_Q].selected_ans !== null" @click="start_hazard_perceptions()">Finish Section</button>
            </div>

            <div v-if="timer_finished" class="overlay">
                <div class="overlay-content" @click.stop>
                    <p>You've ran out of time.</p>
                    <button @click="terminate_mock_exam()">End Exam</button>
                    <button @click="start_hazard_perceptions()">Next</button>
                </div>
            </div>

            <!-- Floating Question Grid -->
            <div class="floating-grid">
                <div
                    v-for="(q, index) in questions"
                    :key="index"
                    class="grid-item"
                    :class="{
                    flagged: q.flagged,
                    answered: q.selected_ans !== null,
                    current: index === current_Q,
                    locked: index > current_Q && q.selected_ans === null
                    }"
                    @click="() => {
                    if (index <= current_Q || q.selected_ans !== null) jump_to_question(index);
                    }"
                    :title="index <= current_Q || q.selected_ans !== null ? 'Question ' + (index + 1) : 'Locked'"
                >
                    {{ index + 1 }}
                </div>
            </div>
        </div>

        <div v-if="current_view === 'hazard_perception'" class="video-container">

            <div v-if="clip_url === ''">
                <h2>LOADING VIDEO CLIP ...</h2>
            </div>
            <div v-else>
                <div>
                    <video ref="hazard_perception"
                        :src="clip_url"
                        @click="handleClick"
                        @ended="finish_video_clip"
                        autoplay 
                        muted 
                        playsinline 
                        width="800"
                        height="500">
                    </video>

                    <!-- Click Effect -->
                    <div 
                        v-for="(click, index) in clicks"
                        :key="index"
                        class="click-circle"
                        :style="{ top: (click.y - 10) + 'px', left: (click.x - 15) + 'px' }"
                    ></div>
                </div>
            </div>

            <div v-if="too_many_clicks" class="overlay">
                <div class="overlay-content" @click.stop>
                    <p>You've clicked too many times.</p>
                    <button @click="load_video_clip()">Next</button>
                </div>
            </div>

            <div class="horizontal-container">
                <div v-for="clicks in click_history" class="item">🚩</div>
            </div>

            <button @click="terminate_mock_exam()">End Exam</button>
        </div>

        <div v-if="current_view === 'scores'">
            <h1 class="title">MOCK EXAM SCORES | {{ logged_in_user }}</h1>
            <h2>Multiple Choice Score: {{ this.scores_1 }} / 50</h2>
            <h2>Hazard Perception Score: {{ this.scores_2 }} / 75</h2>
            <button @click="terminate_mock_exam()">End Exam</button>
            <button @click="init_feedback()">Feedback</button>
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
            finished: false,

            // Multiple Choice Questions
            questions: [], // {question, topic, image, correct_answer, options, selected_ans, flagged}
            current_Q: 0, // Question pointer
            scores_1: 0, // Score for questions

            // Images
            images: images.keys().map(image => images(image)),
            image: "",

            // Hazard Perception Clips
            clips: [], // {name, x, y, time}
            selected_clip: null,
            current_C: 0, // Clip pointer
            clip_url: '',
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
            const input = { 'No_of_Qs': 3, 'username': this.logged_in_user };
            const quiz = await this.azure_function('POST', '/question/get/quiz', input);
            if (quiz.result) {
                // Populate the questions list, and add a flag to them and remove explanation attr.
                this.questions = quiz.msg;
                this.questions.forEach(item => {
                    item.selected_ans = null;
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
                .slice(0, 2);           // Select the first 14 clips
            
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
            this.add_image();
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
        select_answer(option) {
            this.$set(this.questions[this.current_Q], 'selected_ans', option);
            console.log('Selected answer of question ' + (this.current_Q + 1) + ": " + this.questions[this.current_Q].selected_ans);
        },
        next_question() {
            this.current_Q++;
            this.add_image();
        },
        prev_question() {
            this.current_Q--;
            this.add_image();
        },
        toggle_flag() {
            this.questions[this.current_Q].flagged = !this.questions[this.current_Q].flagged;
            console.log('Flagged Question ' + (this.current_Q + 1) + " " + this.questions[this.current_Q].flagged);
        },
        jump_to_question(index) {
            this.current_Q = index;
            this.add_image();
        },
        add_image() {
            // Library of images
            let question_image = this.questions[this.current_Q].image
            if (question_image !== 'n/a') {
                this.image = this.images.filter((image, index) => images.keys()[index].includes(question_image))[0];
            }
        },
        handleClick(event) {
            // This method records when and where in the video you clicked.
            const video = this.$refs.hazard_perception;

            if (this.click_history.length > 10) {
                this.click_fail();
            }

            // Get click position relative to the video element
            this.click_x = (event.offsetX).toFixed(2);
            this.click_y = (event.offsetY).toFixed(2);

            // Get the timestamp of the click
            this.click_time = video.currentTime.toFixed(2);

            // Store in history
            this.click_history.push({
                x: this.click_x,
                y: this.click_y,
                time: this.click_time,
            });

            console.log(
                `Clicked at X: ${this.click_x}, Y: ${this.click_y}, Time: ${this.click_time}s`
            );

            // Add click animation
            this.clicks.push({ x: this.click_x, y: this.click_y});

            // Remove animation after 0.3s
            setTimeout(() => {
                this.clicks.shift();
            }, 600);

        },
        click_fail() {
            // Run this method if the user clicks more than 10 times
            const video = this.$refs.hazard_perception;
            video.pause();
            this.too_many_clicks = true;
            this.current_C++;
        },
        async finish_video_clip() {

            // Check if the user clicked on the appropriate (x,y) range:
            if ((this.click_x <= this.selected_clip.x + 50 && this.click_x >= this.selected_clip.x - 50) && 
                (this.click_y <= this.selected_clip.y + 50 && this.click_y >= this.selected_clip.y - 50)) {

                let interval = 1;

                // Then check if the user clicked at the right time:
                if (this.click_time >= this.selected_clip.time && this.click_time < this.selected_clip.time + interval) {
                    this.scores_2+=5;
                } else if (this.click_time >= this.selected_clip.time + interval && this.click_time < this.selected_clip.time + interval*2) {
                    this.scores_2+=4;
                } else if (this.click_time >= this.selected_clip.time + interval*2 && this.click_time < this.selected_clip.time + interval*3) {
                    this.scores_2+=3;
                } else if (this.click_time >= this.selected_clip.time + interval*3 && this.click_time < this.selected_clip.time + interval*4) {
                    this.scores_2+=2;
                } else if (this.click_time >= this.selected_clip.time + interval*4 && this.click_time < this.selected_clip.time + interval*5) {
                    this.scores_2+=1;
                }

                if (this.scores_2 >= 1) {
                    console.log('Got a score!')
                } else {
                    console.log('No score!')
                }
            }
            // Clicking the video
            this.click_x = 0;
            this.click_y = 0;
            this.click_time = 0;
            this.click_history = [];
            this.clicks = [];
            this.too_many_clicks = false;
            this.current_C++;
            this.load_video_clip();
        },
        start_hazard_perceptions() {
            // Start the hazard perception section
            this.load_video_clip();
            this.toggle_view('hazard_perception');
        },
        async load_video_clip() {
            if (this.current_C < this.clips.length) {
                // Load the corrosponding clip
                this.click_x = 0;
                this.click_y = 0;
                this.click_time = 0;
                this.click_history = [];
                this.clicks = [];
                this.too_many_clicks = false;

                this.selected_clip = this.clips[this.current_C];
                this.clip_url = this.selected_clip.url;
                console.log(this.selected_clip.name);
            } else {
                this.finish_mock_exam();
            }
        },
        finish_mock_exam() {
            // Add up scores
            this.questions.forEach(item => {
                if (item.selected_ans !== item.correct_answer) {
                    this.scores_1+=1;
                    // {question, correct_ans, selected_ans, image}
                    const entry = {question: item.question, selected: item.selected_ans, correct: item.correct_answer, image: item.image};
                    this.feedback.push(entry);
                }
            });
            this.toggle_view('scores')
        },
        async terminate_mock_exam() {
            // Reset states
            this.timeLeft = 60 * 60; // 60 minutes in seconds
            this.timer = null;
            this.questions = [];
            this.current_Q = 0;
            this.scores_1 = 0;
            this.timer_finished = false;
            this.finished = false;
            this.image = "";
            this.clips = [];
            this.selected_clip = null;
            this.clip_url = '',
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
        init_feedback() {
            // Setup for the feedback page
            console.log("/feedback");
            this.$router.push({
                path: `/feedback`,
                query: { input: this.feedback }
            })
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
img {
  max-width: 300px; /* Limits the width to 200px */
  max-height: 200px; /* Limits the height to 100px */
  width: auto; /* Maintain aspect ratio */
  height: auto; /* Maintain aspect ratio */
}

.instruction-box {
  background-color: #f9f9f9;
  border-left: 5px solid #007bff;
  padding: 10px;
  margin: 10px 0;
  font-size: 14px;
  color: #333;
  border-radius: 5px;
}

button.flagged {
  background-color: #ffc107; // Yellow
  color: black;
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

.questionnaire {
  text-align: center;
  max-width: 500px;
  margin: auto;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  background: #f9f9f9;
}

h2 {
  margin-bottom: 15px;
}

.options button {
  display: block;
  width: 100%;
  padding: 10px;
  margin: 5px 0;
  border: none;
  background-color: #969faa;
  color: white;
  cursor: pointer;
  border-radius: 5px;
}

.options button.selected {
  background-color: #418ade;
}

.next-button {
  margin-top: 15px;
  padding: 10px 20px;
  border: none;
  background-color: green;
  color: white;
  cursor: pointer;
  border-radius: 5px;
}

.next-button:hover {
  background-color: darkgreen;
}

.floating-grid {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  z-index: 999;
  width: 160px;
  max-height: 300px;
  overflow-y: auto;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(35px, 1fr));
  gap: 6px;
}

.grid-item {
  padding: 6px;
  text-align: center;
  background-color: #e0e0e0;
  border-radius: 4px;
  font-size: 13px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s ease;
}

.grid-item.answered {
  background-color: #4caf50;
  color: white;
}

.grid-item.flagged {
  background-color: #ffc107;
  color: black;
}

.grid-item.current {
  border: 2px solid #007bff;
}

.video-container {
  position: relative;
  display: inline-block;
}

/* Animated Click Circle */
.click-circle {
  position: absolute;
  width: 30px;
  height: 30px;
  background-color: rgba(237, 18, 18, 0.8);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: clickEffect 0.6s ease-out forwards;
}

@keyframes clickEffect {
  0% {
    transform: scale(0);
    opacity: 1;
  }
  100% {
    transform: scale(2);
    opacity: 0;
  }
}

.horizontal-container {
    display: flex; /* Display items in a row */
    gap: 10px; /* Optional: Adds space between the items */
}

.item {
    width: 20px; /* Set width */
    height: 20px; /* Set height */
    padding: 10px;
    border-radius: 4px;
}

</style>