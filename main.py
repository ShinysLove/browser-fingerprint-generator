import json
import random
import uuid
import os
from pathlib import Path
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.prompt import Prompt, IntPrompt, Confirm
from rich import box
from rich.text import Text
from rich.columns import Columns
from rich.markdown import Markdown

console = Console()

BROWSERS = {
    "chrome": {
        "user_agents": [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36",
        ],
        "versions": ["120.0.6099.109", "121.0.6167.85", "122.0.6261.69", "123.0.6312.58", "124.0.6367.60",
                     "125.0.6422.60"],
        "plugins": [
            {"name": "Chrome PDF Viewer", "filename": "internal-pdf-viewer"},
            {"name": "Chrome PDF Viewer", "filename": "mhjfbmdgcfjbbpaeojofohoefgiehjai"},
        ],
    },
    "firefox": {
        "user_agents": [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{version}) Gecko/20100101 Firefox/{version}",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:{version}) Gecko/20100101 Firefox/{version}",
            "Mozilla/5.0 (X11; Linux x86_64; rv:{version}) Gecko/20100101 Firefox/{version}",
        ],
        "versions": ["121.0", "122.0", "123.0", "124.0", "125.0", "126.0"],
        "plugins": [],
    },
    "safari": {
        "user_agents": [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{version} Safari/605.1.15",
        ],
        "versions": ["17.2", "17.3", "17.4", "17.5"],
        "plugins": [],
    },
    "edge": {
        "user_agents": [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36 Edg/{version}",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36 Edg/{version}",
        ],
        "versions": ["120.0.2210.91", "121.0.2277.83", "122.0.2365.52", "123.0.2420.65"],
        "plugins": [
            {"name": "Microsoft Edge PDF Viewer", "filename": "internal-pdf-viewer"},
        ],
    },
    "brave": {
        "user_agents": [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36",
        ],
        "versions": ["1.61.100", "1.62.153", "1.63.162", "1.64.113"],
        "plugins": [
            {"name": "Brave PDF Viewer", "filename": "internal-pdf-viewer"},
        ],
    },
}

OPERATING_SYSTEMS = {
    "windows": {
        "platforms": ["Win32", "Win64"],
        "locations": {
            "en-US": {"languages": ["en-US", "en"],
                      "timezones": ["America/New_York", "America/Chicago", "America/Los_Angeles", "America/Denver"],
                      "country": "United States"},
            "en-GB": {"languages": ["en-GB", "en"], "timezones": ["Europe/London"], "country": "United Kingdom"},
            "ru-RU": {"languages": ["ru-RU", "ru"],
                      "timezones": ["Europe/Moscow", "Europe/Samara", "Asia/Yekaterinburg", "Asia/Vladivostok"],
                      "country": "Russia"},
            "de-DE": {"languages": ["de-DE", "de"], "timezones": ["Europe/Berlin"], "country": "Germany"},
            "fr-FR": {"languages": ["fr-FR", "fr"], "timezones": ["Europe/Paris"], "country": "France"},
            "es-ES": {"languages": ["es-ES", "es"], "timezones": ["Europe/Madrid"], "country": "Spain"},
            "it-IT": {"languages": ["it-IT", "it"], "timezones": ["Europe/Rome"], "country": "Italy"},
            "pt-BR": {"languages": ["pt-BR", "pt"], "timezones": ["America/Sao_Paulo", "America/Fortaleza"],
                      "country": "Brazil"},
            "ja-JP": {"languages": ["ja-JP", "ja"], "timezones": ["Asia/Tokyo"], "country": "Japan"},
            "zh-CN": {"languages": ["zh-CN", "zh"], "timezones": ["Asia/Shanghai"], "country": "China"},
            "ko-KR": {"languages": ["ko-KR", "ko"], "timezones": ["Asia/Seoul"], "country": "South Korea"},
            "pl-PL": {"languages": ["pl-PL", "pl"], "timezones": ["Europe/Warsaw"], "country": "Poland"},
            "tr-TR": {"languages": ["tr-TR", "tr"], "timezones": ["Europe/Istanbul"], "country": "Turkey"},
            "nl-NL": {"languages": ["nl-NL", "nl"], "timezones": ["Europe/Amsterdam"], "country": "Netherlands"},
            "sv-SE": {"languages": ["sv-SE", "sv"], "timezones": ["Europe/Stockholm"], "country": "Sweden"},
        },
    },
    "macos": {
        "platforms": ["MacIntel"],
        "locations": {
            "en-US": {"languages": ["en-US", "en"], "timezones": ["America/New_York", "America/Los_Angeles"],
                      "country": "United States"},
            "en-GB": {"languages": ["en-GB", "en"], "timezones": ["Europe/London"], "country": "United Kingdom"},
            "ru-RU": {"languages": ["ru-RU", "ru"], "timezones": ["Europe/Moscow", "Asia/Vladivostok"],
                      "country": "Russia"},
            "de-DE": {"languages": ["de-DE", "de"], "timezones": ["Europe/Berlin"], "country": "Germany"},
            "fr-FR": {"languages": ["fr-FR", "fr"], "timezones": ["Europe/Paris"], "country": "France"},
            "ja-JP": {"languages": ["ja-JP", "ja"], "timezones": ["Asia/Tokyo"], "country": "Japan"},
            "zh-CN": {"languages": ["zh-CN", "zh"], "timezones": ["Asia/Shanghai"], "country": "China"},
            "ko-KR": {"languages": ["ko-KR", "ko"], "timezones": ["Asia/Seoul"], "country": "South Korea"},
        },
    },
    "linux": {
        "platforms": ["Linux x86_64"],
        "locations": {
            "en-US": {"languages": ["en-US", "en"], "timezones": ["America/New_York", "America/Los_Angeles"],
                      "country": "United States"},
            "ru-RU": {"languages": ["ru-RU", "ru"], "timezones": ["Europe/Moscow", "Asia/Yekaterinburg"],
                      "country": "Russia"},
            "de-DE": {"languages": ["de-DE", "de"], "timezones": ["Europe/Berlin"], "country": "Germany"},
            "fr-FR": {"languages": ["fr-FR", "fr"], "timezones": ["Europe/Paris"], "country": "France"},
            "zh-CN": {"languages": ["zh-CN", "zh"], "timezones": ["Asia/Shanghai"], "country": "China"},
            "ja-JP": {"languages": ["ja-JP", "ja"], "timezones": ["Asia/Tokyo"], "country": "Japan"},
        },
    },
}

WEBGL_RENDERERS = [
    "ANGLE (NVIDIA GeForce RTX 4090 Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce RTX 4080 Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce RTX 4070 Ti Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce RTX 4070 Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce RTX 4060 Ti Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce RTX 4060 Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce RTX 3090 Ti Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce RTX 3090 Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce RTX 3080 Ti Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce RTX 3080 Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce RTX 3070 Ti Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce RTX 3070 Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce RTX 3060 Ti Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce RTX 3060 Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce RTX 3050 Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce RTX 2080 Ti Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce RTX 2080 Super Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce RTX 2080 Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce RTX 2070 Super Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce RTX 2070 Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce RTX 2060 Super Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce RTX 2060 Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce GTX 1660 Ti Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce GTX 1660 Super Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce GTX 1660 Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce GTX 1650 Ti Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce GTX 1650 Super Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce GTX 1650 Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce GTX 1080 Ti Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce GTX 1080 Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce GTX 1070 Ti Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce GTX 1070 Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce GTX 1060 6GB Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce GTX 1060 3GB Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce GTX 1050 Ti Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce GTX 1050 Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (AMD Radeon RX 7900 XTX Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (AMD Radeon RX 7900 XT Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (AMD Radeon RX 7800 XT Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (AMD Radeon RX 7700 XT Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (AMD Radeon RX 7600 Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (AMD Radeon RX 6950 XT Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (AMD Radeon RX 6900 XT Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (AMD Radeon RX 6800 XT Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (AMD Radeon RX 6800 Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (AMD Radeon RX 6750 XT Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (AMD Radeon RX 6700 XT Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (AMD Radeon RX 6650 XT Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (AMD Radeon RX 6600 XT Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (AMD Radeon RX 6600 Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (AMD Radeon RX 5700 XT Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (AMD Radeon RX 5700 Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (AMD Radeon RX 5600 XT Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (AMD Radeon RX 5500 XT Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (AMD Radeon RX 580 Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (AMD Radeon RX 570 Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (AMD Radeon RX Vega 64 Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (AMD Radeon RX Vega 56 Direct3D11 vs_5_0 ps_5_0)",
    "Intel(R) UHD Graphics 770",
    "Intel(R) UHD Graphics 750",
    "Intel(R) UHD Graphics 730",
    "Intel(R) UHD Graphics 630",
    "Intel(R) UHD Graphics 620",
    "Intel(R) Iris(R) Xe Graphics",
    "Intel(R) Iris(R) Plus Graphics",
    "Mesa Intel(R) UHD Graphics 770 (ADL GT2)",
    "Mesa Intel(R) UHD Graphics 630 (CFL GT2)",
    "Mesa Intel(R) Iris(R) Xe Graphics (ADL GT2)",
    "Apple M3 Max",
    "Apple M3 Pro",
    "Apple M3",
    "Apple M2 Ultra",
    "Apple M2 Max",
    "Apple M2 Pro",
    "Apple M2",
    "Apple M1 Max",
    "Apple M1 Pro",
    "Apple M1",
    "AMD Radeon Pro W6800X",
    "AMD Radeon Pro W6600M",
    "AMD Radeon Pro 5700 XT",
    "AMD Radeon Pro 5700",
    "AMD Radeon Pro 5500M",
    "AMD Radeon Pro 580X",
    "AMD Radeon Pro 560X",
    "Adreno (TM) 740",
    "Adreno (TM) 730",
    "Adreno (TM) 660",
    "Adreno (TM) 650",
    "Mali-G712 MC11",
    "Mali-G710 MC10",
    "Mali-G610 MC6",
]

WEBGL_VENDORS = [
    "Google Inc. (NVIDIA)",
    "Google Inc. (AMD)",
    "Google Inc. (Intel)",
    "Google Inc. (Apple)",
    "Intel Inc.",
    "Apple",
    "ARM",
    "Qualcomm",
]

SCREEN_RESOLUTIONS = {
    "desktop": [(1920, 1080), (2560, 1440), (3840, 2160), (1366, 768), (1440, 900), (1680, 1050), (2560, 1600),
                (3440, 1440)],
    "laptop": [(1920, 1080), (1366, 768), (1440, 900), (2560, 1600), (2880, 1800), (3024, 1964)],
    "mobile": [(390, 844), (414, 896), (375, 812), (428, 926), (360, 800), (393, 873), (412, 915)],
}

TZ_OFFSETS = {
    "America/New_York": -5, "America/Chicago": -6, "America/Los_Angeles": -8,
    "America/Denver": -7, "America/Sao_Paulo": -3, "America/Fortaleza": -3,
    "Europe/London": 0, "Europe/Moscow": 3, "Europe/Berlin": 1,
    "Europe/Paris": 1, "Europe/Rome": 1, "Europe/Madrid": 1,
    "Europe/Warsaw": 1, "Europe/Stockholm": 1, "Europe/Amsterdam": 1,
    "Europe/Istanbul": 3, "Asia/Tokyo": 9, "Asia/Shanghai": 8,
    "Asia/Seoul": 9, "Asia/Yekaterinburg": 5, "Asia/Vladivostok": 10,
    "Asia/Samara": 4,
}


def show_banner():
    banner = Text()
    banner.append("\n", style="bold blue")
    banner.append("╔══════════════════════════════════════════════════════════╗\n", style="bold cyan")
    banner.append("║  🌐 Browser Fingerprint Generator                        ║\n", style="bold cyan")
    banner.append("║  Генератор фейковых отпечатков браузера                  ║\n", style="bold cyan")
    banner.append("╚══════════════════════════════════════════════════════════╝", style="bold cyan")
    banner.append("\n")
    console.print(Panel(banner, box=box.DOUBLE, border_style="bold blue"))


def select_option(options, title):
    console.print(f"\n[bold cyan]{title}[/bold cyan]")
    console.print("  [yellow]0[/yellow] - Случайно")
    for i, opt in enumerate(options, 1):
        console.print(f"  [yellow]{i}[/yellow] - {opt}")

    while True:
        try:
            choice = int(Prompt.ask("Выбор", default="0"))
            if choice == 0:
                return random.choice(options)
            if 1 <= choice <= len(options):
                return options[choice - 1]
            console.print("[red]❌ Неверный выбор[/red]")
        except ValueError:
            console.print("[red]❌ Введите число[/red]")


def generate_fingerprint(browser, os_name, location_key, device_type, screen_res=None):
    browser_data = BROWSERS[browser]
    os_data = OPERATING_SYSTEMS[os_name]
    location_data = os_data["locations"][location_key]

    version = random.choice(browser_data["versions"])
    user_agent = random.choice(browser_data["user_agents"]).format(version=version)

    if screen_res:
        width, height = screen_res
    else:
        width, height = random.choice(SCREEN_RESOLUTIONS[device_type])

    language = random.choice(location_data["languages"])
    timezone = random.choice(location_data["timezones"])
    tz_offset = TZ_OFFSETS.get(timezone, 0)

    webgl_renderer = random.choice(WEBGL_RENDERERS)
    webgl_vendor = random.choice(WEBGL_VENDORS)

    canvas_hash = uuid.uuid4().hex[:32]
    audio_hash = uuid.uuid4().hex[:16]

    common_fonts = ["Arial", "Times New Roman", "Courier New", "Georgia", "Verdana", "Helvetica", "Tahoma",
                    "Trebuchet MS", "Impact", "Comic Sans MS", "Palatino Linotype", "Segoe UI", "Roboto", "Open Sans",
                    "Lato"]
    locale_fonts = {
        "ru": ["Times New Roman", "Arial", "Calibri", "Cambria", "Consolas"],
        "zh": ["SimSun", "SimHei", "Microsoft YaHei"],
        "ja": ["MS UI Gothic", "MS PGothic", "Meiryo", "Yu Gothic"],
        "ko": ["Malgun Gothic", "Batang", "Dotum", "Gulim"],
    }
    lang_prefix = language.split("-")[0]
    fonts = common_fonts + locale_fonts.get(lang_prefix, [])
    fonts = random.sample(fonts, k=min(random.randint(10, 18), len(fonts)))

    if device_type == "mobile":
        touch_points = random.choice([2, 5, 10])
        pixel_ratio = random.choice([2, 2.5, 3, 3.5])
        connection_type = random.choice(["4g", "5g", "wifi"])
    else:
        touch_points = random.choice([0, 0, 0, 1, 2])
        pixel_ratio = random.choice([1, 1.25, 1.5, 2])
        connection_type = random.choice(["wifi", "ethernet"])

    is_apple = "Apple" in webgl_renderer or "M1" in webgl_renderer or "M2" in webgl_renderer or "M3" in webgl_renderer
    arch = "arm64" if is_apple else "x86_64"

    return {
        "id": str(uuid.uuid4()),
        "generated_at": datetime.now().isoformat() + "Z",
        "browser": {
            "name": browser.capitalize(),
            "version": version,
            "user_agent": user_agent,
            "plugins": browser_data["plugins"],
            "languages": [language, lang_prefix],
        },
        "os": {
            "name": os_name.capitalize(),
            "platform": random.choice(os_data["platforms"]),
            "architecture": arch,
        },
        "location": {
            "country": location_data["country"],
            "language": language,
            "timezone": timezone,
            "timezone_offset": tz_offset,
        },
        "screen": {
            "width": width,
            "height": height,
            "color_depth": random.choice([24, 32]),
            "pixel_ratio": pixel_ratio,
            "avail_width": width - random.randint(0, 20),
            "avail_height": height - random.randint(50, 100),
            "device_type": device_type,
        },
        "hardware": {
            "cores": random.choice([4, 6, 8, 12, 16]),
            "memory_gb": random.choice([4, 8, 12, 16, 32]),
            "touch_points": touch_points,
        },
        "webgl": {
            "renderer": webgl_renderer,
            "vendor": webgl_vendor,
            "version": "WebGL 2.0 (OpenGL ES 3.0 Chromium)",
        },
        "canvas": {"hash": canvas_hash, "winding": True},
        "audio": {"hash": audio_hash, "sample_rate": 44100, "channels": 2},
        "fonts": sorted(fonts),
        "privacy": {
            "do_not_track": random.choice([0, 1, None]),
            "cookies_enabled": random.choice([True, True, True, False]),
            "webdriver": False,
        },
        "network": {
            "connection_type": connection_type,
            "effective_type": random.choice(["4g", "5g", "3g"]),
            "downlink": random.choice([10, 50, 100, 500, 1000]),
            "rtt": random.choice([20, 50, 100, 200]),
        },
    }


def show_config_panel(browser, os_name, loc_data, device_type, screen_res, count, output_dir):
    config_text = Text()
    config_text.append("⚙️  Параметры генерации:\n\n", style="bold cyan")
    config_text.append("  🌐 Браузер:    ", style="bold")
    config_text.append(f"{browser.capitalize()}\n", style="yellow")
    config_text.append("  💻 ОС:         ", style="bold")
    config_text.append(f"{os_name.capitalize()}\n", style="yellow")
    config_text.append("  🌍 Локация:    ", style="bold")
    config_text.append(f"{loc_data['country']}\n", style="yellow")
    config_text.append("  🗣️  Язык:      ", style="bold")
    config_text.append(f"{', '.join(loc_data['languages'])}\n", style="yellow")
    config_text.append("  🕐 Timezone:   ", style="bold")
    config_text.append(f"{loc_data['timezones'][0]}\n", style="yellow")
    config_text.append("  📱 Устройство: ", style="bold")
    config_text.append(f"{device_type}\n", style="yellow")
    config_text.append("  📺 Разрешение: ", style="bold")
    config_text.append(f"{screen_res if screen_res else 'auto'}\n", style="yellow")
    config_text.append("  📊 Количество: ", style="bold")
    config_text.append(f"{count}\n", style="yellow")
    config_text.append("  📂 Директория: ", style="bold")
    config_text.append(f"{output_dir}\n", style="yellow")

    console.print(Panel(config_text, title="🎯 Конфигурация", border_style="green", box=box.ROUNDED))


def show_results_table(fingerprints, output_dir):
    table = Table(
        title="📊 Сгенерированные фингерпринты",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta",
        border_style="blue",
    )

    table.add_column("#", style="cyan", width=4)
    table.add_column("ID", style="green", width=10)
    table.add_column("Browser", style="yellow")
    table.add_column("OS", style="blue")
    table.add_column("Location", style="magenta")
    table.add_column("Timezone", style="red")
    table.add_column("Resolution", style="cyan")

    for i, fp in enumerate(fingerprints[:10], 1):
        table.add_row(
            str(i),
            fp["id"][:8],
            fp["browser"]["name"],
            fp["os"]["name"],
            fp["location"]["country"],
            fp["location"]["timezone"],
            f"{fp['screen']['width']}x{fp['screen']['height']}",
        )

    if len(fingerprints) > 10:
        table.add_row(
            "...",
            "...",
            "...",
            "...",
            "...",
            "...",
            f"+{len(fingerprints) - 10} more",
            style="dim",
        )

    console.print()
    console.print(table)
    console.print(f"\n[bold green]💾 Все файлы сохранены в:[/bold green] [cyan]{Path(output_dir).absolute()}[/cyan]")


def main():
    show_banner()

    while True:
        console.print("\n" + "=" * 50)
        console.print(" [bold cyan]1[/bold cyan] - Сгенерировать фингерпринты")
        console.print(" [bold red]0[/bold red] - Выход")
        console.print("=" * 50)

        try:
            choice = int(Prompt.ask("Выберите действие", default="1"))
        except ValueError:
            console.print("[red]❌ Введите число (0 или 1)[/red]")
            continue

        if choice == 0:
            console.print("\n[bold yellow]👋 Выход...[/bold yellow]")
            break
        elif choice == 1:
            browser = select_option(list(BROWSERS.keys()), "🌍 Браузер")
            os_name = select_option(list(OPERATING_SYSTEMS.keys()), "💻 Операционная система")

            locations = list(OPERATING_SYSTEMS[os_name]["locations"].keys())
            location_key = select_option(locations, f"🌐 Локация ({os_name})")
            loc_data = OPERATING_SYSTEMS[os_name]["locations"][location_key]

            console.print(
                f"\n[green]✓ Выбрано:[/green] {loc_data['country']} | {', '.join(loc_data['languages'])} | {loc_data['timezones'][0]}")

            device_type = select_option(["desktop", "laptop", "mobile"], "📱 Тип устройства")

            use_custom = Confirm.ask("\nКастомное разрешение?", default=False)
            screen_res = None
            if use_custom:
                while True:
                    res_in = Prompt.ask("Разрешение (WxH)", default="1920x1080")
                    try:
                        w, h = map(int, res_in.split("x"))
                        screen_res = (w, h)
                        break
                    except ValueError:
                        console.print("[red]❌ Формат: 1920x1080[/red]")

            count = IntPrompt.ask("\n📊 Количество", default=10)
            output_dir = Prompt.ask("📁 Директория", default="./fingerprints")

            show_config_panel(browser, os_name, loc_data, device_type, screen_res, count, output_dir)

            if not Confirm.ask("🚀 Начать генерацию?", default=True):
                console.print("[yellow]⚠️  Отменено[/yellow]")
                continue

            Path(output_dir).mkdir(parents=True, exist_ok=True)

            fingerprints = []

            with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(bar_width=40),
                    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                    TextColumn("[dim]•[/dim]"),
                    TextColumn("[dim]{task.completed}/{task.total}[/dim]"),
                    console=console,
            ) as progress:
                task = progress.add_task(f"[cyan]🔨 Генерация {count} фингерпринтов...", total=count)

                for i in range(count):
                    fp = generate_fingerprint(browser, os_name, location_key, device_type, screen_res)
                    filename = f"fingerprint_{fp['id'][:12]}.json"
                    filepath = Path(output_dir) / filename

                    with open(filepath, "w", encoding="utf-8") as f:
                        json.dump(fp, f, indent=2, ensure_ascii=False)

                    fingerprints.append(fp)
                    progress.update(task, advance=1)

            show_results_table(fingerprints, output_dir)

            success_panel = Panel(
                f"[bold green]✅ Успешно сгенерировано {count} фингерпринтов![/bold green]\n\n"
                f"📂 Директория: [cyan]{Path(output_dir).absolute()}[/cyan]\n"
                f"📄 Формат: JSON\n"
                f"🎲 Уникальных ID: {len(set(fp['id'] for fp in fingerprints))}\n"
                f"🌍 Локация: {loc_data['country']}\n"
                f"🕐 Timezones: {', '.join(loc_data['timezones'])}",
                title="🎉 Готово!",
                border_style="green",
                box=box.DOUBLE,
            )
            console.print(success_panel)
        else:
            console.print("[red]❌ Неверный выбор. Введите 0 или 1[/red]")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Прервано пользователем[/yellow]")