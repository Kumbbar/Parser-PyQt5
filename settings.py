from dataclasses import dataclass


@dataclass
class UserSettings:
    absolute_path: str
    filename: str
    create_json: bool



