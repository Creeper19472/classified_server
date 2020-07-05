# -*- coding: UTF-8 -*-

from colorama import init, Fore, Back, Style
init(autoreset=True)

class Colset(object):
    def Red(self, s):
        return Fore.RED + s + Fore.RESET
 
    def Green(self, s):
        return Fore.GREEN + s + Fore.RESET
 
    def Yellow(self, s):
        return Fore.YELLOW + s + Fore.RESET
 
    def Blue(self, s):
        return Fore.BLUE + s + Fore.RESET
 
    def Magenta(self, s):
        return Fore.MAGENTA + s + Fore.RESET
 
    def Cyan(self, s):
        return Fore.CYAN + s + Fore.RESET
 
    def White(self, s):
        return Fore.WHITE + s + Fore.RESET
 
    def Black(self, s):
        return Fore.BLACK
