def copyArray(array):
    result = []
    for i in array:
        temp = {}
        for key, value in i.items():
            temp[key] = value
        result.append(temp)
    return result


def variableExist(array, name):
    array = array[::-1]
    for i in array:
        for j in i:
            if j['name'] == name:
                return True
    return False


def getValue(array, name):
    array = array[::-1]
    for i in array:
        for j in i:
            if j['name'] == name:
                return j['value']
    return name


def changeValue(array, name, value):
    array = array[::-1]
    for i in array:
        find = False
        for j in i:
            if j['name'] == name:
                j['value'] = value
                find = True
                break
        if find:
            break


# q = [{'name': 'Juan', 'value': 13}, {'name': 'Pedro', 'value': 1}, {'name': 'Paco', 'value': 20}]
# x = [{'name': 'David', 'value': 15}, {'name': 'Nova', 'value': 7}, {'name': 'Fátima', 'value': 29}]
# y = [{'name': 'Jose', 'value': 16}, {'name': 'Nuria', 'value': 5}, {'name': 'Astrid', 'value': 2}]
#
# z = [x, y]
# a = z + [q]
# print(a)
# a[0].append({'name': 'Puppy', 'value': 12})
# print(changeValue(a, "David", 19))
# print(x)