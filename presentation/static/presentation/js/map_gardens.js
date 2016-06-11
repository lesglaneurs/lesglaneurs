"use strict";

var center = [46.3507193554773, 2.603759765625]; //Montluçon
var zoom = 6;
var map = L.map('mapid').setView(center, zoom);

var markers = [];

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    // Alternative maps are listed in https://www.mapbox.com/api-documentation/#maps
    id: 'mapbox.streets',
    // This token is assigned to the user jpnoel (email: jpnoel@gmail.com) - See https://www.mapbox.com/studio/account/tokens/
    accessToken: 'pk.eyJ1IjoianBub2VsIiwiYSI6ImNpbXo5MGdnejAwbG92OWx5amt5cWV4ejAifQ.vJAEgiLq2bdVEGld5mau5A'
}).addTo(map);

function display_garden(index, garden) {
        console.log("display garden");
        var prefix = '' +
            '<b>Nom du proprietaire</b>: ' + garden.person.name + '</br>' +
            '<b>Plante</b>: ' + '</br>';

        var address = garden.address;
        console.log("address");
        console.log(address);

        var marker = L.marker([address.latitude,
                               address.longitude]).addTo(map);

        var content = prefix +
            '<b>Adresse</b> : ' + address.address + '</br>' +
            '<b>Ville</b> : ' + address.city + '</br>' +
            '<b>Code postal</b> : ' + address.code;

        marker.bindPopup(content);
        marker.on('mouseover', function (e) {
            this.openPopup();
        });
        marker.on('mouseout', function (e) {
            this.closePopup();
        });
        markers.push(marker);

}


function display() {
    console.log("javascript");
    var url = '../gardens/';
    var args = [];
    var garden = $('#gardens').val();
    console.log("gardens");
    console.log(garden);
    console.log(markers);

    markers.forEach(function(element, index, array){
        map.removeLayer(element)
    });
    console.log(markers);

    markers = [];
    $.getJSON(url, function(data) {
        console.log("data")
        console.log(data)
        $.each(data['gardens'], display_garden)
            }).fail(function() {
                console.log('fail');
            })
}

$('#gardens').on('change', display);

$('#owners').on('change', display);

display()
