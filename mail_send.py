import smtplib
from email.mime.text import MIMEText


def send_email(user_name, totem_animal):
    sender = "nicyash@mail.ru"
    password = "wsp9kXzyCbP6YmtSXrJx"
    server = smtplib.SMTP('smtp.mail.ru', 25)
    server.starttls()

    try:
        server.login(sender, password)
        text = (f"Пользователь {user_name}, у которого тотемное животное {totem_animal}"
                f" хочет узнать больше про программу опеки.")
        msg = MIMEText(text)
        msg["Subject"] = user_name
        server.sendmail(sender, sender, msg.as_string())

        return "The message was sent successfully!"
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"


def main():
    user_name = input('Ведите имя: ')
    totem_animal = input('Ведите животное: ')
    send_email(user_name, totem_animal)


if __name__ == "__main__":
    main()
