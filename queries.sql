
DROP DATABASE hh_vacancies;

CREATE DATABASE hh_vacancies;

CREATE TABLE vacancies (
    vacancy_id SERIAL PRIMARY KEY,
    company VARCHAR(255) NOT NULL,
    title_vacancies VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    salary INTEGER,
    url TEXT
);

CREATE TABLE top_vacancies (
    vacancy_id SERIAL PRIMARY KEY,
    company VARCHAR(255) NOT NULL,
    title_vacancies VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    salary INTEGER,
    url TEXT
);

INSERT INTO vacancies (company, title_vacancies, city, salary, url)
VALUES (Виста, Junior Python разработчик, Санкт-Петербург, 60000, https://hh.ru/vacancy/84350333
        ТРАФФИК, QA Engineer / Специалист по ручному тестированию, Санкт-Петербург, 0, https://hh.ru/vacancy/84275508
        ПИКАССО, Backend-разработчик (Python), Санкт-Петербург, 70000, https://hh.ru/vacancy/84190497
        Just AI, Junior Data Analyst, Санкт-Петербург, 0, https://hh.ru/vacancy/83606452
        Риалвеб, Интернет-агентство, Frontend developer (react), Санкт-Петербург, 0, https://hh.ru/vacancy/82414325
        YADRO, Стажер-Программист Go / Golang Trainee in Telecom, Санкт-Петербург, 0, https://hh.ru/vacancy/84291964
        СБЕР, QA инженер, Санкт-Петербург, 0, https://hh.ru/vacancy/83644537
        ТехЛАБ, QA-инженер, Санкт-Петербург, 0, https://hh.ru/vacancy/83565988
        YADRO, Junior DevOps Engineer (Tatlin Flex), Санкт-Петербург, 0, https://hh.ru/vacancy/84302953
        ВЕБИМ.РУ, Начинающий full stack разработчик, Санкт-Петербург, 25000, https://hh.ru/vacancy/83619946
        ТайпТайп, Инженер-программист (Junior), Санкт-Петербург, 75000, https://hh.ru/vacancy/83019820
        ИСТ, Инженер по тестированию (Junior), Санкт-Петербург, 65000, https://hh.ru/vacancy/83961336
        ИСТ, Инженер по тестированию (Junior/Middle), Санкт-Петербург, 65000, https://hh.ru/vacancy/84148599
        Сычев Павел Владимирович, Backend Python разработчик, Санкт-Петербург, 80000, https://hh.ru/vacancy/84118400
        Just AI, Стажер Devops engineer, Санкт-Петербург, 0, https://hh.ru/vacancy/84132457
        Partnerkin, FullStack разработчик (remote), Санкт-Петербург, 0, https://hh.ru/vacancy/83419201
        Topface, Младший аналитик, Санкт-Петербург, 30000, https://hh.ru/vacancy/82909280
        буше, Младший бизнес-аналитик / Business Analyst Junior, Санкт-Петербург, 54000, https://hh.ru/vacancy/83450998
        Linxdatacenter, Стажёр в отдел ИТ, Санкт-Петербург, 0, https://hh.ru/vacancy/83244280
        ЮMoney, Аналитик / ML, Санкт-Петербург, 0, https://hh.ru/vacancy/84082171
);

INSERT INTO top_vacancies (company, title_vacancies, city, salary, url)
VALUES (ИСТ, Инженер по тестированию (Junior), Санкт-Петербург, 65000, https://hh.ru/vacancy/83961336
        YADRO, Junior DevOps Engineer (Tatlin Flex), Санкт-Петербург, 0, https://hh.ru/vacancy/84302953
        ТехЛАБ, QA-инженер, Санкт-Петербург, 0, https://hh.ru/vacancy/83565988
        Just AI, Стажер Devops engineer, Санкт-Петербург, 0, https://hh.ru/vacancy/84132457
        Виста, Junior Python разработчик, Санкт-Петербург, 60000, https://hh.ru/vacancy/84350333
        Just AI, Junior Data Analyst, Санкт-Петербург, 0, https://hh.ru/vacancy/83606452
        ИСТ, Инженер по тестированию (Junior/Middle), Санкт-Петербург, 65000, https://hh.ru/vacancy/84148599
        ВЕБИМ.РУ, Начинающий full stack разработчик, Санкт-Петербург, 25000, https://hh.ru/vacancy/83619946
        ТРАФФИК, QA Engineer / Специалист по ручному тестированию, Санкт-Петербург, 0, https://hh.ru/vacancy/84275508
        Topface, Младший аналитик, Санкт-Петербург, 30000, https://hh.ru/vacancy/82909280
        СБЕР, QA инженер, Санкт-Петербург, 0, https://hh.ru/vacancy/83644537
);

SELECT company, count(*)
FROM vacancies
GROUP BY company;

SELECT *
FROM vacancies
WHERE company='СБЕР';

SELECT round(AVG(salary))
from vacancies;

SELECT *
FROM vacancies
WHERE salary > (SELECT AVG(salary)
                    FROM vacancies);

SELECT *
FROM vacancies
WHERE title_vacancies LIKE '%Python%';

SELECT *
FROM top_vacancies;
