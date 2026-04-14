import base64
import os

# Найди последний файл в папке sent_emails
email_folder = 'sent_emails'
files = [f for f in os.listdir(email_folder) if f.endswith('.log')]
if files:
    latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(email_folder, x)))
    with open(os.path.join(email_folder, latest_file), 'r', encoding='utf-8') as f:
        content = f.read()

    # Ищем base64 строку
    lines = content.split('\n')
    for line in lines:
        if len(line) > 100 and not line.startswith('From') and not line.startswith('To') and not line.startswith(
                'Subject'):
            try:
                decoded = base64.b64decode(line).decode('utf-8')
                print("=" * 50)
                print("ДЕКОДИРОВАННОЕ ПИСЬМО:")
                print("=" * 50)
                print(decoded)

                # Находим ссылку
                import re

                links = re.findall(r'http[s]?://[^\s]+', decoded)
                if links:
                    print("\n" + "=" * 50)
                    print("ССЫЛКА ДЛЯ ВОССТАНОВЛЕНИЯ:")
                    print("=" * 50)
                    print(links[0])
            except:
                pass