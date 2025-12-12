document.addEventListener("DOMContentLoaded", () => {
  const speakingTopicElement = document.querySelector(".speaking-topic");
  if (!speakingTopicElement) return;

  const savedTopic = localStorage.getItem("selected_topic_desc");

  if (savedTopic) {
    speakingTopicElement.textContent = savedTopic;
  } else {
    speakingTopicElement.textContent = "No topic selected";
  }

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
