const showMauNotification = function (text, type) {
    if (!document.querySelector('.notification')
        || document.body.lastElementChild.textContent !== text) {

        const iconClass = type == 'error' ? 'notification__icon-error' : 'notification__icon-ok'
        document.body.insertAdjacentHTML('beforeend',
            '<div class="notification flex">' +
            `  <div class="${iconClass}"></div>` +
            `  <p class="notification__text">${text}</p>` +
            '</div>'
        )

        const notificationBlock = document.body.lastElementChild
        setTimeout(() => notificationBlock.style.opacity = '1', 5)
        setTimeout(() => notificationBlock.style.opacity = '', 3000)
        setTimeout(() => notificationBlock.remove(), 3300)
    }
}