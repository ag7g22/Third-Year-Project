import io from 'socket.io-client';
let client_socket = this.$store.state.currentClientSocket;

// Handle server communication
client_socket.on('connection', function() {
    console.log('New Connection')
});

// Handle connection error
client_socket.on('connect_error', function(message) {
    alert('Unable to connect: ' + message);
});

// Handle disconnection
client_socket.on('disconnect', function() {
    console.log('User Disconnected');
});
