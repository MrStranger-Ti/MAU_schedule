from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy, reverse

from mau_auth.models import MauInstitute
from profiles.forms import ProfileUpdateForm
from django.conf import settings

User = get_user_model()


class TestProfilePage(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        institute = MauInstitute.objects.get(name='ИИС и ЦТ')
        cls.user_data = {
            'email': 'test@mauniver.ru',
            'password': '12345',
            'full_name': 'Петров Петр Петрович',
            'institute': institute,
            'course': 1,
            'group': 'БИВТ-ВП-23',
        }
        cls.base_url = reverse_lazy('profiles:profile')
        cls.template_name = 'profiles/profile.html'

    def setUp(self) -> None:
        self.user = User.objects.create_user(**self.user_data)
        self.client.login(**self.user_data)

    def test_get_status_200(self) -> None:
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)

    def test_use_correct_template(self) -> None:
        response = self.client.get(self.base_url)
        self.assertTemplateUsed(response, self.template_name)


class TestProfileUpdateForm(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_profile_update_form_with_valid_data(self) -> None:
        institute = MauInstitute.objects.get(name='ИИС и ЦТ')
        valid_data = {
            'full_name': 'Петров Петр Петрович',
            'institute': institute,
            'course': 1,
            'group': 'БИВТ-ВП-23',
        }
        form = ProfileUpdateForm(valid_data)

        self.assertTrue(form.is_valid())

    def test_get_full_name_field_error(self) -> None:
        test_full_names = ('Петров Иванович', 'КирилловКириллВасильевич')
        for full_name in test_full_names:
            form = ProfileUpdateForm({'full_name': full_name})
            self.assertEqual(form.errors['full_name'], ['ФИО должно быть в формате Фамилия Имя Отчество'])


class TestProfileUpdatePage(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        institute = MauInstitute.objects.get(name='ИИС и ЦТ')
        cls.user_data = {
            'email': 'test@mauniver.ru',
            'password': '12345',
            'full_name': 'Петров Петр Петрович',
            'institute': institute,
            'course': 1,
            'group': 'БИВТ-ВП-23',
        }
        cls.base_url = reverse_lazy('profiles:profile_update')
        cls.template_name = 'profiles/profile_update.html'

    def setUp(self) -> None:
        self.user = User.objects.create_user(**self.user_data)
        self.client.login(**self.user_data)

    def test_get_status_200(self) -> None:
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)

    def test_use_correct_template(self) -> None:
        response = self.client.get(self.base_url)
        self.assertTemplateUsed(response, self.template_name)

    def test_form_in_context(self) -> None:
        response = self.client.get(self.base_url)
        form = response.context.get('form')
        self.assertTrue(form)

    def test_form_fields_display(self) -> None:
        form_fields = ('full_name', 'institute', 'course', 'group')
        response = self.client.get(self.base_url)
        form = response.context.get('form')

        for field in form_fields:
            self.assertTrue(form.fields.get(field))

    def test_change_user_data_successfully(self) -> None:
        institute = MauInstitute.objects.get(name='ИГ и СН')
        form_data = {
            'full_name': 'Сидоров Сергей Петрович',
            'institute': institute,
            'course': 1,
            'group': 'БЛ-ПРВ-23',
        }
        response = self.client.post(self.base_url, data=form_data)
        print(response.content.decode())
        self.assertEqual(response.status_code, 200)

        self.user.refresh_from_db()
        self.assertEqual(self.user.full_name, form_data['full_name'])
        self.assertEqual(self.user.institute, form_data['institute'])
        self.assertEqual(self.user.course, form_data['course'])
        self.assertEqual(self.user.group, form_data['group'])
