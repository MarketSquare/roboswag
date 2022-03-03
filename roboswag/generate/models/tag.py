from typing import List

from roboswag.generate.models.endpoint import Endpoint


class Tag:
    def __init__(self, name: str, description: str = None) -> None:
        # tag is grouped paths/endpoints
        self.name: str = name
        self.description: str = description
        self.endpoints: List[Endpoint] = []

    @staticmethod
    def normalize_tag_name(tag_name: str) -> str:
        return tag_name.strip(" -_").title() + "API"
