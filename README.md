Проект автоматизации тестирования Яндекс Самокат
Основа для написания автотестов — фреймворк pytest.
Установить зависимости — pip install -r requirements.txt
Запуск тестов с отчетом Allure - pytest -v --alluredir=tmp/allure_report
Открытие отчета Allure - allure serve tmp/allure_report
Удаление старого отчета и запуск тестового прогона - rm -rf tmp/allure_report && pytest -v --alluredir=tmp/allure_report