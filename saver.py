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
        """Get status code, must be called for check connection and update status code by default"""
        self.status_code = requests.head(self.url, headers=headers).status_code
        return self.status_code

    def get_html(self, headers: dict) -> str:
        """Get html page to var and self"""
        self.html = requests.get(self.url, headers=headers).text
        return self.html

    def save_html(self) -> None:
        """Save page to html file"""
        with open(f'{self.user_settings.absolute_path}\\{self.user_settings.filename}.html', 'w', encoding='utf-8') \
                as file:
            file.write(self.html)

    def save_json(self, tag_or_class: str) -> None:
        """Get string with tag and optional classname and save data to json"""
        beautiful_soup = BeautifulSoup(self.html, 'html.parser')
        json_data = []
        if ' ' in tag_or_class:
            # Search by tag and classname (space is replaced by * because classname can contain spaces)
            first_space_index = tag_or_class.find(' ')
            tag_or_class = f'{tag_or_class[:first_space_index]}*{tag_or_class[first_space_index + 1:]}'.split('*')
            find_all = beautiful_soup.find_all(tag_or_class[0], {'class': tag_or_class[1]})
            for item in find_all:
                json_data.append(
                    {
                        tag_or_class[0]: item.text
                    }
                )
        else:
            # Search by tag with data
            find_all = beautiful_soup.find_all(tag_or_class)
            for item in find_all:
                json_data.append(
                    {
                        tag_or_class: item.text
                    }
                )
        with open(f'{self.user_settings.absolute_path}\\{self.user_settings.filename}.json', 'w', encoding='utf-8') \
                as file:
            json.dump(json_data, file, indent=4, ensure_ascii=False)
