const socket = new WebSocket(
  'ws://' +
  window.location.host +
  '/ws/chat/' +
  'abc' +
  '/'
);

// Event handler when WebSocket connection is established
socket.onopen = function() {
  console.log('WebSocket connection established');

  // Capture audio from the user's microphone
  navigator.mediaDevices.getUserMedia({ audio: true })
    .then(function(stream) {
      // Create AudioContext and MediaStreamAudioSourceNode
      const audioContext = new AudioContext();
      const audioSourceNode = audioContext.createMediaStreamSource(stream);

      // Create ScriptProcessorNode for audio processing
      const scriptNode = audioContext.createScriptProcessor(4096, 1, 1);
      
      // Event handler for scriptNode onaudioprocess event
      scriptNode.onaudioprocess = function(event) {
        // Get the audio data from the input buffer
        const audioData = event.inputBuffer.getChannelData(0);

        // Encode the audio data as base64
        const base64Data = arrayBufferToBase64(audioData.buffer);

        // Send the base64-encoded audio data to the server
        socket.send(base64Data);
      };

      // Connect the audioSourceNode to the scriptNode
      audioSourceNode.connect(scriptNode);
      
      // Connect the scriptNode to the AudioContext destination
      scriptNode.connect(audioContext.destination);
    })
    .catch(function(err) {
      console.log('Error accessing media devices: ', err);
    });
};

// Event handler for WebSocket connection error
socket.onerror = function(error) {
  console.error('WebSocket error:', error);
};

// Event handler for WebSocket connection close
socket.onclose = function() {
  console.log('WebSocket connection closed');
};

// Function to convert ArrayBuffer to base64
function arrayBufferToBase64(buffer) {
  let binary = '';
  const bytes = new Uint8Array(buffer);
  const len = bytes.byteLength;
  for (let i = 0; i < len; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary);
}