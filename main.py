import time
import yaml
import os
from mail import SendEmail
from icbc import Location, ICBC


class Config:
    def __init__(self):
        with open('./config.yml', 'r') as file:
            conf = yaml.safe_load(file)
            self.start_date = conf['start_date']
            self.end_date = conf['end_date']
            self.sleep_duration = conf['sleep_duration']
            self.locations = []
            for loc in conf['Location']:
                self.locations.append(Location(loc['pos_id'], loc['exam_type'], loc['exam_date'], loc['prf_days_of_week'], loc['prf_parts_of_day']))


def send_to_mail(content):
    SendEmail(content, os.environ["MAIL_SENDER_ADDRESS"], os.environ["MAIL_SENDER_PASS"], os.environ["MAIL_RECEIVER_ADDRESS"])


def main():
    cfg = Config()

    icbc_cli = ICBC(os.environ["ICBC_KEYWORD"], os.environ["ICBC_LAST_NAME"], os.environ["ICBC_NUM"])
    icbc_cli.login()
    if cfg.sleep_duration != 0:
        time.sleep(cfg.sleep_duration)

    available_appointments = None
    for loc in cfg.locations:
        available_appointments = icbc_cli.get_available_appointments(loc)

    content = ""
    for appointment in available_appointments:
        content += f"<li>{appointment}</li>"
    send_to_mail(content)


if __name__ == '__main__':
    main()
