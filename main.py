import click
import sys
import random
import requests
from faker import Faker
fake = Faker('ja_JP')

geolonia_api_base = 'https://geolonia.github.io/japanese-addresses/api'
prefectures = requests.get(f'{geolonia_api_base}/ja.json').json()
prefecture_choices = list(prefectures.keys())
address_details = {}


@click.command()
@click.option("--count", default=1, help="挨拶の回数")
@click.option("--name", prompt="名前を入力してください", help="挨拶する相手")
def hello(count, name):
    """NAMEに合計COUNT回挨拶するシンプルなプログラム。"""
    for _ in range(count):
        click.echo(f"こんにちは, {name}!")
    for _ in range(100):
        address = random_address_jp()
        print(address)


def random_address_jp():
    prefecture = random.choice(prefecture_choices)
    cities = prefectures[prefecture]
    city = cities[random.randrange(0, len(cities) - 1)]

    if prefecture not in address_details or city not in address_details[prefecture]:
        url = f'{geolonia_api_base}/ja/{prefecture}/{city}.json'
        new_entry = requests.get(url).json()
        if prefecture not in address_details:
            address_details[prefecture] = {}

        address_details[prefecture][city] = new_entry

    towns = address_details[prefecture][city]
    town = towns[random.randrange(0, len(towns))]['town']
    koaza = towns[random.randrange(0, len(towns))]['koaza']
    ban = fake.ban()
    gou = fake.gou()

    return f'{prefecture}{city}{town}{koaza}{ban}{gou}'


if __name__ == '__main__':
    hello()
