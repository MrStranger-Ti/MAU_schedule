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
                throw Error()
            }
            return response.text()
        })
        .then(html => {
            noteBlock.innerHTML = html
            for (const el of document.querySelectorAll('.note-block')) {
                if (el === noteBlock) {
                    prepareNoteDisplay(noteBlock)
                    noteBlock.parentElement.parentElement.classList.add('existing_note_tr')

                    showMauNotification('Заметка успешно создана', 'ok')
                }
            }
        })
        .catch(error => showMauNotification('Не удалось создать заметку', 'error'))
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
                throw Error()
            }
            return response.text()
        })
        .then(html => {
            noteBlock.innerHTML = html
            for (const el of document.querySelectorAll('.note-block')) {
                if (el === noteBlock) {
                    prepareNoteCreate(noteBlock)
                    noteBlock.parentElement.parentElement.classList.remove('existing_note_tr')

                    showMauNotification('Заметка успешно удалена', 'ok')
                }
            }
        })
        .catch((error) => showMauNotification('Не удалось удалить заметку', 'error'))
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
                throw Error()
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
        .catch(error => showMauNotification('Не удалось обновить заметку', 'error'))
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