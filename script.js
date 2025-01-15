let timeLeft = 60;
const timerDisplay = document.querySelector('#timer span');
const passageDisplay = document.getElementById('passage');
const typedTextArea = document.getElementById('typedText');
const submitButton = document.getElementById('submitBtn');
const resultDisplay = document.getElementById('results');
const actionButtons = document.getElementById('actionButtons');
const startAgainBtn = document.getElementById('startAgainBtn');
const exitBtn = document.getElementById('exitBtn');

let timerStarted = false;
let timerInterval;

// Function to start the timer
function startTimer() {
    timerInterval = setInterval(() => {
        timeLeft--;
        timerDisplay.textContent = timeLeft;

        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            handleSubmit();
        }
    }, 1000);
}

// Start the timer when the user starts typing
typedTextArea.addEventListener('input', () => {
    if (!timerStarted) {
        startTimer();
        timerStarted = true;
    }
});

// Function to handle submission of typing test
function handleSubmit() {
    // Clear timer interval
    clearInterval(timerInterval);
    
    // Disable textarea and submit button after submission
    typedTextArea.disabled = true;
    submitButton.disabled = true;

    const typedText = typedTextArea.value;
    const passageText = passageDisplay.querySelector('p').textContent;
    const timeTaken = 60 - timeLeft;

    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ typedText: typedText, passage: passageText, timeTaken: timeTaken })
    })
    .then(response => response.json())
    .then(data => {
        const wpm = data.wpm;
        const accuracy = data.accuracy;

        resultDisplay.innerHTML = `Words per minute: ${wpm}, Accuracy: ${accuracy.toFixed(2)}%`;
        resultDisplay.style.display = 'block';

        // Show Start Again and Exit buttons
        actionButtons.style.display = 'block';
    });
}

// Function to start a new typing test
function startTypingTest() {
    // Reset timer variables
    timeLeft = 60;
    timerDisplay.textContent = timeLeft;
    timerStarted = false;

    // Reset textarea and button states
    typedTextArea.value = '';
    typedTextArea.disabled = false;
    submitButton.disabled = false;
    resultDisplay.style.display = 'none';
    actionButtons.style.display = 'none';

    // Set a new random passage
    location.reload();

    // Focus on the textarea
    typedTextArea.focus();
}

// Submit button click handler
submitButton.addEventListener('click', handleSubmit);

// Start Again button click handler
startAgainBtn.addEventListener('click', startTypingTest);

// Exit button click handler
exitBtn.addEventListener('click', () => {
    window.location.href = 'https://www.google.com';
});

// Add visual cues for typing accuracy
typedTextArea.addEventListener('input', () => {
    const typedText = typedTextArea.value;
    const passageText = passageDisplay.querySelector('p').textContent;

    if (passageText === typedText) {
        handleSubmit();
    }
    else if (passageText.startsWith(typedText)) {
        typedTextArea.classList.remove('error');
        typedTextArea.classList.add('good-accuracy');
        typedTextArea.classList.remove('poor-accuracy');
    } else {
        typedTextArea.classList.add('error');
        typedTextArea.classList.remove('good-accuracy');
        typedTextArea.classList.add('poor-accuracy');
    }
});

