function RouteInfoOverlay(point, html_content) {  
    this._point = point;
    this._content = html_content;
}  
RouteInfoOverlay.prototype = new BMap.Overlay(); 
RouteInfoOverlay.prototype.initialize = function(map) {  
    this._map = map;
    var div = this._div = document.createElement("div");  
    div.setAttribute("class", "alert alert-info alert-dismissible");
    div.setAttribute("role", "alert");
    div.style.position = "absolute";
    div.style.width = "310px";
    div.style.zIndex = "10000";
    var btn = document.createElement("button");
    btn.setAttribute("type", "button");
    btn.setAttribute("class", "close");
    btn.setAttribute("data-dismiss", "alert");
    btn.setAttribute("aria-label", "Close");
    btn.innerHTML = '<span aria-hidden="true">×</span>';
    div.appendChild(btn);
    div.innerHTML += this._content;
    map.getPanes().floatPane.appendChild(div); 
    return div;
  
}  
  
RouteInfoOverlay.prototype.draw = function() {  
    var map = this._map;  
    var pixel = map.pointToOverlayPixel(this._point);  
    this._div.style.left = pixel.x + "px";
    this._div.style.top = pixel.y + "px";
}

function ShopInfoOverlay(point, html_content) {  
    this._point = point;
    this._content = html_content;
}  
ShopInfoOverlay.prototype = new BMap.Overlay(); 
ShopInfoOverlay.prototype.initialize = function(map) {  
    this._map = map;
    var div = this._div = document.createElement("div");  
    div.setAttribute("class", "alert alert-info alert-dismissible");
    div.setAttribute("role", "alert");
    div.style.position = "absolute";
    div.style.width = "400px";
    div.style.height = "260px";
    div.style.zIndex = "800";
    //div.style.zIndex = BMap.Overlay.getZIndex(this._point.lat);
    var btn = document.createElement("button");
    btn.setAttribute("type", "button");
    btn.setAttribute("class", "close");
    btn.setAttribute("data-dismiss", "alert");
    btn.setAttribute("aria-label", "Close");
    btn.innerHTML = '<span aria-hidden="true">×</span>';
    div.appendChild(btn);
    div.innerHTML += this._content;
    map.getPanes().floatPane.appendChild(div); 
    return div;
}  
  
ShopInfoOverlay.prototype.draw = function() {  
    var map = this._map;
    var pixel = map.pointToOverlayPixel(this._point);  
    this._div.style.left = pixel.x - 200 + "px";
    this._div.style.top = pixel.y - 280 + "px";
}

