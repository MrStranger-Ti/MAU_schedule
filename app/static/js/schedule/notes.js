// Fetching

const createNote = function (noteBlock, editor) {
    fetch(getIndex() + '/notes/create/', {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json;charset=utf-8',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            location: noteBlock.getAttribute('data-note-location'),
            text: editor.getContents(),
        }),
    })
        .then(response => {
            if (!response.ok) {
                throw Error()
            }
            return response.text()
        })
        .then(json => {
            const jsonData = JSON.parse(json)
            noteBlock.querySelector('.card').innerHTML = jsonData.form
            noteBlock.closest('tr').previousElementSibling.classList.add('schedule__existing-note-tr')
            prepareNoteDisplay(noteBlock, jsonData.value)

            showMauNotification('Заметка успешно создана', 'ok')
        })
        .catch(error => showMauNotification('Не удалось создать заметку', 'error'))
}


const deleteNote = function (noteBlock) {
    fetch(getIndex() + '/notes/delete/', {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json;charset=utf-8',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            location: noteBlock.getAttribute('data-note-location'),
        }),
    })
        .then(response => {
            if (!response.ok) {
                throw Error()
            }
            return response.text()
        })
        .then(html => {
            noteBlock.querySelector('.card').innerHTML = html
            prepareNoteCreate(noteBlock)
            noteBlock.closest('tr').previousElementSibling.classList.remove('schedule__existing-note-tr')

            showMauNotification('Заметка успешно удалена', 'ok')
        })
        .catch((error) => showMauNotification('Не удалось удалить заметку', 'error'))
}


const updateNote = function (noteBlock, editor) {
    fetch(getIndex() + '/notes/update/', {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json;charset=utf-8',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            location: noteBlock.getAttribute('data-note-location'),
            text: editor.getContents()
        }),
    })
        .then(response => {
            if (!response.ok) {
                throw Error()
            }
            return response.text()
        })
        .then(json => {
            const jsonData = JSON.parse(json)
            noteBlock.querySelector('.card').innerHTML = jsonData.form
            prepareNoteDisplay(noteBlock, jsonData.value)

            showMauNotification('Заметка успешно обновлена', 'ok')
        })
        .catch(error => showMauNotification('Не удалось обновить заметку', 'error'))
}


const getUpdateNote = function (noteBlock) {
    const location = noteBlock.getAttribute('data-note-location')

    fetch(getIndex() + `/notes/update/?location=${location}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
        .then(response => response.text())
        .then(json => {
            const jsonData = JSON.parse(json)
            noteBlock.querySelector('.card').innerHTML = jsonData.form
            prepareNoteUpdate(noteBlock, jsonData.value)
        })
}


const getDisplayNote = function (noteBlock) {
    const location = noteBlock.getAttribute('data-note-location')

    fetch(getIndex() + `/notes/display/?location=${location}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
        .then(response => response.text())
        .then(json => {
            const jsonData = JSON.parse(json)
            noteBlock.querySelector('.card').innerHTML = jsonData.form
            prepareNoteDisplay(noteBlock, jsonData.value)
        })
}


// Preparing

const getEditor = function (textarea) {
    return SUNEDITOR.create(textarea, {
        lang: SUNEDITOR_LANG['ru'],
        resizingBar: false,
        width: '100%',
        height: '100%',
        minHeight: '200px',
        font: ['Montserrat'],
        className: 'note-block__editable',
        buttonList: [
            ['undo', 'redo'],
            ['bold', 'underline', 'italic', 'strike'],
            ['textStyle'],
            ['align', 'list', 'lineHeight'],
            ['fullScreen'],
        ],
    })
}


const prepareNoteDisplay = function (noteBlock, text) {
    const form = noteBlock.querySelector('form[name="note-display"]')
    if (form) {
        const editor = getEditor(form.querySelector('textarea'))
        editor.setContents(text)
        editor.toolbar.hide()
        editor.disable()

        noteBlock.querySelector('[name="delete"]').addEventListener('click', () => {
            deleteNote(noteBlock)
        })

        noteBlock.querySelector('[name="update"]').addEventListener('click', () => {
            getUpdateNote(noteBlock)
        })

        prepareBtnCollapse(noteBlock.querySelector('[name="close"]'))
    }
}


const prepareNoteCreate = function (noteBlock) {
    const form = noteBlock.querySelector('form[name="note-create"]')
    if (form) {
        const editor = getEditor(form.querySelector('textarea'))
        form.addEventListener('submit', event => {
            if (editor.getText()) {
                createNote(noteBlock, editor)
            } else {
                showMauNotification('Введите текст в поле ввода', 'error')
            }
            event.preventDefault()
        })

        prepareBtnCollapse(noteBlock.querySelector('[name="close"]'))
    }
}


const prepareNoteUpdate = function (noteBlock, text) {
    const form = noteBlock.querySelector('form[name="note-update"]')
    if (form) {
        const editor = getEditor(form.querySelector('textarea'))
        editor.setContents(text)

        form.addEventListener('submit', event => {
            if (editor.getText()) {
                updateNote(noteBlock, editor)
            } else {
                showMauNotification('Введите текст в поле ввода', 'error')
            }
            event.preventDefault()
        })

        noteBlock.querySelector('[name="display"]').addEventListener('click', () => {
            getDisplayNote(noteBlock)
        })

        prepareBtnCollapse(noteBlock.querySelector('[name="close"]'))
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
                const collapseId = collapsible.getAttribute('id')
                const bsCollapse = new bootstrap.Collapse(`#${collapseId}`, {
                    toggle: false,
                })
                bsCollapse.hide()
            }
        })
    })
}