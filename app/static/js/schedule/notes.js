// Fetching

const createNote = function (form) {
    const noteBlock = form.closest('.note-block')

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
            noteBlock.querySelector('.card').innerHTML = html
            for (const el of document.querySelectorAll('.note-block')) {
                if (el === noteBlock) {
                    prepareNoteDisplay(noteBlock)
                    noteBlock.closest('tr').previousElementSibling.classList.add('schedule__existing-note-tr')

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
            noteBlock.querySelector('.card').innerHTML = html
            for (const el of document.querySelectorAll('.note-block')) {
                if (el === noteBlock) {
                    prepareNoteCreate(noteBlock)
                    noteBlock.closest('tr').previousElementSibling.classList.remove('schedule__existing-note-tr')

                    showMauNotification('Заметка успешно удалена', 'ok')
                }
            }
        })
        .catch((error) => showMauNotification('Не удалось удалить заметку', 'error'))
}


const updateNote = function (form) {
    const noteBlock = form.closest('.note-block')

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
            noteBlock.querySelector('.card').innerHTML = html
            for (const el of document.querySelectorAll('.note-block')) {
                if (el === noteBlock) {
                    prepareNoteDisplay(noteBlock)
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
            noteBlock.querySelector('.card').innerHTML = html
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
            noteBlock.querySelector('.card').innerHTML = html
            for (const el of document.querySelectorAll('.note-block')) {
                if (el === noteBlock) {
                    prepareNoteDisplay(noteBlock)
                }
            }
        })
}


// Preparing

const prepareNoteDisplay = function (noteBlock) {
    const btnDelete = noteBlock.querySelector('[name="delete"]')
    const btnUpdate = noteBlock.querySelector('[name="update"]')
    const btnClose = noteBlock.querySelector('[name="close"]')
    if (btnDelete && btnUpdate && btnClose) {
        btnDelete.addEventListener('click', () => {
            deleteNote(noteBlock)
        })

        btnUpdate.addEventListener('click', () => {
            getUpdateNote(noteBlock)
        })

        prepareBtnCollapse(btnClose)
    }
}


const prepareNoteCreate = function (noteBlock) {
    const form = noteBlock.querySelector('form[name="note-create"]')
    const btnClose = noteBlock.querySelector('[name="close"]')
    if (form && btnClose) {
        form.addEventListener('submit', event => {
            createNote(event.currentTarget)
            event.preventDefault()
        })

        prepareBtnCollapse(btnClose)
    }
}


const prepareNoteUpdate = function (noteBlock) {
    const form = noteBlock.querySelector('form[name="note-update"]')
    const btnBack = noteBlock.querySelector('[name="display"]')
    const btnClose = noteBlock.querySelector('[name="close"]')
    if (form && btnBack && btnClose) {
        form.addEventListener('submit', event => {
            updateNote(event.currentTarget)
            event.preventDefault()
        })

        btnBack.addEventListener('click', () => {
            displayNote(noteBlock)
        })

        prepareBtnCollapse(btnClose)
    }
}


const prepareBtnCollapse = function (btnClose) {
    btnClose.addEventListener('click', event => {
        const collapseId = btnClose.closest('.collapse').getAttribute('id')
        const bsCollapse = new bootstrap.Collapse(`#${collapseId}`, {
            toggle: false
        })
        bsCollapse.hide()
    })
}


const prepareCollapseAll = function (currentCollapsible) {
    currentCollapsible.addEventListener('shown.bs.collapse', event => {
        document.querySelectorAll('.note-block > .collapse').forEach(collapsible => {
            const displayed = collapsible.classList.contains('show') || collapsible.classList.contains('collapsing')
            if (currentCollapsible !== collapsible && displayed) {
                console.log(currentCollapsible)
                const collapseId = collapsible.getAttribute('id')
                const bsCollapse = new bootstrap.Collapse(`#${collapseId}`, {
                    toggle: false,
                })
                bsCollapse.hide()
            }
        })
    })
}