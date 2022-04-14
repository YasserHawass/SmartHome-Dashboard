alert('If you see this alert, then your custom JavaScript script has run!')

// window.addEventListener("DOMContentLoaded", function () {
  // LIGHTS
  const lightsToggleButton = document.getElementById('lights-toggle-button')
  const light1 = document.getElementById('light-1')
  const light2 = document.getElementById('light-2')
  const light3 = document.getElementById('light-3')

  function turnOnLights() {
    lightsToggleButton.addEventListener('change', () => {
      light1.classList.toggle('light')
      light2.classList.toggle('light')
      light3.classList.toggle('light')
    })
  }
  turnOnLights()
// });

  

  

  // VACUUM
  const cleaningToggleButton = document.getElementById('cleaning-toggle-button')
  const vacuum = document.getElementById('vacuum')

  function turnOnVaccum() {
    cleaningToggleButton.addEventListener('change', () => {
      vacuum.classList.toggle('vacuum')
    })
  }

  turnOnVaccum()

  // MUSIC
  const musicToggleButton = document.getElementById('music-toggle-button')
  const audio = document.getElementById('audio')
  const audioContext = new AudioContext()
  const source = audioContext.createMediaElementSource(audio)
  source.connect(audioContext.destination)
  let paused = true

  function turnOnMusic() {
    musicToggleButton.addEventListener('change', () => {
      if (paused) {
        audio.play()
        paused = false
        audioContext.resume() // For best practice (https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Best_practices)
      } else {
        audio.pause()
        paused = true
        audioContext.resume() // For best practice (https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Best_practices)
      }
    })
  }

  turnOnMusic()

  // SENSOR
  const motionSensorToggleButton = document.getElementById('motion-sensor-toggle-button')
  const sensor = document.getElementById('sensor')

  function turnOnSensor() {
    motionSensorToggleButton.addEventListener('change', () => {
      sensor.classList.toggle('sensor')
    })
  }

  turnOnSensor()