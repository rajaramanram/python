#this program is for sorting a set of strings

def sorting_strings():
    input_set = set()
    while True:
            try:
                set_length = int(input("enter the length of your array elements = "))
            except:
                print("enter only integer numbers")
            else:
                break
    for i in range(set_length):
        user_input = input("enter the elements for operation = ")
        input_set.add(user_input.casefold())
    print("length of the given set = ",set_length)
    print("given elements in set = ",input_set)
    print(" ".join(sorted(input_set)))
    while True:
        user_choice=input("want to continue the operation = {y/n} ")
        if (user_choice.casefold()=="y") or (user_choice.casefold() =="yes"):
            sorting_strings()
        else:
            break
sorting_strings()


    
 
