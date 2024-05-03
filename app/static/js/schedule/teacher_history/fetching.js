const deleteTeacherHistory = function (link) {
    const urlParams = new URLSearchParams(link.href)

    fetch(getIndex() + '/schedule/delete-teacher-history/', {
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
                throw Error('Не удалось удалить запись')
            }
            link.parentElement.remove()

            const historyBlock = document.querySelector('.schedule__history-block')
            if (!historyBlock.querySelector('.schedule__history-item')) {
                historyBlock.innerHTML = ''
            }
        })
        .catch(error => {
            const teacherHistoryBlock = document.querySelector('.schedule__history-block')
            if (!teacherHistoryBlock.querySelector('.error')) {
                teacherHistoryBlock.insertAdjacentHTML('beforeend', `<p class="error">${error.message}</p>`)
            }
        })
}