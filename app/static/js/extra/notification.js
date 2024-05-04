const showMauNotification = function (text) {
    if (!document.querySelector('.notification')
        || document.querySelector('.notification__text').textContent !== text) {

        const notificationBlock = document.createElement('div')
        notificationBlock.innerHTML = `<p class="notification__text">${text}</p>`
        notificationBlock.classList.add('notification')
        document.body.append(notificationBlock)

        setTimeout(() => notificationBlock.remove()  ,2000)
    }
}