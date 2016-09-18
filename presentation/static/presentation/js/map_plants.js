"use strict";

var center = [44.572778, -0.190556]; //Saint Pierre d'Aurillac
var zoom = 13;
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


function display_plant(index, plant) {
    var garden = plant.garden[0];
    var address = garden.address;
    if (address.point != null) {
	var point_prefix = 'SRID=4326;POINT (';
        var point_suffix = ')';
        var lon_lat = address.point.slice(point_prefix.length, -point_suffix.length).split(' ');
        var marker = L.marker([lon_lat[1], lon_lat[0]]).addTo(map);

        var content = '' +
            '<b>Plante</b>: ' + plant.name + '</br>' +
            '<b>Chez</b>: ' + garden.person.firstname + ' ' + garden.person.lastname + '</br>' +
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
    } else {
	console.log('null address point for garden:', garden);
    }
}

function display_garden(index, garden) {
        var address = garden.address;
        var marker = L.marker([address.latitude,
                               address.longitude]).addTo(map);

        var content = '' +
            '<b>Nom du proprietaire</b>: ' + garden.person.firstname + '</br>' +
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
    var url = '../plants_info';

    // manage filters
    var args = [];  
    var plant = $('#plants').val()
    if (plant !== 'Tous') {
        args.push('plant=' + plant)
    }
    if (args.length !== 0) {
        url = url + '?' + args.join('&')
    }
    markers.forEach(function(element){
        map.removeLayer(element)
    });

    // create map markers
    markers = [];
    $.getJSON(url, function(data) {
        $.each(data['plants'], display_plant)
            }).fail(function() {
                console.log('fail');
            })
}

$('#plants').on('change', display);

display()
