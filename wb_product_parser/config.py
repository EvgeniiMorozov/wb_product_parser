HEADERS = {
    "user agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like"
        " Gecko) Chrome/92.0.4515.131 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
}

HOST = "https://www.wildberries.ru"
HTTPS_PREF = "https:"

phone_spec_pattern = {
    "Операционная система": "operating_system",
    "Модель": "model",
    "Гарантийный срок": "guarantee",
    "Тип дисплея/экрана": "display_type",
    "Диагональ экрана": "screen_diagonal",
    "Разрешение экрана": "screen_resolution",
    "Процессор": "cpu",
    "Объем встроенной памяти (Гб)": "ROM_size",
    "Объем оперативной памяти (Гб)": "RAM_size",
    "Емкость аккумулятора": "battery_capacity",
    "Количество мп основной камеры": "main_camera_resolution"
}

notebook_spec_pattern = {
    "Операционная система": "operating_system",
    "Модель": "model",
    "Гарантийный срок": "guarantee",
    "Тип дисплея/экрана": "display_type",
    "Диагональ экрана": "screen_diagonal",
    "Разрешение экрана": "screen_resolution",
    "Тип матрицы": "matrix_type",
    "Процессор": "cpu",
    "Количество ядер процессора": "cpu_cores",
    "Тактовая частота процессора": "cpu_clock_speed",
    "Объем встроенной памяти (Гб)": "ROM_size",
    "Объем накопителя SSD": "SSD_ROM_size",
    "Объем накопителя HDD": "HDD_ROM_size",
    "Объем оперативной памяти (Гб)": "RAM_size",
}

phone_local_path_pref = 'source/phones/'
notebook_local_path_pref = 'source/notebooks/'
