from schedule.parser import TeacherKeysParser


class TestTeacherKeysParser:
    html = "teachers-list.html"

    def test_parse_data_success(self, disable_cache, mock_scraper):
        expected_data = {
            "Белогурова Татьяна Павловна": "0f2a8f7b-67cf-11e8-abfc-00155d0aee04",
            "Беспалова Светлана Владимировна": "f5674e52-ecdc-11e5-9338-00155d0aee04",
            "Богданов Артур Олегович Приймак Павел Георгиевич": "a54bd012-2272-11ef-9f67-1cc1de6f817c",
            "Борисюк Павел Ильич": "0b944819-24b5-11ef-b027-1cc1de6f817c",
            "Быченков Павел Артемович": "74a9959d-0ed8-11eb-8e4d-1cc1de6f817c",
            "Волкова Татьяна Павловна": "f5674e76-ecdc-11e5-9338-00155d0aee04",
            "Гнатюк Виктор Степанович": "f5674e8d-ecdc-11e5-9338-00155d0aee04",
            "Гречин Дмитрий Павлович": "481ea25d-24b5-11ef-b027-1cc1de6f817c",
            "Ершов Павел Сергеевич": "9d42fea3-8b93-11e6-af43-00155d0aee04",
            "Захаренко Валентина Степановна": "f5674eb2-ecdc-11e5-9338-00155d0aee04",
            "Конарев Егор Павлович": "3b797c61-5bde-11ec-8ee8-1cc1de6f817c",
            "Ляпакова Маргарита Орестовна": "67eb5b0c-69d9-11ee-b060-1cc1de6f817c",
            "Макаревич Павел Робертович": "f567502c-ecdc-11e5-9338-00155d0aee04",
            "Онопа Оксана Алексеевна": "9c75a7b8-69d5-11ee-b060-1cc1de6f817c",
            "Павлов Николай Александрович": "e2048ccf-69d6-11ee-b060-1cc1de6f817c",
            "Панкратова Майя Евгеньевна": "f5674f31-ecdc-11e5-9338-00155d0aee04",
            "Пантилеев Сергей Петрович": "f5674f33-ecdc-11e5-9338-00155d0aee04",
            "Панченко Тамара Геннадьевна": "e3faa1e4-6eaf-11ef-9f25-1cc1de6f817c",
            "Панченко Татьяна Владимировна": "d65b202c-69d5-11ee-b060-1cc1de6f817c",
            "Парфенов Сергей Анатольевич": "b90fd2a4-69d7-11ee-b060-1cc1de6f817c",
            "Пастушкова Марина Анатольевна": "b90fd1cf-69d7-11ee-b060-1cc1de6f817c",
            "Пашенцев Сергей Владимирович": "f5674f36-ecdc-11e5-9338-00155d0aee04",
            "Пирогов Павел Павлович": "f5674fd5-ecdc-11e5-9338-00155d0aee04",
            "Пославский Вячеслав Пантилимонович": "67eb5c3c-69d9-11ee-b060-1cc1de6f817c",
            "Приймак Павел Георгиевич": "f5674f4c-ecdc-11e5-9338-00155d0aee04",
            "Степанов Артем Валерьевич": "fd373dc8-cafe-11ee-94ed-1cc1de6f817c",
            "Степанова Елена Викторовна Баюкова Надежда Павловна": "eb6eb9a7-ab2f-11ef-b000-1cc1de6f817c",
            "Степанова Наталия Леонидовна": "a03954aa-67ee-11e8-abfc-00155d0aee04",
            "Чунин Павел Анатольевич": "8f4471fe-5bcf-11ef-8285-1cc1de6f817c",
        }
        mock_scraper(self.html)

        response = TeacherKeysParser().get_data()
        assert response.success
        assert response.data == expected_data

    def test_parse_data_fail(self, disable_cache, mock_scraper):
        mock_scraper(self.html, valid=False)

        response = TeacherKeysParser().get_data()
        assert not response.success
