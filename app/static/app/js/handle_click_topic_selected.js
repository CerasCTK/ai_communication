let selectedDecs = "";

document.querySelectorAll(".select-topic-item").forEach(item => {
    item.addEventListener("click", () => {
        if (item.classList.contains("active")) {
            item.classList.remove("active");
            console.log("Remove selection")
            return;
        }

        if (item.classList.contains("disable")) return;

        document.querySelectorAll(".select-topic-item").forEach(i => {
            i.classList.remove("active");
        });

        item.classList.add("active");

        selectedDecs = item.querySelector("p").innerText;
    })
})

document.getElementById("start-btn").addEventListener("click", () => {
  if (!selectedDecs) {
    alert("You have to select topic!");
    return;
  }

  localStorage.setItem("selected_topic_desc", selectedDecs);

  window.location.href = "/speaking";
});


