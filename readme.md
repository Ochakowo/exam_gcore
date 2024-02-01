EN::\
To run the tests, please start the Docker.

In the terminal, enter the command: `docker-compose build`\
This will build the image if you are running it for the first time.

Then, you can run the tests using the following command: `docker-compose up`

The tests are executed with parameterization, using the "flaky" module to rerun failed tests (up to 3 times).\
Allure reports are saved in the directory "allure-results".

At http://localhost:5252 you can access the ready Allure report.\
At http://localhost:7900 you can observe the test execution in real-time (VNC).

I have provided detailed comments about the code's operation in the docstrings. Enjoy!

RU::\
Для запуска тестов запустите Docker.

В терминале введите команду: `docker-compose build`\
Это соберет образ если вы запускаете тесты впервые

Затем вы можете запустить тесты, используя следующую команду: `docker-compose up`

Тесты выполняются с параметризацией, используется модуль "flaky" для повторного прохождения упавших тестов (не более 3 раз).\
Отчеты allure сохраняются в директории "allure-results".

На http://localhost:5252 вы получите готовый отчёт allure.\
На http://localhost:7900 вы сможете наблюдать за выполнением тестов в реальном времени (VNC).

Какие-либо подробные комментарии о работе кода я изложил в docstrings. Спасибо!
