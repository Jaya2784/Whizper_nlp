document.addEventListener('DOMContentLoaded', () => {
    // Tab switching functionality
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all buttons and contents
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            // Add active class to clicked button and corresponding content
            btn.classList.add('active');
            const tabId = btn.dataset.tab;
            document.getElementById(`${tabId}-content`).classList.add('active');
        });
    });

    // Q&A functionality
    document.getElementById("ask-btn").addEventListener("click", sendMessage);
    document.getElementById("question-input").addEventListener("keypress", handleKeyPress);

    async function sendMessage() {
        const userInput = document.getElementById("question-input").value.trim();
        if (!userInput) return; // Prevent empty messages

        const qaHistory = document.querySelector(".qa-history");

        // Append User Message
        const userMessage = document.createElement("div");
        userMessage.className = "qa-item question";
        userMessage.innerHTML = `
            <div class="qa-message user">
                <i class="fas fa-user"></i> <span>${userInput}</span>
            </div>
        `;
        qaHistory.appendChild(userMessage);
        document.getElementById("question-input").value = "";
        qaHistory.scrollTop = qaHistory.scrollHeight;

        // Replace with your actual API key
        const API_KEY = "AIzaSyDlBIw1F_Pva3fZ7E49fTyagNdi00nEDy4"; // Make sure to replace this with your actual API key
        const API_URL = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${API_KEY}`;

        try {
            const response = await fetch(API_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    contents: [{ role: "user", parts: [{ text: userInput }] }]
                })
            });

            const data = await response.json();
            console.log("API Response:", data);

            let reply = "Sorry, I couldn't process that.";

            if (data && data.candidates && data.candidates.length > 0) {
                if (data.candidates[0].content && data.candidates[0].content.parts.length > 0) {
                    reply = data.candidates[0].content.parts[0].text;
                }
            }

            // Replace bot introduction and remove any mention of Google
            reply = reply.replace(/I am a large language model, trained by Google\./g, "I'm SwiftAid bot");

            // Check if user requested paragraph format
            if (!userInput.toLowerCase().includes("i want it as a para")) {
                // Format reply with bullet points and paragraphs
                reply = reply.split('\n').map(line => {
                    if (line.startsWith('*')) {
                        return `<li>${line.substring(1).trim()}</li>`;
                    } else {
                        return `<p>${line.trim()}</p>`;
                    }
                }).join('');
                reply = `<ul>${reply}</ul>`;
            } else {
                // Format as a single paragraph
                reply = `<p>${reply}</p>`;
            }

            // Replace bold text markers with HTML bold tags
            reply = reply.replace(/\*(.*?)\*/g, '<strong>$1</strong>');

            // Append Bot Message
            const botMessage = document.createElement("div");
            botMessage.className = "qa-item answer";
            botMessage.innerHTML = `
                <div class="qa-message bot">
                    <i class="fas fa-robot"></i> <span>${reply}</span>
                </div>
            `;
            qaHistory.appendChild(botMessage);
        } catch (error) {
            console.error("Error:", error);
            const errorMessage = document.createElement("div");
            errorMessage.className = "qa-message bot";
            errorMessage.innerHTML = `<i class="fas fa-robot"></i> <span>Error processing request.</span>`;
            qaHistory.appendChild(errorMessage);
        }

        // Scroll to the latest message
        qaHistory.scrollTop = qaHistory.scrollHeight;
    }

    function handleKeyPress(event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    }

    let audio = null;

    function getActiveTabData() {
        const activeTab = document.querySelector('.tab-content.active'); // Active tab content
        if (!activeTab) {
            alert("No active tab found.");
            return { text: null, type: null };
        }

        const text = activeTab.textContent.trim(); // Get the text content of the active tab
        const type = activeTab.id; // Use the tab's ID as the type (e.g., "text-content", "summary-content")
        return { text, type };
    }

    function playAudio() {
        const { text, type } = getActiveTabData();
        if (!text) {
            alert("No text available to play.");
            return;
        }

        const speech = new SpeechSynthesisUtterance(text);
        speech.lang = 'en-US';
        speech.rate = parseFloat(document.getElementById('speed').value); // Use selected speed
        window.speechSynthesis.speak(speech);

        document.getElementById('playButton').style.display = 'none';
        document.getElementById('pauseButton').style.display = 'inline-block';

        audio = speech;
    }

    function pauseAudio() {
        if (audio) {
            window.speechSynthesis.cancel();
            document.getElementById('playButton').style.display = 'inline-block';
            document.getElementById('pauseButton').style.display = 'none';
        }
    }

    function downloadAudio() {
        const { text, type } = getActiveTabData();
        if (!text) {
            alert("No text available to download.");
            return;
        }

        // Send a POST request to the backend to generate the audio file
        fetch('/download-audio', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                filename: `${type}-audio`,
            }),
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Failed to generate audio file');
                }
                return response.blob();
            })
            .then((blob) => {
                // Create a download link for the audio file
                const url = window.URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;
                link.download = `${type}-audio.mp3`;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                window.URL.revokeObjectURL(url);
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('Failed to download audio.');
            });
    }

    // Expose functions to the global scope
    window.playAudio = playAudio;
    window.pauseAudio = pauseAudio;
    window.downloadAudio = downloadAudio;
});
