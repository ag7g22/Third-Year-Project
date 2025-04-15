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
                <p>3. 🎥 Simulation: 3 Hazard Perception clips</p>
                <p>Good luck!</p>
                <h3>How the daily score works:</h3>
                <div class="feature-list">
                    <p>
                        Each time you answer a question correctly, you'll earn points based on both your speed and accuracy. 
                        Keep the streak going with consecutive correct answers, and you'll unlock a multiplier to boost your score even higher! 
                        Rack up those points and climb the leaderboard! (You get one shot a day to score on the leaderboard, but don't worry—you can still take the daily quiz for fun and practice! :p) 👑
                    </p>
                </div>
            </div>
        </div>

        <div class="right-side">
            <img src="@/assets/titles/DailyQuiz.png" alt="Logo" class="task-logo"/>
            <div v-if="completed_daily_quiz">
                <h3>Completed today's quiz: ✔️</h3>
            </div>
            <div v-else>
                <h3>Completed today's quiz: ❌</h3>
            </div>
            
            <div class="game-buttons">
                <button @click="next_page('dashboard')" class="game-button">Back</button>
                <button @click="init_daily_quiz()" class="game-button">Start</button>
            </div>
        </div>
    </div>
    <div v-else>
        <div v-if="current_view === 'quiz'" class="container">
            <div class="questionnaire">
                <div v-if="currentQuestion < questions.length">
                    <h2>Question {{ currentQuestion + 1 }} of {{ questions.length }}</h2>
                    <div class="progress-bar">
                        <div class="progress-fill" :style="{ width: progressBarWidth + '%' }"></div>
                    </div>
                    <div class="question-container">
                        <div class="question-text">
                            <h1>{{ questions[currentQuestion].question }}</h1>
                        </div>
                        <div class="question-image" v-if="questions[currentQuestion].image !== 'n/a'">
                            <img :src="image" alt="Question Image">
                        </div>
                    </div>
                    <div v-if="explanation.showExplanation" class="overlay" @click="toggleExplanation">
                        <div class="overlay-content" @click.stop>
                            <h2>Explanation (Click outside box to close)</h2>
                            <p>{{ questions[currentQuestion].explanation }}</p>
                        </div>
                    </div>
                    <div class="quiz-buttons-container">
                        <div class="quiz-buttons-grid">
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
                        <div class="game-buttons">
                            <button class="game-button" @click="terminate_daily_quiz()">Stop Quiz</button>
                            <button class="game-button" @click="toggleExplanation">
                                {{ explanation.showExplanation ? "Hide Explanation" : "Show Explanation" }}
                            </button>
                            <div v-if="selectedAnswer">
                                <button v-if="selectedAnswer" @click="nextQuestion" class="game-button">Next</button>
                            </div>
                            <div v-else>
                                <button disabled class="game-button">Next</button>
                            </div>
                        </div>
                    </div>
                </div>
                <div v-if="questions.length === 0 " class="quiz-result">
                    <h1>Loading ...</h1>
                </div>
                <div v-else class="quiz-result">
                    <h1>Finished the {{ current_part }}!</h1>
                    <h1>Moving onto the {{ next_part }}...</h1>
                    <div class="game-buttons">
                        <button  class="game-button" @click="next_section(next_part)">Next</button>
                    </div>
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

        <div v-if="current_view === 'score'" class="container">
            <div class="questionnaire">
                <div class="quiz-result">
                    <h2>You've completed the daily quiz! 💡</h2>
                    <h1> Accuracy: {{ percentage }}% | Daily score: {{ daily_score }} </h1>
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
                        <button @click="init_feedback()" class="game-button">Feedback</button> 
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
    name: "dailyquiz",
    mounted: function() {
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const date = new Date(this.$store.state.currentStats.training_completion_date);
        if ((date.getFullYear() !== today.getFullYear() || date.getMonth() !== today.getMonth() || date.getDate() !== today.getDate()) ||
            (this.$store.state.currentStats.training_completion_date === 'n/a')) {
            this.completed_daily_quiz = false;
        } else {
            this.completed_daily_quiz = true;
        }
    },
    data() {
        return {
            completed_daily_quiz: false,
            current_view: 'instructions', // State of quiz page
            current_part: 'Road sign section',
            next_part: 'Multiple choice section',

            // Quiz variables
            r_questions: [], // Road sign questions
            m_questions: [], // Multiple choice questions
            questions: [], // Quiz questions by API
            currentQuestion: 0, // Question pointer
            selectedAnswer: null, // This is the selected answer
            isCorrect: false, // boolean if the question is actually correct
            explanation: { showExplanation: false, wasClicked: false }, // Explanation of the question, flag if it got clicked on

            // Timer
            answer_time: { elapsedTime: 0, stopwatch: null, stopwatchRunning: false },

            // Clips
            clips: [], // {name, x, y, time}
            selected_clip: null,
            current_C: 0, // Clip pointer
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

            // Score, averaged out by number of questions.
            hazard_score: 0,
            total_score: 0,
            percentage: null,
            final_score: null,
            exp_gain: null,
            quiz_message: "",

            // Daily score is calculated with a multipler.
            daily_score: 0,
            multipler: 1,

            // Images
            images: images.keys().map(image => images(image)),
            image: "",

            logged_in_user: this.$store.state.currentUser,
            currentRank: this.$store.state.currentRank,
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
        daily_score_message(score) {
            toastr.info(`x ${this.multipler}`, `+ ${score} points!`, {
                closeButton: true,
                progressBar: true,
                preventDuplicates: false,
                positionClass: "toast-bottom-left",
                timeOut: 1000,
                showMethod: "fadeIn",
                hideMethod: "fadeOut",
            });
        },
        toggle_view(view) {
            // Reset state
            this.message = { error: "", success: "" };
            this.current_view = view;
        },
        async init_daily_quiz() {
            // Load ALL assests 
            await this.init_road_signs();
            await this.init_multiple_choice();
            await this.init_hazard_perception();

            // Switch to the quiz section, start timer for question.
            this.questions = this.r_questions;
            this.add_image();
            this.toggle_view('quiz');
            this.startStopwatch();
        },
        async init_road_signs() {
            // Initalise the road sign questions.
            const input = { "No_of_Qs": 10, "topic": "sign_question" }
            const quiz = await this.azure_function('POST', '/question/get/category', input);
            if (quiz.result) {
                // Populate the questions list
                this.r_questions = quiz.msg;
            } else {
                this.message.error = quiz.msg || "Loading quiz failed.";
            } 
        },
        async init_multiple_choice() {
            // Initalise the road sign questions.
            const input = { "No_of_Qs": 10, "topic": "no_sign_question" }
            const quiz = await this.azure_function('POST', '/question/get/category', input);
            if (quiz.result) {
                // Populate the questions list
                this.m_questions = quiz.msg;
            } else {
                this.message.error = quiz.msg || "Loading quiz failed.";
            } 
        },
        async init_hazard_perception() {
            // Fetch the 3 clips:
            const dictList = [
                {name: 'Urban Driving 1', x: 370, y: 270, time: 15.25}, {name: 'Urban Driving 2', x: 540, y: 270, time: 18.00}, {name: 'Urban Driving 3', x: 410, y: 260, time: 29.00}, {name: 'Urban Driving 4', x: 415, y: 260, time: 37.60}, {name: 'Urban Driving 5', x: 350, y: 260, time: 29.00}, {name: 'Rural Driving 1', x: 490, y: 220, time: 47.00},
                {name: 'Rural Driving 2', x: 250, y: 250, time: 31.00}, {name: 'Rural Driving 3', x: 395, y: 230, time: 17.50}, {name: 'Rural Driving 4', x: 450, y: 290, time: 13.45}, {name: 'Rural Driving 5', x: 295, y: 240, time: 37.85}, {name: 'Bigger Roads 1', x: 415, y: 250, time: 13.90}, {name: 'Bigger Roads 2', x: 425, y: 240, time: 14.55},
                {name: 'Bigger Roads 3', x: 510, y: 260, time: 26.30}, {name: 'Bigger Roads 4', x: 500, y: 245, time: 21.45}, {name: 'Motorways 1', x: 25, y: 190, time: 2.55}, {name: 'Motorways 2', x: 320, y: 250, time: 25.45}, {name: 'Motorways 3', x: 690, y: 290, time: 30.20}, {name: 'Tricky Conditions 1', x: 110, y: 250, time: 17.10},
                {name: 'Tricky Conditions 2', x: 515, y: 240, time: 31.80}, {name: 'Tricky Conditions 3', x: 280, y: 254, time: 33.45}, {name: 'Tricky Conditions 4', x: 325, y: 235, time: 22.70}, {name: 'Tricky Conditions 5', x: 320, y: 255, time: 24.00}
            ];
            // Shuffle and select random clips
            this.clips = dictList
                .sort(() => 0.5 - Math.random())  // Randomly shuffle
                .slice(0, 3);           // Select the first 3 clips
            this.clips.forEach(async item => {
                const input = {'filename': item.name + ".mp4"};
                const video = await this.azure_function('POST', '/question/get/video', input);
                if (video.result) {
                    // Set the playing video
                    item.url = video.msg;
                    console.log(video.msg);
                }
            });
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
            }
        },
        async next_section(section) {
            // Transition to next section:
            if (section === "Multiple choice section") {
                // Move to multiple choice:
                this.current_part = 'Multiple choice section';
                this.next_part = 'Hazard Perception section';

                // RESET QUIZ VARIABLES
                this.currentQuestion = 0;
                this.selectedAnswer = null;
                this.isCorrect = false;
                this.explanation = { showExplanation: false, wasClicked: false };
                this.answer_time = { elapsedTime: 0, stopwatch: null, stopwatchRunning: false };

                // Switch to the quiz section, start timer for question.
                this.questions = this.m_questions;
                this.add_image();
                this.toggle_view('quiz');
                this.startStopwatch();

            } else if (section === "Hazard Perception section") {
                // Move to hazard perception:
                this.current_part = 'Hazard Perception section.';
                this.next_part = "Results";
                // Start the hazard perception section
                this.load_video_clip();
                this.toggle_view('hazard_perception');

            } else if (section === "Results") {
                // Calculate the scores for upload.
                await this.get_stats();
                console.log("FINAL SCORE:", this.final_score);

                // Update user stats:
                const user_stats = this.$store.state.currentStats;
                await this.update_streak(user_stats);
                await this.update_daily_score(user_stats);
                await this.update_training_completion_date(user_stats);
                await this.update_user_exp(user_stats);
                await this.db_update_scores(user_stats);

                this.toggle_view('score');
            }
        },
        async update_streak(user_stats) {
            if (user_stats.training_completion_date === 'n/a') {
                user_stats.streak+=1;
                console.log('Started streak.');
                return;
            }
            // Get user's completion date, today's date and yesterday's date
            const tcd = new Date(user_stats.training_completion_date);
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            const yesterday = new Date(today);
            yesterday.setDate(today.getDate() - 1);

            if (tcd.getFullYear() === yesterday.getFullYear() && tcd.getMonth() === yesterday.getMonth() && tcd.getDate() === yesterday.getDate()) {
                // If a day hasn't past yet, increase the streak.
                user_stats.streak+=1;
                console.log('Incremented streak.');
            } else if (tcd.getFullYear() === today.getFullYear() && tcd.getMonth() === today.getMonth() && tcd.getDate() === today.getDate()) {
                // If they did their daily quiz, don't increase the streak.
                console.log('Already did daily quiz!');
            } else {
                // If they missed the daily quiz, set to zero.
                user_stats.streak = 0;
                console.log('Restarted streak.');
            }
        },
        async update_daily_score(user_stats) {
            if (!this.completed_daily_quiz) {
                console.log('Updated daily training score!');
                user_stats.daily_training_score = this.daily_score;  
            } else {
                console.log('Keeping original daily training score!');
            }
        },
        async update_training_completion_date(user_stats) {
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            const year = today.getFullYear();
            const month = String(today.getMonth() + 1).padStart(2, '0'); // months are 0-indexed
            const day = String(today.getDate()).padStart(2, '0');
            user_stats.training_completion_date = `${year}-${month}-${day}`;
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
                console.log(this.clip_url);
            } else {
                this.next_section(this.next_part);
            }
        },
        click_fail() {
            // Run this method if the user clicks more than 10 times
            const video = this.$refs.hazard_perception;
            video.pause();
            this.too_many_clicks = true;
            this.current_C++;

            // Add update score
            const topic = this.selected_clip.name.replace(/\s\d+$/, '');
            this.add_update_score(topic, 0);
        },
        async finish_video_clip() {
        // Check if the user clicked on the appropriate (x,y) range:
        if ((this.click_x <= this.selected_clip.x + 50 && this.click_x >= this.selected_clip.x - 50) && 
            (this.click_y <= this.selected_clip.y + 50 && this.click_y >= this.selected_clip.y - 50)) {
            let interval = 1;
            // Then check if the user clicked at the right time:
            let score = 0
            if (this.click_time >= this.selected_clip.time && this.click_time < this.selected_clip.time + interval) {
                score = 1;
                this.multipler+=1;
            } else if (this.click_time >= this.selected_clip.time + interval && this.click_time < this.selected_clip.time + interval*2) {
                score = 0.8;
                this.multipler = 1;
            } else if (this.click_time >= this.selected_clip.time + interval*2 && this.click_time < this.selected_clip.time + interval*3) {
                score = 0.6;
                this.multipler = 1;
            } else if (this.click_time >= this.selected_clip.time + interval*3 && this.click_time < this.selected_clip.time + interval*4) {
                score = 0.4;
                this.multipler = 1;
            } else if (this.click_time >= this.selected_clip.time + interval*4 && this.click_time < this.selected_clip.time + interval*5) {
                score = 0.2;
                this.multipler = 1;
            } else {
                this.multipler = 1;
            }
            const topic = this.selected_clip.name.replace(/\s\d+$/, '');
            this.add_update_score(topic, score);
            this.total_score += score;
            console.log(`Added score: ${score}, Total Score: ${this.total_score}`)

            // Add mulitpled score to daily score.
            this.daily_score += score * this.multipler * 100;
            this.daily_score_message(score * this.multipler * 100);
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
        terminate_daily_quiz() {
            // End the quiz early
            this.resetStopwatch();
            this.completed_daily_quiz = false;
            this.current_part = 'Road sign section';
            this.next_part = 'Multiple choice section';
            this.r_questions = []; // Road sign questions
            this.m_questions = []; // Multiple choice questions
            this.questions = []; // Quiz questions by API
            this.currentQuestion = 0; // Question pointer
            this.selectedAnswer = null; // This is the selected answer
            this.isCorrect = false; // boolean if the question is actually correct
            this.explanation = { showExplanation: false, wasClicked: false }; // Explanation of the question, flag if it got clicked on
            this.answer_time = { elapsedTime: 0, stopwatch: null, stopwatchRunning: false },
            this.clips = [], // {name, x, y, time}
            this.selected_clip = null,
            this.current_C = 0, // Clip pointer
            this.clip_url = '',
            this.click_x = 0,
            this.click_y = 0,
            this.click_time = 0,
            this.click_history = [],
            this.clicks = [],
            this.too_many_clicks = false,
            this.feedback = [],
            this.update_scores = {"Driving Off": [], "Urban Driving": [],"Rural Driving": [],"Bigger Roads": [],"Motorways": [],"Tricky Conditions": [],"Breakdowns": [],},
            this.averaged_scores = {},
            this.total_score = 0,
            this.percentage = null,
            this.final_score = null,
            this.exp_gain = null,
            this.quiz_message = "",
            this.image = "",
            this.daily_score = 0,
            this.multipler = 1,


            this.toggle_view('instructions');
        },
        add_score() {
            let score = 0;
            if (this.isCorrect) { // If answered correct, calculate score based on how long was spent on that question.
                score = Math.ceil(((90 - this.answer_time.elapsedTime) / 90) * 10) / 10;
                this.multipler+=1;
            }
            if (this.explanation.wasClicked) { // If the explanation was toggled, cap the score to 0.1.
                score = 0.1;
                this.multipler = 1;
            } 
            if (!this.isCorrect) { // If not answered correct, add nothing to the score.
                score = 0;
                this.multipler = 1;
                this.add_feedback();
            }
            // Add to category score
            const topic = this.questions[this.currentQuestion].topic;
            this.add_update_score(topic, score);
            this.total_score += score;
            console.log(`Time taken: ${this.answer_time.elapsedTime}, Added score: ${score}, Total Score: ${this.total_score}`)

            // Add mulitpled score to daily score.
            this.daily_score += score * this.multipler * 100;
            this.daily_score_message(score * this.multipler * 100);
        },
        add_feedback() {
            // Add to feedback list to send to API later
            let question_image = this.questions[this.currentQuestion].image
            let q_obj = this.questions[this.currentQuestion]
            console.log('Added feedback for Question ' + this.currentQuestion);
            this.feedback.push({question: q_obj.question, selected: this.selectedAnswer, correct: q_obj.correct_answer, image: question_image, explanation: q_obj.explanation})
        },
        add_update_score(topic, score) {
            // Adding score to database
            console.log(`Adding score for ${topic}: ${score}`);
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
            let input = this.feedback;
            this.terminate_daily_quiz();
            console.log("/feedback");
            this.$router.push({
                path: `/feedback`,
                query: { input: input }
            })
        },
        get_stats() {
            this.percentage = parseFloat((this.total_score / 23) * 100).toFixed(1);
            this.final_score = parseFloat((this.total_score / 23)).toPrecision(2);
            this.exp_gain = Math.round(((this.total_score / 23) * 500) / 100) * 100; 
            console.log(this.exp_gain)
        },
        async update_user_exp(user_stats) {
            // Add changes to database
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
            // Only update rank if they already did the daily quiz!
            let input = { id: user_stats.id, updates: { "rank": this.currentRank } };
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            if (!this.completed_daily_quiz) {// Only update exp
                input = { id: user_stats.id, updates: { 
                    "rank": this.currentRank,
                    "streak": user_stats.streak,
                    "daily_training_score": user_stats.daily_training_score,
                    "training_completion_date": user_stats.training_completion_date
                } };
                this.completed_daily_quiz = true;
            }
            console.log(input);

            const update_response = await this.azure_function("PUT", "/user/update/info", input);
            // Show message incase the API response fails, otherwise update state.
            if (update_response.result) {
                // Update rank in UI too.
                this.$store.commit("setCurrentRank", this.currentRank);
                this.$store.commit("setCurrentStats", user_stats);
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
</style>