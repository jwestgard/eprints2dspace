import re
import requests
from .mapping import fields
from .mapping import defaults


def parse_source(path):
    result = {}
    with open(path, 'r') as handle:
        lines = [line.strip() for line in handle.readlines()]
    for line in lines:
        if line is not '':
            key, value = tuple(line.split(': ', 1))
            if not key in result:
                result[key] = [value.strip()]
            else:
                result[key].append(value.strip())
    return result


def transform(path):

    eprint = parse_source(path)
    result = {}

    for field in fields:
        src_value = eprint.get(field['source'], '')
        dest_key  = field.get('destination')
        required  = field.get('required', False)
        unique    = field.get('unique', False)
        condition = field.get('condition', None)
        mapping   = field.get('mapping', None)
        match     = field.get('match', None)
        replace   = field.get('replace', None)

        result.setdefault(dest_key, [])

        # check for well-formed input according to specified parameters
        if required:
            if src_value is '':
                logging.warning(f'required field {field["source"]} is blank')
        if unique:
            if len(src_value) > 1:
                logging.warning(f'non-unique error {field["source"]} {src_value}')

        # filter the possible results if called for
        if condition:
            filtered = [v for v in src_value if condition(v)]
        else:
            filtered = src_value
        
        # if a value mapping is specified, map each result appropriately
        if mapping:
            for v in filtered:
                if mapping[v] is not None:
                    result[dest_key].append(mapping[v])

        # if a match pattern is specified, extract the match
        elif match:
            for v in filtered:
                m = re.search(match, v)
                if m:
                    result[dest_key].append(m.group(1))

        # if replacement pattern has been specified, perform the replacement
        elif replace:
            for v in filtered:
                updated = re.sub(replace[0], replace[1], v)
                if updated:
                    result[dest_key].append(updated)

        # otherwise, just send the filtered values through unaltered
        else:
            result[dest_key].extend(filtered)

        # finally, strip any excess whitespace from all values in the field
        result[dest_key] = [' '.join(v.split()) for v in result[dest_key]]
        
    # set appropriate defaults for any fields that remain empty
    for field in defaults:
        if len(result[field]) == 0:
            result[field].append(defaults[field])

    return result

