# 🌐 Browser Fingerprint Generator

CLI-утилита для генерации реалистичных фейковых отпечатков браузера с красивым интерфейсом. Позволяет настроить параметры (браузер, ОС, локацию, тип устройства) и массово генерировать JSON-файлы с фингерпринтами для тестирования систем антифрода, приватности и безопасности.

> 🔒 **Приватность и прозрачность**  
> Утилита работает полностью локально и не собирает, не хранит и не передаёт никакие персональные данные. Все генерации происходят в памяти и сохраняются только в указанную пользователем директорию.

---

## ⚡ Возможности

| Категория | Описание |
|---|---|
| 🎨 **Красивый CLI** | Интерфейс на базе Rich: цветные панели, таблицы, прогресс-бары и спиннеры. |
| 🌍 **15+ локаций** | США, Великобритания, Россия, Германия, Франция, Япония, Китай, Корея и другие. |
| 🕐 **Согласованные таймзоны** | Timezone автоматически подбирается под выбранную локацию и язык. |
| 🌐 **5 браузеров** | Chrome, Firefox, Safari, Edge, Brave с реалистичными User-Agent. |
| 💻 **3 ОС** | Windows, macOS, Linux с корректными платформами и архитектурами. |
| 🎮 **100+ GPU** | NVIDIA RTX/GTX, AMD RX, Intel UHD/Iris, Apple Silicon, мобильные GPU. |
| 📱 **3 типа устройств** | Desktop, laptop, mobile с адаптивными разрешениями и pixel ratio. |
| 📊 **Массовая генерация** | До 1000 фингерпринтов за раз с прогресс-баром. |
| 💾 **JSON вывод** | Каждый фингерпринт — отдельный файл с уникальным UUID. |
| 🪶 **Без зависимостей** | Стандартная библиотека Python + опциональный Rich для UI. |

---

## 📦 Структура генерируемых данных

Каждый JSON-файл содержит полный набор параметров фингерпринта:

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "generated_at": "2026-06-04T12:00:00Z",
  "browser": {
    "name": "Chrome",
    "version": "123.0.6312.58",
    "user_agent": "Mozilla/5.0 ...",
    "plugins": [...],
    "languages": ["ru-RU", "ru"]
  },
  "os": {
    "name": "Windows",
    "platform": "Win64",
    "architecture": "x86_64"
  },
  "location": {
    "country": "Russia",
    "language": "ru-RU",
    "timezone": "Europe/Moscow",
    "timezone_offset": 3
  },
  "screen": {
    "width": 1920,
    "height": 1080,
    "color_depth": 24,
    "pixel_ratio": 1,
    "device_type": "desktop"
  },
  "hardware": {
    "cores": 8,
    "memory_gb": 16,
    "touch_points": 0
  },
  "webgl": {
    "renderer": "ANGLE (NVIDIA GeForce RTX 3080 Direct3D11 vs_5_0 ps_5_0)",
    "vendor": "Google Inc. (NVIDIA)",
    "version": "WebGL 2.0 (OpenGL ES 3.0 Chromium)"
  },
  "canvas": { "hash": "a1b2c3d4...", "winding": true },
  "audio": { "hash": "f6e5d4c3...", "sample_rate": 44100, "channels": 2 },
  "fonts": ["Arial", "Times New Roman", ...],
  "privacy": {
    "do_not_track": 1,
    "cookies_enabled": true,
    "webdriver": false
  },
  "network": {
    "connection_type": "ethernet",
    "effective_type": "4g",
    "downlink": 100,
    "rtt": 50
  }
}
```

---

## 🛠️ Установка

### Вариант 1: Клонирование репозитория

```bash
git clone https://github.com/ShinysLove/browser-fingerprint-generator.git
cd browser-fingerprint-generator
pip install -r requirements.txt
```

### Вариант 2: Быстрый старт (только базовая версия)

```bash
# Базовая версия работает без зависимостей
python fingerprint_generator.py
```

### 📦 Зависимости (`requirements.txt`)

Для базовой версии (plain CLI):
```txt
# Без внешних зависимостей — только стандартная библиотека Python
```

Для версии с Rich UI:
```txt
rich>=13.0.0
```

---

## 🚀 Использование

### Запуск

```bash
python main.py
```

### Пример работы

```
==================================================
  Browser Fingerprint Generator
 1 - Сгенерировать фингерпринты
 0 - Выход
==================================================
Выберите действие: 1

Браузер:
 0 - Случайно
 1 - chrome
 2 - firefox
 3 - safari
 4 - edge
 5 - brave
Выбор: 1

Операционная система:
 0 - Случайно
 1 - windows
 2 - macos
 3 - linux
Выбор: 1

Локация (windows):
 0 - Случайно
 1 - en-US
 2 - en-GB
 3 - ru-RU
 4 - de-DE
 5 - fr-FR
 ...
Выбор: 3
[+] Выбрано: Russia | ru-RU, ru | Europe/Moscow

Тип устройства:
 0 - Случайно
 1 - desktop
 2 - laptop
 3 - mobile
Выбор: 1

Кастомное разрешение? (y/n) [n]: n
Количество [10]: 5
Директория [./fingerprints]: ./fingerprints

--------------------------------------------------
Браузер:    chrome
ОС:         windows
Локация:    Russia
Устройство: desktop
Разрешение: auto
Количество: 5
Директория: ./fingerprints
--------------------------------------------------
Генерировать? (y/n) [y]: y

[+] [1/5] fingerprint_a3f8b2c1d4e5.json
[+] [2/5] fingerprint_9e7d6c5b4a3f.json
[+] [3/5] fingerprint_2b1c3d4e5f6a.json
[+] [4/5] fingerprint_8f7e6d5c4b3a.json
[+] [5/5] fingerprint_1a2b3c4d5e6f.json

[+] Готово! Сгенерировано 5 файлов в /path/to/fingerprints
```

---

## 🌍 Поддерживаемые локации

### Windows
- `en-US` — United States (America/New_York, America/Chicago, America/Los_Angeles)
- `en-GB` — United Kingdom (Europe/London)
- `ru-RU` — Russia (Europe/Moscow, Asia/Yekaterinburg, Asia/Vladivostok)
- `de-DE` — Germany (Europe/Berlin)
- `fr-FR` — France (Europe/Paris)
- `es-ES` — Spain (Europe/Madrid)
- `it-IT` — Italy (Europe/Rome)
- `pt-BR` — Brazil (America/Sao_Paulo)
- `ja-JP` — Japan (Asia/Tokyo)
- `zh-CN` — China (Asia/Shanghai)
- `ko-KR` — South Korea (Asia/Seoul)
- `pl-PL` — Poland (Europe/Warsaw)
- `tr-TR` — Turkey (Europe/Istanbul)
- `nl-NL` — Netherlands (Europe/Amsterdam)
- `sv-SE` — Sweden (Europe/Stockholm)

### macOS
- `en-US`, `en-GB`, `ru-RU`, `de-DE`, `fr-FR`, `ja-JP`, `zh-CN`, `ko-KR`

### Linux
- `en-US`, `ru-RU`, `de-DE`, `fr-FR`, `zh-CN`, `ja-JP`

---

## 🎮 Поддерживаемые GPU

| Производитель | Модели |
|---|---|
| **NVIDIA RTX** | 4090, 4080, 4070 Ti, 4070, 4060 Ti, 4060, 3090 Ti, 3090, 3080 Ti, 3080, 3070 Ti, 3070, 3060 Ti, 3060, 3050 |
| **NVIDIA GTX** | 1660 Ti, 1660 Super, 1660, 1650 Ti, 1650 Super, 1650, 1080 Ti, 1080, 1070 Ti, 1070, 1060, 1050 Ti, 1050 |
| **AMD Radeon RX** | 7900 XTX/XT, 7800 XT, 7700 XT, 7600, 6950 XT, 6900 XT, 6800 XT, 6800, 6750 XT, 6700 XT, 6600 XT, 6600, 5700 XT, 5700, 5600 XT, 5500 XT, 580, 570 |
| **Intel** | UHD 770/750/730/630/620, Iris Xe, Iris Plus |
| **Apple Silicon** | M3 Max/Pro, M3, M2 Ultra/Max/Pro, M2, M1 Ultra/Max/Pro, M1 |
| **Mobile** | Adreno 740/730/660/650, Mali-G712/G710/G610 |

---

## 📋 Требования

- Python 3.7+
- Rich library (опционально, для красивого UI)

---

## ⚠️ Дисклеймер

Инструмент предназначен исключительно для образовательных целей и тестирования систем безопасности. Автор не несёт ответственности за неправомерное использование.
