def extend_list_to_360(lst):
    new_list = lst[:]  # Copy the original list
    while len(new_list) < 360:
        for i in range(len(new_list) - 1):
            new_element = (new_list[i] + new_list[i + 1]) / 2
            new_list.insert(i + 1, new_element)
            if len(new_list) >= 360:
                break
    return new_list[:360]

# Example usage:
original_list = [1, 2, 3, 4, 5]  # Change this list to whatever you want
extended_list = extend_list_to_360(original_list)
print(extended_list)
print(len(extended_list))  # Ensure the length of the list is 360
