import datetime
import inspect
import json

import numpy as np


class ObjMapperConfig(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, datetime.date):
            return str(obj)
        elif inspect.isfunction(obj) or inspect.ismethod(obj):
            return str(obj)
        elif isinstance(obj, Exception):
            return type(obj).__name__
        else:
            return super(ObjMapperConfig, self).default(obj)

    def coerce_to_strict(self, const):
        invalid_parameters = ('Infinity', '-Infinity', 'NaN', None)
        if const in invalid_parameters:
            return "inf"
        else:
            return const

    # overload encoder to replace “Infinity”
    def encode(self, obj):
        """
        1. `loads` to switch Infinity, -Infinity, NaN to None
        2. `dumps` again, so you get 'null' instead of extended JSON
        """
        encoded_object = super(ObjMapperConfig, self).encode(obj)
        try:
            new_o = json.loads(encoded_object, parse_constant=self.coerce_to_strict)
        except ValueError:
            raise ValueError("Encoding into strict JSON failed.")
        else:
            return json.dumps(
                new_o,
                sort_keys=self.sort_keys,
                indent=self.indent,
                separators=(
                    self.item_separator,
                    self.key_separator
                )
            )
