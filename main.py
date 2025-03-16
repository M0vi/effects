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
    """ Verifica usernames extraindo dados do HTML da página """
    for username in usernames:
        url = f"https://www.instagram.com/{username}/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)

            # Se o status for 404, o usuário não existe
            if response.status_code == 404:
                print(f"{green}{username}{white} is NOT taken")
                with open("available.txt", 'a') as f:
                    f.write(f"{username}\n")
                continue  # Pula para o próximo usuário

            # Se o status for 200, procuramos no JSON se o perfil existe
            if response.status_code == 200:
                if check_if_profile_exists(response.text):
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

def check_if_profile_exists(page_content):
    """ Verifica se o perfil existe com base no conteúdo da página (JSON embutido) """
    start = page_content.find("window._sharedData = ")
    if start == -1:
        return False  # Não encontrou o JSON

    start += len("window._sharedData = ")
    end = page_content.find(";</script>", start)
    if end == -1:
        return False  # Não encontrou o final do JSON

    json_text = page_content[start:end].strip()
    try:
        data = json.loads(json_text)
        # Verifique se o "user" está presente
        return 'user' in data.get('entry_data', {}).get('ProfilePage', [{}])[0]
    except json.JSONDecodeError:
        return False  # Se o JSON estiver corrompido ou mal formatado

# Ler nomes de usuário do arquivo
usernames = [line.strip() for line in open("usernames.txt")]

# Dividir a lista de usuários em partes iguais para threads
user_chunks = split_list(usernames, threads)

# Iniciar as threads
for chunk in user_chunks:
    threading.Thread(target=check_usernames, args=(chunk,)).start()
