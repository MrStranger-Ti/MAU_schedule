const getSchedule = function (url) {
    fetch(url, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
        .then(response => response.text())
        .then(html => {
            document.querySelector('.schedule__content').innerHTML = html

            const tablesList = document.querySelector('.schedule__content')
            const notePopUpNodes = document.querySelectorAll('.note-pop-up')
            const tableRows = document.querySelectorAll('tbody > tr')

            tablesList.addEventListener('click', (event) => {
                tableRows.forEach(row => {
                    if (row.contains(event.target) && row.lastElementChild.classList.contains('hidden')) {
                        row.lastElementChild.classList.remove('hidden')
                        row.lastElementChild.style.opacity = '1'
                    }
                })
            })

            tablesList.addEventListener('click', (event) => {
                notePopUpNodes.forEach(notePopUp => {
                    if (event.target.getAttribute('name') === 'close') {
                        notePopUp.style.opacity = '0'
                        setTimeout(() => notePopUp.classList.add('hidden'), 200)
                    }
                })
            })

            window.addEventListener('click', (event) => {
                tableRows.forEach(row => {
                    if (!row.contains(event.target) && !row.lastElementChild.classList.contains('hidden')) {
                        row.lastElementChild.style.opacity = '0'
                        setTimeout(() => row.lastElementChild.classList.add('hidden'), 200)
                    }
                })
            })

            tablesList.querySelectorAll('form').forEach(form => {
                form.addEventListener('submit', (event) => {
                    if (form.name === 'note-create') {
                        createNote(form)
                        event.preventDefault()
                    }
                })
            })

            tablesList.querySelectorAll('[name="delete"]').forEach(btn => {
                btn.addEventListener('click', () => {
                    deleteNote(btn.parentElement.parentElement.parentElement)
                })
            })

            tablesList.querySelectorAll('[name="update"]').forEach(btn => {
                btn.addEventListener('click', () => {
                    getUpdateNote(btn.parentElement.parentElement.parentElement)
                })
            })

            prepareBookmarkDisplay()
            prepareBookmarkAdd()

            const spinner = document.querySelector('.spinner-border')
            spinner.classList.remove('spinner-border-visible')
            spinner.classList.add('spinner-border-hidden')
        })
}