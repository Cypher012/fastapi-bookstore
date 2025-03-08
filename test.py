from typing import Annotated

def find_max(arr: Annotated[list[int], "The list of numbers to find the maximum"]):
  
    if not arr:  # Check if the array is empty
      return None
  
    max_num = arr[0]  # Initialize max_num with the first element
    arr2 = []
    for num in arr:
      if num > max_num:
        max_num = num
      arr2.append(max_num)
  
    return max_num,arr2

# Example usage:
numbers = [10, 5, 20, 8, 30, 15]
max_value = find_max(numbers)
print(f"The maximum number is: {max_value}")


def greetings(name, age):
    return f"Hello, {name}, you are {age} years old!"

profile = {
    "name": "johndoe",
    "age": 25,
 }

print(greetings(**profile))

