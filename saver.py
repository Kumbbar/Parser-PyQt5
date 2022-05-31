from bs4 import BeautifulSoup
import requests
from settings import UserSettings
import json


class ParsingSaver:
    def __init__(self, user_settings: UserSettings, url: str):
        self.user_settings = user_settings
        self.url = url
        self.status_code = 404
        self.html = ''

    def get_status_code(self, headers: dict) -> int:
        self.status_code = requests.head(self.url, headers=headers).status_code
        return self.status_code

    def get_html(self) -> str:
        self.html = requests.get(self.url).text
        return self.html

    def save_html(self) -> None:
        with open(f'{self.user_settings.absolute_path}\\{self.user_settings.filename}.html', 'w', encoding='utf-8') as file:
            file.write(self.html)

    def save_json(self, tag_or_class: str) -> None:
        beautiful_soup = BeautifulSoup(self.html, 'html.parser')
        json_data = []
        if ' ' in tag_or_class:
            first_space_index = tag_or_class.find(' ')
            tag_or_class = f'{tag_or_class[:first_space_index]}*{tag_or_class[first_space_index + 1:]}'.split('*')
            find_all = beautiful_soup.find_all(tag_or_class[0], {'class': tag_or_class[1]})
        else:
            find_all = beautiful_soup.find_all(tag_or_class)

        for item in find_all:
            json_data.append(
                {
                    item.title,
                    item.text
                }
            )
        with open(f'{self.user_settings.absolute_path}\\{self.user_settings.filename}.json', 'w', encoding='utf-8') as file:
            json.dump(json_data, file, indent=4, ensure_ascii=False)


