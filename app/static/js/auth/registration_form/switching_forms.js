const prepareSwitchForm = function () {
    document.getElementById('step-1').addEventListener('click', () => {
        switchForm(2)
    })

    document.getElementById('step-2').addEventListener('click', () => {
        switchForm(1)
    })

    document.getElementById('registration').addEventListener('click', () => {
        const form = document.querySelector('.auth__form')
        if (!form.full_name.validity.valid || !form.email.validity.valid || !form.password.validity.valid) {
            switchForm(1)
        }
    })
}


const switchForm = function (page) {
    const hiddenPage = page == 1 ? 2 : 1
    document.getElementById('step-number').textContent = page
    document.querySelector(`.auth__step-${hiddenPage}`).setAttribute('hidden', '')
    document.querySelector(`.auth__step-${page}`).removeAttribute('hidden')
}