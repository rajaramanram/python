#f = open("F://creating id.txt",'w+')

from random import randint

#rows = int(input("enter number of rows:"))
#columns = int(input("enter number of columns:"))


f = open("D://creating id.txt",'w+')
name = input("enter your name:")
dob = (input("enter your date of birth:"))
blood_group = input("enter your blood group:")
#def random(n):
   # range_start = 10**(n-1)
    #range_end = (10**n)-1
    #return randint(range_start, range_end)
#id = random(5)
id = randint(10000,19999)

print('+','-'*len(dob),'+',file=f)
print('|',name,' '*(len(dob)-len(name)-1),'|',file=f)
print('|',dob,'|',file=f)
print('|',blood_group,' '*(len(dob)-len(blood_group)-1),'|',file=f)
print('|',id,' '*(len(dob)-6),'|',file=f)
print('+','-'*len(dob),'+',file=f)
f.close()
