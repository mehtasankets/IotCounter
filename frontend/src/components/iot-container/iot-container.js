'use strict';

function _addStrips(self) {
  let stripRefNames = ['Phoenix Office', 'Raheja Office'];
  for(let i in stripRefNames) {
    var stripNode = document.createElement('iot-strip');
    stripNode.refName = stripRefNames[i];
    self.shadowRoot.querySelector('#strips').appendChild(stripNode);
  }
}

(function() {
  console.log("initializing container");
  var currentScriptElement = document._currentScript || document.currentScript;
  var importDoc = currentScriptElement.ownerDocument;
  var template = document.querySelector('#iot-container-template');
  var proto = Object.create(HTMLElement.prototype);
  proto.createdCallback = function() {
    if (!template) {
      template = importDoc.querySelector('#iot-container-template');
    }
    var clone = document.importNode(template.content, true);
    this.createShadowRoot().appendChild(clone);
    _addStrips(this);
  }
  document.registerElement('iot-container', {prototype: proto});
}());