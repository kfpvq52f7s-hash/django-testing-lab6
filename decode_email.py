import base64
import os
import re

# Найди последний файл в папке sent_emails
email_folder = 'sent_emails'

if not os.path.exists(email_folder):
    print(f"Папка {email_folder} не найдена!")
    exit()

files = [f for f in os.listdir(email_folder) if f.endswith('.log')]

if not files:
    print("Нет файлов с письмами в папке sent_emails")
    exit()

latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(email_folder, x)))
print(f"Читаем файл: {latest_file}")

with open(os.path.join(email_folder, latest_file), 'r', encoding='utf-8') as f:
    content = f.read()

# Ищем base64 строку (длинную строку символов)
lines = content.split('\n')
for line in lines:
    # Если строка длинная и не похожа на заголовок
    if len(line) > 100 and not line.startswith('From') and not line.startswith('To') and not line.startswith('Subject') and not line.startswith('Date') and not line.startswith('MIME') and not line.startswith('Content'):
        try:
            decoded = base64.b64decode(line).decode('utf-8')
            print("\n" + "=" * 50)
            print("ССЫЛКА ДЛЯ ВОССТАНОВЛЕНИЯ ПАРОЛЯ:")
            print("=" * 50)
            
            # Находим ссылку
            links = re.findall(r'http[s]?://[^\s]+', decoded)
            if links:
                print(links[0])
            else:
                print(decoded)
            break
        except:
            pass