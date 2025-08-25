// JavaScript для страницы добавления цитаты

function updateWeightValue(value) {
    document.getElementById('weight-value').textContent = value;
}

// Инициализация значения веса при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    const weightInput = document.getElementById('id_weight');
    if (weightInput) {
        updateWeightValue(weightInput.value);
    }
});
