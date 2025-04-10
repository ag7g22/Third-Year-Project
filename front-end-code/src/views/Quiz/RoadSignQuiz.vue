<template>
    <div v-if="current_view === 'instructions'" class="split-container">
        <div class="left-side">
            <div class="instructions-container">
                <h3>WHY ARE THERE SO MANY ROAD SIGNS!?!</h3>
                <p>It's important to memorize these signs because they help ensure safety on the road by making you aware of potential hazards, speed limits, and important regulations. 
                    Knowing road signs is essential for passing the driving theory exam and driving safely in real-life situations.</p>
                <h3>The quiz rules as follows:</h3>
                <div class="feature-list">
                    <p>- You are given 4 options, 1 is the correct answer.</p>
                    <p>- You can see the question explanation, but that'll lower your final score.</p>
                    <p>- The score is also time-based, the quicker the better! (You'll need to spend at most a minute per question.)</p>
                </div>
                <p>Good luck!</p>
            </div>
        </div>
        <div class="right-side">
            <img src="@/assets/titles/RoadSign.png" alt="Logo" class="task-logo"/>
            <div class="options-dropdown">
                <label for="num-questions">Select Number of Questions: </label>
                <select id="num-questions" v-model="num_questions.selected">
                <option v-for="num in num_questions.options" :key="num" :value="num">{{ num }}</option>
                </select>
            </div>

            <div class="game-buttons">
                <button @click="next_page('dashboard')" class="game-button">Back</button>
                <button @click="init_quiz()" class="game-button">Start</button>
            </div>
        </div>
    </div>
    
    <div v-else>
        <div v-if="current_view === 'quiz'" class="container">
            <div class="questionnaire">
                <div v-if="currentQuestion < questions.length">
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
                    <button class="stop-button" @click="terminate_quiz()">Stop Quiz</button>

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
                    <h2>You've completed the road sign quiz! 🎉</h2>
                    <h3> Score: {{ percentage }}% </h3>
                    <p> {{ quiz_message }} </p>
                    <button v-if="updateFinished" class="stop-button" @click="terminate_quiz()">Back</button>
                    <button @click="init_feedback()">Feedback</button>
                </div>
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
    name: "roadsignquiz",
    data() {
        return {
            current_view: 'instructions',
            num_questions: { options: [8, 10, 12], selected: 8 }, // Dropdown menu

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

            logged_in_user: this.$store.state.currentUser,
            message: { error: "", success: "" },
        };
    },
    methods: {
        toggle_view(view) {
            // Reset state
            this.message.error = "";
            this.message.success = "";
            this.current_view = view;
            this.num_questions = { options: [8, 10, 12], selected: 8 }
        },
        async init_quiz() {
            // Reset messages
            this.message.error = "";
            this.message.success = "";

            this.message.success = 'Loading road quiz ...'

            // Initalise the quiz
            const input = { "No_of_Qs": this.num_questions.selected, "topic": "sign_question" }
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
        get_stats() {
            this.percentage = parseFloat((this.total_score / this.num_questions.selected) * 100).toPrecision(2);
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
                    this.message.success = `LEVELED UP TO LEVEL ${this.currentRank.level}!` 
                } else {
                    this.message.success = `Gained ${this.exp_gain} exp!`
                }

            } else {
                this.message.error = update_response.msg || "Score update Failed."
            }
        },
        terminate_quiz() {
            // Reset everything
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

            this.toggle_view('instructions')
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

.options-dropdown {
    color: white;
    text-align: center;
    padding: 10px;
}

#num-questions {
    background-color: rgb(20, 20, 20);
    color: #f3af59;
    border: 1px solid #f3af59;
    padding: 5px;
}

#num-questions option {
    background-color: rgb(20, 20, 20);
    color: #f3af59;
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
</style>