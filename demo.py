import requests
from math import sin
import copy

# response = requests.get('openweather.org').json()

a : int  = 5
b = 0.5
s = "Demo string"
name_list = ['Dmitry', 'Vladimir', 'Arina', [1,2,3,4,5]]


#
# print(" a = ", a)
# print( "a = {}, b = {}".format(a, b))
# print (f'a = {a}, b = {b}')
# print(f'{a=} {b=}')
#

def my_sin(x):  # Pass by Value
    x = 1
    return sin(x)


def print_names(arr):  # Pass by reference
    arr += ['Vladik']

    for name in arr:
        arr[3] = 'YYY'
        print(name)
        # arr.pop()
        # arr.pop()
        # arr.append('xxx')


# shallow copy
arr2 = copy.copy(name_list)
arr3 = copy.deepcopy(name_list)

print_names(arr2)
print(f'{arr2=}')
print(f'{name_list=}')
print(f'{arr3=}')
