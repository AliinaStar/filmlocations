// Перевіряємо, чи користувач авторизований
const isAuthorized = false; // Це значення має приходити з вашого бекенду

// Отримуємо всі потрібні елементи
const authorizedProfile = document.getElementById('authorizedProfile');
const registerForm = document.getElementById('registerForm');
const loginForm = document.getElementById('loginForm');

// Показуємо потрібний контент залежно від стану авторизації
if (isAuthorized) {
    authorizedProfile.classList.remove('hidden');
    registerForm.classList.add('hidden');
    loginForm.classList.add('hidden');
} else {
    authorizedProfile.classList.add('hidden');
    registerForm.classList.remove('hidden');
    loginForm.classList.add('hidden');
}

// Обробка переключення між формами
const tabBtns = document.querySelectorAll('.tab-btn');
tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const tab = btn.dataset.tab;
        if (tab === 'register') {
            registerForm.classList.remove('hidden');
            loginForm.classList.add('hidden');
        } else {
            registerForm.classList.add('hidden');
            loginForm.classList.remove('hidden');
        }
        
        // Оновлюємо активні стани кнопок
        tabBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
    });
});