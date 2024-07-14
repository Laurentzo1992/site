function nextQuestion(current) {
    var currentQuestion = document.getElementById('question' + current);
    var nextQuestion = document.getElementById('question' + (current + 1));

    currentQuestion.style.display = 'none';
    nextQuestion.style.display = 'block';
}

function previousQuestion(current) {
    var currentQuestion = document.getElementById('question' + current);
    var previousQuestion = document.getElementById('question' + (current - 1));

    currentQuestion.style.display = 'none';
    previousQuestion.style.display = 'block';
}
