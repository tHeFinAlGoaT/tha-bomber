from bomber import Bomber
from bomber import Stats
from rich import print

bomber = Bomber()
bomber.start()
print(f"[green]Sent: {Stats.sent}   [red]Failed: {Stats.failed}")
 