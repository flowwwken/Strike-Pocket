# -*- coding: utf-8 -*-
"""
Модуль безопасности веб-сервиса «Strike & Pocket».
Занятие 15: Проверки безопасности и средства защиты.
1. Валидация загружаемых файлов (MIME, расширения, защита от двойных расширений, лимит размера).
2. Защита от перебора паролей (Brute-force protection middleware).
"""

import os
import time
from django.core.exceptions import ValidationError
from django.http import HttpResponse

# Разрешенные типы файлов и расширения
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.pdf'}
FORBIDDEN_EXTENSIONS = {'.php', '.phtml', '.exe', '.sh', '.py', '.bat', '.cmd', '.js', '.vbs', '.msi'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 МБ

# Сигнатуры (magic numbers) для проверки типа контента
FILE_SIGNATURES = {
    'jpeg': b'\xFF\xD8\xFF',
    'png': b'\x89PNG\r\n\x1a\n',
    'webp': b'RIFF',
    'pdf': b'%PDF'
}


def validate_safe_file_upload(file_obj):
    """
    Комплексная проверка безопасности загружаемого файла:
    1. Проверка размера файла (<= 10 МБ).
    2. Проверка расширения (запрет исполняемых файлов .php, .exe и др.).
    3. Защита от двойных расширений (например, shell.php.png).
    4. Проверка сигнатуры файла (magic bytes).
    """
    if not file_obj:
        return

    # 1. Проверка размера
    if file_obj.size > MAX_FILE_SIZE:
        raise ValidationError(f"Размер файла ({file_obj.size / 1024 / 1024:.2f} МБ) превышает лимит 10 МБ.")

    name = file_obj.name.lower()

    # 2. Защита от двойных расширений
    parts = name.split('.')
    if len(parts) > 2:
        for p in parts[1:-1]:
            if f".{p}" in FORBIDDEN_EXTENSIONS:
                raise ValidationError(f"Обнаружено потенциально опасное двойное расширение: '.{p}'. Загрузка заблокирована.")

    # 3. Проверка конечного расширения
    ext = os.path.splitext(name)[1]
    if ext in FORBIDDEN_EXTENSIONS:
        raise ValidationError(f"Загрузка файлов с расширением '{ext}' строго запрещена из соображений безопасности.")

    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(f"Недопустимый тип файла '{ext}'. Разрешены только: {', '.join(sorted(ALLOWED_EXTENSIONS))}.")

    # 4. Проверка сигнатуры (magic bytes)
    initial_pos = file_obj.tell()
    header = file_obj.read(16)
    file_obj.seek(initial_pos)

    is_valid_magic = False
    if ext in ['.jpg', '.jpeg'] and header.startswith(FILE_SIGNATURES['jpeg']):
        is_valid_magic = True
    elif ext == '.png' and header.startswith(FILE_SIGNATURES['png']):
        is_valid_magic = True
    elif ext == '.webp' and FILE_SIGNATURES['webp'] in header:
        is_valid_magic = True
    elif ext == '.pdf' and header.startswith(FILE_SIGNATURES['pdf']):
        is_valid_magic = True

    if not is_valid_magic:
        raise ValidationError("Содержимое файла не соответствует заявленному расширению (неверная сигнатура magic bytes).")


# Память для счетчика попыток входа (IP -> [timestamp, count])
LOGIN_ATTEMPTS = {}
MAX_ATTEMPTS = 5
LOCKOUT_DURATION = 300  # 5 минут


class BruteForceProtectionMiddleware:
    """
    Middleware для защиты от атак методом подбора паролей (Brute-Force).
    Ограничивает количество неуспешных попыток входа до 5 в течение 5 минут на один IP-адрес.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/login/') and request.method == 'POST':
            ip = self.get_client_ip(request)
            now = time.time()

            record = LOGIN_ATTEMPTS.get(ip)
            if record:
                first_attempt_time, count = record
                if now - first_attempt_time < LOCKOUT_DURATION:
                    if count >= MAX_ATTEMPTS:
                        remaining = int(LOCKOUT_DURATION - (now - first_attempt_time))
                        return HttpResponse(
                            f"<h1>429 Слишком много запросов</h1>"
                            f"<p>Превышено допустимое количество попыток входа ({MAX_ATTEMPTS}). "
                            f"Ваш IP-адрес временно заблокирован на {remaining} сек. "
                            f"(Защита от подбора паролей OWASP A07).</p>",
                            status=429
                        )
                else:
                    # Сброс окна времени
                    LOGIN_ATTEMPTS[ip] = [now, 0]

            response = self.get_response(request)

            # Если после POST пользователь остался неавторизован (неуспешный вход)
            if response.status_code == 200:
                rec = LOGIN_ATTEMPTS.setdefault(ip, [now, 0])
                rec[1] += 1
            elif response.status_code == 302 and request.user.is_authenticated:
                # Успешный вход — сбрасываем счетчик
                LOGIN_ATTEMPTS.pop(ip, None)

            return response

        return self.get_response(request)

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
        return ip
