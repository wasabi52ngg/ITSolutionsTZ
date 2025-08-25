// JavaScript для страницы популярных цитат

function likeQuote(quoteId, button) {
    $.post(`/like/${quoteId}/`, {
        'csrfmiddlewaretoken': getCsrfToken()
    })
    .done(function(data) {
        if (data.success) {
            const card = button.closest('.quote-card');
            const likesElement = card.querySelector('.fa-thumbs-up').parentElement.querySelector('.stat-number-small');
            const dislikesElement = card.querySelector('.fa-thumbs-down').parentElement.querySelector('.stat-number-small');
            
            likesElement.textContent = data.likes_count;
            dislikesElement.textContent = data.dislikes_count;
            
            showToast(data.message, 'success');
            
            location.reload();
        } else {
            showToast(data.message, 'warning');
        }
    })
    .fail(function() {
        showToast('Ошибка при голосовании', 'error');
    });
}

function dislikeQuote(quoteId, button) {
    $.post(`/dislike/${quoteId}/`, {
        'csrfmiddlewaretoken': getCsrfToken()
    })
    .done(function(data) {
        if (data.success) {
            const card = button.closest('.quote-card');
            const likesElement = card.querySelector('.fa-thumbs-up').parentElement.querySelector('.stat-number-small');
            const dislikesElement = card.querySelector('.fa-thumbs-down').parentElement.querySelector('.stat-number-small');
            
            likesElement.textContent = data.likes_count;
            dislikesElement.textContent = data.dislikes_count;
            
            showToast(data.message, 'info');
            
            location.reload();
        } else {
            showToast(data.message, 'warning');
        }
    })
    .fail(function() {
        showToast('Ошибка при голосовании', 'error');
    });
}

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

function showToast(message, type) {
    const toast = $(`
        <div class="toast align-items-center text-white bg-${type === 'success' ? 'success' : type === 'error' ? 'danger' : type === 'warning' ? 'warning' : 'info'} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `);
    
    $('.toast-container').append(toast);
    const bsToast = new bootstrap.Toast(toast[0]);
    bsToast.show();
    
    toast.on('hidden.bs.toast', function() {
        toast.remove();
    });
}
