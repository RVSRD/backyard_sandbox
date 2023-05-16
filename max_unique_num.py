# script returns max NON-duplicate number in numbers raw or None
# if there's no unique numbers in it

inlist_1 = [8, 8, 7, 9, 3, 6, 3, 4]
inlist_2 = [8, 8, 7, 7, 9, 9, 3, 3]


def maxdistinct(num_raw):
    inset = set(num_raw)
    result_list = []
    for num in inset:
        if num_raw.count(num) > 1:
            continue
        else:
            result_list.append(num)
    if result_list:
        return max(result_list)
    else:
        return None


# test 1
print(maxdistinct(inlist_1))
# test 2
print(maxdistinct(inlist_2))