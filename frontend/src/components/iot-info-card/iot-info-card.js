function _setCircle(self, val, limit) {
  let canvas = self.shadowRoot.querySelector('.count-anim');
  let context = canvas.getContext('2d');
  let centerX = canvas.width / 2;
  let centerY = canvas.height / 2;
  let radius = 50;

  if(val >= limit) {
    val = limit - 2;
  }
  let fillUpto = 100 * val / limit;
  context.clearRect(0, 0, canvas.width, canvas.height);
  let amount = 0;
  let amountToIncrease = 2;
  let colorStep = Math.floor(((255/limit)*val)/(fillUpto/amountToIncrease));
  //sconsole.log(colorStep);
  let r = 0;
  let g = 255;
  let b = 0;
  function _draw() {
      if(amount > fillUpto) {
        return;
      }
      context.save();
      context.beginPath();
      context.arc(centerX, centerY, radius, 0, 2 * Math.PI, false);
      context.clip();
      r = (r + colorStep);
      g = (g - colorStep);
      context.fillStyle = "rgb("+r+","+g+","+b+")";
      context.fillRect(centerX - radius, centerY + radius, radius * 2, -amount);
      context.restore();
      context.beginPath();
      context.arc(centerX, centerY, radius, 0, 2 * Math.PI, false);
      context.lineWidth = 2;
      context.strokeStyle = '#000000';
      context.stroke();
      
      // Every time, raise amount by some value:
      amount += amountToIncrease;
  }

  _draw();
  // Every second we'll fill more;
  setInterval(_draw, 20);
}

function _setComingSoonCircle(self) {
  let canvas = self.shadowRoot.querySelector('.count-anim');
  let context = canvas.getContext('2d');
  let centerX = canvas.width / 2;
  let centerY = canvas.height / 2;
  let radius = 50;
  context.beginPath();
  context.arc(centerX, centerY, radius, 0, 2 * Math.PI, false);
  context.lineWidth = 2;
  context.strokeStyle = '#000000';
  context.stroke();
  context.textBaseline = "center";
  context.fillText("Coming soon!", centerX-radius/4, centerY-radius/2);
  context.save();
  
}

function _getTableName(self){
  let tableName = self.stripConfig[self.stripName] + self.refName + 'Counter';
  return tableName;
}

function _attachRefreshListener(self) {
    if(self.stripName === 'Raheja Office' && self.refName != 'Parking') {
      _setComingSoonCircle(self);
      self.shadowRoot.querySelector('.count-text').innerHTML = '<h3>Coming Soon!</h3>';
      return;
    }
    let db = firebase.database();
    let tableName = _getTableName(self);
    self.counterRef = db.ref(tableName);
    self.counterRef.off();
    let setCounter = function(data) {
      let val = data.val();
      _setCircle(self, val, 60);
      let name = self.shadowRoot.querySelector('.header').innerText;
      console.log(val);
      let countText = '<h3>Currently, there are <strong>' + data.val() + '</strong> people in ' + name + '</h3>';
      self.shadowRoot.querySelector('.count-text').innerHTML = countText;
    }
    self.counterRef.on('child_added', setCounter);
    self.counterRef.on('child_changed', setCounter);
}

function _setCardHeader(self) {
  self.shadowRoot.querySelector('.header').innerHTML = self.headerConfig[self.refName];
  self.shadowRoot.querySelector('.history').href = '/graph.html?ref=' + _getTableName(self);
}

(function() {
  console.log("initializing info card");
  let _refName = '';
  let _stripName = '';
  let _stripConfig = {
    'Phoenix Office': 'phoenix',
    'Raheja Office': 'raheja'
  };
  let _headerConfig = {
    'Badminton': 'Badminton',
    'Gym': 'Gym',
    'Parking': 'Car Parking'
  };
  let currentScriptElement = document._currentScript || document.currentScript;
  let importDoc = currentScriptElement.ownerDocument;
  let template = document.querySelector('#iot-info-card-template');
  let proto = Object.create(HTMLElement.prototype);
  proto.createdCallback = function() {
    if (!template) {
      template = importDoc.querySelector('#iot-info-card-template');
    }
    let clone = document.importNode(template.content, true);
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