export const config = {
    API_HOST: "localhost:8000",
    SCHEDULE_URL: "https://www.mauniver.ru/student/timetable/new/",
    DEVELOPER_URL: "https://t.me/MrStrangerTi"
}

export const pagesPaths = {
    index: "/",
    accounts: {
        login: "/accounts/login/",
        register: "/accounts/register/",
        baseRegisterConfirm: "/accounts/register/confirm/",
        registerConfirm: "/accounts/register/confirm/:uidb64/:token/",
        passwordReset: "/accounts/password-reset/",
        basePasswordResetConfirm: "/accounts/password-reset/confirm/",
        passwordResetConfirm: "/accounts/password-reset/confirm/:uidb64/:token/",
        profile: "/accounts/profile/",
    },
    schedule: {
        group: "/schedule/group/",
        teacherSearch: "/schedule/teacher-search/",
        teacher: "/schedule/teacher/"
    }
}