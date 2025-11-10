import imaplib
import smtplib
import email
import os
from email.mime.text import MIMEText
from email.header import decode_header


INBOX_EMAIL    = "pmedina@sagulpa.com"
INBOX_PASSWORD = os.getenv("INBOX_PASSWORD")


def get_new_mail():
    """ 
    Filtra la bandeja de correo para obtener nuevos correos de los remitentes permitidos.
    Devuelve un diccionario con claves que son los nombres de los archivos adjuntos y valores que son el contenido.
    """

    ALLOWED_SENDERS = [
        "pmedina",
        "jmunoz",
        "jgonzalez",
        "javieracosta",
        "maricarmensuarez",
        "aparcamientos",
        "debora",  # ! ?    
        "frfranco" # ! ?
    ]

    attachments = {}

    print("Conectando al servidor de correo...")

    # Conectar al servidor IMAP
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(INBOX_EMAIL, INBOX_PASSWORD)
    mail.select("inbox")

    print("Buscando correos nuevos...")

    for sender in ALLOWED_SENDERS:

        print(f'Procesando remitente: {sender}')
        
        # Buscar correos no leídos de cada remitente
        status, messages = mail.search(None, f'(SEEN FROM "{sender}@sagulpa.com")')
        if status != "OK": continue

        # Para cada uno de los correos encontrados:
        for mail_id in messages[0].split():
            
            # Obtener el correo completo
            status, data = mail.fetch(mail_id, "(RFC822)")
            if status != "OK": continue
            msg = email.message_from_bytes(data[0][1])
            
            # Extraer los archivos adjuntos
            for part in msg.walk():
                if part.get_content_maintype() == "multipart": continue
                if part.get("Content-Disposition") is None:    continue
                filename = part.get_filename()
                filename_utf = email.header.decode_header(filename)
                print(f"ARCHIVO ADJUNTO ENCONTRADO: {filename_utf}")
                # if filename:
                #     # Decodificar correctamente nombres codificados en MIME
                #     decoded_filename, charset = decode_header(filename)[0]
                #     if isinstance(decoded_filename, bytes):
                #         decoded_filename = decoded_filename.decode(charset or "utf-8")
                #         # print(f"NOMBRE DEL ARCHIVO: {decoded_filename}")
                #     attachments[decoded_filename] = part.get_payload(decode=True)

    mail.logout()

    return attachments

def send_email(to, subject, body):

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "<oficinadato@sagulpa.com>"
    msg["To"] = f"{to}@sagulpa.com"

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(INBOX_EMAIL, INBOX_PASSWORD)
        server.sendmail(INBOX_EMAIL, [msg["To"]], msg.as_string())

def notify_warning(missing_files):

    for recipient, files in missing_files.items():

        if len(files) > 1:
            body = f"Mensaje generado automáticamente.\nRecuerda mandar los siguientes ficheros a {INBOX_EMAIL} antes del día 15:\n"
            for f in files: body += f"\n• {'.'.join(f.split('.')[-2:])}"
        else:
            body = f"Mensaje generado automáticamente.\nRecuerda mandar el siguiente fichero a {INBOX_EMAIL} antes del día 15:\n"
            body += f"\n• {'.'.join(files[0].split('.')[-2:])}"

        send_email(to=recipient, subject="⚠️ Archivos faltantes", body=body)        
