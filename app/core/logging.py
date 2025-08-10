# logging.py

import logging

def setup_logging(level: int = logging.INFO) -> None:
    # Инициализируется один раз при старте приложения
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True,  # перезапишет базовую конфигурацию, если что-то настроено раньше
    )