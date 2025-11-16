# Инструкция по запуску тестов для лабораторной работы №10

## Требования задания

✅ Запуск UI тестов в двух разных браузерах (Chrome и Firefox)  
✅ Использование RemoteWebDriver для взаимодействия с удаленным драйвером по сети  
✅ Настройка Selenium Grid  

## Шаги для запуска

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Запуск Selenium Grid

```bash
docker-compose up -d
```

Эта команда запустит:
- **Selenium Hub** на порту 4444 (http://localhost:4444)
- **Chrome Node** - нода для запуска тестов в Chrome
- **Firefox Node** - нода для запуска тестов в Firefox

### 3. Проверка работы Selenium Grid

Откройте в браузере: http://localhost:4444

Вы должны увидеть веб-интерфейс Selenium Grid с информацией о доступных нодах (Chrome и Firefox).

### 4. Запуск тестов

**ВАЖНО**: Убедитесь, что Selenium Grid запущен!

```bash
pytest tests/ -v
```

Каждый тест будет автоматически выполнен дважды:
- Один раз в Chrome
- Один раз в Firefox

### 5. Остановка Selenium Grid (после завершения тестов)

```bash
docker-compose down
```

## Проверка выполнения требований

### ✅ RemoteWebDriver

В файле `conftest.py` используется `webdriver.Remote()` для подключения к Selenium Hub:

```python
driver = webdriver.Remote(
    command_executor="http://localhost:4444/wd/hub",
    options=options
)
```

### ✅ Два браузера

В `conftest.py` настроена параметризация фикстуры:

```python
@pytest.fixture(scope="function", params=["chrome", "firefox"])
def driver(request):
    # ...
```

Это обеспечивает автоматический запуск каждого теста в обоих браузерах.

### ✅ Selenium Grid

В `docker-compose.yml` настроены:
- Selenium Hub (центральный узел)
- Chrome Node (нода для Chrome)
- Firefox Node (нода для Firefox)

## Пример вывода при запуске тестов

```
tests/test_login.py::test_login[chrome] PASSED
tests/test_login.py::test_login[firefox] PASSED
tests/test_login.py::test_invalid_login[chrome] PASSED
tests/test_login.py::test_invalid_login[firefox] PASSED
...
```

Обратите внимание на `[chrome]` и `[firefox]` - это показывает, что тесты запускаются в обоих браузерах.

## Устранение проблем

### Проблема: Не удается подключиться к Selenium Hub

**Решение**: Убедитесь, что Selenium Grid запущен:
```bash
docker-compose ps
```

Должны быть запущены 3 контейнера: selenium-hub, chrome-node, firefox-node.

### Проблема: Тесты падают с ошибкой подключения

**Решение**: Проверьте, что Hub доступен по адресу http://localhost:4444

### Проблема: Тесты запускаются только в одном браузере

**Решение**: Убедитесь, что в `conftest.py` указан параметр `params=["chrome", "firefox"]` в декораторе фикстуры.

