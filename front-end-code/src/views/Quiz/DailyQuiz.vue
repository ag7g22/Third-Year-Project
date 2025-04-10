<template>
    <div v-if="current_view === 'instructions'" class="split-container">
        <div class="left-side">
            <div class="instructions-container">
                <h3>Welcome to Your Daily Training Session!</h3>
                <div class="feature-list">
                    <p>
                        Daily training sessions are essential for combating the forgetting curve — a psychological principle that shows how quickly we forget information after learning it. 
                        Without regular review, our memory of new knowledge fades rapidly over time. The training routine is as follows:
                    </p>
                </div>
                <p>1. 🚦 Warm-Up: 10 Road Sign Questions </p>
                <p>2. 🧠 Core Quiz: 10 Multiple Choice Questions</p>
                <p>3. 🎥 Simulation: 1 Hazard Perception clip</p>
                <p>Good luck!</p>
            </div>
        </div>

        <div class="right-side">
            <img src="@/assets/titles/DailyQuiz.png" alt="Logo" class="task-logo"/>
            <div class="game-buttons">
                <button @click="next_page('dashboard')" class="game-button">Back</button>
                <button @click="init_road_signs()" class="game-button">Start</button>
            </div>
        </div>
    </div>
    <div v-else>
        <div v-if="current_view === 'quiz'" class="container">
            <h1 class="title">DAILY QUIZ | {{ logged_in_user }}</h1>
            <div class="questionnaire">
                <div v-if="questions.length === 0">
                    <p>LOADING ASSETS ...</p>
                </div>
                <div v-else-if="currentQuestion < questions.length">
                    <p>Question {{ currentQuestion + 1 }} of {{ questions.length }}</p>

                    <!-- Progress Bar -->
                    <div class="progress-container">
                    <div class="progress-bar" :style="{ width: progressBarWidth + '%' }"></div>
                    </div>

                    <h2>{{ questions[currentQuestion].question }}</h2>

                    <div v-if="questions[currentQuestion].image !== 'n/a'">
                        <img :src=image alt="Question Image">
                    </div>

                    <button @click="toggleExplanation" class="explanation-button">
                        {{ explanation.showExplanation ? "Hide Explanation" : "Show Explanation" }}
                    </button>
                    <button class="stop-button" @click="terminate_daily_quiz()">Stop Quiz</button>

                    <div v-if="explanation.showExplanation" class="overlay" @click="toggleExplanation">
                        <div class="overlay-content" @click.stop>
                            <h2>Explanation</h2>
                            <p>{{ questions[currentQuestion].explanation }}</p>
                            <button @click="explanation.showExplanation = false">Close</button>
                        </div>
                    </div>

                    <div class="options">
                        <button 
                        v-for="(option, index) in questions[currentQuestion].options"
                        :key="index"
                        :class="{
                            selected: selectedAnswer === option,
                            correct: selectedAnswer === option && isCorrect,
                            incorrect: selectedAnswer === option && !isCorrect
                        }"
                        @click="selectAnswer(option)"
                        >
                        {{ option }}
                        </button>
                    </div>
                    <button v-if="selectedAnswer" @click="nextQuestion">Next</button>
                </div>
                <div v-else>
                    <h3>Finished the {{ current_part }}!</h3>
                    <h3>Moving onto the {{ next_part }}...</h3>
                    <button @click="next_section(next_part)">Next</button>
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

                <div v-if="too_many_clicks" class="overlay">
                    <div class="overlay-content" @click.stop>
                        <p>You've clicked too many times.</p>
                        <button @click="toggle_view('score')">Next</button>
                    </div>
                </div>
                
                <div class="horizontal-container">
                    <div v-for="clicks in click_history" class="item">🚩</div>
                </div>
            </div>
            <button class="stop-button" @click="terminate_daily_quiz()">Stop Quiz</button>
        </div>

        <div v-if="current_view === 'score'">
            <h1 class="title">DAILY QUIZ | {{ logged_in_user }}</h1>
            <div class="score">
                <h2>You've completed the video! 🎉</h2>
                <h3> Score: {{ hazard_score }} / 5 </h3>
                <p> {{ score_message }} </p>
                <button @click="init_feedback()">Feedback</button>
            </div>
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
            current_part: 'Road sign section',
            next_part: 'Multiple choice section',

            // Quiz variables
            questions: [], // Quiz questions by API
            currentQuestion: 0, // Question pointer
            selectedAnswer: null, // This is the selected answer
            isCorrect: false, // boolean if the question is actually correct
            explanation: { showExplanation: false, wasClicked: false }, // Explanation of the question, flag if it got clicked on

            // Timer
            answer_time: { elapsedTime: 0, stopwatch: null, stopwatchRunning: false },

            // Clips
            clips: [],
            selected_clip: null,
            clip_url: '',

            // Clicking the video
            click_x: 0,
            click_y: 0,
            click_time: 0,
            click_history: [],
            clicks: [],
            too_many_clicks: false,

            // Feedback
            feedback: [],
            // {question, correct_ans, selected_ans, image}

            // Score, averaged out by number of questions.
            hazard_score: 0,
            total_score: 0,
            percentage: null,
            final_score: null,
            exp_gain: null,
            quiz_message: "",

            // Images
            images: images.keys().map(image => images(image)),
            image: "",

            // Flag for updating database scores.
            updateFinished: false,

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
        async init_road_signs() {
            // Reset messages
            this.message = { error: "", success: "" };
            this.message.success = 'Loading daily quiz ...';

            // Initalise the road sign questions.
            const input = { "No_of_Qs": 10, "topic": "sign_question" }
            const quiz = await this.azure_function('POST', '/question/get/category', input);
            if (quiz.result) {
                // Populate the questions list
                this.message.success = 'Loading quiz successful!';
                this.questions = quiz.msg;

                this.add_image();

                // Switch to the quiz section, start timer for question.
                this.toggle_view('quiz');
                this.startStopwatch();
            } else {
                this.message.error = quiz.msg || "Loading quiz failed.";
            } 

        },
        async init_multiple_choice() {
            // Reset messages
            this.message = { error: "", success: "" };
            this.questions = [];

            // Initalise the road sign questions.
            const input = { "No_of_Qs": 10, "username": this.logged_in_user }
            const quiz = await this.azure_function('POST', '/question/get/quiz', input);
            if (quiz.result) {
                // Populate the questions list
                this.message.success = 'Loading quiz successful!';
                this.questions = quiz.msg;

                // RESET QUIZ VARIABLES
                this.currentQuestion = 0;
                this.selectedAnswer = null;
                this.isCorrect = false;
                this.explanation = { showExplanation: false, wasClicked: false };
                this.answer_time = { elapsedTime: 0, stopwatch: null, stopwatchRunning: false };
                this.add_image();

                // Switch to the quiz section again, start timer for question.
                this.toggle_view('quiz');
                this.startStopwatch();
            } else {
                this.message.error = quiz.msg || "Loading quiz failed.";
            } 
        },
        async init_hazard_perception() {
            // Reset messages
            this.message = { error: "", success: "" };
            this.message.success = 'Loading hazard perception clips ...';

            // Initalise the hazard perception clips.
            // List of dictionaries
            const dictList = [
                {name: 'Urban Driving 1', x: 370, y: 270, time: 15.25}, {name: 'Urban Driving 2', x: 540, y: 270, time: 18.00}, {name: 'Urban Driving 3', x: 410, y: 260, time: 29.00},
                {name: 'Urban Driving 4', x: 415, y: 260, time: 37.60}, {name: 'Urban Driving 5', x: 350, y: 260, time: 29.00}, {name: 'Rural Driving 1', x: 490, y: 220, time: 47.00},
                {name: 'Rural Driving 2', x: 250, y: 250, time: 31.00}, {name: 'Rural Driving 3', x: 395, y: 230, time: 17.50}, {name: 'Rural Driving 4', x: 450, y: 290, time: 13.45},
                {name: 'Rural Driving 5', x: 295, y: 240, time: 37.85}, {name: 'Bigger Roads 1', x: 415, y: 250, time: 13.90}, {name: 'Bigger Roads 2', x: 425, y: 240, time: 14.55},
                {name: 'Bigger Roads 3', x: 510, y: 260, time: 26.30}, {name: 'Bigger Roads 4', x: 500, y: 245, time: 21.45}, {name: 'Motorways 1', x: 25, y: 190, time: 2.55},
                {name: 'Motorways 2', x: 320, y: 250, time: 25.45}, {name: 'Motorways 3', x: 690, y: 290, time: 30.20}, {name: 'Tricky Conditions 1', x: 110, y: 250, time: 17.10},
                {name: 'Tricky Conditions 2', x: 515, y: 240, time: 31.80}, {name: 'Tricky Conditions 3', x: 280, y: 254, time: 33.45}, {name: 'Tricky Conditions 4', x: 325, y: 235, time: 22.70},
                {name: 'Tricky Conditions 5', x: 320, y: 255, time: 24.00}
            ];
            // Shuffle and select random clips
            this.clips = dictList
                .sort(() => 0.5 - Math.random())  // Randomly shuffle
                .slice(0, 1);           // Select the first item

            console.log(this.clips[0]);
            await this.load_video_clip(this.clips[0]);
        },
        selectAnswer(option) {
            // When you select an answer it locks in, and calculate score and add it to total.
            if (!this.selectedAnswer) {
                this.stopStopwatch();
                this.selectedAnswer = option;
                this.isCorrect = option === this.questions[this.currentQuestion].correct_answer;
                this.add_score();
            }
        },
        async nextQuestion() {
            // Moving to next question, reset question state and stopwatch and time again.
            this.resetStopwatch();
            this.selectedAnswer = null;
            this.explanation = { showExplanation: false, clickedOn: false };
            this.isCorrect = false;
            this.currentQuestion++;
            if (this.currentQuestion < this.questions.length) {
               this.add_image();
               this.startStopwatch();
            } else {
                this.next_section();
            }
        },
        async next_section(section) {
            // Transition to next section:
            if (section === "Multiple choice section") {
                // Move to multiple choice:
                this.current_part = 'Multiple choice section';
                this.next_part = 'Hazard Perception section';
                this.init_multiple_choice();

            } else if (section === "Hazard Perception section") {
                // Move to hazard perception:
                this.current_part = 'Hazard Perception section.';
                this.next_part = "Results";
                this.init_hazard_perception();

            } else if (section === "Results") {
                // Move to results:
                await this.get_stats();
                // Update score if quiz completed:
                console.log("FINAL SCORE:", this.final_score);
                await this.update_user_topic_score();
                await this.update_user_exp();
                this.updateFinished = true;
            }
        },
        toggleExplanation() {
            // Toggle flag id the explanation was toggled at least once.
            if (!this.explanation.showExplanation && !this.explanation.wasClicked) {
                this.explanation.wasClicked = true;
            }
            // Toggle explanation
            this.explanation.showExplanation = !this.explanation.showExplanation;
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
        async load_video_clip(clip) {
            // Load the corrosponding clip
            console.log(clip.name);
            this.selected_clip = clip;
            const input = {'filename': clip.name + ".mp4"};

            const video = await this.azure_function('POST', '/question/get/video', input);
            if (video.result) {
                // Set the playing video
                this.clip_url = video.msg;
                console.log(this.clip_url);
                this.toggle_view('hazard_perception');
            } else {
                this.message.error = video.msg || 'Loading video failed.'
            }
        },
        click_fail() {
            // Run this method if the user clicks more than 10 times
            const video = this.$refs.hazard_perception;
            video.pause();
            this.too_many_clicks = true;
            this.score_message = "Don't give up! Every attempt makes you better. Keep pushing forward!";
            this.message.success = "Gained no exp."
            this.updateFinished = true;
        },
        async finish_video_clip() {

            // Check if the user clicked on the appropriate (x,y) range:
            if ((this.click_x <= this.selected_clip.x + 50 && this.click_x >= this.selected_clip.x - 50) && 
                (this.click_y <= this.selected_clip.y + 50 && this.click_y >= this.selected_clip.y - 50)) {

                let interval = 1;

                // Then check if the user clicked at the right time:
                if (this.click_time >= this.selected_clip.time && this.click_time < this.selected_clip.time + interval) {
                    this.hazard_score = 5;
                    this.score_message = "Eagle eyed legend!";
                    this.exp_gain = 350;
                } else if (this.click_time >= this.selected_clip.time + interval && this.click_time < this.selected_clip.time + interval*2) {
                    this.hazard_score = 4;
                    this.score_message = "You almost got it, keep trying!";
                    this.exp_gain = 280;
                } else if (this.click_time >= this.selected_clip.time + interval*2 && this.click_time < this.selected_clip.time + interval*3) {
                    this.hazard_score = 3;
                    this.score_message = "This is pretty good, you can do better!";
                    this.exp_gain = 210;
                } else if (this.click_time >= this.selected_clip.time + interval*3 && this.click_time < this.selected_clip.time + interval*4) {
                    this.hazard_score = 2;
                    this.score_message = "You're learning, and that's what matters! Keep challenging yourself!";
                    this.exp_gain = 140;
                } else if (this.click_time >= this.selected_clip.time + interval*4 && this.click_time < this.selected_clip.time + interval*5) {
                    this.hazard_score = 1;
                    this.score_message = "Not bad! Mistakes help us grow—review what you missed and try again!";
                    this.exp_gain = 70;
                } else {
                    this.hazard_score = 0;
                    this.score_message = "Don't give up! Every attempt makes you better. Keep pushing forward!";
                }

            } else {
                this.score_message = "Don't give up! Every attempt makes you better. Keep pushing forward!";
            }

            this.toggle_view('score');

            if (this.hazard_score >= 1) {
                console.log('Got a score!')
                //await this.update_user_exp();
                this.updateFinished = true;
            } else {
                console.log('No score!')
                this.message.error = "Gained no exp."
                this.updateFinished = true;
            }
        },
        terminate_daily_quiz() {
            // End the quiz early
            this.current_view = 'instructions';
            this.current_part = 'Road sign section';
            this.next_part = 'Multiple choice section';
            this.questions = [];
            this.currentQuestion = 0;
            this.selectedAnswer = null;
            this.isCorrect = false;
            this.explanation = { showExplanation: false, wasClicked: false };
            this.answer_time = { elapsedTime: 0, stopwatch: null, stopwatchRunning: false };
            this.clips = [];
            this.selected_clip = null;
            this.clip_url = '';
            this.feedback = [];
            this.total_score = 0;
            this.percentage = null;
            this.final_score = null;
            this.exp_gain = null;
            this.quiz_message = "";
            this.image = "";
            this.updateFinished = false;
            this.clips = [];
            this.selected_clip = null;
            this.clip_url = '';
            this.click_x = 0;
            this.click_y = 0;
            this.click_time = 0;
            this.click_history = [];
            this.clicks = [];
            this.too_many_clicks = false;

            this.toggle_view('instructions');
        },
        end_quiz() {
            // End the daily quiz

        },
        add_score() {
            let score = 0;
            if (this.isCorrect) { // If answered correct, calculate score based on how long was spent on that question.
                score = parseFloat(((60-this.answer_time.elapsedTime) / 60).toPrecision(2))
            }
            if (this.explanation.wasClicked) { // If the explanation was toggled, cap the score to 0.1.
                score = 0.1;
            } 
            if (!this.isCorrect) { // If not answered correct, add nothing to the score.
                score = 0;
                this.add_feedback();
            }
            this.total_score += score;
            console.log(`Time taken: ${this.answer_time.elapsedTime}, Added score: ${score}, Total Score: ${this.total_score}`)
        },
        add_feedback() {
            // Add to feedback list to send to API later
            let question_image = this.questions[this.currentQuestion].image
            let q_obj = this.questions[this.currentQuestion]
            console.log(JSON.stringify({question: q_obj.question, selected: this.selectedAnswer, correct: q_obj.correct_answer, image: question_image}))
            this.feedback.push({question: q_obj.question, selected: this.selectedAnswer, correct: q_obj.correct_answer, image: question_image})
        },
        add_image() {
            // Library of images
            let question_image = this.questions[this.currentQuestion].image
            if (question_image !== 'n/a') {
                this.image = this.images.filter((image, index) => images.keys()[index].includes(question_image))[0];
            }
        },
        startStopwatch() {
            if (!this.answer_time.stopwatchRunning) {
                this.answer_time.stopwatchRunning = true;
                this.answer_time.stopwatch = setInterval(() => {
                this.answer_time.elapsedTime++; // Increment time
                }, 1000);
            }
        },
        stopStopwatch() {
            clearInterval(this.answer_time.stopwatch);
            this.answer_time.stopwatchRunning = false;
        },
        resetStopwatch() {
            this.stopStopwatch();
            this.answer_time.elapsedTime = 0; // Reset back to 0
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
        progressBarWidth() {
        return (this.currentQuestion / (this.questions.length - 1)) * 100;
        }
    }
};
</script>

<style lang="scss" scoped>
img {
  max-width: 300px; /* Limits the width to 200px */
  max-height: 200px; /* Limits the height to 100px */
  width: auto; /* Maintain aspect ratio */
  height: auto; /* Maintain aspect ratio */
}

.right-side img {
    max-width: 100%;
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

select {
  padding: 5px;
  font-size: 16px;
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
  background-color: #595f66;
}

/* Flash green for correct answers */
.options button.correct {
    background-color: #5bd45f;
}

/* Flash red for incorrect answers */
.options button.incorrect {
    background-color: #e34242;
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

/* Open button */
.open-overlay-btn {
  padding: 10px 15px;
  background: blue;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}

/* Close button */
.close-overlay-btn {
  margin-top: 10px;
  padding: 10px;
  background: red;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}

.progress-container {
  width: 100%;
  height: 20px;
  background-color: #f3f3f3;
  border-radius: 2px;
  margin-bottom: 2px;
}

.progress-bar {
  height: 100%;
  background-color: #4caf50;
  border-radius: 10px;
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