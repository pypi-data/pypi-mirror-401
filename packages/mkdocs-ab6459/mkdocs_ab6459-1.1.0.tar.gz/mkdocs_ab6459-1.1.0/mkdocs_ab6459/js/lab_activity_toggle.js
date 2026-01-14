function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function updateTaskState($task, isOpen) {
    if (isOpen) {
        $task.removeClass('collapsed');
    } else {
        $task.addClass('collapsed');
    }
}

$(document).ready(function () {
    // Initialize all task blocks with saved state
    $('[id^="task-"]').each(function () {
        var taskId = $(this).attr('id');
        var state = getCookie(taskId);
        var $task = $(this);

        if (state === 'collapsed') {
            $task.addClass('collapsed');
        }
    });

    // Add click handler to all task headers
    $('[id^="task-"] > h2').on('click', function (e) {
        e.preventDefault();

        var $task = $(this).parent('[id^="task-"]');
        var taskId = $task.attr('id');

        // Toggle the collapsed state
        var isCurrentlyOpen = !$task.hasClass('collapsed');
        var willBeOpen = !isCurrentlyOpen;

        updateTaskState($task, willBeOpen);

        // Save state to cookie
        if (willBeOpen) {
            setCookie(taskId, 'open', 30);
        } else {
            setCookie(taskId, 'collapsed', 30);
        }
    });
});