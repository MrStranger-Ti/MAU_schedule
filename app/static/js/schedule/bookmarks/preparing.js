const prepareBookmarkDisplay = function () {
    const btns = document.querySelectorAll('[name="bookmark-delete"]')
    if (btns) {
        btns.forEach(btn => {
            btn.addEventListener('click', (event) => {
                deleteBookmark(event.currentTarget.previousElementSibling)
            })
        })
    }
}


const prepareBookmarkAdd = function () {
    const btn = document.querySelector('[name="bookmark-create"]')
    if (btn) {
        btn.addEventListener('click', () => {
            createBookmark()
        })
    }
}