const prepareBookmarkDisplay = function () {
    document.querySelector('[name="bookmark-delete"]').addEventListener('click', (event) => {
        deleteBookmark(event.currentTarget.previousElementSibling)
    })
}