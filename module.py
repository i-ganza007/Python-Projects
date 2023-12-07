def max_integer(my_list=[]):
    sorted_numbers = sorted(my_list,reverse=True)
    if len(my_list) == 0:
        return None
    else:
        return sorted_numbers[0]
result = max_integer(my_list=[1, 90, 2, 13, 34, 5, -13, 3])
print(result)




