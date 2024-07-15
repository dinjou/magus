document.addEventListener('DOMContentLoaded', function () {
    const ongoingTask = {{ is_ongoing|yesno:"true,false" }};
    document.querySelectorAll('.task-button-start').forEach(button => {
        button.addEventListener('click', function (event) {
            if (ongoingTask) {
                event.preventDefault();
                const confirmInterrupt = confirm("Your previous task has not yet been marked as complete. Would you like me to mark it as interrupted?");
                if (confirmInterrupt) {
                    this.submit();
                }
            }
        });
    });

    // Heartbeat mechanism
    setInterval(function () {
        fetch("{% url 'magus:heartbeat' %}", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify({ status: 'alive' })
        }).catch(error => {
            console.error('Error sending heartbeat:', error);
        });
    }, 30000); // Send heartbeat every 30 seconds
});
