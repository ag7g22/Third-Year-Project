'use strict';

// Express and socket.io setup for client-server communication
const express = require('express');
const { hostname } = require('os');
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

function handle_login(username) {
    // Add logged in user
    logged_users.push(username);
    console.log(username + " has logged in");
}

function handle_logout(username) {
    // Remove logged out user
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
    let user_state = {username: host_username, host: host_username, role: "HOST", isWinner: false};
    let game_state = {host: host_username, password: host_password, players: [host_username], state: 0};

    // Add to the Maps:
    users.set(host_username, user_state);
    usersToSockets.set(host_username, socket);
    socketsToUsers.set(socket, host_username);
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
        usersToSockets.delete(username);
        socketsToUsers.delete(theSocket);

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
                let user_state = {username: username, host: host, role: "PLAYER", isWinner: false};
                game_state.players.push(username);

                // Add to the Maps:
                users.set(username, user_state);
                usersToSockets.set(username, socket);
                socketsToUsers.set(socket, username);

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
    usersToSockets.delete(username);
    socketsToUsers.delete(socket);
    theGame.players = theGame.players.filter(playername => playername !== username);

    // Notify successful leave
    socket.emit('leave-lobby-success');
    console.log(username + ' left ' + host_username + "'s lobby");

    console.log([...users]);
    console.log([...games]);

    updateAllInServer(host_username);
}

// GAME HANDLERS
function handle_start_game(host_username) {
    // Set game state to 1 in that GAME:
    let theGame = games.get(host_username);
    theGame.state = 1;

    // Put all players to game.
    for (const username of theGame.players) {
        // console.log(username);
        const theSocket = usersToSockets.get(username);
        theSocket.emit('start-game-success');
    }

    console.log([...users]);
    console.log([...games]);

    console.log(host_username + "'s game started");
    updateAllInServer(host_username);
}

function handle_leave_game(playername, host_username, isWinner) {
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
        usersToSockets.delete(username);
        socketsToUsers.delete(theSocket);

        theSocket.emit('leave-game-success');
    }

    games.delete(host_username);
    console.log(host_username + "'s game has been terminated");

    console.log([...users]);
    console.log([...usersToSockets]);
    console.log([...socketsToUsers]);
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
        handle_login(username);
    });

    socket.on('logout', (username) => {
        handle_logout(username);
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

    socket.on('leave-game', (username, host_username, isWinner) => {
        handle_leave_game(username, host_username, isWinner);
    });

});

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