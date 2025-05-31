// function nextQuestion(current) {
//     var currentQuestion = document.getElementById('question' + current);
//     var nextQuestion = document.getElementById('question' + (current + 1));

//     currentQuestion.style.display = 'none';
//     nextQuestion.style.display = 'block';
// }

function nextQuestion(current) {
    // Sélectionne la question actuelle et la suivante
    var currentQuestion = document.getElementById('question' + current);
    var nextQuestion = document.getElementById('question' + (current + 1));
    
    // Trouve tous les champs dans la question actuelle
    var inputs = currentQuestion.querySelectorAll('input, textarea, select');
    var valid = true;

    // Boucle sur chaque champ pour vérifier s'il est rempli
    inputs.forEach(function(input) {
        var errorDiv = input.nextElementSibling; // Trouve le div juste après l'input pour afficher l'erreur
        if (!input.value || input.value.trim() === '') {
            valid = false;
            
            // Si le div pour l'erreur n'existe pas, on le crée
            if (!errorDiv || !errorDiv.classList.contains('error-message')) {
                errorDiv = document.createElement('div');
                errorDiv.className = 'error-message text-danger mt-1';
                errorDiv.innerText = 'Ce champ est requis.';
                input.parentNode.appendChild(errorDiv);
            }
        } else if (errorDiv && errorDiv.classList.contains('error-message')) {
            // Si le champ est valide et qu'un message d'erreur est déjà affiché, on le retire
            errorDiv.remove();
        }
    });

    // Si tous les champs sont valides, on passe à la question suivante
    if (valid) {
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
