<template>
    <div class="container">
        <h1 class="title">CRASH QUIZ | {{ state.current_view }} | {{ logged_in_user }}</h1>

        <!-- Toogle Buttons -->
        <div v-if="state.current_view !== 'LOBBY'" class="buttons">
            <button @click="next_page('dashboard')">Back</button>
            <button @click="toggle_view('RULES')">Rules</button>
            <button @click="toggle_view('HOST')">Host Game</button>
            <button @click="toggle_view('JOIN')">Join Game</button>
        </div>

        <div v-if="state.current_view === 'RULES'">
            <div class="instruction-box"> 
                <p> You are against another player answering different questions </p>
                <p> and once you click the answer immediately locks in. </p>
                <p> There will be a car at the top of the screen. </p>
                <p> If you get the question correct, the car will move towards your opponenent </p>
                <p> Otherwise the car will move towards you. </p>
                <p> Once the car crashes on a player, they lose! </p>
            </div>

        </div>

        <div v-if="state.current_view === 'HOST'">
            <h2> Create a HOST password </h2>
            <input type="text" placeholder="password" v-model="host_password" />
            <button @click="create_game()">Create Game</button>
        </div>

        <div v-if="state.current_view === 'JOIN'">
            <h2> Enter a HOST password </h2>
            <input type="text" placeholder="password" v-model="host_password" />
            <button @click="join_game()">Join Game</button>
        </div>

        <div v-if="state.current_view === 'LOBBY'">

            <div v-if="state.role === 'HOST'">
                <button>Start Game</button>
                <button @click="delete_game()">Delete Lobby</button>
            </div>
            <div v-else>
                <button @click="leave_game()">Leave Game</button>
            </div>

            <h2>HOST: {{ game_state.host }}</h2>
            <h2>PLAYERS:</h2>
            <div v-for="player in game_state.players">
                <p>{{ player }}</p>
            </div>
            
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
            state: { current_view: "RULES", role: '' },
            client_socket: this.$store.state.currentClientSocket,

            // Password to join a hosted game
            host_password: '', 
            
            // States updated by server:
            game_state: {host: '', password: '', players: []},
            user_state: {username: '', host: '', role: ''},

            logged_in_user: this.$store.state.currentUser,
            message: { error: "", success: "" },
        };
    },
    methods: {
        reset_states() {
            // Run this when leaving a lobby
            this.state = { current_view: "RULES", role: '' };
            this.host_password = '';
            this.game_state = {host: '', password: '', players: []};
            this.user_state = {username: '', host: '', role: ''};

        },
        create_game() {
            // Send to server to register game.
            this.message.error = "";
            this.message.success = "";
            this.host_password = '';
            this.client_socket.emit('create-lobby', this.logged_in_user, this.host_password);
        },
        delete_game() {
            // Send to server to remove game.
            this.message.error = "";
            this.message.success = "";
            this.client_socket.emit('delete-lobby', this.logged_in_user);
            this.reset_states();
        },
        join_game() {
            // Send to server to join game.
            this.message.error = "";
            this.message.success = "";
            this.host_password = '';
            this.client_socket.emit('join-lobby', this.logged_in_user, this.host_password);
        },
        leave_game() {
            // Send to server to leave game.
            this.message.error = "";
            this.message.success = "";
            this.client_socket.emit('leave-lobby', this.logged_in_user, this.user_state.host);
            this.reset_states();
        },
        toggle_view(view) {
            // Reset state
            this.message.error = "";
            this.message.success = "";
            this.state.current_view = view;

            if (view === "HOST") {
                this.state.role = "HOST"
            } else if (view === "JOIN") {
                this.state.role = "PLAYER"
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
        leave_server() {
            socket.emit('disconnect');
            this.next_page('dashboard');
        },
        next_page(page) {
            console.log("/" + page);
            this.$router.push(`/${page}`);
        }
    },
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
}

</script>

<style lang="scss" scoped>
.instruction-box {
  background-color: #f9f9f9;
  border-left: 5px solid #007bff;
  padding: 10px;
  margin: 10px 0;
  font-size: 14px;
  color: #333;
  border-radius: 5px;
}
</style>