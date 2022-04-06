document.getElementById("search-near-me").addEventListener('click', searchNearMe)
document.getElementById("search-button").addEventListener('click', search)

function search() {
  setPosition(null, null)

}

function searchNearMe() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(populatePosition, onError)
  } else {
    setPosition(52, 13)
  }
}

function populatePosition(position) {
  setPosition(position.coords.latitude, position.coords.longitude)
}

function setPosition(lat, lng) {
  const latInput = document.getElementsByName("lat")[0]
  const lngInput = document.getElementsByName("lng")[0]

  latInput.value = lat
  lngInput.value = lng
  document.forms["search-form"].submit()
}

function onError(error) {
  switch (error.code) {
    case error.PERMISSION_DENIED:
      console.log("User denied the request for Geolocation.")
      break;
    case error.POSITION_UNAVAILABLE:
      console.log("Location information is unavailable.")
      break;
    case error.TIMEOUT:
      console.log("The request to get user location timed out.")
      break;
    case error.UNKNOWN_ERROR:
      console.log("An unknown error occurred.")
      break;
  }
}