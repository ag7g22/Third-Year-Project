<template>
    <div v-if="state.current_view !== 'quiz'" class="split-container">
        <!-- Left side: Empty or can contain an image -->
        <div class="left-side">
            <div class="instructions-container">
                <h3>Time to practice specfics!</h3>
                <div class="feature-list">
                    <p>Polishing your knowledge in these areas helps ensure you understand the details of each category, which can improve your overall driving skills and safety on the road. 
                        Mastering these categories increases your chances of passing the theory exam and becoming a more confident driver.</p>
                </div>
                <h3>The quiz rules as follows:</h3>
                <div class="feature-list">
                    <p>- You are given 4 options, 1 is the correct answer.</p>
                    <p>- You can see the question explanation, but that'll lower your final score.</p>
                    <p>- The score is also time-based, the quicker the better! (You'll need to spend at most a minute per question.)</p>
                </div>
            </div>
        </div>
        <div v-if="state.current_view === 'categories'" class="right-side">
            <img src="@/assets/titles/CategoryQuiz.png" alt="Logo" class="task-logo"/>
            <div class="cat-buttons">
                <button @click="init_quiz_instructions('Driving Off')">Driving Off</button>
                <button @click="init_quiz_instructions('Urban Driving')">Urban Driving</button>
                <button @click="init_quiz_instructions('Rural Driving')">Rural Driving</button>
                <button @click="init_quiz_instructions('Bigger Roads')">Bigger Roads</button>
                <button @click="init_quiz_instructions('Motorways')">Motorways</button>
                <button @click="init_quiz_instructions('Tricky Conditions')">Tricky Conditions</button>
                <button @click="init_quiz_instructions('Breakdowns')">Breakdowns</button>
            </div>
            <div class="game-buttons">
                <button @click="next_page('dashboard')" class="game-button">Back</button>
            </div>
        </div>
        <div v-if="state.current_view === 'instructions'"  class="right-side">
            <h1>{{ state.current_topic }} {{ state.emoji }}</h1>
            <div class="description-box">
                <p>{{ state.current_description }}</p>
            </div>
            <div class="options-dropdown">
                <label for="num-questions">Select Number of Questions: </label>
                <select id="num-questions" v-model="num_questions.selected">
                <option v-for="num in num_questions.options" :key="num" :value="num">{{ num }}</option>
                </select>
            </div>
            <div class="game-buttons">
                <button @click="toggle_view('categories')" class="game-button">Back</button>
                <button @click="init_quiz()" class="game-button">Start</button>
            </div>
        </div> 
    </div>

    <div v-else>
        <div v-if="state.current_view === 'quiz'" class="container">
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
                            <button class="game-button" @click="terminate_quiz()">Stop Quiz</button>
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
                <div v-else class="quiz-result">
                    <h1>You've completed the category quiz! 🔎</h1>
                    <h1> Score: {{ percentage }}% </h1>
                    <h2> {{ quiz_message }} </h2>
                    <div class="game-buttons">
                        <div v-if="feedback.length === 0">
                            <button class="game-button" @click="terminate_quiz()">Back</button>
                        </div>
                        <div v-else>
                            <button @click="init_feedback()" class="game-button">Feedback</button> 
                        </div>
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
    name: "categoryquiz",
    data() {
        return {
            state: { current_view: 'categories', current_topic: '', current_description: '', emoji: '' }, // State of quiz page
            num_questions: { options: [5, 10, 15, 20], selected: 10 }, // Dropdown menu

            // Quiz variables
            questions: [], // Quiz questions by API
            currentQuestion: 0, // Question pointer
            selectedAnswer: null, // This is the selected answer
            isCorrect: false, // boolean if the question is actually correct
            explanation: { showExplanation: false, wasClicked: false }, // Explanation of the question, flag if it got clicked on

            // Timer
            answer_time: { elapsedTime: 0, stopwatch: null, stopwatchRunning: false },

            // Feedback
            feedback: [],
            // {question, correct_ans, selected_ans, image}

            // Score, averaged out by number of questions.
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
            this.message.error = "";
            this.message.success = "";
            this.state.current_view = view;
            this.num_questions = { options: [5, 10, 15, 20], selected: 10 }
        },
        init_quiz_instructions(topic) {
            // Reset messages
            this.message.error = "";
            this.message.success = "";

            // Initalise the quiz instructions
            this.state.current_topic = topic;

            switch (topic) {
                case 'Driving Off':
                    this.state.emoji = '🚗💨';
                    this.state.current_description = "There are a few things to consider before driving off. This includes checking your vehicle's condition, adjusting your seat and mirrors, fastening your seatbelt, and ensuring all necessary equipment like lights and wipers are functioning. It's also important to check your surroundings for any obstacles, pedestrians, or traffic. Taking these steps helps ensure safety and readiness before you begin driving."
                    break;
                case 'Urban Driving':
                    this.state.emoji = '🏙️🚙';
                    this.state.current_description = 'Driving in towns and cities requires extra attention due to the higher volume of traffic, pedestrians, cyclists, and frequent stops at traffic signals. Drivers must be alert to changing road conditions, one-way streets, parking restrictions, and the presence of other road users. Navigating these areas safely involves anticipating potential hazards and maintaining a lower, more controlled speed.'
                    break;
                case 'Rural Driving':
                    this.state.emoji = '🌳🚘';
                    this.state.current_description = "Driving in rural areas often involves quieter roads with fewer distractions, but it also comes with its own set of challenges. Drivers must be cautious of narrow, winding roads, limited visibility, and the potential for livestock or wildlife crossings. Speed limits may be higher, but it's important to stay alert for sudden changes in road conditions or unexpected obstacles."
                    break;
                case 'Bigger Roads':
                    this.state.emoji = '🛤️🚘';
                    this.state.current_description = "Driving on A roads and dual carriageways requires attention to higher speeds and more complex traffic flow. These roads often have multiple lanes, junctions, and faster-moving vehicles, so it's important to maintain a safe distance, signal early, and be prepared for lane changes. Always stay aware of speed limits and other road users to ensure a safe journey."
                    break;
                case 'Motorways':
                    this.state.emoji = '🛣️🚙';
                    this.state.current_description = "Driving on the motorway involves higher speeds and multiple lanes, requiring greater attention and concentration. It's important to maintain a safe following distance, signal when changing lanes, and observe speed limits. Drivers should be aware of joining and leaving traffic, as well as lane discipline, to ensure a smooth and safe journey for everyone."
                    break;
                case 'Tricky Conditions':
                    this.state.emoji = '🌧️❄️';
                    this.state.current_description = "Driving at night and in bad weather requires extra caution. Reduced visibility, such as in rain, fog, or snow, makes it harder to judge distances and spot hazards. It's crucial to adjust your speed, keep headlights on, and increase following distances. Always stay alert and be prepared for sudden changes in road conditions to ensure your safety and that of others."
                    break;
                case 'Breakdowns':
                    this.state.emoji = '⚠️🛠️';
                    this.state.current_description = "Breakdowns and car accidents can happen unexpectedly, so it's important to stay calm and follow the right procedures. If your vehicle breaks down, move to a safe location, turn on hazard lights, and call for roadside assistance. In case of an accident, always prioritize safety and follow legal protocols to handle these situations effectively."
                    break;
            }
            
            this.toggle_view('instructions')
        },
        async init_quiz() {
            // Reset messages
            this.message = { error: "", success: "" };

            this.message.success = 'Loading quiz ...';

            // Initalise the quiz
            const input = { "No_of_Qs": this.num_questions.selected, "topic": this.state.current_topic }
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
                await this.get_stats();
                // Update score if quiz completed:
                console.log("FINAL SCORE:", this.final_score);
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
        add_score() {
            let score = 0;
            if (this.isCorrect) { // If answered correct, calculate score based on how long was spent on that question.
                score = Math.ceil(((90 - this.answer_time.elapsedTime) / 90) * 10) / 10;
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
            this.feedback.push({question: q_obj.question, selected: this.selectedAnswer, correct: q_obj.correct_answer, image: question_image, explanation: q_obj.explanation})
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
        get_stats() {
            this.percentage = parseFloat((this.total_score / this.num_questions.selected) * 100).toFixed(1);
            this.final_score = parseFloat((this.total_score / this.num_questions.selected)).toPrecision(2);
            this.exp_gain = Math.round(((this.total_score / this.num_questions.selected) * 500) / 100) * 100; 
            console.log(this.exp_gain)
            
            if (this.final_score >= 0.9 && this.final_score < 1.0) {
                this.quiz_message = "Amazing job! You crushed it! Your hard work really paid off!"
            }
            if (this.final_score >= 0.8 && this.final_score < 0.9) {
                this.quiz_message = "Great work! You're so close to perfection—keep it up!"
            }
            if (this.final_score >= 0.7 && this.final_score < 0.8) {
                this.quiz_message = "Nice effort! You've got a solid understanding. A little more practice, and you'll master it!"
            }
            if (this.final_score >= 0.6 && this.final_score < 0.7) {
                this.quiz_message = "You're doing well! Keep going, and you'll improve even more!"
            }
            if (this.final_score >= 0.5 && this.final_score < 0.6) {
                this.quiz_message = "Good attempt! Every step is progress—keep practicing, and you'll get there!"
            }
            if (this.final_score >= 0.4 && this.final_score < 0.5) {
                this.quiz_message = "You're learning, and that's what matters! Keep challenging yourself!"
            }
            if (this.final_score >= 0.3 && this.final_score < 0.4) {
                this.quiz_message = "Not bad! Mistakes help us grow—review what you missed and try again!"
            }
            if (this.final_score < 0.3) {
                this.quiz_message = "Don't give up! Every attempt makes you better. Keep pushing forward!"
            }
        },
        async update_user_exp() {
            // Add changes to database
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
        terminate_quiz() {
            // Reset everything
            this.resetStopwatch();
            this.state = { current_view: 'categories', current_topic: '', current_description: '' } // State of quiz page
            this.num_questions = { options: [5, 10, 15, 20], selected: 10 } // Dropdown menu
            this.questions = [] // Quiz questions by API
            this.currentQuestion = 0 // Question pointer
            this.selectedAnswer = null // This is the selected question
            this.isCorrect = false, // boolean if the question is actually correct
            this.explanation = { showExplanation: false, wasClicked: false }, // Explanation of the question, flag if it got clicked on
            this.answer_time = { elapsedTime: 0, stopwatch: null, stopwatchRunning: false }
            this.feedback = []
            this.total_score = 0
            this.percentage = null
            this.final_score = null
            this.exp_gain = null
            this.quiz_message = ""
            this.scoreWasAdded = false;
            this.message = { error: "", success: "" }

            this.toggle_view('categories')
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
                    let response = await fetch( url, { method: function_type, headers: { "Content-Type": "application/json"} });
                    const API_reply = await response.json();
                    console.log("Result: " + JSON.stringify(API_reply.result));
                    return API_reply
                } else {
                    let response = await fetch( url, { method: function_type, headers: { "Content-Type": "application/json"}, body: JSON.stringify(json_doc)});
                    const API_reply = await response.json();
                    console.log("Result: " + JSON.stringify(API_reply.result));
                    return API_reply
                }

            } catch (error) {
                console.error("Error:", error);
                this.message.success = "";
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
  },
};
</script>

<style lang="scss" scoped>
</style>