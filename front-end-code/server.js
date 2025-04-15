'use strict';

// Express and socket.io setup for client-server communication
const express = require('express');
const path = require('path');
const app = express();
const server = require('http').Server(app);
const io = require('socket.io')(server);

// Serve Vue.js static files from the 'dist' folder
app.use(express.static(path.join(__dirname, 'dist')));
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'dist', 'index.html'));  // Serve Vue's index.html
});

// Users logged in
let logged_users = [];

// Key-Value Maps for the CHALLENGE portion.
let users = new Map(); // (username, {username: "username", host: "host game they're in", role: [HOST/PLAYER], isWinner: true/false }) ADDED ONCE THEY'RE IN A GAME
let usersToSockets = new Map(); // username -> user's socket
let socketsToUsers = new Map(); // user's socket -> username

let games = new Map(); // (host, {host: "host game", password: "password", players: ["username" ... ], state: 0})
// game.state -> 0: in lobby, 1: in game

// LOGGING IN AND OUT
function handle_check_login(socket, username) {
    // Check if the user has already logged in
    if (logged_users.includes(username)) {
        socket.emit('check-login-fail');
    } else {
        socket.emit('check-login-successful');
    }
}

function handle_login(socket, username) {
    // Add logged in user
    usersToSockets.set(username, socket);
    socketsToUsers.set(socket, username);
    logged_users.push(username);
    console.log(username + " has logged in");
}

function handle_logout(socket, username) {
    // Remove logged out user
    usersToSockets.delete(username);
    socketsToUsers.delete(socket);
    logged_users = logged_users.filter(item => item !== username)
    console.log(username + " has logged out");
}

// UPDATING USERS
function updateAllInServer(host) {
    const theGame = games.get(host);
    for (const username of theGame.players) {
        const theSocket = usersToSockets.get(username);
        update_user(theSocket, host);
    }
}

function update_user(socket, host) {
    const username = socketsToUsers.get(socket);
    const theUser = users.get(username);
    const theGame = games.get(host);
    const data = { game_state: theGame, user_state: theUser };
    socket.emit('update-user', data);
    console.log('Updated user: ', username);
}

function handle_disconnect(socket) {
    // Search for player in the game if inside any
    const theUsername = socketsToUsers.get(socket);
    for (let [host, game_state] of games) {
        if (game_state.players.includes(theUsername)) {
            if (game_state.state === 0 && host === theUsername) {
                // Terminate lobby if host disconnects
                handle_delete_lobby(host);
            } else if (game_state.state === 0 && host !== theUsername) {
                // Leave lobby if a player disconnects
                handle_leave_lobby(socket, theUsername, host);
            } else if (game_state.state === 1) {
                // Terminate game if any player disconnects
                handle_leave_game(theUsername, host, false);
            }
        }
    }
    // Log the user out
    if (logged_users.includes(theUsername)) {
      handle_logout(socket, theUsername);  
    }
    console.log('User Disconnected');
}

// LOBBY HANDLERS
function handle_create_lobby(socket, host_username, host_password) {
    // Check if password is used already. If so, send to user to rewrite a password
    for (let [host, game_state] of games) {
        if (game_state.password === host_password) {
            socket.emit('create-lobby-fail');
            console.log(host_username + ' failed to create a new lobby');
            return;
        }
    }

    // Initalise states
    let user_state = {username: host_username, host: host_username, role: "HOST", isWinner: false, isCorrect: null, isWaiting: false, selected_answer: null};
    let game_state = {host: host_username, password: host_password, players: [host_username], state: 0, questions: [], currentQuestion: 0, q_counter: 1, 
        home: { username: host_username, chances: 3, elapsedTime: 0, selected_answer: null }, 
        away: { username: '', chances: 3, elapsedTime: 0, selected_answer: null }};

    // Add to the Maps:
    users.set(host_username, user_state);
    games.set(host_username, game_state);

    // Notify successful game creation
    socket.emit('create-lobby-success');
    console.log(host_username + ' created a new lobby');

    console.log([...users]);
    console.log([...games]);

    update_user(socket, host_username);
}

function handle_delete_lobby(host_username) {
    // Remove all players from lobby:
    const theGame = games.get(host_username);
    for (const username of theGame.players) {
        const theSocket = usersToSockets.get(username);

        // Remove from the Maps:
        users.delete(username);

        theSocket.emit('remove-player');
    }

    games.delete(host_username);
    console.log(host_username + ' terminated their lobby');

    console.log([...users]);
    console.log([...games]);
}

function handle_join_lobby(socket, username, host_password) {
    // Check if theres any matching passwords in existing games
    for (let [host, game_state] of games) {
        if (game_state.password === host_password) {
            if (game_state.players.length < 2) {
                // Add player to the maps if theres space:

                // Initalise states
                let user_state = {username: username, host: host, role: "PLAYER", isWinner: false, isCorrect: null, isWaiting: false, selected_answer: null};
                game_state.players.push(username);
                game_state.away = { username: username, chances: 3, elapsedTime: 0, selected_answer: null }

                // Add to the Maps:
                users.set(username, user_state);

                // Notify successful game creation
                socket.emit('join-lobby-success');
                console.log(username + ' joined ' + host + "'s lobby");

                console.log([...users]);
                console.log([...games]);

                updateAllInServer(host);
                return;

            } else {
                // If the lobby is full, notify client
                socket.emit('lobby-full');
                console.log(host + "'s lobby is full");
                return;
            }
        }
    }
    // If theres no matching passwords, notify client
    socket.emit('join-lobby-fail');
    console.log(username + ' failed to join a lobby');
}

function handle_leave_lobby(socket, username, host_username) {
    // Only remove user from the lobby and the maps
    const theGame = games.get(host_username);
    users.delete(username);
    theGame.players = theGame.players.filter(playername => playername !== username);
    theGame.away = { username: '', chances: 3, elapsedTime: 0, selected_answer: null };

    // Notify successful leave
    socket.emit('leave-lobby-success');
    console.log(username + ' left ' + host_username + "'s lobby");

    console.log([...users]);
    console.log([...games]);

    updateAllInServer(host_username);
}

// GAME HANDLERS
async function handle_start_game(host_username) {
    // Get first few questions:
    const input = {"No_of_Qs": 30, "username": "n/a"}
    const quiz = await azure_function('POST', '/question/get/quiz', input)
    if (quiz.result) {
        // Set game state to 1 and set the questions.
        const theGame = games.get(host_username);
        theGame.questions = quiz.msg;
        theGame.state = 1;
        updateAllInServer(host_username);

        // Put all players to game.
        for (const username of theGame.players) {
            const theSocket = usersToSockets.get(username);
            theSocket.emit('start-game-success');
        }

        console.log([...users]);
        console.log([...games]);
        console.log(host_username + "'s game started");

    } else {
        // Notify host that questions failed to load.
        const theSocket = usersToSockets.get(host_username);
        theSocket.emit('start-game-fail');
        console.log(host_username + "'s game failed to start");
        console.log(quiz.msg);
    }
}

function handle_selected_answer(socket, selected_answer, elapsedTime, host_username) {
    // Update the user's state and game state after one user selecting the answer.
    let theGame = games.get(host_username);
    let theUsername = socketsToUsers.get(socket);
    let theUser = users.get(theUsername);
    console.log(theUsername + " answered question " + theGame.q_counter + " in " + elapsedTime + " seconds in " + host_username + "'s game " );

    // Update the game state from either the home/away user
    if (theUsername == host_username) {
        users.get(theUsername).selected_answer = selected_answer;
        theGame.home.elapsedTime = elapsedTime;
        theGame.home.selected_answer = selected_answer;
    } else {
        users.get(theUsername).selected_answer = selected_answer;
        theGame.away.elapsedTime = elapsedTime;
        theGame.away.selected_answer = selected_answer;   
    }

    // If both users answered, compare answers
    if (theGame.home.selected_answer !== null && theGame.away.selected_answer !== null) {
        compare_answers(theGame);

        // Setup next question
        load_next_question(theGame);

    } else {
        theUser.isWaiting = true;
        socket.emit('selected-answer-waiting');
        updateAllInServer(host_username);
    }
    
}

function compare_answers(theGame) {
    // Whoever answered the quickest
    let correct_answer = theGame.questions[theGame.currentQuestion].correct_answer;
    let home = theGame.home
    let away = theGame.away

    if (home.selected_answer === correct_answer && away.selected_answer !== correct_answer) {
        end_round(home, away, theGame.host);
    } else if (home.selected_answer !== correct_answer && away.selected_answer === correct_answer) {
        end_round(away, home, theGame.host);
    } else if (home.selected_answer === away.selected_answer || (home.selected_answer !== correct_answer && away.selected_answer !== correct_answer)) {
        tie_round(home, away, home.selected_answer, correct_answer, theGame.host);
    }
}

async function load_next_question(theGame) {
    // Update to the next question
    console.log("Setting up next round in " + theGame.host + "'s game");
    theGame.currentQuestion++;
    theGame.q_counter++;

    // Reset state of home and away
    theGame.home.elapsedTime = 0;
    theGame.home.selected_answer = null;
    theGame.away.elapsedTime = 0;
    theGame.away.selected_answer = null;

    // Refresh bank if it's the last question on the questions list.
    if (theGame.currentQuestion >= theGame.questions.length) {
        // Get first few questions:
        const input = {"No_of_Qs": 30, "username": "n/a"}
        const quiz = await azure_function('POST', '/question/get/quiz', input)
        if (quiz.result) {
            // Set game state to 1 and set the questions.
            theGame.currentQuestion = 0;
            theGame.questions = quiz.msg;
        } else {
            // End game if questions fail to load.
            const host_username = theGame.host;
            console.log("Terminating " + host_username + "'s game");

            for (const username of theGame.players) {
                let theSocket = usersToSockets.get(username);
                let theUser = users.get(username);
                theUser.isWinner = null;

                update_user(theSocket, host_username);
        
                // Remove from the Maps:
                users.delete(username);
        
                theSocket.emit('leave-game-success');
            }
        
            games.delete(host_username);
            console.log(host_username + "'s game has been terminated");
        
            console.log([...users]);
            console.log([...games]);
        }
    }
    console.log(theGame.home);
    console.log(theGame.away);
    updateAllInServer(theGame.host);
}

function end_round(winner, loser, host_username) {
    // Winner is correct and gets an extra chance.
    let winner_user = users.get(winner.username);
    winner_user.isCorrect = true;
    winner_user.isWaiting = false;
    winner.chances += 1;

    // Loser is incorect and loses a chance.
    let loser_user = users.get(loser.username);
    loser_user.isCorrect = false;
    loser_user.isWaiting = false;
    loser.chances -= 1;

    // Send the users results
    console.log(winner.username + " WON the round in " + host_username + "'s game");
    updateAllInServer(host_username);
    let theGame = games.get(host_username);
    for (const username of theGame.players) {
        const theSocket = usersToSockets.get(username);
        if (loser.chances === 0) {
            theSocket.emit('end-of-game', winner.username);
        } else {
            theSocket.emit('end-of-round', winner.username);    
        }
    }
}

function tie_round(home, away, selected_answer, correct_answer, host_username) {
    // If both players are correct the one who answered the quickest wins the round.
    const usersAreCorrect = selected_answer === correct_answer;

    if (home.elapsedTime < away.elapsedTime && usersAreCorrect) {
        // If home player was quicker than away player, home wins
        end_round(home, away, host_username);
    } else if (away.elapsedTime < home.elapsedTime && usersAreCorrect) {
        // If away player was quicker than home player, away wins
        end_round(away, home, host_username);
    } else if ((home.elapsedTime === away.elapsedTime && usersAreCorrect) || !usersAreCorrect) {
        // If both have the same answer and same answering time, OR both are wrong, they tie.
        let home_user = users.get(home.username);
        home_user.isCorrect = usersAreCorrect;
        home_user.isWaiting = false;

        let away_user = users.get(away.username);
        away_user.isCorrect = usersAreCorrect;
        away_user.isWaiting = false;

        console.log(home.username + " and " + away.username + " TIED in " + host_username + "'s game");
        updateAllInServer(host_username);

        let theGame = games.get(host_username);
        for (const username of theGame.players) {
            const theSocket = usersToSockets.get(username);
            theSocket.emit('end-of-round', "tie"); 
        }
    }
}

async function handle_next_question(socket, host_username) {
    // Update all users after calling for next question.
    const theUsername = socketsToUsers.get(socket);
    let theUser = users.get(theUsername);
    theUser.isCorrect = false;
    theUser.selected_answer = null;
    update_user(socket, host_username);
}


function handle_leave_game(playername, host_username, isWinner) {

    // If game already terminated, don't run!
    if (!games.has(host_username)) {
        return;
    }

    // Terminate game and send users to game over screen.
    console.log("Terminating " + host_username + "'s game");
    const theGame = games.get(host_username);
    for (const username of theGame.players) {
        let theSocket = usersToSockets.get(username);
        let theUser = users.get(username);

        // Assign the winner OR loser
        if (username == playername) {
            theUser.isWinner = isWinner;
        } else {
            theUser.isWinner = !isWinner;
        }
        update_user(theSocket, host_username);

        // Remove from the Maps:
        users.delete(username);

        theSocket.emit('leave-game-success');
    }

    games.delete(host_username);
    console.log(host_username + "'s game has been terminated");

    console.log([...users]);
    console.log([...games]);
}

// Handle socket.io connections
io.on('connection', socket => {
    console.log('New connected user'); 

    socket.on('disconnect', () => {
        handle_disconnect(socket);
    });

    // LOGIN AND LOGOUT
    socket.on('check-login', (username) => {
        handle_check_login(socket, username);
    });

    socket.on('login', (username) => {
        handle_login(socket, username);
    });

    socket.on('logout', (username) => {
        handle_logout(socket, username);
    })

    // LOBBY
    socket.on('create-lobby', (host_username, host_password) => {
        handle_create_lobby(socket, host_username, host_password);
    });

    socket.on('delete-lobby', (host) => {
        handle_delete_lobby(host);
    });

    socket.on('join-lobby', (username, host_password) => {
        handle_join_lobby(socket, username, host_password);
    });

    socket.on('leave-lobby', (username, host_username) => {
        handle_leave_lobby(socket, username, host_username)
    });

    // GAME
    socket.on('start-game', (host_username) => {
        handle_start_game(host_username);
    });

    socket.on('selected-answer', (selected_answer, elapsedTime, host_username) => {
        handle_selected_answer(socket, selected_answer, elapsedTime, host_username);
    })

    socket.on('next-question', (host_username) => {
        handle_next_question(socket, host_username);
    })

    socket.on('leave-game', (username, host_username, isWinner) => {
        handle_leave_game(username, host_username, isWinner);
    });

});

// API Requests are handled here
async function azure_function(function_type, function_route, json_doc) {
    console.log(function_route);
    // Call Azure function with request
    try {
        const url = "https://driving-theory.azurewebsites.net" + function_route + '?code=' + "p8l8U5CrimGa5Z35x5bq3Tf2X1KiVJKsYY7yyGL8OQOeAzFuEHeOLA=="
        
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
}

// Start the server
function startServer() {
    const PORT = process.env.PORT || 8080;
    server.listen(PORT, () => {
        console.log(`Server listening on port ${PORT}`);
    });
}

// Start server if the script is run directly.
if (module === require.main) {
    startServer();
}

module.exports = server;