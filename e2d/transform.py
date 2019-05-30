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
                result[key] = [value]
            else:
                result[key].append(value)
    return result


def check_ext_link(original):
    try:
        response = requests.head(original, timeout=5)
        status = response.status_code
        msg = requests.status_codes._codes[status][0]
        new = None
        if status >= 300 and status < 400:
            redirect = requests.get(original, timeout=5)
            new = redirect.url
        return (status, msg, original, new)
    except:
        return ("error", None, original, None)


def transform(path):

    eprint = parse_source(path)
    result = {}

    for field in fields:
        src_value = eprint.get(field['source'], '')
        dest_key  = field['destination']
        required  = field['required']
        unique    = field['unique']
        condition = field['condition']
        mapping   = field['mapping']
        pattern   = field['pattern']

        result.setdefault(dest_key, [])

        if required:
            if src_value is '':
                print('required field error')
        if unique:
            if len(src_value) > 1:
                print('non-unique error', field['source'], src_value)

        # filter the possible results
        if condition:
            filtered = [v for v in src_value if condition(v)]
        else:
            filtered = src_value
        # if a mapping is specified map each result appropriately
        if mapping:
            for v in filtered:
                if mapping[v] is not None:
                    result[dest_key].append(mapping[v])
        # otherwise, if a pattern is set, try to match it
        elif pattern:
            for v in filtered:
                match = re.search(pattern, v)
                if match:
                    result[dest_key].append(match.group(1))
        # otherwise, just send the filtered values through unaltered
        else:
            result[dest_key].extend(filtered)
        # finally, strip excess whitespace from all values in the field
        result[dest_key] = [' '.join(v.split()) for v in result[dest_key]]
        
    # set appropriate defaults for any fields that remain empty
    for field in defaults:
        if len(result[field]) == 0:
            result[field].append(defaults[field])

    print(result)
    return result

