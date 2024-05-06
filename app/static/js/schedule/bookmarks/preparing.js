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