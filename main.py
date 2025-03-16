import requests
import threading
import time
import json
from colorama import Fore, init

# Inicializa o Colorama para colorir o terminal
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
    """ Verifica usernames extraindo JSON do HTML da página """
    for username in usernames:
        url = f"https://www.instagram.com/{username}/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 404:
                print(f"{green}{username}{white} is NOT taken")
                with open("available.txt", 'a') as f:
                    f.write(f"{username}\n")
                continue  # Pula para o próximo usuário

            if response.status_code == 200:
                # Extrai JSON da página
                json_data = extract_json(response.text)

                if json_data and json_data.get("entry_data"):
                    print(f"{red}{username}{white} is TAKEN")
                else:
                    print(f"{green}{username}{white} is NOT taken")
                    with open("available.txt", 'a') as f:
                        f.write(f"{username}\n")
            else:
                print(f"{red}x {white} Unknown error for {username} [Status code {response.status_code}]")

        except requests.exceptions.RequestException as e:
            print(f"{red}Error checking {username}: {e}")

        time.sleep(1)  # Pequeno delay para evitar bloqueios

def extract_json(html):
    """ Extrai JSON embutido na página do Instagram """
    start = html.find("window._sharedData = ")
    if start == -1:
        return None  # JSON não encontrado

    start += len("window._sharedData = ")
    end = html.find(";</script>", start)
    if end == -1:
        return None  # JSON não encontrado

    json_text = html[start:end].strip()
    try:
        return json.loads(json_text)
    except json.JSONDecodeError:
        return None  # JSON inválido

# Ler nomes de usuário do arquivo
usernames = [line.strip() for line in open("usernames.txt")]

# Dividir a lista de usuários em partes iguais para threads
user_chunks = split_list(usernames, threads)

# Iniciar as threads
for chunk in user_chunks:
    threading.Thread(target=check_usernames, args=(chunk,)).start()
