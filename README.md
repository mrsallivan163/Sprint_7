# Проект автотизации тестирования API сервиса Яндекс Самокат
1. Основа для написания автотестов — фреймворк pytest.
2. Установить зависимости — pip install -r requirements.txt
3. Запуск тестов с отчетом Allure - pytest -v --alluredir=tmp/allure_report
4. Открытие отчета Allure - allure serve tmp/allure_report 
5. Удаление старого отчета и запуск тестового прогона - rm -rf tmp/allure_report && pytest -v --alluredir=tmp/allure_report 