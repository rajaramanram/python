# this program is for bitwise operation XOR and count number of 1's.
class BitWise:
    def __init__(self,first_number,second_number):
        self.first_number = first_number
        self.second_number = second_number
    def operation(self):
        result = self.first_number ^ self.second_number
        print(result)
        count = 0
        while result:
            print(result&1)
            count += result & 1
            print(count)
            result >>= 1
        return count
class NumberInput:
    def input_number():
        first_number = int(input("Enter first number = "))
        second_number = int(input("Enter second number = "))
        return first_number,second_number
objectnum = NumberInput
number_input = objectnum.input_number()
objoperation = BitWise(number_input[0],number_input[1])
print(objoperation.operation())
        
