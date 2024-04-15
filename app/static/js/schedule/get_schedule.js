const getSchedule = function (url) {
    const spinner = document.querySelector('.spinner-border')
    fetch(url)
        .then(response => response.text())
        .then(schedule => {
            const container = document.querySelector('.tables__container')
            const parser = new DOMParser()
            const htmlSchedule = parser.parseFromString(schedule, 'text/html')
            const divTables = htmlSchedule.querySelector('.tables__list')
            container.append(divTables)

            spinner.classList.remove('spinner-border-visible')
            spinner.classList.add('spinner-border-hidden')
        })
}
