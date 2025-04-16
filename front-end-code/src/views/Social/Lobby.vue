<template>
    <div v-if="state.current_view !== 'GAME' && state.current_view !== 'GAMEOVER'" class="split-container">
        <div class="left-side">
            <div class="instructions-container">
                <h3>Win the CRASH OFF or CRASH OUT 🤬</h3>
                <p>Crash Quiz-Off is a high-speed, 1v1 battle where two drivers face off to see who can answer driving theory questions the fastest and most accurately. 
                    It's like a race—except instead of speedometers, you're racing against the clock and your brain! Buckle up, it's time to prove who's the real road genius!</p>
                <h3>The Crash Quiz-Off rules are as follows:</h3>
                <div class="feature-list">
                    <p>- You will both be given time to read a question.</p>
                    <p>- After a countdown, you will be given 4 options in the question.</p>
                    <p>- You will win the round if you're the fastest and most correct!</p>
                    <p>- The bar will fill up on the winner's side and if it fills up, you WIN!</p>
                </div>
                <p>Hope you're not the loser!</p>
            </div>
        </div>
        <div class="right-side">
            <div v-if="state.current_view === 'HOST'">
                <img src="@/assets/titles/CrashQuizOff.png" alt="Logo" class="task-logo"/>
                <h2> Create a HOST password </h2>
                <input type="text" placeholder="password" v-model="host_password" />
                <button @click="create_game()" class="game-button">Create Game</button>
                <div class="game-buttons">
                    <button @click="next_page('dashboard')" class="game-button">Back</button>
                    <button disabled class="game-button">Host</button>
                    <button @click="toggle_view('JOIN')" class="game-button">Join</button>
                </div>
            </div>

            <div v-if="state.current_view === 'JOIN'">
                <img src="@/assets/titles/CrashQuizOff.png" alt="Logo" class="task-logo"/>
                <h2> Enter a HOST password </h2>
                <input type="text" placeholder="password" v-model="host_password" />
                <button @click="join_game()" class="game-button">Join Game</button>
                <div class="game-buttons">
                    <button @click="next_page('dashboard')" class="game-button">Back</button>
                    <button @click="toggle_view('HOST')" class="game-button">Host</button>
                    <button disabled class="game-button">Join</button>
                </div>
            </div>

            <div v-if="state.current_view === 'LOBBY'">
                <h2>HOST: {{ game_state.host }} | PASSWORD: {{ game_state.password }}</h2>
                <div class="players-list">
                    <div v-for="player in game_state.players" class="player-item">
                        <p>{{ player }}</p>
                    </div>
                </div>
                <div v-if="state.role === 'HOST'">
                    <div class="game-buttons" v-if="game_state.players.length > 1">
                        <button @click="start_game()" class="game-button">Start</button>
                        <button @click="delete_game()" class="game-button">Leave</button>    
                    </div>
                    <div class="game-buttons" v-else>
                        <button @click="delete_game()" class="game-button">Leave</button>   
                    </div>
                </div>
                <div v-else class="game-buttons"> 
                    <button @click="leave_lobby()" class="game-button">Leave</button>
                </div>
                
            </div>
        </div>
    </div>
    <div v-else>
        <div v-if="state.current_view === 'GAME'" class="container">
            <div class="questionnaire">
                <!-- Count down for game -->
                <div v-if="game_timer !== null" class="quiz-result">
                    <h1> GAME STARTS IN: </h1>
                    <h1>{{ countdown }}</h1>
                </div>
                <div v-else>
                    <div v-if="end_of_round_timer !== null">
                        <h2> Question {{ game_state.q_counter - 1}} </h2>
                    </div>
                    <div v-else-if="end_of_round_timer === null">
                        <h2> Question {{ game_state.q_counter }} </h2>
                    </div>
                    <div class="progress-container">
                        <!-- Player 1 (Left Side) -->
                        <div class="player player-left">{{ game_state.home.username }}</div>
                        <!-- Progress Bar -->
                        <div class="progress-bar">
                            <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
                        </div>
                        <!-- Player 2 (Right Side) -->
                        <div class="player player-right">{{ game_state.away.username }}</div>
                    </div>

                    <div v-if="end_of_round_timer !== null" class="question-container">
                        <div class="question-text">
                            <h1>{{ game_state.questions[game_state.currentQuestion - 1].question }}</h1>
                        </div>
                        <div class="question-image" v-if="game_state.questions[game_state.currentQuestion - 1].image !== 'n/a'">
                            <img :src="image" alt="Question Image">
                        </div>
                    </div>
                    <div v-else-if="end_of_round_timer === null" class="question-container">
                        <div class="question-text">
                            <h1>{{ game_state.questions[game_state.currentQuestion].question }}</h1>
                        </div>
                        <div class="question-image" v-if="game_state.questions[game_state.currentQuestion].image !== 'n/a'">
                            <img :src="image" alt="Question Image">
                        </div>
                    </div>

                    <!-- Count down for question -->
                    <div v-if="question_timer !== null" class="feedback-box">
                        <h1>{{ countdown }}</h1>
                    </div>
                    <!-- Show results for a few seconds -->
                    <div v-else-if="end_of_round_timer !== null" class="feedback-box">
                        <div v-if="user_state.selected_answer === game_state.questions[game_state.currentQuestion - 1].correct_answer" class="answer-row">
                            <p class="correct">{{ user_state.selected_answer }}✔️</p>
                        </div>
                        <div v-else class="answer-row">
                            <p class="incorrect">{{ user_state.selected_answer }}❌</p>
                            <p class="correct">{{ game_state.questions[game_state.currentQuestion - 1].correct_answer }}✔️</p>
                        </div>
                        <div class="feedback-text">
                            <h3>{{ game_state.questions[game_state.currentQuestion - 1].explanation }}</h3>
                        </div>
                    </div>
                    <div v-else class="quiz-buttons-container">
                        <div class="quiz-buttons-grid">
                            <button 
                            v-for="(option, index) in game_state.questions[game_state.currentQuestion].options"
                            :key="index"
                            :class="{
                                selected: user_state.selected_answer === option && user_state.isWaiting,
                            }"
                            @click="select_answer(option)"
                            >
                            {{ option }}
                            </button>
                        </div>
                    </div>

                    <!-- Buttons -->
                    <div class="game-buttons">
                        <button class="game-button" @click="leave_game(false)">Concede</button>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="state.current_view === 'GAMEOVER'" class="container">
            <div class="questionnaire">
                <div class="quiz-result">
                    <div v-if="user_state.isWinner === true">
                        <h1> VICTORY! 🎉</h1>
                    </div>
                    <div v-else>
                        <h1> DEFEATED! ⚰️</h1>
                    </div>
                    <div class="game-buttons">
                        <button class="game-button" @click="return_lobby()">Lobby</button>  
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
    name: "lobby",
    mounted() {
        this.setup_socket_listeners();
    },
    unmounted() {
        this.remove_socket_listeners();
    },
    data() {
        return {
            state: { current_view: "HOST", role: 'HOST' },

            // Password to join a hosted game
            host_password: '', 
            
            // States updated by server:
            game_state: {host: '', password: '', players: [], state: 0, questions: [], currentQuestion: 0, q_counter: 1, 
            home: { username: '', chances: 3, elapsedTime: 0, selected_answer: null }, 
            away: { username: '', chances: 3, elapsedTime: 0, selected_answer: null }},

            user_state: {username: '', host: '', role: '', isWinner: false, isCorrect: false, isWaiting: false, selected_answer: null},

            // Timer for user answering question
            answer_time: { elapsedTime: 0, stopwatch: null, stopwatchRunning: false },

            countdown: null, // Number of seconds in timer
            question_timer: null, // Timer before the answers show up.
            game_timer: null, // Timer before the game starts.
            end_of_round_timer: null, // Timer after the round finishes.

            // Images
            images: images.keys().map(image => images(image)),
            image: "",

            client_socket: this.$store.state.currentClientSocket,
            logged_in_user: this.$store.state.currentUser,
            currentRank: this.$store.state.currentRank,
            message: { error: "", success: "" },
        };
    },
    methods: {
        exp_message(exp_gain) {
            if (exp_gain === 0) return;
            toastr.info(" ", `Gained ${exp_gain} exp!`, {
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
        successful_message(title, msg) {
            toastr.success(msg, title, {
            closeButton: true,
            progressBar: true,
            positionClass: "toast-bottom-full-width",
            timeOut: 3000,
            showMethod: "fadeIn",
            hideMethod: "fadeOut",
            preventDuplicates: true
            });
        },
        error_message(title, msg) {
        toastr.error(msg, title, {
            closeButton: true,
            progressBar: true,
            positionClass: "toast-bottom-full-width",
            timeOut: 3000,
            showMethod: "fadeIn",
            hideMethod: "fadeOut",
            preventDuplicates: true
            });
        },
        toggle_view(view) {
            // Reset state
            this.message = { error: "", success: "" };
            this.state.current_view = view;
            if (view === "HOST") {
                this.state.role = "HOST"
            } else if (view === "JOIN") {
                this.state.role = "PLAYER"
            }
        },
        // LOBBY METHODS
        reset_states() {
            // Run this when leaving a lobby
            this.state = { current_view: "HOST", role: 'HOST' };
            this.host_password = '';
            this.game_state = {host: '', password: '', players: [], state: 0, questions: [], currentQuestion: 0, q_counter: 1, 
            home: { username: '', chances: 3, elapsedTime: 0, selected_answer: null }, 
            away: { username: '', chances: 3, elapsedTime: 0, selected_answer: null }};
            this.user_state = {username: '', host: '', role: '', isWinner: false, isCorrect: false, isWaiting: false, selected_answer: null};

        },
        start_game() {
            // Tell server that game is starting.
            this.client_socket.emit('start-game', this.logged_in_user);
        },
        create_game() {
            // Send to server to register game.
            this.message.error = "";
            this.message.success = "";
            const password = this.host_password;
            this.host_password = '';
            this.client_socket.emit('create-lobby', this.logged_in_user, password);
        },
        delete_game() {
            // Send to server to remove game.
            this.reset_states();
            this.client_socket.emit('delete-lobby', this.logged_in_user);
        },
        join_game() {
            // Send to server to join game.
            this.message.error = "";
            this.message.success = "";
            const password = this.host_password;
            this.host_password = '';
            this.client_socket.emit('join-lobby', this.logged_in_user, password);
        },
        leave_lobby() {
            // Send to server to leave lobby.
            const host = this.user_state.host;
            this.reset_states();
            this.client_socket.emit('leave-lobby', this.logged_in_user, host);
        },
        leave_game(isWinner) {
            this.isWinner = isWinner;
            this.add_achievement('The Crash-out King','🥀');
            // Remove players from game and end game.
            this.client_socket.emit('leave-game', this.logged_in_user, this.game_state.host);
        },
        return_lobby() {
            // RESET STATES
            this.message = { error: "", success: "" }
            this.game_state = {host: '', password: '', players: [], state: 0, questions: [], currentQuestion: 0, q_counter: 1, 
            home: { username: '', chances: 3, elapsedTime: 0, selected_answer: null }, 
            away: { username: '', chances: 3, elapsedTime: 0, selected_answer: null }}
            this.user_state = {username: '', host: '', role: '', isWinner: false, isCorrect: null, isWaiting: false, selected_answer: null};
            this.state = { current_view: "HOST", role: 'HOST', gamemodes: ['quiz', 'hazard perception', 'road sign'], selected_gamemode: 'quiz' }
        },
        // GAME METHODS
        async load_quiz() {
            // Load the quiz for both users
            this.opponent_user = this.game_state.players.find(player => player !== this.logged_in_user);
            this.toggle_view('GAME');
            await this.start_game_countdown(5);
        },
        select_answer(option) {
            // Selecting an answer and locking it in, send to server.
            if (!this.user_state.selected_answer) {
                this.stopStopwatch();
                this.user_state.selected_answer = option;
                this.client_socket.emit('selected-answer', this.user_state.selected_answer, this.answer_time.elapsedTime, this.game_state.host);
                this.resetStopwatch();
            }
        },
        async end_of_round(winner) {
            // Show both users the results
            if (winner === this.logged_in_user) {
                toastr.success(" ", "You WIN the round!", {
                    closeButton: true,
                    progressBar: true,
                    positionClass: "toast-top-right",
                    timeOut: 4000,
                    showMethod: "fadeIn",
                    hideMethod: "fadeOut",
                    preventDuplicates: true
                });
            } else if (winner === "tie") {
                toastr.warning(" ", "Round Tie!", {
                    closeButton: true,
                    progressBar: true,
                    positionClass: "toast-top-right",
                    timeOut: 4000,
                    showMethod: "fadeIn",
                    hideMethod: "fadeOut",
                    preventDuplicates: true
                });
            } else {
                toastr.error(" ", `${winner} WINS the round!`, {
                    closeButton: true,
                    progressBar: true,
                    positionClass: "toast-top-right",
                    timeOut: 4000,
                    showMethod: "fadeIn",
                    hideMethod: "fadeOut",
                    preventDuplicates: true
                });
            }
            await this.start_end_round_countdown(7);
        },
        async end_of_game(winner) {
            // Show both users the results
            this.add_achievement('1 v 1 me rn m8','💥');
            this.message = { error: "", success: "" }
            if (winner === this.logged_in_user) {
                this.add_achievement('The Crash-off King','👑');
                this.user_state.isWinner = true;
                toastr.success(" ", "You WIN the game!", {
                    closeButton: true,
                    progressBar: true,
                    positionClass: "toast-top-right",
                    timeOut: 4000,
                    showMethod: "fadeIn",
                    hideMethod: "fadeOut",
                    preventDuplicates: true
                });
            } else {
                this.add_achievement('The Humble King','🏳️');
                this.user_state.isWinner = false;
                toastr.error(" ", `${winner} WINS the game!`, {
                    closeButton: true,
                    progressBar: true,
                    positionClass: "toast-top-right",
                    timeOut: 4000,
                    showMethod: "fadeIn",
                    hideMethod: "fadeOut",
                    preventDuplicates: true
                });
            }
            await this.start_end_game_countdown(7, winner);
        },
        async next_question() {
            // Transition client to next question.
            this.message = { error: "", success: "" }
            this.client_socket.emit('next-question', this.user_state.host);
            await this.start_question_countdown(5);
        },
        async start_game_countdown(countdown) {
            // Pick the timer and countdown setting
            this.countdown = countdown;
            this.game_timer = setInterval(async () => {
                if (this.countdown > 0) {
                    this.countdown--;
                } else {
                    if (this.game_timer) {
                        clearInterval(this.game_timer);
                        this.game_timer = null;
                        this.countdown = null;
                        console.log("Starting game ... ");
                        await this.start_question_countdown(5);
                    }
                }
            }, 1000);
        },
        async start_question_countdown(countdown) {
            // Pick the timer and countdown setting
            this.add_image();
            this.countdown = countdown;
            this.question_timer = setInterval(() => {
                if (this.countdown > 0) {
                    this.countdown--;
                } else {
                    if (this.question_timer) {
                        clearInterval(this.question_timer);
                        this.question_timer = null;
                        this.countdown = null;
                        console.log("Showing answers ... ");
                        this.startStopwatch();
                    }
                }
            }, 1000);
        },
        async start_end_round_countdown(countdown) {
            // Pick the timer and countdown setting
            this.countdown = countdown;
            this.end_of_round_timer = setInterval(async () => {
                if (this.countdown > 0) {
                    this.countdown--;
                } else {
                    if (this.end_of_round_timer) {
                        clearInterval(this.end_of_round_timer);
                        this.end_of_round_timer = null;
                        this.countdown = null;
                        console.log("Showing next question ... ");
                        this.next_question();
                    }
                }
            }, 1000);
        },
        async start_end_game_countdown(countdown, winner) {
            // Pick the timer and countdown setting
            this.countdown = countdown;
            this.end_of_round_timer = setInterval(async () => {
                if (this.countdown > 0) {
                    this.countdown--;
                } else {
                    if (this.end_of_round_timer) {
                        clearInterval(this.end_of_round_timer);
                        this.end_of_round_timer = null;
                        this.countdown = null;
                        console.log("Ending game ... ");
                        this.client_socket.emit('leave-game', this.logged_in_user, this.game_state.host, this.user_state.isWinner);
                        if (this.logged_in_user === winner) {
                            this.update_user_exp(500);
                        } else {
                            this.update_user_exp(100);
                        }
                    }
                }
            }, 1000);
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
        add_image() {
            // Library of images
            let question_image = this.game_state.questions[this.game_state.currentQuestion].image
            if (question_image !== 'n/a') {
                this.image = this.images.filter((image, index) => images.keys()[index].includes(question_image))[0];
            }
        },
        async add_achievement(name, emoji) {
            // Add an achievement in the user's data!
            if (this.$store.state.currentAchievements.includes(name)) {
                console.log("Already gotten the " + name + " achievement!")
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
        async update_user_exp(exp_gain) {
            // Add changes to database
            const user_stats = this.$store.state.currentStats;
            const prev_level = this.currentRank.level;

            // Increment level if exp exceeds threshold:
            if (this.currentRank.exp + exp_gain >= this.currentRank.exp_threshold) {
                // Reset exp progress but add leftover exp and update exp threshold
                this.currentRank.exp = (this.currentRank.exp + exp_gain) - this.currentRank.exp_threshold;
                this.currentRank.level += 1;
                this.currentRank.exp_threshold += 500;
            } else {
                this.currentRank.exp += exp_gain;
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
                    this.exp_message(exp_gain);
                }
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
            this.$router.replace(`/${page}`);
        },
        setup_socket_listeners() {
            if (!this.client_socket) return;

            this.remove_socket_listeners(); // Clean slate

            this.client_socket.on('update-user', (data) => {
                this.game_state = data.game_state;
                this.user_state = data.user_state; 
            });

            this.client_socket.on('create-lobby-fail', () => {
                this.error_message('Lobby creation failed!', "Password already being used.");
            });

            this.client_socket.on('create-lobby-success', () => {
                this.toggle_view('LOBBY');
                this.successful_message('Lobby creation success!', 'Share password for another player to join.');
            });

            this.client_socket.on('remove-player', () => {
                this.toggle_view('HOST');
                this.error_message('Lobby was terminated!', "Host left game.");
            });

            this.client_socket.on('join-lobby-success', () => {
                this.toggle_view('LOBBY');
                this.successful_message('Joined lobby!', 'Waiting for host ...');
            });

            this.client_socket.on('lobby-full', () => {
                this.error_message('Failed to join lobby!', 'Game in progress.');
            });

            this.client_socket.on('join-lobby-fail', () => {
                this.error_message('Failed to join lobby!', 'No lobby found.');
            });

            this.client_socket.on('start-game-success', () => {
                this.load_quiz();
            });

            this.client_socket.on('start-game-fail', () => {
                this.error_message('Failed to start game!', 'Failed to load questions. Try again.');
            });

            this.client_socket.on('selected-answer-waiting', () => {
                toastr.info("Waiting for other player to answer ...", "Answered question!", {
                    closeButton: true,
                    progressBar: true,
                    positionClass: "toast-top-right",
                    timeOut: 3000,
                    showMethod: "fadeIn",
                    hideMethod: "fadeOut",
                    preventDuplicates: true
                });
            });

            this.client_socket.on('end-of-round', (winner) => {
                this.end_of_round(winner);
            });

            this.client_socket.on('end-of-game', (winner) => {
                this.end_of_game(winner);
            });

            this.client_socket.on('next-question', () => {
                this.next_question();
            });

            this.client_socket.on('leave-game-success', () => {
                this.toggle_view('GAMEOVER');
            });
        },
        remove_socket_listeners() {
            if (!this.client_socket) return;

                this.client_socket.off('update-user');
                this.client_socket.off('create-lobby-fail');
                this.client_socket.off('create-lobby-success');
                this.client_socket.off('remove-player');
                this.client_socket.off('join-lobby-success');
                this.client_socket.off('lobby-full');
                this.client_socket.off('join-lobby-fail');
                this.client_socket.off('start-game-success');
                this.client_socket.off('start-game-fail');
                this.client_socket.off('selected-answer-waiting');
                this.client_socket.off('end-of-round');
                this.client_socket.off('end-of-game');
                this.client_socket.off('next-question');
                this.client_socket.off('leave-game-success');
            },
    },
    computed: {
        progressPercentage() {
        return (this.game_state.home.chances / 6) * 100;
    }
  }
};
</script>

<style lang="scss" scoped>
.players-list {
  display: flex;
  gap: 20px; /* Space between player names */
  overflow-x: auto; /* Allow horizontal scrolling if too many players */
  padding: 10px;
  background-color: black;
  border: 2px solid #f3af59;
  justify-content: center;
  border-radius: 10px; /* Rounded corners for the container */
}

.player-item {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px 20px;
  background-color: none;
  border: none;
  color: #f3af59;
}

.progress-container {
    color: white;
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 80%;
    position: relative;
    margin: 20px auto;
}

/* Player Containers */
.player-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 50%;
    gap: 20px;
}

/* Player Names on Top */
.player-name {
    font-weight: bold;
    font-size: 24px;
}

/* Progress Bar */
.progress-bar {
  width: 100%;
  height: 6px;
  background-color: #d53333;
  border-radius: 0; /* squared edges */
  overflow: hidden;
  position: relative;
}

/* Progress Fill */
.progress-fill {
  height: 100%;
  background-color: #2d94e3;
  transition: width 0.3s ease-in-out;
}
</style>