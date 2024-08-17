const createBookmark = function () {
    const urlParams = new URLSearchParams(window.location.search)

    fetch(getIndex() + '/bookmarks/create/', {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json;charset=utf-8',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            'name': urlParams.get('name'),
            'key': urlParams.get('key'),
        })
    })
        .then(response => {
            if (!response.ok) {
                throw Error()
            }
            return response.text()
        })
        .then(html => {
            const btn = document.querySelector('[name="bookmark-create"]')

            document.querySelector('.schedule__bookmarks').outerHTML = html
            prepareBookmarkDisplay()

            btn.setAttribute('disabled', 'true')

            showMauNotification('Закладка успешно создана', 'ok')
        })
        .catch(error => {
            showMauNotification('Не удалось создать закладку', 'error')
        })
}


const deleteBookmark = function (link) {
    const urlParams = new URLSearchParams(link.href.split('?')[1])

    fetch(getIndex() + '/bookmarks/delete/', {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json;charset=utf-8',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            'name': urlParams.get('name'),
            'key': urlParams.get('key'),
        })
    })
        .then(response => {
            if (!response.ok) {
                throw Error()
            }

            return response.text()
        })
        .then(html => {
            link.parentElement.remove()
            if (link.href == window.location.href) {
                const btn = document.querySelector('[name="bookmark-create"]')
                btn.removeAttribute('disabled')
            }

            document.querySelector('.schedule__bookmarks').outerHTML = html
            prepareBookmarkDisplay()

            showMauNotification('Закладка успешно удалена', 'ok')
        })
        .catch(error => {
            showMauNotification('Не удалось удалить закладку', 'error')
        })
}