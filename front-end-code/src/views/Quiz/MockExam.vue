<template>
    <div v-if="current_view === 'instructions'" class="split-container">
        <div class="left-side">
            <div class="instructions-container">
                <h3>Shh ... time to do your mock exam ...</h3>
                <div class="feature-list">
                    <p>
                        The driving theory exam has two parts: a multiple-choice section with 50 questions, where you need at least 43 correct to pass, and a hazard perception test. 
                        You have 57 minutes for the multiple-choice section, and the hazard perception test consists of 14 video clips. Both parts must be passed to proceed to the practical test.
                    </p>
                </div>
                <p>1. 🧠 Core Quiz: 50 Multiple Choice Questions</p>
                <p>2. 🎥 Simulation: 14 Hazard Perception clips</p>
                <p>Good luck!</p>
            </div>
        </div>
        <div class="right-side">
            <img src="@/assets/titles/MockTest.png" alt="Logo" class="task-logo"/>
            <div class="game-buttons">
                <button @click="next_page('dashboard')" class="game-button">Back</button>
                <button @click="init_questions()" class="game-button">Start</button>
            </div>
        </div>
    </div>

    <div v-else>
        <div v-if="current_view === 'multiple_choice'" class="container">
            <div class="questionnaire">
                <h2>Question {{ current_Q + 1 }} of {{ questions.length }} | {{ formattedTime }}</h2>
                <div class="progress-bar">
                    <div class="progress-fill" :style="{ width: progressBarWidth + '%' }"></div>
                </div>
                <div class="question-container">
                    <div class="question-text">
                        <h1>{{ questions[current_Q].question }}</h1>
                    </div>
                    <div class="question-image" v-if="questions[current_Q].image !== 'n/a'">
                        <img :src="image" alt="Question Image">
                    </div>
                </div>
                <div class="quiz-buttons-container">
                    <div class="quiz-buttons-grid">
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
                    <div class="game-buttons">
                        <button @click="terminate_mock_exam()" class="game-button">End Exam</button>
                        <button 
                            @click="toggle_flag"
                            class="game-button"
                            >
                            <span v-if="questions[current_Q].flagged">Unflag</span>
                            <span v-else>Flag</span></button>
                        <div v-if="current_Q !== 0">
                            <button @click="prev_question()" class="game-button">Previous</button>
                        </div>
                        <div v-else><button disabled class="game-button">Previous</button></div>

                        <div v-if="questions[current_Q].selected_ans !== null && current_Q !== questions.length - 1">
                            <button @click="next_question()" class="game-button">Next</button>
                        </div>
                        <div v-else><button disabled class="game-button">Next</button></div>

                        <div v-if="current_Q === questions.length - 1 && questions[current_Q].selected_ans !== null" >
                            <button  @click="start_hazard_perceptions" class="game-button">Finish Section</button>
                        </div>
                        <div v-else><button disabled class="game-button">Finish Section</button></div>
                    </div>
                </div>
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

        <div v-if="current_view === 'hazard_perception'" class="container">
            <div v-if="clip_url === ''" class="quiz-result">
                <h1>Loading ...</h1>
            </div>
            <div v-if="too_many_clicks" class="overlay" @click="load_video_clip()">
                <div class="overlay-content" @click.stop>
                    <h2>You've clicked too many times.</h2>
                    <p>(Click outside the box.)</p>
                </div>
            </div>
            <div class="video-container">
                <video ref="hazard_perception"
                    :src="clip_url"
                    @click="handleClick"
                    @ended="finish_video_clip"
                    autoplay 
                    muted 
                    playsinline 
                    width="950"
                    height="650">
                </video>
                <!-- Click Effect -->
                <div 
                    v-for="(click, index) in clicks"
                    :key="index"
                    class="click-circle"
                    :style="{ top: (click.y - 10) + 'px', left: (click.x - 15) + 'px' }"
                ></div>
                <!-- Footer Section -->
                <div class="video-footer">
                    <div class="flags-container">
                        <div v-for="clicks in click_history" class="item">🚩</div>
                    </div>
                    <button @click="terminate_daily_quiz()" class="game-button">Back</button>  
                </div>
            </div>
        </div>

        <div v-if="current_view === 'scores'" class="container">
            <div class="questionnaire">
                <div class="quiz-result">
                    <h2>You've completed the mock test! 📖</h2>
                    <h3>Multiple Choice: {{ this.scores_1 }} / 50 | Hazard Perception: {{ this.scores_2 }} / 75</h3>
                    <div class="graph-box">
                        <div class="score-row" v-for="(score, topic) in averaged_scores" :key="topic">
                            <div class="label">{{ topic }}</div>
                            <div class="bar-container">
                                <div class="bar"
                                    :style="{ width: (score * 100) + '%', backgroundColor: colorMap[topic] }">
                                </div>
                            </div>
                            <div class="value">{{ (score * 100).toFixed(0) }}%</div>
                        </div>
                    </div>
                    <div class="game-buttons">
                        <button class="game-button" @click="init_feedback()">Feedback</button> 
                    </div>
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

            // Scores the upload to database
            update_scores: {
                "Driving Off": [],
                "Urban Driving": [],
                "Rural Driving": [],
                "Bigger Roads": [],
                "Motorways": [],
                "Tricky Conditions": [],
                "Breakdowns": [],
            },
            colorMap: {
                "Driving Off": "#4caf50",         // green
                "Urban Driving": "#2196f3",       // blue
                "Rural Driving": "#9c27b0",       // purple
                "Bigger Roads": "#ff9800",        // orange
                "Motorways": "#f44336",           // red
                "Tricky Conditions": "#ffc107",   // amber
                "Breakdowns": "#795548",          // brown
            },
            averaged_scores: {},

            logged_in_user: this.$store.state.currentUser,
            currentRank: this.$store.state.currentRank,
            message: { error: "", success: "" },
        };
    },
    methods: {
        exp_message() {
            if (this.exp_gain === 0) return;
            toastr.info(" ", `Gained ${this.exp_gain} exp!`, {
                closeButton: true,
                progressBar: true,
                positionClass: "toast-bottom-center",
                timeOut: 5000,
                showMethod: "fadeIn",
                hideMethod: "fadeOut",
                preventDuplicates: true
            });
        },
        level_up_message() {
            toastr.info(" ", "LEVELED UP!", {
                closeButton: true,
                progressBar: true,
                positionClass: "toast-bottom-center",
                timeOut: 5000,
                showMethod: "fadeIn",
                hideMethod: "fadeOut",
                preventDuplicates: true
            });
        },
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
                    item.selected_ans = null;
                    item.flagged = false;
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
        async finish_mock_exam() {
            // Add up scores
            this.questions.forEach(async item => {
                if (item.selected_ans === item.correct_answer) {
                    this.scores_1 += 1;
                    await this.add_update_score(item.topic, 1);
                } else {
                    // {question, correct_ans, selected_ans, image}
                    await this.add_update_score(item.topic, 0);
                    const entry = { question: item.question, selected: item.selected_ans, correct: item.correct_answer, image: item.image, explanation: item.explanation };
                    this.feedback.push(entry);
                }
            });
            const user_stats = this.$store.state.currentStats;
            await this.update_user_exp(user_stats);
            await this.db_update_scores(user_stats);

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
            this.update_scores = {"Driving Off": [], "Urban Driving": [],"Rural Driving": [],"Bigger Roads": [],"Motorways": [],"Tricky Conditions": [],"Breakdowns": [],},
            this.averaged_scores = {},
            this.toggle_view('instructions');
        },
        init_feedback() {
            // Setup for the feedback page
            let input = this.feedback;
            this.terminate_mock_exam();
            console.log("/feedback");
            this.$router.push({
                path: `/feedback`,
                query: { input: input }
            })
        },
        async update_user_exp() {
            // Add changes to database
            const total_score = this.scores_1 + this.scores_2;
            this.exp_gain = Math.round(((total_score / 125) * 500) / 100) * 100; 
            const user_stats = this.$store.state.currentStats;
            const prev_level = this.currentRank.level;

            // Increment level if exp exceeds threshold:
            if (this.currentRank.exp + this.exp_gain >= this.currentRank.exp_threshold) {
                // Reset exp progress but add leftover exp and update exp threshold
                this.currentRank.exp = (this.currentRank.exp + this.exp_gain) - this.currentRank.exp_threshold;
                this.currentRank.level += 1;
                this.currentRank.exp_threshold += 500;
            } else {
                this.currentRank.exp += this.exp_gain;
            }
            const input = { id: user_stats.id, updates: { "rank": this.currentRank } };
            console.log(input);
            const update_response = await this.azure_function("PUT", "/user/update/info", input)
            // Show message incase the API response fails, otherwise update state.
            if (update_response.result) {
                // Update rank in UI too.
                this.$store.commit("setCurrentRank", this.currentRank);
                this.currentRank = this.$store.state.currentRank;
                if (prev_level < this.currentRank.level) {
                    this.level_up_message();
                } else {
                    this.exp_message();
                }
            } else {
                this.message.error = update_response.msg || "Score update Failed."
            }
        },
        async add_update_score(topic, score) {
            // Adding score to database
            this.update_scores[topic].push(score);
        },
        async db_update_scores(user_stats) {
            for (let topic in this.update_scores) {
                const scores = this.update_scores[topic];
                const average = scores.length > 0
                    ? (scores.reduce((sum, val) => sum + val, 0) / scores.length)
                    : 0;

                this.averaged_scores[topic] = parseFloat(average.toFixed(2));
            }
            // Update database
            const input = { 'id': user_stats.id, 'updates': this.averaged_scores }
            console.log(input);
            const update = await this.azure_function("PUT", "/user/update/scores", input)
            if (update) {
                console.log('Updated scores!');
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
            console.log("/" + page);
            this.$router.push(`/${page}`);
        }
    },
    computed: {
    formattedTime() {
      const minutes = String(Math.floor(this.timeLeft / 60)).padStart(2, '0');
      const seconds = String(this.timeLeft % 60).padStart(2, '0');
      return `${minutes}:${seconds}`;
    },
    progressBarWidth() {
        return (this.current_Q / (this.questions.length - 1)) * 100;
    }
  },
};
</script>

<style lang="scss" scoped>
.floating-grid {
  position: fixed;
  bottom: 0;
  right: 0;
  background-color: black;
  border: 2px solid #f3af59;
  padding: 10px;
  z-index: 999;
  width: 160px;
  max-height: 120px;
  overflow-y: auto;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(35px, 1fr));
  gap: 6px;
}

.grid-item {
    color: #f3af59;
    padding: 6px;
    text-align: center;
    background-color: #5c5c5c;
    border: 2px solid black;
    font-size: 13px;
    font-weight: bold;
    cursor: pointer;
}

.grid-item.answered {
    background-color: #079cb0;
    color: white;
}

.grid-item.flagged {
    background-color: #f3af59;
    color: black;
}

.grid-item.current {
    border: 2px solid #ffffff;  
}
</style>