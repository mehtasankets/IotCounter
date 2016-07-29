function _addCards(self) {
  var cardNode = document.createElement('iot-info-card');
  self.shadowRoot.querySelector('.row').appendChild(cardNode);
}

function _setHeader(self) {
  var cardNode = self.shadowRoot.querySelector('.row iot-info-card');
  cardNode.shadowRoot.querySelector('.card-title').innerText = self.dataName;
}

(function() {
  console.log("initializing strip");
  var _dataName = '';
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
  Object.defineProperty(proto, 'dataName', {
    get: function() {
      return _dataName;
    },
    set: function(dataName) {
      _dataName = dataName;
      _setHeader(this);
    },
    enumberable: true,
    writeable: true
  });
  document.registerElement('iot-strip', {prototype: proto});
}());