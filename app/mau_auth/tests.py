from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse_lazy, reverse

from mau_auth.forms import UserRegistrationForm


User = get_user_model()


class UserTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            full_name='Иванов Иван Иванович',
            password='test',
            email='test@example.com',
        )
        self.assertTrue(user)


class RegistrationViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.base_url = reverse_lazy('mau_auth:registration')
        cls.template_name = 'mau_auth/registration.html'

    def test_status_code_200(self) -> None:
        response = self.client.get(self.base_url)
        self.assertEqual(200, response.status_code)

    def test_uses_correct_template(self):
        response = self.client.get(self.base_url)
        self.assertTemplateUsed(response, self.template_name)

    def test_correct_form_display(self):
        field_names = ('full_name', 'password', 'email', 'institute', 'course', 'group')
        response = self.client.get(self.base_url)
        response_form = response.context.get('form')
        self.assertTrue(response_form)

        for field_name in field_names:
            self.assertTrue(response_form.fields.get(field_name))


class UserRegistrationFormTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.base_url = reverse_lazy('mau_auth:registration')

    def test_registration_form_with_valid_data(self) -> None:
        form = UserRegistrationForm({
            'password': 'testpassword',
            'email': 'test@example.com',
            'full_name': 'Петров Петр Петрович',
            'institute': 'ЦТ',
            'course': 2,
            'group': 'БИВТ-24',
        })
        self.assertTrue(form.is_valid())

    def test_set_invalid_email_of_registration_form(self) -> None:
        test_data = ('Петров Петр', 'dasdass')
        for data in test_data:
            form = UserRegistrationForm({'full_name': data})
            self.assertEqual(form.errors['full_name'], ['ФИО должно быть в формате Фамилия Имя Отчество'])


class LoginTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user_data = {
            'full_name': 'Иванов Иван Иванович',
            'password': 'test',
            'email': 'test@example.com',
        }

    def setUp(self) -> None:
        self.test_user = User.objects.create_user(**self.user_data)

    def tearDown(self) -> None:
        self.test_user.delete()

    def test_login_user(self) -> None:
        self.client.login(**self.user_data)
        response = self.client.get(reverse('schedule:index'))
        self.assertEqual(str(response.context.get('user')), self.user_data['email'])

    def test_login_url(self):
        response = self.client.get(reverse('mau_auth:login'))
        self.assertEqual(200, response.status_code)