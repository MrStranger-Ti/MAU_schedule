from schedule.parser import TeacherKeysParser


class TestTeacherKeysParser:
    html = "teachers-list.html"

    def test_parse_data_success(self, disable_cache, mock_scraper):
        expected_data = [
            {
                "key": "0f2a8f7b-67cf-11e8-abfc-00155d0aee04",
                "name": "Белогурова Татьяна Павловна",
            },
            {
                "key": "f5674e52-ecdc-11e5-9338-00155d0aee04",
                "name": "Беспалова Светлана Владимировна",
            },
            {
                "key": "a54bd012-2272-11ef-9f67-1cc1de6f817c",
                "name": "Богданов Артур Олегович Приймак Павел Георгиевич",
            },
            {
                "key": "0b944819-24b5-11ef-b027-1cc1de6f817c",
                "name": "Борисюк Павел Ильич",
            },
            {
                "key": "74a9959d-0ed8-11eb-8e4d-1cc1de6f817c",
                "name": "Быченков Павел Артемович",
            },
            {
                "key": "f5674e76-ecdc-11e5-9338-00155d0aee04",
                "name": "Волкова Татьяна Павловна",
            },
            {
                "key": "f5674e8d-ecdc-11e5-9338-00155d0aee04",
                "name": "Гнатюк Виктор Степанович",
            },
            {
                "key": "481ea25d-24b5-11ef-b027-1cc1de6f817c",
                "name": "Гречин Дмитрий Павлович",
            },
            {
                "key": "9d42fea3-8b93-11e6-af43-00155d0aee04",
                "name": "Ершов Павел Сергеевич",
            },
            {
                "key": "f5674eb2-ecdc-11e5-9338-00155d0aee04",
                "name": "Захаренко Валентина Степановна",
            },
            {
                "key": "3b797c61-5bde-11ec-8ee8-1cc1de6f817c",
                "name": "Конарев Егор Павлович",
            },
            {
                "key": "67eb5b0c-69d9-11ee-b060-1cc1de6f817c",
                "name": "Ляпакова Маргарита Орестовна",
            },
            {
                "key": "f567502c-ecdc-11e5-9338-00155d0aee04",
                "name": "Макаревич Павел Робертович",
            },
            {
                "key": "9c75a7b8-69d5-11ee-b060-1cc1de6f817c",
                "name": "Онопа Оксана Алексеевна",
            },
            {
                "key": "e2048ccf-69d6-11ee-b060-1cc1de6f817c",
                "name": "Павлов Николай Александрович",
            },
            {
                "key": "f5674f31-ecdc-11e5-9338-00155d0aee04",
                "name": "Панкратова Майя Евгеньевна",
            },
            {
                "key": "f5674f33-ecdc-11e5-9338-00155d0aee04",
                "name": "Пантилеев Сергей Петрович",
            },
            {
                "key": "e3faa1e4-6eaf-11ef-9f25-1cc1de6f817c",
                "name": "Панченко Тамара Геннадьевна",
            },
            {
                "key": "d65b202c-69d5-11ee-b060-1cc1de6f817c",
                "name": "Панченко Татьяна Владимировна",
            },
            {
                "key": "b90fd2a4-69d7-11ee-b060-1cc1de6f817c",
                "name": "Парфенов Сергей Анатольевич",
            },
            {
                "key": "b90fd1cf-69d7-11ee-b060-1cc1de6f817c",
                "name": "Пастушкова Марина Анатольевна",
            },
            {
                "key": "f5674f36-ecdc-11e5-9338-00155d0aee04",
                "name": "Пашенцев Сергей Владимирович",
            },
            {
                "key": "f5674fd5-ecdc-11e5-9338-00155d0aee04",
                "name": "Пирогов Павел Павлович",
            },
            {
                "key": "67eb5c3c-69d9-11ee-b060-1cc1de6f817c",
                "name": "Пославский Вячеслав Пантилимонович",
            },
            {
                "key": "f5674f4c-ecdc-11e5-9338-00155d0aee04",
                "name": "Приймак Павел Георгиевич",
            },
            {
                "key": "fd373dc8-cafe-11ee-94ed-1cc1de6f817c",
                "name": "Степанов Артем Валерьевич",
            },
            {
                "key": "eb6eb9a7-ab2f-11ef-b000-1cc1de6f817c",
                "name": "Степанова Елена Викторовна Баюкова Надежда Павловна",
            },
            {
                "key": "a03954aa-67ee-11e8-abfc-00155d0aee04",
                "name": "Степанова Наталия Леонидовна",
            },
            {
                "key": "8f4471fe-5bcf-11ef-8285-1cc1de6f817c",
                "name": "Чунин Павел Анатольевич",
            },
        ]
        mock_scraper(self.html)

        response = TeacherKeysParser().get_data()
        assert response.success
        assert response.data == expected_data

    def test_parse_data_fail(self, disable_cache, mock_scraper):
        mock_scraper(self.html, valid=False)

        response = TeacherKeysParser().get_data()
        assert not response.success
