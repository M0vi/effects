import requests
import random
import string
import time

def generate_random_email():
    random_email = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + "@example.com"
    return random_email

def check_username_availability(username):
    get_url = "https://www.instagram.com/accounts/web_create_ajax/attempt/"
    session = requests.Session()
    response = session.get(get_url)
    csrftoken = session.cookies.get('csrftoken')

    if not csrftoken:
        print("Erro ao obter csrftoken.")
        return

    headers = {
        'Referer': 'https://www.instagram.com/',
        'X-CSRFToken': csrftoken
    }

    data = {
        'email': generate_random_email(),
        'password': 'strongPassword123!',
        'username': username,
        'first_name': '',
    }

    post_url = "https://www.instagram.com/accounts/web_create_ajax/attempt/"
    post_response = session.post(post_url, headers=headers, data=data)

    if post_response.status_code == 200:
        response_json = post_response.json()
        if 'errors' in response_json and 'username' in response_json['errors']:
            print(f"Nome de usuário '{username}' não disponível.")
        else:
            print(f"Nome de usuário '{username}' está disponível.")
    else:
        print(f"Erro ao verificar o nome de usuário. Status code: {post_response.status_code}")

def check_usernames_from_file():
    with open("usernames.txt", "r") as file:
        usernames = [line.strip() for line in file.readlines()]

    for username in usernames:
        check_username_availability(username)
        time.sleep(2)

check_usernames_from_file()
