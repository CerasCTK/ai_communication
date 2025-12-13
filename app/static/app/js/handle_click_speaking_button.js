const WS_URL = "ws://localhost:8000/ws/audio/";
let ws;
let audioContext;
let mediaStream;
let workletNode;
let workletLoaded = false;

const recordBtn = document.getElementById("speakingButton");

const buttonContentWhenNotSpeaking = recordBtn.textContent;
const buttonContentWhenSpeaking = `
  <div class="recording-text">
    <span>●</span>
    <span>●</span>
    <span>●</span>
    <span>●</span>
  </div>
`;

async function startRecording() {
  ws = new WebSocket(WS_URL);
  ws.binaryType = "arraybuffer";

  ws.onmessage = (e) => {
    console.log("TRANSCRIBED:", e.data);
  };

  ws.onopen = async () => {
    console.log("WS connected");

    mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
    audioContext = new AudioContext({ sampleRate: 48000 });

    if (!workletLoaded) {
      await audioContext.audioWorklet.addModule(
        "static/app/js/audio_worklet_processor.js"
      );
      console.log("Worket loaded");
      workletLoaded = true;
    }

    const source = audioContext.createMediaStreamSource(mediaStream);

    workletNode = new AudioWorkletNode(audioContext, "recorder-processor");

    workletNode.port.onmessage = (event) => {
      if (!ws || ws.readyState !== WebSocket.OPEN) return;

      const chunk = event.data;
      const pcm16 = float32ToPCM16(chunk);
      console.log("pcm16", pcm16);
      ws.send(pcm16);
    };

    source.connect(workletNode);
    console.log("Recording started");
  };
}

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

function float32ToPCM16(float32Array) {
  const buffer = new ArrayBuffer(float32Array.length * 2);
  const view = new DataView(buffer);
  for (let i = 0; i < float32Array.length; i++) {
    let s = Math.max(-1, Math.min(1, float32Array[i]));
    view.setInt16(i * 2, s * 0x7fff, true);
  }
  return buffer;
}

recordBtn.addEventListener("click", () => {
  if (!recordBtn.classList.contains("recording")) {
    recordBtn.classList.add("recording");
    recordBtn.innerHTML = buttonContentWhenSpeaking;
    startRecording();
  } else {
    recordBtn.classList.remove("recording");
    recordBtn.innerHTML = buttonContentWhenNotSpeaking;
    stopRecording();
  }
});
