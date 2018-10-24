data = {
    0: ['E1', -1],
    1: ['E2', 0],
    2: ['E3', 0],
    3: ['E4', 0],
    4: ['E3', 1],
    5: ['E4', 1],
    6: ['E5', 5],
}


def get_all_names(index):
    answer = {}
    upward = get_all_names_upward(index)
    for i in upward:
        answer.update({i: upward[i]})

    downward = get_all_names_downward(index)
    for i in downward:
        answer.update({i: downward[i]})

    return answer


def get_all_names_upward(index):
    if index == -1:
        return {}
    element = data[index]
    names = {index: [element[0], element[1]]}

    for i in data:
        if data[i][1] == element[1]:
            names.update(get_all_names_upward(element[1]))

    return names


def get_all_names_downward(index):
    element = data[index]
    names = {index: [element[0], element[1]]}

    for i in data:
        if data[i][1] == index:
            names.update(get_all_names_downward(i))

    return names


print(get_all_names(3))
