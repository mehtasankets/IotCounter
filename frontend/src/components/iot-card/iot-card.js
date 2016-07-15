export default window.IotCard = (function() {
  var currentScriptElement = document._currentScript || document.currentScript;
  var importDoc = currentScriptElement.ownerDocument;
  class IotCard extends HTMLElement {
  
    // Use createdCallback instead of constructor to init an element.
    createdCallback() {
      var root = this.createShadowRoot();
      var template = document.querySelector('#iot-card');
      var clone = null;

      if (!template) {
        template = importDoc.querySelector('#iot-card');
      }

      clone = document.importNode(template.content, true);
      root.appendChild(clone);
    }
  }
  const IotCardElement = document.registerElement('iot-card', IotCard);
  Object.freeze(IotCard.prototype);
  Object.freeze(IotCard);
  return IotCardElement;
})();
