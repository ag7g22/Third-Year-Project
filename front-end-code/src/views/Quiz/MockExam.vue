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
                    <button @click="terminate_daily_quiz()" class="game-button">End Exam</button>  
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
        };
    },
    methods: {
        info_message(title, msg) {
            toastr.info(msg, title, {
                closeButton: true,
                progressBar: true,
                positionClass: "toast-top-right",
                timeOut: 1000,
                showMethod: "fadeIn",
                hideMethod: "fadeOut",
                preventDuplicates: true
            });
        },
        exp_message() {
            if (this.exp_gain === 0) return;
            toastr.info(" ", `Gained ${this.exp_gain} exp!`, {
                closeButton: true,
                progressBar: true,
                positionClass: "toast-top-right",
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
                positionClass: "toast-top-right",
                timeOut: 5000,
                showMethod: "fadeIn",
                hideMethod: "fadeOut",
                preventDuplicates: true
            });
        },
        toggle_view(view) {
            this.current_view = view;
        },
        async init_questions() {
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
            }
        },
        async init_clips() {
            // Fetch the 14 clips:
            const dictList = [
                {name: 'Urban Driving 1', x: 455, y: 335, time: 15.00},
                {name: 'Urban Driving 2', x: 665, y: 330, time: 14.80},
                {name: 'Urban Driving 3', x: 485, y: 325, time: 28.45},
                {name: 'Urban Driving 4', x: 475, y: 325, time: 34.90},
                {name: 'Urban Driving 5', x: 415, y: 345, time: 29.60},
                {name: 'Rural Driving 1', x: 620, y: 300, time: 47.65},
                {name: 'Rural Driving 2', x: 280, y: 325, time: 31.00},
                {name: 'Rural Driving 3', x: 475, y: 310, time: 18.70},
                {name: 'Rural Driving 4', x: 530, y: 370, time: 13.90},
                {name: 'Rural Driving 5', x: 350, y: 320, time: 38.85},
                {name: 'Bigger Roads 1', x: 485, y: 320, time: 13.80},
                {name: 'Bigger Roads 2', x: 485, y: 315, time: 14.50},
                {name: 'Bigger Roads 3', x: 600, y: 320, time: 27.70},
                {name: 'Bigger Roads 4', x: 590, y: 325, time: 22.00},
                {name: 'Motorways 1', x: 20, y: 263, time: 2.35},
                {name: 'Motorways 2', x: 400, y: 325, time: 26.85},
                {name: 'Motorways 3', x: 815, y: 360, time: 30.85},
                {name: 'Tricky Conditions 1', x: 165, y: 325, time: 17.10},
                {name: 'Tricky Conditions 2', x: 600, y: 320, time: 31.90},
                {name: 'Tricky Conditions 3', x: 510, y: 335, time: 33.20},
                {name: 'Tricky Conditions 4', x: 400, y: 315, time: 23.50},
                {name: 'Tricky Conditions 5', x: 375, y: 335, time: 25.83},
            ];
            // Shuffle and select random clips
            this.clips = dictList
                .sort(() => 0.5 - Math.random())  // Randomly shuffle
                .slice(0, 14);           // Select the first 14 clips

            this.clips.forEach(async item => {
                const input = {'filename': item.name + ".mp4"};
                const video = await this.azure_function('POST', '/question/get/video', input);
                if (video.result) {
                    // Set the playing video
                    item.url = video.msg;
                    console.log(video.msg);
                }
            });
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
            this.add_achievement('Where are you clicking lil bro','🚩');
            this.too_many_clicks = true;
            this.current_C++;
        },
        async finish_video_clip() {
            // Check if the user clicked on the appropriate (x,y) range:
            if ((this.click_x <= this.selected_clip.x + 50 && this.click_x >= this.selected_clip.x - 50) && 
                (this.click_y <= this.selected_clip.y + 50 && this.click_y >= this.selected_clip.y - 50)) {

                let interval = 1.5;

                // Then check if the user clicked at the right time:
                if (this.click_time >= this.selected_clip.time && this.click_time < this.selected_clip.time + interval) {
                    this.scores_2+=5;

                    if (this.selected_clip.name === "Urban Driving 5") {
                        this.add_achievement('Takin out the trash','🗑️');
                    } 
                    if (this.selected_clip.name === "Rural Driving 2") {
                        this.add_achievement('NEIGHHHHHH!','🐎');
                    } 
                    if (this.selected_clip.name === "Bigger Roads 1") {
                        this.add_achievement('Fireman sam','👨‍🚒');
                    } 
                    if (this.selected_clip.name === "Tricky Conditions 2") {
                        this.add_achievement('Oh deer','🦌');
                    } 
                    if (this.selected_clip.name === "Tricky Conditions 4") {
                        this.add_achievement('You snooze you lose!','💤');
                    } 

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
            this.info_message("Finished multiple choice!", "Loading hazard perception ...");
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
            this.add_achievement('Mock & Roll','📖');
            this.info_message("Finished hazard perception!", "Loading results ...");

            if (this.scores_1 === 50 && this.scores_2 === 75) {
                this.add_achievement('"Just put the license in the bag bro"','💯');
            }

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
                this.currentRank.exp_threshold += 200;
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
                    if (this.currentRank.level === 20) {
                        this.add_achievement('Absolute Bang out','🤓');
                    }
                    this.level_up_message();
                } else {
                    this.exp_message();
                }
            }
        },
        async add_update_score(topic, score) {
            // Adding score to database
            this.update_scores[topic].push(score);
        },
        async db_update_scores(user_stats) {
            let cat_scores = this.$store.state.currentRecentCatScores;
            for (let topic in this.update_scores) {
                const scores = this.update_scores[topic];
                const average = scores.length > 0
                    ? (scores.reduce((sum, val) => sum + val, 0) / scores.length)
                    : 0;
                this.averaged_scores[topic] = parseFloat(average.toFixed(2));
                cat_scores[topic].push(parseFloat(average.toFixed(2)));
                if (cat_scores.length > 10) {
                    cat_scores[topic].shift();
                }
            }
            // Update database
            const input = { 'id': user_stats.id, 'updates': this.averaged_scores }
            console.log(input);
            const update = await this.azure_function("PUT", "/user/update/scores", input)
            if (update) {
                this.$store.commit("setCurrentRecentCatScores", cat_scores);
                console.log('Updated scores!');
            }
        },
        async add_achievement(name, emoji) {
            // Add an achievement in the user's data!
            if (this.$store.state.currentAchievements.includes(name)) {
                console.log(name + " achievement already unlocked.");
                return;
            }
            const user_stats = this.$store.state.currentStats;
            const achievements = [...this.$store.state.currentAchievements, name];
            const input = { id: user_stats.id, updates: { achievements } };
            const update = await this.azure_function("PUT", "/user/update/info", input);
            if (update) {
                this.$store.commit("setCurrentAchievements", achievements);
                toastr.success(`${name} ${emoji}`, "Achievement Unlocked:", {
                closeButton: true,
                progressBar: true,
                positionClass: "toast-top-right",
                timeOut: 10000,
                showMethod: "fadeIn",
                hideMethod: "fadeOut"
                });
            }
        },
        async azure_function(method, route, body) {
            // Send a request to the function app.
            console.log(route);
            const url = `${process.env.VUE_APP_BACKEND_URL}${route}?code=${process.env.VUE_APP_MASTER_KEY}`;
            try {
                const options = {
                method,
                headers: { "Content-Type": "application/json" },
                };
                if (method !== "GET") options.body = JSON.stringify(body);
                const response = await fetch(url, options);
                const result = await response.json();
                console.log("Result:", JSON.stringify(result.result));
                return result;
            } catch (error) {
                console.error("Error:", error);
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