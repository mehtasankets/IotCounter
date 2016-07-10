'use strict';

function IotUI() {
  this.badmintonCount = document.querySelector('#badminton-court-count');
  this.initFirebase();
  this.refreshCounter();
}

IotUI.prototype.initFirebase = function () {
  // Initialize Firebase
  var config = {
    apiKey: "AIzaSyCJ6hsMhbWViZ8ozlubxS2B7NstsQTcv8w",
    authDomain: "iotcounter.firebaseapp.com",
    databaseURL: "https://iotcounter.firebaseio.com",
    storageBucket: "iotcounter.appspot.com",
  };
  firebase.initializeApp(config);
  this.database = firebase.database();
  console.log("initialized firebase.");
}

IotUI.prototype.refreshCounter = function() {
  this.counterRef = this.database.ref('badmintonCounter');
  // Make sure we remove all previous listeners.
  this.counterRef.off();
  var setCounter = function(data) {
    var val = data.val();
    this.badmintonCount.innerHTML = data.val();
  }.bind(this);
  this.counterRef.on('child_added', setCounter);
  this.counterRef.on('child_changed', setCounter);

}

window.onload = function() {
  window.IotUI = new IotUI();
};
