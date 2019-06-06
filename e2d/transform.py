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
    print(f'checking {original}')
    try:
        response = requests.head(original, timeout=20)
        status = response.status_code
        print(response.status_code)
        msg = requests.status_codes._codes[status][0]
        new = ''
        if status >= 300 and status < 400:
            redirect = requests.get(original, timeout=20)
            new = redirect.url
        return (status, msg, original, new)
    except:
        return ("error", '', original, '')


def transform(path):

    eprint = parse_source(path)
    result = {}

    for field in fields:
        print(field)
        src_value = eprint.get(field['source'], '')
        print(src_value)
        dest_key  = field.get('destination')
        print(dest_key)
        required  = field.get('required', False)
        print(required)
        unique    = field.get('unique', False)
        print(unique)
        condition = field.get('condition', None)
        print(condition)
        mapping   = field.get('mapping', None)
        print(mapping)
        match     = field.get('match', None)
        print(match)
        replace   = field.get('replace', None)
        print(replace)

        result.setdefault(dest_key, [])

        # check for well-formed input according to specified parameters
        if required:
            if src_value is '':
                print('required field error')
        if unique:
            if len(src_value) > 1:
                print('non-unique error', field['source'], src_value)

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

