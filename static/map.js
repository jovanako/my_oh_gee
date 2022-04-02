function initMap() {
  const berlin = new google.maps.LatLng(52.51807415366815, 13.403719548295928)

  const map = new google.maps.Map(document.getElementById("map"), {
    center: berlin,
    zoom: 12,
  })

  const infoWindow = new google.maps.InfoWindow()
  venues.forEach(venue => initMarker(venue, map, infoWindow))
}

function initMarker(venue, map, infoWindow) {
  const marker = new google.maps.Marker({
    map: map,
    position: venue.location
  })

  marker.addListener('click', () => {
    infoWindow.setContent(
      `<img src='/static/venue_pics/${venue.imagePath}'>
      <div class='venue-name'><a href="${venue.webpage}">${venue.name}</a></div>
      <div class="venue-address">${venue.address}</div>
      <div class="venue-requirement">${venue.requirement}</div>`)

    infoWindow.open({
      anchor: marker,
      map,
      shouldFocus: false,
    })
  })
}