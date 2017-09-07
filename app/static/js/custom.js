//----------------复杂的自定义覆盖物-----------------------------------------------  
//还未点击的覆盖物  
//初始化，提供一下主要改变的参数  
function BusUnclickedOverlay(point, pay, id) {  
    this._point = point;  
    this._pay = pay;  
    this._id = id;  
}  
BusUnclickedOverlay.prototype = new BMap.Overlay(); //继承百度地图提供的覆盖物的类  
BusUnclickedOverlay.prototype.initialize = function(map) {  
    this._map = map;  
    var div = this._div = document.createElement("div");  
    div.setAttribute("id", "busUnclickedoverLay" + this._id);  
    div.setAttribute("class", "btn btn-primary btn-sm");
    div.style.position = "absolute";  
    div.style.zIndex = BMap.Overlay.getZIndex(this._point.lat);   
    // div.style.fontSize = "42px";
    div.innerHTML = "￥" + this._pay;
    map.getPanes().labelPane.appendChild(div); //将自定义窗口插入到地图样式内部，宠儿达到覆盖默认样式的效果  
  
    return div;
  
}  
  
BusUnclickedOverlay.prototype.draw = function() {  
    var map = this._map;  
    var pixel = map.pointToOverlayPixel(this._point);  
    this._div.style.left = pixel.x + "px"; //控制这个信息窗口针对标注物原点的偏移量，这也是前面div要设置样式position:absolute;  
    this._div.style.top = pixel.y - 60 + "px";
}  