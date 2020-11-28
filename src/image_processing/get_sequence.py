def compare(p1, p2):
    if p1[0] == p2[0] and p1[1] == p2[1]:
        return True
    return False


def create_sequence():
    pairs = (((39, 3), (40, 3)), ((19, 12), (20, 12)), ((17, 14), (18, 13)), ((16, 14), (17, 14)), ((9, 19), (10, 19)), ((22, 11), (23, 10)), ((33, 5), (34, 4)), ((38, 3), (39, 3)), ((21, 11), (22, 11)), ((44, 2), (45, 2)), ((49, 6), (49, 7)), ((26, 8), (27, 8)), ((49, 7), (49, 8)), ((37, 3), (38, 3)), ((47, 3), (48, 4)), ((48, 15), (48, 16)), ((34, 4), (35, 4)), ((46, 19), (46, 20)), ((35, 4), (36, 4)), ((18, 13), (19, 12)), ((25, 9), (26, 8)), ((4, 24), (5, 23)), ((48, 4), (49, 5)), ((36, 4), (37, 3)), ((41, 3), (42, 2)), ((49, 9), (49, 10)), ((14, 16), (15, 15)), ((13, 17), (14, 16)), ((45, 2), (46, 3)), ((48, 12), (48, 13)), ((12, 17), (13, 17)), ((31, 6), (32, 5)), ((47, 17), (47, 18)), ((15, 15), (16, 14)), ((48, 12), (49, 11)), ((
        43, 2), (44, 2)), ((43, 25), (43, 26)), ((48, 13), (48, 14)), ((7, 21), (8, 20)), ((27, 8), (28, 8)), ((24, 9), (25, 9)), ((28, 8), (29, 7)), ((23, 10), (24, 9)), ((46, 19), (47, 18)), ((8, 20), (9, 19)), ((6, 22), (7, 21)), ((29, 7), (30, 6)), ((47, 17), (48, 16)), ((5, 23), (6, 22)), ((11, 18), (12, 17)), ((30, 6), (31, 6)), ((41, 28), (42, 27)), ((42, 27), (43, 26)), ((44, 23), (44, 24)), ((40, 3), (41, 3)), ((1, 26), (2, 25)), ((10, 19), (11, 18)), ((32, 5), (33, 5)), ((42, 2), (43, 2)), ((45, 21), (45, 22)), ((49, 5), (49, 6)), ((49, 8), (49, 9)), ((49, 10), (49, 11)), ((48, 14), (48, 15)), ((2, 25), (3, 24)), ((45, 21), (46, 20)), ((46, 3), (47, 3)), ((44, 23), (45, 22)), ((3, 24), (4, 24)), ((43, 25), (44, 24)), ((20, 12), (21, 11)))
    return pairs


def one_way_append(pairs, last_index, last, sequence, checked):
    for i in range(0, len(pairs)):
        for index in range(1, len(pairs)):
            if index != last_index:
                first = compare(pairs[index][0], last)
                second = compare(pairs[index][1], last)
                if first or second:
                    if first:
                        sequence.append(pairs[index][1])
                        last = pairs[index][1]
                    if second:
                        sequence.append(pairs[index][0])
                        last = pairs[index][0]
                    last_index = index
                    checked.append(pairs[index])
                    break


def get_sequence():
    pairs = get_sequence()
    print(pairs)
    sequence = []
    sequence.append(pairs[0][0])
    sequence.append(pairs[0][1])
    last = pairs[0][1]
    last_index = 0
    checked = []
    one_way_append(pairs, last_index, last, sequence, checked)
    print('\n\nRESULT')
    print(sequence)
    # print('\n\n')
    # print(checked)
    # print(
    #     f"Pairs len: {len(pairs)}\nSequence len: {len(sequence)}\nChecked: {len(checked)}")
    # diff = []
    # for i in range(len(pairs)):
    #     add = True
    #     for j in range(len(checked)):
    #         if (compare(pairs[i][0], checked[j][0]) and compare(pairs[i][1], checked[j][1])) or (compare(pairs[i][1], checked[j][0]) and compare(pairs[i][0], checked[j][1])):
    #             add = False
    #             break
    #     if add:
    #         diff.append(pairs[i])
    # print('\n\n\n')
    # print(diff)
    # print(len(diff))


if __name__ == '__main__':
    get_sequence()
