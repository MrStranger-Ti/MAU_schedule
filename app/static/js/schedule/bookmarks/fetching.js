const getBookmarks = function () {
    fetch(getIndex() + '/bookmarks/display/', {
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
        .then(response => response.text())
        .then(html => {

        })
}


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
                throw Error('Не удалось создать закладку')
            }
            return response.text()
        })
        .then(html => {
            const btn = document.querySelector('[name="bookmark-create"]')

            document.querySelector('.schedule__bookmarks-block').innerHTML = html

            btn.setAttribute('disabled', 'true')
            btn.textContent = 'Расписание в закладках'

            prepareBookmarkDisplay()

            showMauNotification('Закладка успешно создана')
        })
        .catch(error => {
            // const btn = document.querySelector('[name="bookmark-create"]')
            // if (!btn.parentElement.querySelector('.error')) {
            //     btn.insertAdjacentHTML('afterend', `<p class="error">${error.message}</p>`)
            // }
            showMauNotification(error.message)
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
                throw Error('Не удалось удалить закладку')
            }

            link.parentElement.remove()
            document.querySelector('[name="bookmark-create"]').removeAttribute('disabled')

            showMauNotification('Закладка успешно удалена')
        })
        .catch(error => {
            showMauNotification(error.message)
        })
}