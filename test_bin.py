with open('file.bin', 'rb') as file:
    file.read(20)
    more_time, less_time, more_value, less_value = [x for x in file.read(4)]
    print(more_time, less_time, more_value, less_value)
    lst_values = list()
    dict_data = dict()
    for c in file.read():
        lst_values.append(c)
    for i in range(0, len(lst_values), 2):
        dict_data[lst_values[i]] = lst_values[i + 1]
print(dict_data.keys())