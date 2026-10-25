const introVideo = document.getElementById("introVideo");
const bookVideo = document.getElementById("bookVideo");

const askBtn = document.getElementById("askBtn");
const questionInput = document.getElementById("questionInput");

const loading = document.getElementById("loading");
const answerContainer = document.getElementById("answerContainer");
const answer = document.getElementById("answer");
const questionContainer = document.getElementById("questionContainer");

loading.style.display = "none";
answerContainer.style.display = "none";

askBtn.addEventListener("click", async function () {

    const question = questionInput.value.trim();

    if (question === "") {
        alert("Please enter a question.");
        return;
    }

    questionContainer.style.display = "none";

    introVideo.pause();
    introVideo.style.display = "none";

    bookVideo.style.display = "block";
    bookVideo.currentTime = 0;
    bookVideo.play();

    loading.style.display = "flex";

    try {

        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question,
                language: "en"
            })
        });

        const data = await response.json();

        bookVideo.onended = function () {

            loading.style.display = "none";
            answerContainer.style.display = "block";
            answer.innerHTML = "";

            let i = 0;

            function typeWriter() {
                if (i < data.answer.length) {
                    answer.innerHTML += data.answer.charAt(i);
                    i++;
                    setTimeout(typeWriter, 15);
                }
            }

            typeWriter();

            const audio = new Audio(data.audio.url);
            audio.play();
        };

    } catch (err) {
        console.error(err);
        loading.innerHTML = "Something went wrong.";
    }

});