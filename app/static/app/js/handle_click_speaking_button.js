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

  speakingButtonElement.addEventListener("click", async () => {
    const isRecording = speakingButtonElement.classList.contains("recording");

    if (!isRecording) {
      speakingButtonElement.classList.add("recording");
      speakingButtonElement.innerHTML = buttonContentWhenSpeaking;

      // 1. Mở WebSocket
      ws = new WebSocket(WS_URL);
      ws.binaryType = "arraybuffer";

      ws.onopen = () => {
        console.log("✅ WebSocket connected");

        // 2. Lấy micro
        navigator.mediaDevices.getUserMedia({ audio: true })
          .then(stream => {
            mediaStream = stream;
            audioContext = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
            const source = audioContext.createMediaStreamSource(stream);

            // 3. Tạo ScriptProcessorNode để lấy PCM
            processor = audioContext.createScriptProcessor(1024, 1, 1);
            source.connect(processor);
            processor.connect(audioContext.destination);

            processor.onaudioprocess = e => {
              const inputData = e.inputBuffer.getChannelData(0);
              const buffer = new ArrayBuffer(inputData.length * 2);
              const view = new DataView(buffer);

              // Float32 -> Int16
              for (let i = 0; i < inputData.length; i++) {
                let s = Math.max(-1, Math.min(1, inputData[i]));
                view.setInt16(i * 2, s < 0 ? s * 0x8000 : s * 0x7fff, true);
              }

              if (ws.readyState === WebSocket.OPEN) {
                console.log("Buffer: ", buffer);
                ws.send(buffer);
              }
            };
          })
          .catch(err => {
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
        mediaStream.getTracks().forEach(track => track.stop());
      }
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    }
  });
});
