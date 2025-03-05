'use strict';

const express = require('express');
const path = require('path');
const app = express();

// Setup socket.io for Server-Client Communication
const server = require('http').Server(app);
const io = require('socket.io')(server);

// Serve Vue.js static files from the 'dist' folder
app.use(express.static(path.join(__dirname, 'dist')));

// Serve index.html as the entry point for Vue.js
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'dist', 'index.html'));  // Serve Vue's index.html
});

// Handle socket.io connections (if needed)
io.on('connection', socket => {
    console.log('New connected user'); 

    socket.on('disconnect', () => {
        console.log('User Disconnected');
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