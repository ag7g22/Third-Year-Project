<template>
    <div class="container">
        <h1 class="title">DRIVING THEORY CATEGORY QUIZ | {{ logged_in_user }}</h1>

        <div v-if="state.current_view === 'categories'" >
            <div class="instruction-box"> 
                <p> Here are the questions organised by category. </p>
                <p> These quizzes are for self-study purposes only. </p>
            </div>
            <div class="buttons">
                <button @click="init_quiz_instructions('Driving Off')">Driving Off</button>
                <button @click="init_quiz_instructions('Urban Driving')">Urban Driving</button>
                <button @click="init_quiz_instructions('Rural Driving')">Rural Driving</button>
                <button @click="init_quiz_instructions('Bigger Roads')">Bigger Roads</button>
                <button @click="init_quiz_instructions('Motorways')">Motorways</button>
                <button @click="init_quiz_instructions('Tricky Conditions')">Tricky Conditions</button>
                <button @click="init_quiz_instructions('Breakdowns')">Breakdowns</button>
            </div>

            <div class="buttons">
                <button @click="next_page('dashboard')">Back</button>
            </div>
        </div>

        <div v-if="state.current_view === 'instructions'">
            <div class="instruction-box"> 
                <h2 class="title">{{ this.state.current_topic }}: {{ this.state.current_description }}</h2>
                <p> You will be given a select amount of questions to answer </p>
                <p> and once you click the answer immediately locks in. </p>
                <p> If you are certainly not sure, then click the explanation box. </p>
                <p> Select how many questions before you start. </p>
            </div>

            <div class="options-dropdown">
                <label for="num-questions">Select Number of Questions:</label>
                <select id="num-questions" v-model="num_questions.selected">
                <option v-for="num in num_questions.options" :key="num" :value="num">{{ num }}</option>
                </select>
                <p>You selected: {{ num_questions.selected }} questions</p>
            </div>

            <div class="buttons">
                <button @click="toggle_view('categories')">Back</button>
                <button @click="init_quiz()">Start</button>
            </div>
        </div>

        <div v-if="state.current_view === 'quiz'">
            <div class="questionnaire">
                <div v-if="currentQuestion < questions.length">
                    <h2>{{ questions[currentQuestion].question }}</h2>

                    <div v-if="questions[currentQuestion].image !== 'n/a'">
                        <img :src=image alt="Question Image">
                    </div>

                    <button @click="toggleExplanation" class="explanation-button">
                        {{ showExplanation ? "Hide Explanation" : "Show Explanation" }}
                    </button>
                    <button class="stop-button" @click="terminate_quiz()">Stop Quiz</button>

                    <div v-if="showExplanation" class="overlay" @click="toggleExplanation">
                        <div class="overlay-content" @click.stop>
                            <h2>Explanation</h2>
                            <p>{{ questions[currentQuestion].explanation }}</p>
                            <button @click="showExplanation = false">Close</button>
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
                    <h2>You've completed the questionnaire! 🎉</h2>
                    <button class="stop-button" @click="terminate_quiz()">Stop Quiz</button>
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
    name: "categoryquiz",
    data() {
        return {
            state: { current_view: 'categories', current_topic: '', current_description: '' }, // State of quiz page
            num_questions: { options: [8, 10, 12], selected: 8 }, // Dropdown menu

            // Quiz variables
            questions: [], // Quiz questions by API
            currentQuestion: 0, // Question pointer
            selectedAnswer: null, // This is the selected question
            isCorrect: false, // boolean if the question is actually correct
            showExplanation: false, // Explanation of the question

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
            this.message.error = "";
            this.message.success = "";
            this.state.current_view = view;
            this.num_questions = { options: [8, 10, 12], selected: 8 }
        },
        init_quiz_instructions(topic) {
            // Reset messages
            this.message.error = "";
            this.message.success = "";

            // Initalise the quiz instructions
            this.state.current_topic = topic;

            switch (topic) {
                case 'Driving Off':
                    this.state.current_description = 'things to consider before driving off.'
                    break;
                case 'Urban Driving':
                    this.state.current_description = 'driving in towns and cities.'
                    break;
                case 'Rural Driving':
                    this.state.current_description = 'driving in rural areas.'
                    break;
                case 'Bigger Roads':
                    this.state.current_description = 'driving in A roads and dual carriageways.'
                    break;
                case 'Motorways':
                    this.state.current_description = 'driving on the motorway.'
                    break;
                case 'Tricky Conditions':
                    this.state.current_description = 'driving at night and in bad weather.'
                    break;
                case 'Breakdowns':
                    this.state.current_description = 'breakdowns and car accidents.'
                    break;
            }
            
            this.toggle_view('instructions')
        },
        async init_quiz() {
            // Reset messages
            this.message.error = "";
            this.message.success = "";

            this.message.success = 'Loading quiz ...'

            // Initalise the quiz
            const input = { "No_of_Qs": this.num_questions.selected, "topic": this.state.current_topic }
            const quiz = await this.azure_function('POST', '/question/get/category', input);
            if (quiz.result) {
                // Populate the questions list
                this.message.success = 'Loading quiz successful!';
                this.questions = quiz.msg;

                this.add_image()

                // Switch to the quiz section
                this.toggle_view('quiz')
            } else {
                this.message.error = response.msg || "Loading quiz failed.";
            }
        },
        selectAnswer(option) {
            if (!this.selectedAnswer) {
                this.selectedAnswer = option;
                this.isCorrect = option === this.questions[this.currentQuestion].correct_answer;
            }
        },
        toggleExplanation() {
            this.showExplanation = !this.showExplanation;
        },
        nextQuestion() {
            this.selectedAnswer = null;
            this.showExplanation = false;
            this.isCorrect = false;
            this.currentQuestion++;
            if (this.currentQuestion < this.questions.length) {
               this.add_image();
            }
            
        },
        add_image() {
            // Library of images
            let question_image = this.questions[this.currentQuestion].image
            if (question_image !== 'n/a') {
                this.image = this.images.filter((image, index) => images.keys()[index].includes(question_image))[0];
            }
        },
        terminate_quiz() {
            // Reset state
            this.state = { current_view: 'categories', current_topic: '', current_description: '' }
            this.num_questions = { options: [8, 10, 12], selected: 8 }
            this.questions = []
            this.currentQuestion = 0,
            this.selectedAnswer = null,
            this.isCorrect = false,
            this.showExplanation = false,

            this.toggle_view('categories')
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
};
</script>

<style lang="scss" scoped>
img {
  width: 200px;
  height: 100px;
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

.options-dropdown {
  text-align: center;
  padding: 10px;
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

</style>