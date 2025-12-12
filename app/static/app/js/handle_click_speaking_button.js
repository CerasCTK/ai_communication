document.addEventListener("DOMContentLoaded", () => {
  const speakingTopicElement = document.querySelector(".speaking-topic");
  if (!speakingTopicElement) return;

  const savedTopic = localStorage.getItem("selected_topic_desc");
  speakingTopicElement.textContent = savedTopic || "No topic selected";

  const speakingButtonElement = document.getElementById("speakingButton");
  if (!speakingButtonElement) return;

  const buttonContentWhenNotSpeaking = speakingButtonElement.textContent;
  const buttonContentWhenSpeaking = `
    <div class="recording-text">
      <span>●</span>
      <span>●</span>
      <span>●</span>
      <span>●</span>
    </div>
  `;

  const WS_URL = "ws://localhost:8000/ws/audio/";
  let ws;
  let mediaStream;
  let audioContext;
  let processor;
  let source;

  const resampleTo16k = (buffer, inputSampleRate) => {
    const targetSampleRate = 16000;
    const ratio = inputSampleRate / targetSampleRate;
    const newLength = Math.round(buffer.length / ratio);
    const resampled = new Float32Array(newLength);

    for (let i = 0; i < newLength; i++) {
      const index = i * ratio;
      const left = Math.floor(index);
      const right = Math.ceil(index);
      const frac = index - left;
      const leftVal = buffer[left] || 0;
      const rightVal = buffer[right] || leftVal;
      resampled[i] = leftVal + (rightVal - leftVal) * frac;
    }
    return resampled;
  };

  speakingButtonElement.addEventListener("click", async () => {
    const isRecording = speakingButtonElement.classList.contains("recording");

    if (!isRecording) {
      speakingButtonElement.classList.add("recording");
      speakingButtonElement.innerHTML = buttonContentWhenSpeaking;

      ws = new WebSocket(WS_URL);
      ws.binaryType = "arraybuffer";

      ws.onopen = () => {
        console.log("✅ WebSocket connected");

        navigator.mediaDevices
          .getUserMedia({ audio: true })
          .then((stream) => {
            mediaStream = stream;

            audioContext = new (window.AudioContext ||
              window.webkitAudioContext)();
            console.log("Mic samplerate = ", audioContext.sampleRate);

            source = audioContext.createMediaStreamSource(stream);

            processor = audioContext.createScriptProcessor(1024, 1, 1);

            source.connect(processor);
            processor.connect(audioContext.destination);

            processor.onaudioprocess = (e) => {
              if (!ws || ws.readyState !== WebSocket.OPEN) return;

              const inputData = e.inputBuffer.getChannelData(0);

              const resampled = resampleTo16k(
                inputData,
                audioContext.sampleRate
              );

              const buffer = new ArrayBuffer(resampled.length * 2);
              const view = new DataView(buffer);

              for (let i = 0; i < resampled.length; i++) {
                let s = Math.max(-1, Math.min(1, resampled[i]));
                view.setInt16(i * 2, s < 0 ? s * 0x8000 : s * 0x7fff, true);
              }

              console.log("Buffer: ", buffer);
              ws.send(buffer);
            };
          })
          .catch((err) => {
            console.error("Microphone error:", err);
          });
      };

      ws.onclose = () => console.log("🔒 WebSocket closed");
      ws.onerror = (err) => console.error("❌ WebSocket error:", err);
    } else {
      // Stop recording
      speakingButtonElement.classList.remove("recording");
      speakingButtonElement.innerHTML = buttonContentWhenNotSpeaking;

      if (processor) {
        processor.disconnect();
      }
      if (audioContext) {
        audioContext.close();
      }
      if (mediaStream) {
        mediaStream.getTracks().forEach((track) => track.stop());
      }
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    }
  });
});
