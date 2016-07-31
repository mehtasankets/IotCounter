function _addCards(self) {
  var cards = ['Badminton', 'Gym', 'Parking'];
  for(let i in cards) {
    var cardNode = document.createElement('iot-info-card');
    cardNode.stripName = self.refName;
    cardNode.refName = cards[i];
    self.shadowRoot.querySelector('.info-card').appendChild(cardNode);
  }
}

function _setHeader(self) {
  var header = self.shadowRoot.querySelector('.header');
  header.innerText = self.refName;
}

(function() {
  console.log("initializing strip");
  var _refName = '';
  var currentScriptElement = document._currentScript || document.currentScript;
  var importDoc = currentScriptElement.ownerDocument;
  var template = document.querySelector('#iot-strip-template');
  var proto = Object.create(HTMLElement.prototype);
  proto.createdCallback = function() {
    if (!template) {
      template = importDoc.querySelector('#iot-strip-template');
    }
    var clone = document.importNode(template.content, true);
    this.createShadowRoot().appendChild(clone);
  }
  Object.defineProperty(proto, 'refName', {
    get: function() {
      return _refName;
    },
    set: function(refName) {
      _refName = refName;
      _setHeader(this);
      _addCards(this);
    },
    enumberable: true,
    writeable: true
  });
  document.registerElement('iot-strip', {prototype: proto});
}());