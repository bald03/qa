# Быстрый старт - Лабораторная работа №10

## Краткая инструкция по запуску

### 1. Запуск Selenium Grid

```bash
docker-compose up -d
```

Проверьте статус Grid: http://localhost:4444

### 2. Запуск тестов

#### В Chrome:
```bash
pytest tests/ -v --browser=chrome
```

#### В Firefox:
```bash
pytest tests/ -v --browser=firefox
```

#### Во всех браузерах (Windows):
```bash
run_tests_all_browsers.bat
```

#### Во всех браузерах (Linux/Mac):
```bash
chmod +x run_tests_all_browsers.sh
./run_tests_all_browsers.sh
```

### 3. Остановка Selenium Grid

```bash
docker-compose down
```

## Что было реализовано

✅ **Selenium Grid** настроен через Docker Compose
- Hub на порту 4444
- Chrome Node в контейнере
- Firefox Node в контейнере

✅ **RemoteWebDriver** используется вместо локального драйвера
- Подключение к Hub по сети (http://localhost:4444/wd/hub)
- Браузеры запускаются в Docker контейнерах

✅ **Параметризация браузеров**
- Выбор браузера через параметр `--browser=chrome` или `--browser=firefox`
- Все тесты могут запускаться в любом из браузеров

## Структура Selenium Grid

```
┌─────────────────────────────────────────┐
│         Selenium Grid Hub               │
│      (localhost:4444)                    │
│                                          │
│  ┌──────────────┐  ┌──────────────┐    │
│  │ Chrome Node  │  │ Firefox Node │    │
│  │  (Docker)    │  │   (Docker)   │    │
│  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────┘
           ▲
           │ RemoteWebDriver
           │ (http://localhost:4444/wd/hub)
           │
    ┌──────┴──────┐
    │   Тесты    │
    │  (pytest)  │
    └────────────┘
```

## Просмотр браузеров через VNC

Для просмотра работы браузеров в реальном времени можно использовать VNC:

1. **Chrome Node**: http://localhost:6900
   - Пароль VNC: `secret`

2. **Firefox Node**: http://localhost:6901
   - Пароль VNC: `secret`

**Примечание**: Для просмотра через VNC используйте браузер или VNC клиент (например, TightVNC, RealVNC).

## Проверка работы

1. Убедитесь, что Docker запущен
2. Запустите `docker-compose up -d`
3. Откройте http://localhost:4444 в браузере
4. Вы должны увидеть доступные браузеры (Chrome и Firefox)
5. Запустите тесты с параметром `--browser=chrome` или `--browser=firefox`
6. Для просмотра работы браузеров откройте VNC по адресам выше (пароль: `secret`)

