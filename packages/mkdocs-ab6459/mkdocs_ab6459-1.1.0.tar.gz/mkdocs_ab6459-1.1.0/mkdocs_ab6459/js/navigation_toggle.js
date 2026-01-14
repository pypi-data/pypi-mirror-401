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

function updateIcon($button, isOpen) {
    var $icon = $button.find('i');
    if (isOpen) {
        $icon.removeClass('bi-plus-square').addClass('bi-dash-square');
    } else {
        $icon.removeClass('bi-dash-square').addClass('bi-plus-square');
    }
}

$(document).ready(function () {
    $('ul.collapse').each(function () {
        var menuId = $(this).attr('id');
        var state = getCookie(menuId);
        var $button = $('#' + menuId + '-button');

        if (state === 'open') {
            $(this).show();
            updateIcon($button, true);
        }
    });

    // Only target links that have a corresponding collapse menu
    $('a[id$="-button"][role="button"]').on("click", function (e) {
        var targetId = this.id.replace('-button', '');

        // Try to find the menu - first with exact ID, then with patterns
        var $menu = $('#' + targetId);

        // If not found, try looking for an ID that starts with the targetId
        if (!$menu.length || !$menu.is('ul.collapse')) {
            $menu = $('ul.collapse[id^="' + targetId + '"]').first();
        }

        // Only prevent default and toggle if we found a valid collapse menu
        if ($menu.length && $menu.is('ul.collapse')) {
            e.preventDefault();

            var $button = $(this);
            $menu.toggle();

            var isOpen = $menu.is(':visible');
            updateIcon($button, isOpen);

            // Use the actual menu ID for the cookie
            var actualMenuId = $menu.attr('id');
            if (isOpen) {
                setCookie(actualMenuId, 'open', 30);
            } else {
                setCookie(actualMenuId, 'closed', 30);
            }
        }
    });
});