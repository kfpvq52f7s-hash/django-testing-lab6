import base64
from django.core.mail.backends.filebased import EmailBackend


class ReadableEmailBackend(EmailBackend):
    def _write_message(self, message):
        # Get the email body
        payload = message.body()

        # Try to decode base64
        try:
            if isinstance(payload, bytes):
                decoded = base64.b64decode(payload).decode('utf-8')
                payload = decoded
            elif isinstance(payload, str) and len(payload) > 50:
                decoded = base64.b64decode(payload).decode('utf-8')
                payload = decoded
        except:
            pass  # If not base64, leave as is

        # Save email in readable format
        email_data = f"""
From: {message.from_email}
To: {', '.join(message.to)}
Subject: {message.subject()}
Date: {message.date()}

{payload}
"""
        self.stream.write(email_data)
        self.stream.write('\n' + '-' * 79 + '\n')