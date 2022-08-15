from typing import List

from roboswag.generate.models.endpoint import Endpoint
from roboswag.generate.models.utils import pythonify_name


class Tag:
    def __init__(self, name: str, description: str = "") -> None:
        # tag is grouped paths/endpoints
        self.name: str = pythonify_name(name, join_mark="", join_fn="title")
        self.description: str = description
        self.endpoints: List[Endpoint] = []

    @staticmethod
    def normalize_tag_name(tag_name: str) -> str:
        return tag_name.strip(" -_").title() + "API"
