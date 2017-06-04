def chain(iterable):
    last = None
    for i in iterable:
        if last is None:
            last = i
            continue
        yield last, i
        last = i


def get_set_dict(dictionary, key, factory):
    if key not in dictionary:
        dictionary[key] = factory()
    return dictionary[key]
