function nextQuestion(current) {
    var currentQuestion = document.getElementById('question' + current);
    var nextQuestion = document.getElementById('question' + (current + 1));
    var inputs = currentQuestion.querySelectorAll('input, select');
    var isValid = true;

    inputs.forEach(function(input) {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });

    if (isValid) {
        currentQuestion.style.display = 'none';
        nextQuestion.style.display = 'block';
    }
}

function previousQuestion(current) {
    var currentQuestion = document.getElementById('question' + current);
    var previousQuestion = document.getElementById('question' + (current - 1));

    currentQuestion.style.display = 'none';
    previousQuestion.style.display = 'block';
}
