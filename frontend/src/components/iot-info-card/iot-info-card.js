
function _getTableName(self){
  let tableName = self.stripConfig[self.stripName] + self.refName + 'Counter';
  return tableName;
}

function _attachRefreshListener(self) {
    if(self.stripName === 'Raheja Office' && self.refName != 'Parking') {
      self.shadowRoot.querySelector('.count').innerHTML = 'Coming Soon!';
      return;
    }
    let db = firebase.database();
    let tableName = _getTableName(self);
    self.counterRef = db.ref(tableName);
    self.counterRef.off();
    var setCounter = function(data) {
      var val = data.val();
      self.shadowRoot.querySelector('.count').innerHTML = data.val();
    }.bind(self);
    self.counterRef.on('child_added', setCounter);
    self.counterRef.on('child_changed', setCounter);
}

function _setCardHeader(self) {
  self.shadowRoot.querySelector('.header').innerHTML = self.headerConfig[self.refName];
}

(function() {
  console.log("initializing info card");
  var _refName = '';
  var _stripName = '';
  var _stripConfig = {
    'Phoenix Office': 'phoenix',
    'Raheja Office': 'raheja'
  };
  var _headerConfig = {
    'Badminton': 'Badminton',
    'Gym': 'Gym',
    'Parking': 'Car Parking'
  };
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
  Object.defineProperty(proto, 'refName', {
    get: function() {
      return _refName;
    },
    set: function(refName) {
      _refName = refName;
      _setCardHeader(this);
      _attachRefreshListener(this);
    },
    enumberable: true,
    writeable: true
  });
  Object.defineProperty(proto, 'stripConfig', {
    get: function() {
      return _stripConfig;
    },
    set: function(refName) {
      _stripConfig = stripConfig;
    },
    enumberable: true,
    writeable: true
  });
  Object.defineProperty(proto, 'headerConfig', {
    get: function() {
      return _headerConfig;
    },
    set: function(headerConfig) {
      _headerConfig = headerConfig;
    },
    enumberable: true,
    writeable: true
  });
  Object.defineProperty(proto, 'stripName', {
    get: function() {
      return _stripName;
    },
    set: function(stripName) {
      _stripName = stripName;
    },
    enumberable: true,
    writeable: true
  });
  document.registerElement('iot-info-card', {prototype: proto});
}());