import requests
import threading
import time
from colorama import Fore, init

# Inicializa o Colorama
init(autoreset=True)
purple = Fore.MAGENTA
white = Fore.WHITE
green = Fore.GREEN
red = Fore.RED

# Exibir título
print(f""" {purple}
      ______        __    
 ___ / _/ _/__ ____/ /____
/ -_) _/ _/ -_) __/ __(_-<
\__/_//_/ \__/\__/\__/___/ {white}usrnm chckr by @kl666v <3
{purple}.  .::.  .
 """)

# Definir número de threads
threads = int(input(f"{purple}threads{white}: "))

def split_list(alist, wanted_parts=1):
    """ Divide a lista de usuários em partes para threading """
    return [alist[i * len(alist) // wanted_parts: (i + 1) * len(alist) // wanted_parts] for i in range(wanted_parts)]

def check_usernames(usernames):
    """ Função para verificar disponibilidade de usernames """
    for username in usernames:
        url = f"https://www.instagram.com/{username}/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)

            if "Sorry, this page isn't available." in response.text:
                print(f"{green}{username}{white} is NOT taken")
                with open("available.txt", 'a') as f:
                    f.write(f"{username}\n")

            else:
                print(f"{red}{username}{white} is TAKEN")

        except requests.exceptions.RequestException as e:
            print(f"{red}Error checking {username}: {e}")

        time.sleep(1)  # Adiciona um pequeno delay para evitar bloqueio

# Ler nomes de usuário do arquivo
usernames = [line.strip() for line in open("usernames.txt")]

# Dividir a lista de usuários em partes iguais para threads
user_chunks = split_list(usernames, threads)

# Iniciar as threads
for chunk in user_chunks:
    threading.Thread(target=check_usernames, args=(chunk,)).start()
