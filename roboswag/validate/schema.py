import json
from pathlib import Path
from typing import Dict, Union

import jsonschema

from roboswag.validate.core import Validate


class ValidateSchema(Validate):
    def schema(self, response, schema: Union[str, Path, Dict]):
        self.logger.info("Validating schema...")
        if isinstance(schema, (str, Path)):
            with open(schema) as fp:
                schema = json.load(fp)
        self.logger.debug(f"Schema:\n{json.dumps(schema, indent=4)}")
        try:
            jsonschema.validate(instance=response.json(), schema=schema)
        except jsonschema.exceptions.ValidationError as err:
            raise err
        self.logger.info("Schema is valid.")
