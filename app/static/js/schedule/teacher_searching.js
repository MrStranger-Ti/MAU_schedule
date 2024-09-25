const getTeachersLinks = function () {
    const input = document.querySelector('[name="query"]')
    const btn = document.querySelector('.schedule__form > button')

    input.setAttribute('disabled', 'true')
    btn.setAttribute('disabled', 'true')
    btn.children[0].removeAttribute('hidden')

    const query = document.querySelector('[name="query"]').value
    fetch(getIndex() + `/schedule/get-teachers-links/?query=${query}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
        .then(response => response.text())
        .then(html => {
            document.querySelector('.schedule__teachers-list').innerHTML = html

            input.removeAttribute('disabled')
            btn.removeAttribute('disabled')
            btn.children[0].setAttribute('hidden', '')
        })
}