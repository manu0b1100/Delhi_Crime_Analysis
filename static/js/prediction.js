var mapgoogle;
var lat;
var long;
var marker;


function placemarker_panto(latLng, mapgoogle) {

    marker = new google.maps.Marker({
        position: latLng,
        map: mapgoogle
    });
    mapgoogle.panTo(latLng);

}

function geocodeAddress(geocoder, resultsMap) {
    var address = document.getElementById('address').value;
    geocoder.geocode({'address': address}, function (results, status) {
        if (status === 'OK') {
            resultsMap.setCenter(results[0].geometry.location);
            marker = new google.maps.Marker({
                map: resultsMap,
                position: results[0].geometry.location
            });
            lat = results[0].geometry.location.lat();
            long = results[0].geometry.location.lng();
            set_district()
        } else {
            alert('Geocode was not successful for the following reason: ' + status);
        }
    });
}

function onDistrictChange() {
    console.log('select changed');

    $.ajax({
        type: 'POST',
        url: '/getpoliceStation',
        data: {
            district: $('#proba_district_select').val()
        },
        success: function (data) {
            data = JSON.parse(data)
            $('#proba_pstation_select').find('option').remove()
            $.each(data, function (index, value) {

                $('#proba_pstation_select').append($('<option>', {value: value}).text(value));

            });
            set_pstation()


        }
    });

}

function set_pstation() {

    $.ajax({
        type: 'POST',
        url: '/predictPstation',
        data: {
            "lat": lat,
            "long": long,
            "district": $('#proba_district_select').val()
        },
        success: function (data) {
            data = JSON.parse(data);
            console.log(data)

            $('#proba_pstation_select option').each(function () {
                // console.log($(this).val())

                if ($(this).val() === data['pstation']) {
                    // console.log($(this).val())
                    $('#proba_pstation_select').val($(this).val())
                }

            })


        }
    });

}

function set_district() {

    $.ajax({
        type: 'POST',
        url: '/predictDistrict',
        data: {
            "lat": lat,
            "long": long
        },
        success: function (data) {
            console.log(data)
            data = JSON.parse(data)
            $('#proba_district_select').val(data['district'])
            onDistrictChange()

        }
    });


}

function initMap() {
    mapgoogle = new google.maps.Map(document.getElementById('mapgoogle'), {
        center: {lat: 28.644800, lng: 77.216721},
        zoom: 12
    });
    placemarker_panto({lat: 28.644800, lng: 77.216721}, mapgoogle);
    mapgoogle.addListener('click', function (e) {
        if (marker) {
            marker.setMap(null)
        }
        var latLng = e.latLng;
        console.log(latLng.lat());
        lat = latLng.lat();
        long = latLng.lng();
        placemarker_panto(latLng, mapgoogle);
        set_district();

    });
    var geocoder = new google.maps.Geocoder();

    document.getElementById('submit').addEventListener('click', function () {
        if (marker) {
            marker.setMap(null)
        }
        geocodeAddress(geocoder, mapgoogle);

    });
}

$(document).ready(function () {

    $('#subproba').click(function () {
        $.ajax({
            type: 'POST',
            url: "calc_func",
            data: {
                function: 'probachart',
                hour: $('#proba_hour_select').val(),
                district: $('#proba_district_select').val(),
                pstation: $('#proba_pstation_select').val(),
                lat: lat,
                long: long
            }
            , success: function (data) {
                $('#proba_graph').html(data)
            }
        });
    });

    $('#proba_district_select').change(onDistrictChange);

});
