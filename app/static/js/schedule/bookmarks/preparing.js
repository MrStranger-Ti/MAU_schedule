const prepareBookmarkDisplay = function () {
    const btn = document.querySelector('[name="bookmark-delete"]')
    if (btn) {
        btn.addEventListener('click', (event) => {
            deleteBookmark(event.currentTarget.previousElementSibling)
        })
    }
}