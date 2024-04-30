const getTeachersLinks = function () {
    const input = document.querySelector('[name="query"]')
    const btn = document.querySelector('.schedule__form > button')

    input.setAttribute('disabled', 'true')
    btn.setAttribute('disabled', 'true')
    btn.children[0].classList.remove('btn-spinner-hidden')
    btn.children[1].textContent = 'Загрузка...'

    const query = document.querySelector('[name="query"]').value
    fetch(getIndex() + `/schedule/get-teachers-links/?query=${query}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
        .then(response => response.text())
        .then(html => {
            document.querySelector('.schedule__list-block').innerHTML = html

            btn.children[0].classList.add('btn-spinner-hidden')
            btn.children[1].textContent = 'Найти'
            input.removeAttribute('disabled')
            btn.removeAttribute('disabled')
        })
}