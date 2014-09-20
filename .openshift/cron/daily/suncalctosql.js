/**
 * Created by tneier on 9/16/14.
 */
var x = 182; //days to go back in time

var today = new Date()

var SunCalc = require('suncalc');

for (x; x > 0; x--){
    var d = new Date();
    d.setDate(today.getDate()-x);
    var sun = SunCalc.getTimes(d, 37.0101, -122.0324)
    var moon = SunCalc.getMoonIllumination(d)
    console.log("INSERT INTO astro VALUES(NULL, '" + d.toISOString().slice(0, 19).replace('T', ' ') + "','" + sun.sunrise.getHours() + ":" + sun.sunrise.getMinutes() + ":00','" + sun.sunset.getHours() +":"+ sun.sunset.getMinutes() + ":00'," +(moon.fraction * 100).toFixed(2) + ", " + (moon.phase*100).toFixed(2) +");" )
}//end for