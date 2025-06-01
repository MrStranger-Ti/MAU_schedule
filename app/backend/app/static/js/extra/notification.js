const showMauNotification = function (text, type) {
    if (!document.querySelector('.notification')
        || document.body.lastElementChild.textContent !== text) {

        const iconClass = type == 'error' ? 'notification__icon-error' : 'notification__icon-ok'
        const notificationBlock = document.querySelector('.notification')

        document.querySelector('.notification').insertAdjacentHTML('beforeend',
            '<div class="notification__block flex">' +
            `  <div class="${iconClass}"></div>` +
            `  <p class="notification__descr">${text}</p>` +
            '</div>'
        )

        const newNotification = notificationBlock.lastElementChild
        setTimeout(() => newNotification.style.opacity = '1', 5)
        setTimeout(() => newNotification.style.opacity = '', 3000)
        setTimeout(() => newNotification.remove(), 3300)
    }
}