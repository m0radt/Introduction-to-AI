def max_semi_cooperative_comparator(a, b):
    if a[0] > b[0]:
        return -1
    if a[0] == b[0]:
        if a[1] < b[1]:
            return -1
        if a[1] == b[1]:
            return 0
    return 1


def min_semi_cooperative_comparator(a, b):
    if a[1] > b[1]:
        return -1
    if a[1] == b[1]:
        if a[0] < b[0]:
            return -1
        if a[0] == b[0]:
            return 0
    return 1


def fully_cooperative_comparator(a, b):
	a_value = a[0] + a[1]
	b_value = b[0] + b[1]
	a_depth = a[2]
	b_depth = b[2]
	if a_value > b_value:
		return -1
	elif a_value == b_value and b_depth > a_depth:
		return -1
	return 1

