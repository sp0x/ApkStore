import client from 'socket.io-client';
let whref = window.location.href;
if(whref.indexOf("localhost")!==-1){
  whref = "http://localhost:5000";
}else{
  var arr = window.location.href.split("/");
  var scheme = arr[0];
  whref = scheme + "//" + window.location.hostname + "/"
}
//const  s = openSocket(whref);
function socket(cb) {
  let socket = client(whref);
  socket.on('timer', timestamp => cb(null, timestamp));
  socket.emit('subscribeToTimer', 1000);
  socket.on('connection', ()=>{
    console.log("Connected");
  })
}
export { socket };