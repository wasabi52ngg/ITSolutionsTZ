// JavaScript для страницы случайной цитаты

function likeQuote(quoteId) {
    $.ajax({
        url: `/quotes/like/${quoteId}/`,
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': getCsrfToken()
        },
        success: function(data) {
            if (data.success) {
                $('#likes-count').text(data.likes_count);
                $('#dislikes-count').text(data.dislikes_count);
                showToast(data.message, 'success');
                location.reload();
            } else {
                showToast(data.message, 'warning');
            }
        },
        error: function() {
            showToast('Ошибка при голосовании', 'error');
        }
    });
}

function dislikeQuote(quoteId) {
    $.ajax({
        url: `/quotes/dislike/${quoteId}/`,
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': getCsrfToken()
        },
        success: function(data) {
            if (data.success) {
                $('#likes-count').text(data.likes_count);
                $('#dislikes-count').text(data.dislikes_count);
                showToast(data.message, 'info');
                location.reload();
            } else {
                showToast(data.message, 'warning');
            }
        },
        error: function() {
            showToast('Ошибка при голосовании', 'error');
        }
    });
}

function getCsrfToken() {
    let token = $('#csrf-form [name=csrfmiddlewaretoken]').val();
    
    if (!token) {
        token = $('meta[name="csrf-token"]').attr('content');
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
