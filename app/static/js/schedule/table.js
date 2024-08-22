const getSchedule = function (url) {
    fetch(url, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
        .then(response => response.text())
        .then(html => {
            document.querySelector('.schedule__content').innerHTML = html

            const noteBlocks = document.querySelectorAll('.note-block')

            noteBlocks.forEach(noteBlock => {
                prepareCollapseAll(noteBlock.querySelector('.collapse'))
                prepareNoteCreate(noteBlock)
                prepareNoteDisplay(noteBlock)
            })

            prepareBookmarkDisplay()
            prepareBookmarkAdd()

            const spinner = document.querySelector('.spinner-border')
            spinner.classList.remove('spinner-border-visible')
            spinner.classList.add('spinner-border-hidden')
        })
}