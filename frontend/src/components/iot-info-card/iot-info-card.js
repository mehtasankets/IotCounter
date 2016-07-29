function _setName(self) {
  console.log('set value', self.dataName);
  self.shadowRoot.querySelector('.card-title').innerText = self.dataName;
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
  Object.defineProperty(proto, 'dataName', {
    get: function() {
      return _dataName;
    },
    set: function(dataName) {
      _dataName = dataName;
      _setName(this);
    },
    enumberable: true,
    writeable: true
  });
  document.registerElement('iot-info-card', {prototype: proto});
}());