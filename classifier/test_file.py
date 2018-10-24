testAvailableSymbol = [
    'A', 'b', 'z', 'А', 'Б', 'Я',
]

testNotAvailableSymbol = [
    '1', '0', '9', '.', '\\', '+', '^',
]

testAvailableName = [
    "Test", "teST", "Тест", "неТест", "Полу test", "Test spaces", "Test spaces again"
]

testNotAvailableName = [
    "", " Test not from space", "Test, test", "Test  much   space",
]

testHierarchyExperimental = [
    "E1", ["E2", ["E3", "E4", "E5"]], ["E3", ["E4", "E5"]]
]

testHierarchy = {
    0: ["E1", -1],
    1: ["E2", 0],
    4: ["E3", 1],
    5: ["E4", 1],
    2: ["E3", 0],
    6: ["E2"],
    3: ["E4", 0],
}

testAvailableInsert = [
    ["E4", 4], ["E2", 2]
]

testNotAvailableInsert = [
    ["E2", 4], ["E1", 2]
]

data = [
    'E1',
    ['E2', ['E3', []], ['E4', ['E5']], ],
    ['E3', [], ],
    ['E4', [], ],
]


def is_available_name(name):
    if len(name) == 0:
        return False

    for i in name:
        if not is_available_symbol(i):
            return False

    words = name.split(" ")
    for i in words:
        if len(i) == 0:
            return False
    return True


def is_available_symbol(symbol):
    return ('a' <= symbol <= 'z') or \
           ('A' <= symbol <= 'Z') or \
           ('а' <= symbol <= 'я') or \
           ('А' <= symbol <= 'Я') or \
           (symbol == ' ')


def is_available_for_insert(new_name, index, data):
    debug_counter = 0
    current_element = data[index]
    while current_element[1] != -1:
        debug_counter += 1
        if debug_counter > 50:
            return "Overflow"

        new_index = current_element[1]
        if data.get(new_index) is None:
            return "End"

        current_element = data[new_index]
        if current_element[0] == new_name:
            return False
    return True


# def is_available_for_insertExperimental(array, lastName, newName):
#     findNext()
#     return True
#
# def findNext(array, element):


# If you got some message - it is Error anyway
def test():
    # for i in testAvailableSymbol:
    #     if not is_available_symbol(i):
    #         print("testAvailableSymbol: ", i)
    #
    # for i in testNotAvailableSymbol:
    #     if is_available_symbol(i):
    #         print("testNotAvailableSymbol: ", i)
    #
    # for i in testAvailableName:
    #     if not is_available_name(i):
    #         print("testAvailableName: ", i)
    #
    # for i in testNotAvailableName:
    #     if is_available_name(i):
    #         print("testNotAvailableName:", i)

    make_test("testAvailableSymbol", testAvailableSymbol, is_available_symbol, True)
    make_test("testNotAvailableSymbol", testNotAvailableSymbol, is_available_symbol, False)
    make_test("testAvailableName", testAvailableName, is_available_name, True)
    make_test("testNotAvailableName", testNotAvailableName, is_available_name, False)
    make_test2("testAvailableInsert", testAvailableInsert, is_available_for_insert, True)
    make_test2("testNotAvailableInsert", testNotAvailableInsert, is_available_for_insert, False)


def make_test(name, array, func, condition):
    print("Test ", name)
    errors = 0
    for i in array:
        if func(i) != condition:
            print("Value: -", i, "-", sep='')
            errors += 1

    print("Tasks =", len(array), " with error = ", errors)


def make_test2(name, array, func, condition):
    print("Test ", name)
    errors = 0
    for i in array:
        if func(i[0], i[1], testHierarchy) != condition:
            print("Value: -", i, "-", sep='')
            errors += 1

    print("Tasks =", len(array), " with error = ", errors)

test()
