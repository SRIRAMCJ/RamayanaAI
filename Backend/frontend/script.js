const form = document.getElementById("chatForm");
const questionInput = document.getElementById("questionInput");
const languageSelect = document.getElementById("languageSelect");
const askButton = document.getElementById("askBtn");
const status = document.getElementById("status");
const answerContainer = document.getElementById("answerContainer");
const answer = document.getElementById("answer");
const audio = document.getElementById("answerAudio");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const question = questionInput.value.trim();
  if (!question) {
    questionInput.focus();
    return;
  }

  askButton.disabled = true;
  status.textContent = "Searching the Ramayana…";
  answerContainer.hidden = true;
  audio.hidden = true;
  audio.pause();

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, language: languageSelect.value }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "The request failed.");

    answer.textContent = data.answer;
    answerContainer.hidden = false;
    if (data.audio?.url) {
      audio.src = data.audio.url;
      audio.hidden = false;
    }
    status.textContent = "Answer ready.";
  } catch (error) {
    status.textContent = error.message || "Could not reach the assistant. Check that the server is running.";
  } finally {
    askButton.disabled = false;
  }
});
