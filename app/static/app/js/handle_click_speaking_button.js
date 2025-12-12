document.addEventListener("DOMContentLoaded", () => {
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

  speakingButtonElement.addEventListener("click", () => {
    const isRecording = speakingButtonElement.classList.contains("recording");

    if (!isRecording) {
      speakingButtonElement.classList.add("recording");
      speakingButtonElement.innerHTML = buttonContentWhenSpeaking;
    } else {
      speakingButtonElement.classList.remove("recording");
      speakingButtonElement.innerHTML = buttonContentWhenNotSpeaking;
    }
  });
});
