const prepareRemoveErrorStyle = function () {
    const errors = document.querySelectorAll('.error-input')
    errors.forEach((error) => {
        error.addEventListener('input', () => {
            error.classList.remove('error-input')
        })
    })
}