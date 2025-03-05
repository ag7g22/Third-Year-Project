'use strict';

const express = require('express');
const path = require('path');
const app = express();

// Setup socket.io for Server-Client Communication
const server = require('http').Server(app);
const io = require('socket.io')(server);

// Serve Vue.js static files from the 'dist' folder
app.use(express.static(path.join(__dirname, 'dist')));
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'dist', 'index.html'));  // Serve Vue's index.html
});

// Key-Value Maps for the CHALLENGE portion.
let users = new Map(); // (username, {username: "username", host: "host game they're in", role: [HOST/PLAYER] }) ADDED ONCE THEY'RE IN A GAME

let usersToSockets = new Map(); // username -> user's socket
let socketsToUsers = new Map(); // user's socket -> username

let games = new Map(); // (host, {host: "host game", password: "password", players: ["username" ... ]})

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

// LOBBY HANDLERS
function handle_create_game(socket, host_username, host_password) {
    // Check if password is used already. If so, send to user to rewrite a password
    for (let [host, game_state] of games) {
        if (game_state.password === host_password) {
            socket.emit('create-game-fail');
            return;
        }
    }

    // Initalise states
    let user_state = {username: host_username, host: host_username, role: "HOST"};
    let game_state = {host: host_username, password: host_password, players: [host_username]};

    // Add to the Maps:
    users.set(host_username, user_state);
    usersToSockets.set(host_username, socket);
    socketsToUsers.set(socket, host_username);
    games.set(host_username, game_state);

    // Notify successful game creation
    socket.emit('create-game-success');
    console.log('Created NEW GAME:', host_username);

    console.log([...users]);
    console.log([...usersToSockets]);
    console.log([...socketsToUsers]);
    console.log([...games]);
}

function handle_delete_game(host) {
    // Remove all players from lobby:
    const theGame = games.get(host);
    for (const username of theGame.players) {
        const theSocket = usersToSockets.get(username);

        // Remove from the Maps:
        users.delete(username);
        usersToSockets.delete(username);
        socketsToUsers.delete(theSocket);

        theSocket.emit('remove-player');
    }

    games.delete(theGame);
    console.log('Deleted GAME: ', host);

    console.log([...users]);
    console.log([...usersToSockets]);
    console.log([...socketsToUsers]);
    console.log([...games]);
}

// Handle socket.io connections
io.on('connection', socket => {
    console.log('New connected user'); 

    socket.on('disconnect', () => {
        console.log('User Disconnected');
    });

    socket.on('ACK', () => {
        console.log('User sent ACK');
        socket.emit('server_ACK');
    });

    socket.on('create-game', (host_username, host_password) => {
        handle_create_game(socket, host_username, host_password);
    });

    socket.on('delete-game', (host) => {
        handle_delete_game(host);
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