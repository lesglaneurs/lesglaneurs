"use strict";

if (!$) {
    $ = django.jQuery;
}

function hide() {
    /* This a dirty hack to hide 2 useless buttons on the map of the
       Address admin form.
       When the current JS script is loaded, the buttons are not yet created,
       that is why we reschedule the function until they exist.
       Then, we hide them.
    */
    if ($('.leaflet-draw-edit-edit').length == 0 ||
        $('.leaflet-draw-edit-remove').length == 0) {
        setTimeout(hide, 50);
    }
    else {
        $('.leaflet-draw-edit-edit').hide()
        $('.leaflet-draw-edit-remove').hide()
    }
}

$(document).ready(function() {
    hide()
})
