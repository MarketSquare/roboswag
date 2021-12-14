import re


def pythonify_name(name: str) -> str:
    names = re.sub("([A-Z][a-z]+)", r" \1", re.sub("([A-Z]+)", r" \1", name)).split()
    name = "_".join(name.lower() for name in names)
    name = name.replace("-", "")
    return name
