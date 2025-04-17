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
const images = require.context('@/assets/questions/.', false, /\.(jpg|jpeg|png)$/);
export default {
    // Page member variables and methods:
    name: "feedback",
    mounted() {
        // Set up input to send to openai model
        this.input = this.$route.query.input || [];
        this.get_feedback_explanation();
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
        };
    },
    methods: {
        toggle_view(view) {
            // Reset state
            this.state.current_view = view;
        },
        async get_feedback_explanation() {
            // alternative method due to budget constraints:
            console.log('Generating instant feedback with explanations.');
            this.state.feedback = this.input.map(({ image, explanation, ...rest }) => ({
                feedback: explanation,
                ...rest
            }));
            this.add_image();
            this.toggle_view('feedback');
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
        next_page(page) {
            this.input = [];
            this.state = { current_view: 'loading', feedback: []};
            this.current_Q = 0;
            this.image = "";
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