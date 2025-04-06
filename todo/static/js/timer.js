let socket;
let taskId;

function startTimer(task_id) {
    taskId = task_id;
    socket = new WebSocket(`ws://${window.location.host}/ws/timer/${taskId}/`);
    
    socket.onopen = function(e) {
        // Start the timer when the WebSocket is open
        socket.send(JSON.stringify({ 'action': 'start' }));
    };

    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const timerElement = document.getElementById(`timer-${taskId}`);
        
        if (timerElement) {
            timerElement.innerText = data.timer;  // Update timer on the screen
        }
    };

    socket.onclose = function(e) {
        console.log('WebSocket closed');
    };
}

function stopTimer() {
    if (socket) {
        socket.send(JSON.stringify({ 'action': 'stop' }));
    }
}

function resetTimer() {
    if (socket) {
        socket.send(JSON.stringify({ 'action': 'reset' }));
    }
}
