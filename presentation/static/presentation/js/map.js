"use strict";

var center = [46.3507193554773, 2.603759765625]; //Montluçon
var zoom = 6;

var map = L.map('mapid').setView(center, zoom);

var markers = []

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    // Alternative maps are listed in https://www.mapbox.com/api-documentation/#maps
    id: 'mapbox.streets',
    // This token is assigned to the user jpnoel (email: jpnoel@gmail.com) - See https://www.mapbox.com/studio/account/tokens/
    accessToken: 'pk.eyJ1IjoianBub2VsIiwiYSI6ImNpbXo5MGdnejAwbG92OWx5amt5cWV4ejAifQ.vJAEgiLq2bdVEGld5mau5A'
}).addTo(map);


function display_event(index, event) {
    var addresses = event.addresses
    console.log(addresses);
    var prefix = '' +
        '<b>Nom</b>: ' + event.name + '</br>' +
        '<b>Association</b>: ' + event.project.fields.name + '</br>' +
        '<b>Contact</b>: ' + event.contact + '</br>' +
        '<b>Date de début</b>: ' + event.start_date.slice(0, 10) + '</br>' +
        '<b>Date de fin</b>: ' + event.end_date.slice(0, 10) + '</br>'
    for (var index in addresses) {
        var address = addresses[index]
        var point_prefix = 'SRID=4326;POINT ('
        var point_suffix = ')'
        var lon_lat = address.fields.point.slice(point_prefix.length, -point_suffix.length).split(' ')
        var marker = L.marker([lon_lat[1], lon_lat[0]]).addTo(map);
        var content = prefix +
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
        markers.push(marker);
    }
}

function display() {
    var url = 'map_events';
    var args = []
    var month = $('#month').val()
    if (month !== 'Tous') {
        args.push('month=' + month)
    }
    var project = $('#project').val()
    if (project !== 'Tous') {
        args.push('project=' + project)
    }
    var department = $('#department').val()
    if (department !== 'Tous') {
        args.push('department=' + department)
    }
    if (args.length !== 0) {
        url = url + '?' + args.join('&')
    }
    console.log('url', url)
    console.log('markers', markers)
    for (var index in markers) {
        map.removeLayer(markers[index]);
    }
    markers = [];
    console.log('markers_empty', markers)
    $.getJSON(url, function(data) {
        $.each(data['events'], display_event)
            }).fail(function() {
                console.log('fail');
            })
}

$('#project').on('change', display)

$('#department').on('change', display)

$('#month').on('change', display)

display()
