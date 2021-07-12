import csv
with open("gearman_sample.csv",'r')as file:
    reader=csv.reader(file)
    for row in reader:
        print(row)
