const getSchedule = function (url) {
    fetch(url, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
        .then(response => response.text())
        .then(html => {
            document.querySelector('.tables__list').outerHTML = html

            const tablesList = document.querySelector('.tables__list')
            const notePopUpNodes = document.querySelectorAll('.note-pop-up')
            const tableRows = document.querySelectorAll('tbody > tr')

            tablesList.addEventListener('click', (event) => {
                tableRows.forEach(row => {
                    if (row.contains(event.target)) {
                        row.lastElementChild.classList.remove('hidden')
                        row.lastElementChild.style.opacity = '1'
                    }
                })
            })

            tablesList.addEventListener('click', (event) => {
                notePopUpNodes.forEach(notePopUp => {
                    if (event.target.getAttribute('name') === 'close') {
                        notePopUp.style.opacity = '0'
                        setTimeout(() => notePopUp.classList.add('hidden'), 300)
                    }
                })
            })

            window.addEventListener('click', (event) => {
                tableRows.forEach(row => {
                    if (!row.contains(event.target) && !row.lastElementChild.classList.contains('hidden')) {
                        row.lastElementChild.style.opacity = '0'
                        setTimeout(() => row.lastElementChild.classList.add('hidden'), 300)
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

            const spinner = document.querySelector('.spinner-border')
            spinner.classList.remove('spinner-border-visible')
            spinner.classList.add('spinner-border-hidden')
        })
}


const createNote = function (form) {
    const noteBlock = form.parentElement

    const note = {
        schedule_name: noteBlock.getAttribute('data-schedule-name'),
        day: noteBlock.getAttribute('data-day'),
        lesson_number: noteBlock.getAttribute('data-lesson-number'),
        text: form.note.value,
    }

    fetch(getIndex() + '/notes/create/', {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json;charset=utf-8',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(note),
    })
        .then(response => {
            if (!response.ok) {
                throw Error('Не получилось создать заметку')
            }
            return response.text()
        })
        .then(html => {
            noteBlock.innerHTML = html
            for (const el of document.querySelectorAll('.note-block')) {
                if (el === noteBlock) {
                    prepareNoteDisplay(noteBlock)
                    noteBlock.parentElement.parentElement.classList.add('existing_note_tr')
                }
            }
        })
        .catch(error => {
            const noteBlockOptions = noteBlock.querySelector('.note-block__options')
            if (!noteBlock.querySelector('.error')) {
                noteBlockOptions.insertAdjacentHTML('beforebegin', `<p class="error">${error.message}</p>`)
            }
        })
}


const deleteNote = function (noteBlock) {
    const note = {
        schedule_name: noteBlock.getAttribute('data-schedule-name'),
        day: noteBlock.getAttribute('data-day'),
        lesson_number: noteBlock.getAttribute('data-lesson-number'),
    }

    fetch(getIndex() + '/notes/delete/', {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json;charset=utf-8',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify(note),
    })
        .then(response => {
            if (!response.ok) {
                throw Error('Не удалось удалить заметку')
            }
            return response.text()
        })
        .then(html => {
            noteBlock.innerHTML = html
            for (const el of document.querySelectorAll('.note-block')) {
                if (el === noteBlock) {
                    prepareNoteCreate(noteBlock)
                    noteBlock.parentElement.parentElement.classList.remove('existing_note_tr')
                }
            }
        })
        .catch((error) => {
            const noteBlockOptions = noteBlock.querySelector('.note-block__options')
            if (!noteBlock.querySelector('.error')) {
                noteBlockOptions.insertAdjacentHTML('beforebegin', `<p class="error">${error.message}</p>`)
            }
        })
}


const updateNote = function (form) {
    const noteBlock = form.parentElement

    const note = {
        schedule_name: noteBlock.getAttribute('data-schedule-name'),
        day: noteBlock.getAttribute('data-day'),
        lesson_number: noteBlock.getAttribute('data-lesson-number'),
        text: form.note.value,
    }

    fetch(getIndex() + '/notes/update/', {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json;charset=utf-8',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(note),
    })
        .then(response => {
            if (!response.ok) {
                throw Error('Не получилось изменить заметку')
            }
            return response.text()
        })
        .then(html => {
            noteBlock.innerHTML = html
            for (const el of document.querySelectorAll('.note-block')) {
                if (el === noteBlock) {
                    prepareNoteDisplay(noteBlock)
                    noteBlock.parentElement.parentElement.classList.add('existing_note_tr')
                }
            }
        })
        .catch(error => {
            const noteBlockOptions = noteBlock.querySelector('.note-block__options')
            if (!noteBlock.querySelector('.error')) {
                noteBlockOptions.insertAdjacentHTML('beforebegin', `<p class="error">${error.message}</p>`)
            }
        })
}


const getUpdateNote = function (noteBlock) {
    const note = {
        schedule_name: noteBlock.getAttribute('data-schedule-name'),
        day: noteBlock.getAttribute('data-day'),
        lesson_number: noteBlock.getAttribute('data-lesson-number'),
    }

    fetch(getIndex() + `/notes/update/?schedule_name=${note.schedule_name}&day=${note.day}&lesson_number=${note.lesson_number}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
        .then(response => response.text())
        .then(html => {
            noteBlock.innerHTML = html
            prepareNoteUpdate(noteBlock)
        })
}


const displayNote = function (noteBlock) {
    const note = {
        schedule_name: noteBlock.getAttribute('data-schedule-name'),
        day: noteBlock.getAttribute('data-day'),
        lesson_number: noteBlock.getAttribute('data-lesson-number'),
    }

    fetch(getIndex() + `/notes/display/?schedule_name=${note.schedule_name}&day=${note.day}&lesson_number=${note.lesson_number}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
        .then(response => response.text())
        .then(html => {
            noteBlock.innerHTML = html
            for (const el of document.querySelectorAll('.note-block')) {
                if (el === noteBlock) {
                    prepareNoteDisplay(noteBlock)
                }
            }
        })
}


const prepareNoteDisplay = function (noteBlock) {
    noteBlock.querySelectorAll('[name="delete"]').forEach(btn => {
        btn.addEventListener('click', () => {
            deleteNote(noteBlock)
        })
    })

    noteBlock.querySelectorAll('[name="update"]').forEach(btn => {
        btn.addEventListener('click', () => {
            getUpdateNote(noteBlock)
        })
    })
}


const prepareNoteCreate = function (noteBlock) {
    noteBlock.querySelector('[name="note-create"]').addEventListener('submit', (event) => {
        createNote(event.currentTarget)
        event.preventDefault()
    })
}


const prepareNoteUpdate = function (noteBlock) {
    noteBlock.querySelector('[name="display"]').addEventListener('click', () => {
        displayNote(noteBlock)
    })

    noteBlock.querySelector('[name="note-update"]').addEventListener('submit', (event) => {
        updateNote(event.currentTarget)
        event.preventDefault()
    })
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


const getIndex = () => window.location.protocol + '//' + window.location.host
