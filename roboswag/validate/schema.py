import json
from pathlib import Path
from typing import Dict, Union

import jsonschema


class ValidateSchema:
    @staticmethod
    def schema(response, schema: Union[str, Path, Dict]):
        if isinstance(schema, (str, Path)):
            with open(schema) as fp:
                schema = json.load(fp)
        try:
            jsonschema.validate(instance=response.json(), schema=schema)
        except jsonschema.exceptions.ValidationError as err:
            raise err
