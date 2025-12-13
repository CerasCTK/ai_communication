// handle_click_speaking_button.js

const WS_URL = "ws://localhost:8000/ws/audio/"; // your WebSocket URL
let ws;
let audioContext;
let mediaStream;
let workletNode;
let workletLoaded = false;

const recordBtn = document.getElementById("speakingButton");
const translationBox = document.getElementById("translationBox");

// Button content
const buttonContentWhenNotSpeaking = recordBtn.textContent;
const buttonContentWhenSpeaking = `
  <div class="recording-text">
    <span>●</span>
    <span>●</span>
    <span>●</span>
    <span>●</span>
  </div>
`;

// Convert Float32Array [-1,1] to PCM16 bytes
function float32ToPCM16(float32Array) {
  const buffer = new ArrayBuffer(float32Array.length * 2);
  const view = new DataView(buffer);
  for (let i = 0; i < float32Array.length; i++) {
    let s = Math.max(-1, Math.min(1, float32Array[i]));
    view.setInt16(i * 2, s * 0x7fff, true);
  }
  return buffer;
}

// Start recording
async function startRecording() {
  ws = new WebSocket(WS_URL);
  ws.binaryType = "arraybuffer";

  // Update the translation box when server sends transcription
  ws.onmessage = (e) => {
    console.log("TRANSCRIBED:", e.data);
    translationBox.textContent = e.data; // display transcription in the box
  };

  ws.onopen = async () => {
    console.log("WebSocket connected");

    // Get microphone
    mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
    audioContext = new AudioContext({ sampleRate: 48000 });

    // Load AudioWorklet if not loaded
    if (!workletLoaded) {
      await audioContext.audioWorklet.addModule(
        "static/app/js/audio_worklet_processor.js"
      );
      console.log("Worklet loaded");
      workletLoaded = true;
    }

    const source = audioContext.createMediaStreamSource(mediaStream);

    // Create worklet node to process audio
    workletNode = new AudioWorkletNode(audioContext, "recorder-processor");

    // Listen to processed audio chunks
    workletNode.port.onmessage = (event) => {
      if (!ws || ws.readyState !== WebSocket.OPEN) return;

      const chunk = event.data; // Float32Array chunk
      const pcm16 = float32ToPCM16(chunk); // convert to PCM16 bytes
      ws.send(pcm16); // send to Django WebSocket
    };

    source.connect(workletNode);
    workletNode.connect(audioContext.destination); // optional for monitoring
    console.log("Recording started");
  };

  ws.onclose = () => {
    console.log("WebSocket disconnected");
  };

  ws.onerror = (err) => {
    console.error("WebSocket error:", err);
  };
}

// Stop recording
async function stopRecording() {
  if (workletNode) {
    workletNode.disconnect();
    workletNode = null;
  }

  if (mediaStream) {
    mediaStream.getTracks().forEach((t) => t.stop());
    mediaStream = null;
  }

  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.close();
  }
  ws = null;
}

// Handle button click
recordBtn.addEventListener("click", () => {
  if (!recordBtn.classList.contains("recording")) {
    // Start speaking
    translationBox.textContent = ""; // clear previous transcription
    recordBtn.classList.add("recording");
    recordBtn.innerHTML = buttonContentWhenSpeaking;
    startRecording();
  } else {
    // Stop speaking
    recordBtn.classList.remove("recording");
    recordBtn.innerHTML = buttonContentWhenNotSpeaking;
    stopRecording();
  }
});
