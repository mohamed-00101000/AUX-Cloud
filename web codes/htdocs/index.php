<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0" , user-scalable=no>
  <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>

  <title>Vehicle Dashboard</title>
  <link rel="stylesheet" href="style.css">

</head>

<body>
  <div class="homepage__bg" style="background-image: url('/assets/home.jpg');"></div>

  <div class="header">Vehicle Dashboard</div>

  <script>
    $(function () {
      var range = $("#range")[0];

      function updateCircle() {
        var percent = ((range.value - range.min) / (range.max - range.min)) * 5;
        var percentshow = Math.round(((range.value - range.min) / (range.max - range.min)) * 100);

        // Remove the previous style and update based on the percentage
        $("#meterstyle").remove();

        if (percent < 5) {
          $(".progress .circle").attr("style", "animation-delay:-" + percent + "s");
          $("body").append("<div id='meterstyle'><style>.progress:after{animation-delay:-" + percent + "s;}</style></div>");
        } else {
          $(".progress .circle").attr("style", "animation-delay:5s");
          $("body").append("<div id='meterstyle'><style>.progress:after{animation-delay:5s;}</style></div>");
        }

        $(".progress .precent").text(percentshow + " km/h");
      }

      // Update the circle periodically
      setInterval(updateCircle, 1);

      // Update the circle on input change
      $(document).on("input", "#range", function () {
        updateCircle();
      });
    });

    // Function to update the icons visibility based on JSON data
    function updateIcons(data) {

    }






    function fetchDataFromJSON() {

      const isOn = v => v === "1" || v === 1;
      const setIndicator = (id, on, { blink = false } = {}) => {
        const el = document.getElementById(id);
        if (!el) return;
        el.classList.toggle('on', !!on);
        el.classList.toggle('blink', !!(on && blink));
      };


      fetch('./new/data.json') // Fetch data from the external URL
        .then(response => response.json())
        .then(data => {
          if (data.length === 0) {
            console.error('No data found');
            return;
          }
          const latestData = data[0]; // Assuming the JSON contains an array and we want the first object

          console.log('Fetched data:', latestData); // Log the data to the console

          // Update dashboard values
          document.getElementById('energyConsumed').textContent = `${latestData.energy_consumed || 'N/A'} J`;
          document.getElementById('powerConsumed').textContent = `${latestData.power_consumed || 'N/A'} W`;
          document.getElementById('totalCurrent').textContent = `${latestData.total_current || 'N/A'} A`;
          document.getElementById('totalVoltage').textContent = `${latestData.total_voltage || 'N/A'} v`;
          document.getElementById('YawRatefast').textContent = `${latestData.yaw_rate || 'N/A'} rad/s`;
          document.getElementById('ambientTemp').textContent = `${latestData.ambient_temperature || 'N/A'} °C`;
          document.getElementById('righttemp').textContent = `${latestData.right_inverter_max_temp || 'N/A'} °C`;
          document.getElementById('leftInverterTemp').textContent = `${latestData.left_inverter_max_temp || 'N/A'} °C`;


          // Display number_of_labs
          // document.querySelector('.text_button').textContent = latestData.number_of_labs || 'N/A';

          // Update SOC and battery-level
          const socValue = latestData.soc || 0;
          const batteryLevel = document.querySelector('.battery-level');
          batteryLevel.style.height = `${socValue}%`;
          batteryLevel.style.backgroundColor = getBatteryColor(socValue);
          batteryLevel.querySelector('span').textContent = `${socValue}%`;

          // Additionally, display raw JSON in #data-display div
          //  document.getElementById('data-display').textContent = JSON.stringify(latestData, null, 2);

          // Update car speed
          //const carSpeed = latestData.car_speed_gauge || 0;
          //document.getElementById('range').value = carSpeed;
          //document.querySelector('.precent').textContent = `${carSpeed} km/h`;
          // Update car speed
          const carSpeedRaw = parseFloat(latestData.car_speed_gauge || 0);
          const carSpeedRounded = Math.round(carSpeedRaw); // you can change to: parseFloat(carSpeedRaw.toFixed(1))

          if (lastSpeedDisplayed === null || Math.abs(carSpeedRounded - lastSpeedDisplayed) >= 1) {
            document.getElementById('range').value = carSpeedRounded;
            document.querySelector('.precent').textContent = `${carSpeedRounded} km/h`;
            lastSpeedDisplayed = carSpeedRounded;
          }


          // // Check turn right status and apply style changes
          // if (latestData.turnright === "0") {
          //   document.getElementById('turnright_off').style.display = 'block'; // Show the "off" icon
          //   document.getElementById('turnright_on').style.display = 'none'; // Hide the "on" icon
          // } else {
          //   document.getElementById('turnright_on').style.display = 'block'; // Show the "on" icon
          //   document.getElementById('turnright_off').style.display = 'none'; // Hide the "off" icon
          // }

          // // Check turn right status and apply style changes
          // if (latestData.turnleft === "0") {
          //   document.getElementById('turnleft_off').style.display = 'block'; // Show the "off" icon
          //   document.getElementById('turnleft_on').style.display = 'none'; // Hide the "on" icon
          // } else {
          //   document.getElementById('turnleft_on').style.display = 'block'; // Show the "on" icon
          //   document.getElementById('turnleft_off').style.display = 'none'; // Hide the "off" icon
          // }

          // // Check turn right status and apply style changes
          // if (latestData.lights_v1 === "0") {
          //   document.getElementById('lights_v1_off').style.display = 'block'; // Show the "off" icon
          //   document.getElementById('lights_v1_on').style.display = 'none'; // Hide the "on" icon
          // } else {
          //   document.getElementById('lights_v1_on').style.display = 'block'; // Show the "on" icon
          //   document.getElementById('lights_v1_off').style.display = 'none'; // Hide the "off" icon
          // }

          setIndicator('ind-left', isOn(latestData.turnleft), { blink: true }); // left signal blinks
          setIndicator('ind-right', isOn(latestData.turnright), { blink: true }); // right signal blinks
          setIndicator('ind-high', isOn(latestData.lights_v1), { blink: false }); // high beam steady



        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
    }

    function fetchdriverFromJSON() {
      fetch('https://racingteam.rf.gd/new/driver.json') // Fetch driver from the external URL
        .then(response => response.json())
        .then(driver => {
          if (driver.length === 0) {
            console.error('No driver found');
            return;
          }
          const latestdriver = driver[0]; // Assuming the JSON contains an array and we want the first object

          console.log('Fetched driver:', latestdriver); // Log the driver to the console


          // Display number_of_labs
          document.querySelector('.text_button').textContent = latestdriver.number_of_labs || '0';


        })
        .catch(error => {
          console.error('Error fetching driver:', error);
        });
    }



    // Fetch data every 500ms
    setInterval(fetchDataFromJSON, 500);
    setInterval(fetchdriverFromJSON, 500);

    setInterval(updateIcons, 500);

    // Helper function to get battery color based on SOC
    function getBatteryColor(soc) {
      if (soc >= 0 && soc < 20) return 'red';
      if (soc >= 20 && soc < 50) return 'orange';
      if (soc >= 50 && soc < 80) return '#3d5a80';
      if (soc >= 80 && soc <= 100) return 'green';
      return 'gray';
    }
  </script>



  </div>

  <div id="data-display"></div>


  <div class="All">
    <!-- Button showing number_of_labs -->
    <button class="button">
      <div class="dots_border"></div>
      <span class="text_button">N/A</span>
      <p>Number of labs</p>
    </button>

    <div class="r">
      <div class="progress">
        <div class="precent">0 km/h</div>
        <div class="circle"></div>
        <div class="range">
          <input type="range" min="0" max="100" value="0" id="range">
        </div>
      </div>
    </div>

    <!-- Battery SOC -->
    <div class="c_battery" style="border: 2px solid gray;">
      <div class="battery-icon" style="border: 2px solid gray;">
        <div class="battery-level" style="background-color: gray; height: 0%;">
          <span>N/A%</span>
        </div>
      </div>
    </div>
  </div>

  <!-- put indicators under the gauge -->
  <div class="mini-container indicators">
    
    <div class="indicator right" id="ind-right" title="Right indicator">
      <img src="assets/right.svg" alt="Right">
    </div>

    <div class="indicator high" id="ind-high" title="High beam">
      <img src="assets/high-beam.svg" alt="High beam">
    </div>

    <div class="indicator left" id="ind-left" title="Left indicator">
      <img src="assets/left.svg" alt="Left">
    </div>

  </div>



  <script>
    let lastSpeedDisplayed = null;

    document.addEventListener('DOMContentLoaded', function () {
      const mediaQuery = window.matchMedia('(max-width: 768px)');
      const button = document.querySelector('.button');
      const cBattery = document.querySelector('.c_battery');
      const miniContainer = document.querySelector('.mini-container');
      const allDiv = document.querySelector('.All');
      const rDiv = document.querySelector('.r');

      // Store original positions
      const originalButtonNextSibling = button.nextElementSibling; // Should be .r
      const originalCBatteryNextSibling = cBattery.nextElementSibling; // Should be .mini-container

      function handleMediaChange(e) {
        if (e.matches) {
          // Move to mini-container when width <= 768px
          if (button.parentNode === allDiv) {
            miniContainer.appendChild(button);
            miniContainer.appendChild(cBattery);
          }
        } else {
          // Move back to original positions in .All when width > 768px
          if (button.parentNode === miniContainer) {
            allDiv.insertBefore(button, rDiv);
            allDiv.insertBefore(cBattery, miniContainer);
          }
        }
      }

      // Initial check
      handleMediaChange(mediaQuery);

      // Listen for changes
      mediaQuery.addListener(handleMediaChange);
    });
  </script>

  </div>
  <div class="warp">
    <div class="box">
      <div class="dashboard">
        <div class="item">
          <h3>Energy Consumed</h3>
          <div class="value" id="energyConsumed"></div>
        </div>
        <div class="item">
          <h3>Power Consumed</h3>
          <div class="value" id="powerConsumed"></div>
        </div>
        <div class="item">
          <h3>Total Current</h3>
          <div class="value" id="totalCurrent"></div>
        </div>
        <div class="item">
          <h3>Total Voltage</h3>
          <div class="value" id="totalVoltage"></div>
        </div>
        <div class="item">
          <h3>Yaw Rate</h3>
          <div class="value" id="YawRatefast"></div>
        </div>
        <div class="item">
          <h3>Ambient Temperature</h3>
          <div class="value" id="ambientTemp"></div>
        </div>
        <div class="item">
          <h3>Right Inverter Temperature</h3>
          <div class="value" id="righttemp"></div>
        </div>
        <div class="item">
          <h3>Left Inverter Temperature</h3>
          <div class="value" id="leftInverterTemp"></div>
        </div>
      </div>
    </div>
  </div>
</body>

</html>