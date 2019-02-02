from colorama import init
from colorama import Fore, Back, Style
init()

def sprint(msg):
    print(Fore.GREEN + msg + Style.RESET_ALL)
    Style.RESET_ALL

def fprint(msg):
    print(Fore.RED + msg + Style.RESET_ALL)
    