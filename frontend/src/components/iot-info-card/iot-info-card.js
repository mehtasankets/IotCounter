
function _setHeader(self) {
  self.shadowRoot.querySelector('.header').innerHTML = self.refName;
}

(function() {
  console.log("initializing info card");
  var _dataName = '';
  var currentScriptElement = document._currentScript || document.currentScript;
  var importDoc = currentScriptElement.ownerDocument;
  var template = document.querySelector('#iot-info-card-template');
  var proto = Object.create(HTMLElement.prototype);
  proto.createdCallback = function() {
    if (!template) {
      template = importDoc.querySelector('#iot-info-card-template');
    }
    var clone = document.importNode(template.content, true);
    this.createShadowRoot().appendChild(clone);
  }  
  proto.attachedCallback = function() {
      //_setName(this);
  }
  Object.defineProperty(proto, 'refName', {
    get: function() {
      return _refName;
    },
    set: function(refName) {
      _refName = refName;
      _setHeader(this);
    },
    enumberable: true,
    writeable: true
  });
  document.registerElement('iot-info-card', {prototype: proto});
}());