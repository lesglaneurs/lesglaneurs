"use strict";

if (!$) {
    $ = django.jQuery;
}

// We must manage the presence of the marker at 3 levels:
// - the map
// - leaflet-draw
// - the django field
function clean_markers(field) {
    field._map.eachLayer(function (layer) {
        if (layer instanceof L.Marker) {
            field._map.removeLayer(layer);
            field.drawnItems.removeLayer(layer);
            field.store.save(field.drawnItems);
        }
    })
}

// Just like for clean_markers,
// we must manage the presence of the marker at 3 levels
function set_marker(field, lat, lon) {
    clean_markers(field);
    var marker = L.marker(L.latLng(lat, lon));
    field._map.addLayer(marker);
    field.drawnItems.addLayer(marker);
    field.store.save(field.drawnItems);
}

function register_events(field) {

    $('.fa-search').on('click', function(e) {
        var url = 'http://api-adresse.data.gouv.fr/search/?' +
            'q=' + $('#id_address').val() + '&' +
            'postcode=' + $('#id_code').val() + '&' +
            'limit=1'
        $.getJSON(url, function(data) {
            if (data.features.length === 0) {
                alert('Il n\'y a pas de coordonnées correspondant à ' +
                      'cette adresse')
                return
            }
            var feature = data.features[0]
            var coordinates = feature.geometry.coordinates;
            var lon = coordinates[0];
            var lat = coordinates[1];
            set_marker(field, lat, lon)
            // We seize the opportunity to normalize the address fields
            var properties = feature.properties
            $('#id_address').val(properties.name);
            $('#id_code').val(properties.postcode);
            $('#id_city').val(properties.city);
        }).fail(function() {
            alert('Impossible de se connecter au serveur de géocodage')
        })
    })

    $('.fa-edit').on('click', function(e) {
        var lat = 47;
        var lon = 1.7;
        field._map.eachLayer(function (layer) {
            if (layer instanceof L.Marker) {
                var latlng = layer._latlng
                lat = latlng.lat
                lon = latlng.lng
            }
        })

        var new_lon = prompt('Longitude', lon)
        if (new_lon !== null) {
            var new_lat = prompt('Latitude', lat)
            if (new_lat !== null) {
                set_marker(field, new_lat, new_lon)
            }
        }
    })

    $('.fa-trash').on('click', function(e) {
        clean_markers(field)
    })
}

$(document).ready(function() {

    // The event map:init is triggered by the JS of django-leaflet when the
    // map is loaded
    $(window).on('map:init', function (e) {
        var map = e.originalEvent.detail.map;

        // The event map:loadfield is triggered by the JS of django-leaflet
        // when the field corresponding to the marker is initialized
        map.on('map:loadfield', function (e) {

            // The button with leaflet-draw-draw-marker is associated to the
            // function of leaflet-draw allowing to set a marker on the map.
            // Simultaneously, this class imposes a specific layout of the
            // button, which is not consistent with the other buttons.
            // Therefore, we keep the button, but we modify the styles so that
            // it looks like the other buttons.
            $('.leaflet-draw-draw-marker').addClass('fa fa-map-marker')
            $('.leaflet-draw-draw-marker').css('background-image', 'inherit')
            $('.leaflet-draw-draw-marker').css('width', '100%')
            $('.leaflet-draw-draw-marker').css('height', '30px')

            var buttons = '' +
                '<div class="btn-group-vertical role=group">' +

                '<button type="button" class="btn btn-default fa fa-search" ' +
                'title="Chercher le point à partir de l\'adresse et du code ' +
                'postal"></button>' +

                '<button type="button" class="btn btn-default fa fa-edit" ' +
                'title="Editer les coordonnées du point"></button>' +

                '<button type="button" class="btn btn-default fa fa-trash" ' +
                'title="Supprimer le point"></button>' +

                '</div>'

            $('.leaflet-draw-draw-marker').after(buttons)

            // These 2 buttons are useful only when we want to edit a complex
            // geometry. For a simple marker, it is rather confusing.
            $('.leaflet-draw-edit-edit').hide()
            $('.leaflet-draw-edit-remove').hide()

            register_events(e.field)
        })

    });
})
