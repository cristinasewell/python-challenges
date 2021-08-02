import csv
import os

data_file = os.path.abspath('Resources/budget_data.csv')

with open(data_file) as f:
    months_list = []
    totals_list = []
    reader_obj = csv.reader(f)
    for row in reader_obj:
        print(row)
        if len(row) > 0:
            months_list.append(row[0])
            totals_list.append(row[1])
    months_list.pop(0)
    totals_list.pop(0)
    print(len(months_list))
    data_numbers = [int(num) for num in totals_list]
    
    data_numbers2 = data_numbers.copy()
    deltas = []
    count = 0
    for x, y, m in zip(data_numbers, data_numbers2[1:], months_list[1:]):
        #print(x, y)
        #print(y-x)
        delta_num = y-x, m
        deltas.append(delta_num)

   # print(deltas)
   # for i, b in deltas.items():
   #     print(b)
