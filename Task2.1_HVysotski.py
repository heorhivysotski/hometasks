
keys = ['one', 'two', 'three', 'four']
values = [1, 2, 3]


def dictionary(keys, values):
    if len(keys) > len(values):
        while len(keys) > len(values):
            values.append(None)
    else:
        values = values[0:len(keys)]
    return {key: value for key, value in zip(keys, values)}

print(dictionary(keys, values))
