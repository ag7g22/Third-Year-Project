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
                <button @click="create_game()" class="create-button">Create Game</button>
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
                <button @click="join_game()" class="create-button">Join Game</button>
                <div class="game-buttons">
                    <button @click="next_page('dashboard')" class="game-button">Back</button>
                    <button @click="toggle_view('HOST')" class="game-button">Host</button>
                    <button disabled class="game-button">Join</button>
                </div>
            </div>

            <div v-if="state.current_view === 'LOBBY'">
                <h2>HOST: {{ game_state.host }} | PASSWORD: {{ game_state.password }}</h2>
                <h2>PLAYERS:</h2>
                <div class="players-list">
                    <div v-for="player in game_state.players" class="player-item">
                        <p>{{ player }}</p>
                    </div>
                </div>
                <div v-if="state.role === 'HOST'">
                    <div class="game-buttons">
                        <div v-if="game_state.players.length > 1">
                            <div class="game-buttons">
                                <button @click="start_game()" class="game-button">Start Game</button>
                                <button @click="delete_game()" class="game-button">Delete Lobby</button>    
                            </div>
                        </div>
                        <div v-else>
                            <div class="game-buttons">
                                <button @click="delete_game()" class="game-button">Delete Lobby</button>   
                            </div>
                        </div>
                    </div>
                </div>
                <div v-else class="game-buttons"> 
                    <button @click="leave_lobby()" class="game-button">Leave Lobby</button>
                </div>
                
            </div>
        </div>
    </div>
    <div v-else>
        <div v-if="state.current_view === 'GAME'" class="container">
            <!-- Count down for game -->
            <div v-if="game_timer !== null">
                <h1> GAME STARTS IN: </h1>
                <h1>{{ countdown }}</h1>
            </div>
            <div v-else>
                <!-- Buttons -->
                <div class="buttons">
                    <button @click="leave_game(false)">Leave Game</button>
                </div>
                <div class="questionnaire">
                    <p> Question {{ game_state.q_counter }} </p>
                    
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

                    <p>{{ game_state.questions[game_state.currentQuestion].question }}</p>

                    <!-- Count down for question -->
                    <div v-if="question_timer !== null">
                        <h2>{{ countdown }}</h2>
                    </div>
                    <div v-else>
                        <div class="options">
                            <button 
                            v-for="(option, index) in game_state.questions[game_state.currentQuestion].options"
                            :key="index"
                            :class="{
                                selected: user_state.selected_answer === option && user_state.isWaiting,
                                correct: user_state.selected_answer === option && user_state.isCorrect && !user_state.isWaiting,
                                incorrect: user_state.selected_answer === option && !user_state.isCorrect && !user_state.isWaiting
                            }"
                            @click="select_answer(option)"
                            >
                            {{ option }}
                            </button>
                        </div>
                    </div>
                    <!-- Show results for a few seconds -->
                    <div v-if="end_of_round_timer !== null">
                        <p>{{ game_state.questions[game_state.currentQuestion].explanation }}</p>
                    </div>
                </div>
            </div>
        </div>

        <div v-if="state.current_view === 'GAMEOVER'" class="container">
            <div v-if="user_state.isWinner === true">
                <h2> VICTORY! 🎉</h2>
            </div>
            <div v-else>
                <h2> DEFEATED! ⚰️</h2>
            </div>

            <button @click="return_lobby()">Return to lobby</button>
        </div>

        <p v-if="message.error" class="error-message">{{ message.error }}</p>
        <p v-if="message.success" class="success-message">{{ message.success }}</p>
    </div>
</template>

<script>
import toastr from 'toastr';

export default {
    // Page member variables and methods:
    name: "lobby",
    mounted: function() {
        listen(this, this.client_socket); 
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

            client_socket: this.$store.state.currentClientSocket,
            logged_in_user: this.$store.state.currentUser,
            currentRank: this.$store.state.currentRank,
            message: { error: "", success: "" },
        };
    },
    methods: {
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
            this.state = { current_view: "RULES", role: '', gamemodes: ['quiz', 'hazard perception', 'road sign'], selected_gamemode: 'quiz' }
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
            this.message = { error: "", success: "" }
            if (winner === this.logged_in_user) {
                this.message.success = " You WON the round!"
            } else if (winner === "tie") {
                this.message.success = "Round Tie!"
            } else {
                this.message.success = winner + " WON the round!" 
            }
            await this.start_end_round_countdown(7);
        },
        async end_of_game(winner) {
            // Show both users the results
            this.message = { error: "", success: "" }
            if (winner === this.logged_in_user) {
                this.user_state.isWinner = true;
                this.message.success = " You WON the game!"
            } else {
                this.user_state.isWinner = false;
                this.message.success = winner + " WON the game!" 
            }
            await this.start_end_game_countdown(7);
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
        async start_end_game_countdown(countdown) {
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
                        if (this.user_state.isWinner) {
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
                    this.message.success = `LEVELED UP TO LEVEL ${this.currentRank.level}!` 
                } else {
                    this.message.success = `Gained ${exp_gain} exp!`
                }

            } else {
                this.message.error = update_response.msg || "Score update Failed."
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
        }
    },
    computed: {
        progressPercentage() {
        return (this.game_state.home.chances / 6) * 100;
    }
  }
};

function listen(vue, client_socket) {
    console.log("Current Client: ", client_socket);

    client_socket.on('update-user', function(data) {
        vue.game_state = data.game_state;
        vue.user_state = data.user_state; 
    });

    client_socket.on('create-lobby-fail', function() {
        vue.message.error = "Password already being used."
    });

    client_socket.on('create-lobby-success', function() {
        vue.toggle_view('LOBBY');
    });

    client_socket.on('remove-player', function() {
        vue.toggle_view('RULES');
        vue.message.success = "Lobby was terminated."
    });

    client_socket.on('join-lobby-success', function() {
        vue.toggle_view('LOBBY');
        vue.message.success = 'Joined Lobby.';
    });

    client_socket.on('lobby-full', function() {
        vue.message.error = 'Lobby is currently full.';
    });

    client_socket.on('join-lobby-fail', function() {
        vue.message.error = "Lobby doesn't exist.";
    });

    client_socket.on('start-game-success', function() {
        vue.load_quiz();
    });

    client_socket.on('start-game-fail', function() {
        vue.message.error = 'Failed to load questions. Try again.'
    });
    
    client_socket.on('selected-answer-waiting', function() {
        vue.message.success = "Waiting for other player to answer ..."
    });

    client_socket.on('end-of-round', function(winner) {
        vue.end_of_round(winner);
    });

    client_socket.on('end-of-game', function(winner) {
        vue.end_of_game(winner);
    });

    client_socket.on('next-question', function() {
        vue.next_question();
    });

    client_socket.on('leave-game-success', function() {
        vue.toggle_view('GAMEOVER');
    });
}

</script>

<style lang="scss" scoped>
.create-button {
    width: 100%;
    padding: 12px;
    background-color: #f3af59;
    border: none;
    border-radius: 5px;
    color: white;
    font-size: 18px;
    cursor: pointer;
    margin-bottom: 20px;
}
.create-button:hover {
  background-color: #e09548; /* Hover effect for the button */
}

.players-list {
  display: flex;
  gap: 20px; /* Space between player names */
  overflow-x: auto; /* Allow horizontal scrolling if too many players */
  padding: 10px;
  background-color: black;
  border: 2px solid #f3af59;
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

.progress-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 80%;
  margin: 20px auto;
  position: relative;
}

/* Player Containers */
.player-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 50%;
}

/* Player Names on Top */
.player-name {
  font-weight: bold;
  font-size: 16px;
  margin-bottom: 5px;
}

/* Progress Bar */
.progress-bar {
  width: 100%;
  height: 20px;
  background-color: #d53333;
  border-radius: 10px;
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