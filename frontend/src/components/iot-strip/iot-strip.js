function _addCards(self) {
  var cardNode = document.createElement('iot-info-card');
  self.shadowRoot.querySelector('.row').appendChild(cardNode);
}

function _setHeader(self, headerMap) {
  var header = self.shadowRoot.querySelector('.header');
  header.innerText = headerMap[self.refName];
}

(function() {
  console.log("initializing strip");
  var _headerMap = {
    'badminton': 'Badminton Court',
    'gym': 'Gym',
    'activityRoom': 'Activity Room'
  };
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
    _addCards(this);
  }
  Object.defineProperty(proto, 'refName', {
    get: function() {
      return _refName;
    },
    set: function(refName) {
      _refName = refName;
      _setHeader(this, _headerMap);
    },
    enumberable: true,
    writeable: true
  });
  document.registerElement('iot-strip', {prototype: proto});
}());