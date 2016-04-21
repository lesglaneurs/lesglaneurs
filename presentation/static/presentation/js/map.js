"use strict";

var center = [46.3507193554773, 2.603759765625]; //Montluçon
var zoom = 6;

var map = L.map('mapid').setView(center, zoom);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    // Alternative maps are listed in https://www.mapbox.com/api-documentation/#maps
    id: 'mapbox.streets',
    // This token is assigned to the user jpnoel (email: jpnoel@gmail.com) - See https://www.mapbox.com/studio/account/tokens/
    accessToken: 'pk.eyJ1IjoianBub2VsIiwiYSI6ImNpbXo5MGdnejAwbG92OWx5amt5cWV4ejAifQ.vJAEgiLq2bdVEGld5mau5A'
}).addTo(map);

function display_address(index, address) {
    var marker = L.marker([address.fields.latitude,
                           address.fields.longitude]).addTo(map);
    var content = '' +
        '<b>Adresse</b> : ' + address.fields.address + '</br>' +
        '<b>Ville</b> : ' + address.fields.city + '</br>' +
        '<b>Code postal</b> : ' + address.fields.code
    marker.bindPopup(content);
    marker.on('mouseover', function (e) {
        this.openPopup();
    });
    marker.on('mouseout', function (e) {
        this.closePopup();
    });
}

function display_event(index, event) {
    var addresses = event.addresses
    var content = '' +
        '<b>Nom</b>: ' + event.name + '</br>' +
        '<b>Association</b>: ' + event.project.fields.name + '</br>'
    for (var index in addresses) {
        var address = addresses[index]
        var marker = L.marker([address.fields.latitude,
                               address.fields.longitude]).addTo(map);
        var content = content +
            '<b>Adresse</b> : ' + address.fields.address + '</br>' +
            '<b>Ville</b> : ' + address.fields.city + '</br>' +
            '<b>Code postal</b> : ' + address.fields.code
        marker.bindPopup(content);
        marker.on('mouseover', function (e) {
            this.openPopup();
        });
        marker.on('mouseout', function (e) {
            this.closePopup();
        });
    }
}

//var display = 'addresses'
var display = 'events'

if (display === 'addresses') {
    $.getJSON('map_addresses', function(data) {
        $.each(data['addresses'], display_address)
            }).fail(function() {
                console.log('fail');
            })
}
else {
    $.getJSON('map_events', function(data) {
        $.each(data['events'], display_event)
            }).fail(function() {
                console.log('fail');
            })
}
