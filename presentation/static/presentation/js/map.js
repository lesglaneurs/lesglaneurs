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

var points = [{'name': "Saint-Pierre d'Aurillac", 'coords': [44.572329, -0.19046500000001743]},
              {'name': 'Paris', 'coords': [48.856614, 2.3522219000000177]},
              {'name': 'Guiseniers', 'coords': [49.21267599999999, 1.4749530000000277]}]

for (var index in points) {
    var point = points[index];
    var marker = L.marker(point['coords']).addTo(map);
    marker.bindPopup('Je suis <b>' + point['name'] + '</b>');
    marker.on('mouseover', function (e) {
        this.openPopup();
    });
    marker.on('mouseout', function (e) {
        this.closePopup();
    });
}
