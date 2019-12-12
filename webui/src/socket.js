import openSocket from 'socket.io-client';

let whref = window.location.href;
if(whref.indexOf("localhost")!==-1){
  whref = "http://localhost:5000";
}else{
  var arr = window.location.href.split("/");
  var scheme = arr[0];
  whref = scheme + "//" + window.location.hostname + "/"
}
const  s = openSocket(whref);
function socket(cb) {
  s.on('timer', timestamp => cb(null, timestamp));
  s.emit('subscribeToTimer', 1000);
}
export { socket };