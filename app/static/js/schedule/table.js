const getSchedule = function (url) {
    const spinner = document.querySelector('.spinner-border')
    document.querySelector('.schedule__content').innerHTML = ''
    spinner.removeAttribute('hidden')

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
            prepareScheduleForm(url)

            const spinner = document.querySelector('.spinner-border')
            spinner.setAttribute('hidden', '')
        })
}


const prepareScheduleForm = function (url) {
    const form = document.querySelector('.schedule__form')
    if (form) {
        const searchBtn = form.querySelector('button')
        searchBtn.addEventListener('click', event => {
            const period = form.elements[0].querySelector(':checked')
            if (period.value) {
                url = new URL(url)
                url.searchParams.set('period', period.text)

                getSchedule(url.href)
            } else {
                showMauNotification('Выберите период', 'error')
            }
        })
    }
}