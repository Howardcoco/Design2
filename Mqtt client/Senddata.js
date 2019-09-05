var timing;
var timesRun = 1;
var awsIot = require('aws-iot-device-sdk');
var myDate = new Date(); 
var mytime=myDate.toLocaleTimeString();

var device = awsIot.device({
    keyPath: '743533e38d-private.pem.key',
    caPath: 'RootCA.pem',
    certPath: '743533e38d-certificate.pem.crt',
    clientId: 'TestforDesign',
    host: 'a1voi1b6rjis8a-ats.iot.us-east-1.amazonaws.com'
});

var contents ="started....!!";
console.log('connect');

  device.on('connect', function() {
     device.publish('DesignPolicy', JSON.stringify({ sensor_message: "water",sensor_data: Math.floor(Math.random()*500),time: myDate.toLocaleString( )}));
    console.log('message sent...');
});

//setInterval("device.publish()","1000");
//sensor_data: String(Math.floor(Math.random()*500))
timing=setInterval(function(){
     
var time_s =myDate.getTime();
var newtime =new Date();
newtime.setTime(time_s+5000*timesRun);

device.publish('DesignPolicy', JSON.stringify({ sensor_message: "water",sensor_data:Math.floor(Math.random()*500),time: newtime.toLocaleString( )}));
  console.log('message sent...');

  timesRun += 1;
  if(timesRun === 20){
clearInterval(timing);
}
  }, 100);


device
  .on('message', function(topic, payload) { 
   console.log('message', topic, payload.toString());
 });




