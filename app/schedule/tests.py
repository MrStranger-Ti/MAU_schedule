from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy, reverse

from mau_auth.models import MauInstitute

User = get_user_model()


class TestSchedulePage(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        institute = MauInstitute.objects.get(name='ИИС и ЦТ')
        cls.user_data = {
            'full_name': 'Иван Иван Иванович',
            'email': 'testuser@mauniver.ru',
            'password': 'test',
            'institute': institute,
            'course': 1,
            'group': 'БИВТ-ВП-23',
        }
        cls.base_url = reverse_lazy('schedule:index')
        cls.template_name = 'schedule/group.html'

    def setUp(self) -> None:
        self.user = User.objects.create_user(**self.user_data)
        self.client.login(
            email=self.user_data.get('email'),
            password=self.user_data.get('password')
        )

    def test_login_redirect_not_authenticated_user(self):
        self.client.logout()
        login_url = reverse('mau_auth:login')

        response = self.client.get(self.base_url)
        self.assertRedirects(response, f'{login_url}?next={self.base_url}')

    def test_get_status_200(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)

    def test_use_correct_template(self):
        response = self.client.get(self.base_url)
        self.assertTemplateUsed(response, self.template_name)

    def test_schedule_display_with_valid_user_data(self):
        response = self.client.get(self.base_url)
        self.assertContains(response, '<table class="schedule_table">')

    def test_schedule_not_display_with_invalid_user_data(self):
        self.user.group = 'invalid_group'
        self.user.save()

        response = self.client.get(self.base_url)
        self.assertContains(response, 'Расписания нет. Проверьте свои данные в профиле.')
