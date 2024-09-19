const getSchedule = function (url) {
    const spinner = document.querySelector('.spinner-border')
    document.querySelector('.schedule__content').innerHTML = ''
    spinner.classList.remove('spinner-border-hidden')
    spinner.classList.add('spinner-border-visible')

    return fetch(url, {
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


const prepareScheduleForm = function (url) {
    const form = document.querySelector('.schedule__form')
    if (form) {
        addEventListener('submit', event => {
            const period = event.target.elements[0].querySelector(':checked').text
            url = new URL(url)
            url.searchParams.set('period', period)

            getSchedule(url.href)
            event.preventDefault()
        })
    }
}