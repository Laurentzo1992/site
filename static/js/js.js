function nextStep(current) {
    var currentStep = document.getElementById('step' + current);
    var nextStep = document.getElementById('step' + (current + 1));

    currentStep.style.display = 'none';
    nextStep.style.display = 'block';
}

function previousStep(current) {
    var currentStep = document.getElementById('step' + current);
    var previousStep = document.getElementById('step' + (current - 1));

    currentStep.style.display = 'none';
    previousStep.style.display = 'block';
}
