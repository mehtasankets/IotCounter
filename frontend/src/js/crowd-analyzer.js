function _initFirebase (self) {
  var config = {
    apiKey: "AIzaSyCJ6hsMhbWViZ8ozlubxS2B7NstsQTcv8w",
    authDomain: "iotcounter.firebaseapp.com",
    databaseURL: "https://iotcounter.firebaseio.com",
    storageBucket: "iotcounter.appspot.com",
  };
  firebase.initializeApp(config);
  console.log("initialized firebase");
}

(function() {
    _initFirebase(this);
}());