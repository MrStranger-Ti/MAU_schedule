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