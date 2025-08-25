
// Функция для получения CSRF токена
function getCsrfToken() {
    let token = $('meta[name="csrf-token"]').attr('content');
    
    if (!token) {
        token = $('[name=csrfmiddlewaretoken]').val();
    }
    
    if (!token) {
        token = getCookie('csrftoken');
    }
    
    return token;
}

// Функция для получения cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Функция для показа toast уведомлений
function showToast(message, type = 'info') {
    const toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        const container = document.createElement('div');
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(container);
    }
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type === 'success' ? 'success' : type === 'error' ? 'danger' : type === 'warning' ? 'warning' : 'info'} border-0`;
    toast.setAttribute('role', 'alert');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    const container = document.querySelector('.toast-container');
    container.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

// Функция для анимации счетчиков
function animateCounter(element, start, end, duration = 1000) {
    const startTime = performance.now();
    const difference = end - start;
    
    function updateCounter(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const current = Math.floor(start + (difference * progress));
        element.textContent = current;
        
        if (progress < 1) {
            requestAnimationFrame(updateCounter);
        }
    }
    
    requestAnimationFrame(updateCounter);
}

// Функция для плавной прокрутки к элементу
function smoothScrollTo(element) {
    element.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
}

// Функция для копирования текста в буфер обмена
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showToast('Текст скопирован в буфер обмена!', 'success');
    }).catch(function() {
        showToast('Ошибка при копировании', 'error');
    });
}

// Функция для добавления эффекта печатания
function typeWriter(element, text, speed = 50) {
    let i = 0;
    element.innerHTML = '';
    
    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    
    type();
}

// Функция для валидации форм
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Функция для добавления эффекта загрузки к кнопке
function addLoadingToButton(button, text = 'Загрузка...') {
    const originalText = button.innerHTML;
    button.innerHTML = `<span class="loading me-2"></span>${text}`;
    button.disabled = true;
    
    return function() {
        button.innerHTML = originalText;
        button.disabled = false;
    };
}

// Функция для создания модального окна
function createModal(title, content, buttons = []) {
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.setAttribute('tabindex', '-1');
    
    modal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">${title}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    ${content}
                </div>
                <div class="modal-footer">
                    ${buttons.map(btn => `
                        <button type="button" class="btn ${btn.class || 'btn-secondary'}" 
                                data-bs-dismiss="modal" ${btn.onclick ? `onclick="${btn.onclick}"` : ''}>
                            ${btn.text}
                        </button>
                    `).join('')}
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
    
    modal.addEventListener('hidden.bs.modal', function() {
        modal.remove();
    });
    
    return bsModal;
}

// Функция для добавления эффекта параллакса
function addParallaxEffect() {
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const parallaxElements = document.querySelectorAll('.parallax');
        
        parallaxElements.forEach(element => {
            const speed = element.dataset.speed || 0.5;
            const yPos = -(scrolled * speed);
            element.style.transform = `translateY(${yPos}px)`;
        });
    });
}

// Функция для добавления анимации при скролле
function addScrollAnimation() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    animatedElements.forEach(el => observer.observe(el));
}

// Функция для добавления темной темы
function toggleDarkTheme() {
    const body = document.body;
    const isDark = body.classList.toggle('dark-theme');
    
    localStorage.setItem('darkTheme', isDark);
    
    if (isDark) {
        showToast('Темная тема включена', 'info');
    } else {
        showToast('Светлая тема включена', 'info');
    }
}

// Функция для инициализации темной темы
function initDarkTheme() {
    const isDark = localStorage.getItem('darkTheme') === 'true';
    if (isDark) {
        document.body.classList.add('dark-theme');
    }
}

// Функция для добавления кнопки "Наверх"
function addScrollToTopButton() {
    const button = document.createElement('button');
    button.className = 'btn btn-primary position-fixed bottom-0 end-0 m-3 d-none';
    button.innerHTML = '<i class="fas fa-arrow-up"></i>';
    button.style.zIndex = '1000';
    button.onclick = () => window.scrollTo({ top: 0, behavior: 'smooth' });
    
    document.body.appendChild(button);
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            button.classList.remove('d-none');
        } else {
            button.classList.add('d-none');
        }
    });
}

// Функция для добавления эффекта печатания к заголовкам
function addTypewriterToHeadings() {
    const headings = document.querySelectorAll('h1, h2');
    headings.forEach(heading => {
        if (heading.textContent && !heading.dataset.typed) {
            heading.dataset.typed = 'true';
            const originalText = heading.textContent;
            typeWriter(heading, originalText, 100);
        }
    });
}

// Инициализация всех функций при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    initDarkTheme();
    
    addScrollToTopButton();
    
    addScrollAnimation();
    
    addTypewriterToHeadings();
    
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                showToast('Пожалуйста, заполните все обязательные поля', 'error');
            }
        });
    });
    
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    });
});

// Экспорт функций для использования в других файлах
window.QuoteApp = {
    showToast,
    animateCounter,
    smoothScrollTo,
    copyToClipboard,
    typeWriter,
    validateForm,
    addLoadingToButton,
    createModal,
    addParallaxEffect,
    addScrollAnimation,
    toggleDarkTheme,
    addScrollToTopButton,
    addTypewriterToHeadings,
    getCsrfToken,
    getCookie
};
