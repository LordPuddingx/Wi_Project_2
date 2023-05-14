from email.message import EmailMessage
import ssl
import smtplib

sender = "TransportunternehmenX@gmail.com"
pw = "kcbdxkgklbholunt"

subject = "Sie haben sich erfolgreich bei Transportunternehmen X registriert!"
text = """
Liebe*r Kund*in,

Sie haben sich soeben mit ihrer E-Mail-Adresse auf unserer Website registriert: http://127.0.0.1:5000/.

Sollte es sich dabei um einen Fehler handeln, kontaktieren Sie uns bitte umgehend.

Beste Grüße

Ihr Transportunternehmen X

"""

def write_mail(receiver):
    mail = EmailMessage()
    mail["From"] = sender
    mail["To"] = receiver
    mail["Subject"] = subject
    mail.set_content(text)

    encryption = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context = encryption) as smtp:
        smtp.login(sender, pw)
        smtp.sendmail(sender, receiver, mail.as_string())
