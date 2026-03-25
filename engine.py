import psutil
from datetime import datetime
import time
import platform
import socket
import sys
import os
from pathlib import Path


def cpu_infos():
    global core
    global frequency
    global cpu_usage
    core = psutil.cpu_count(())
    print(f"Nombre de coeurs: {core}")
    frequency = psutil.cpu_freq(())
    print("Fréquence du CPU: ", frequency.max)
    cpu_usage = psutil.cpu_percent(interval=1)
    print(f"Pourcentage d'utilisation du CPU: {cpu_usage}%")


def memory_infos():
    global ram
    global ram_usedformat
    global ram_totalformat
    global rampourcentformat
    ram = psutil.virtual_memory()

    ram_used1 = ram.used / (1024**3)
    ram_usedformat = f"{ram_used1:.2f}"

    ram_total1 = ram.total / (1024**3)
    ram_totalformat = f"{ram_total1:.2f}"

    rampourcent = ram.active / ram.total * 100
    rampourcentformat = f"{rampourcent:.2f}"

    print(f"RAM utilisée en Gb: {ram_usedformat} GB")
    print("RAM totale: ", ram_total1, "GB")
    print("Pourcentage d'utilisation de la RAM: ", rampourcent, "GB")
