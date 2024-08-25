const getSchedule = function (url) {
    fetch(url, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
        .then(response => response.text())
        .then(json => {
            const json_data = JSON.parse(json)
            document.querySelector('.schedule__content').innerHTML = json_data.html

            const noteBlocks = document.querySelectorAll('.note-block')
            noteBlocks.forEach(noteBlock => {
                const note = json_data.notes.find(el => el.location === noteBlock.getAttribute('data-note-location'))
                if (note) {
                    prepareNoteDisplay(noteBlock, note.text)
                }

                prepareNoteCreate(noteBlock)
                prepareCollapseAll(noteBlock.querySelector('.collapse'))
            })

            prepareBookmarkDisplay()
            prepareBookmarkAdd()

            const spinner = document.querySelector('.spinner-border')
            spinner.classList.remove('spinner-border-visible')
            spinner.classList.add('spinner-border-hidden')
        })
}