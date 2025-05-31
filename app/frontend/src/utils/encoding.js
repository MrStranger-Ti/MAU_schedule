export const encodeBase64 = (value) => {
    return window.btoa(encodeURIComponent(value));
}

export const decodeBase64 = (value) => {
    return decodeURIComponent(window.atob(value));
}