def has_decimal_places_str(number):
    return "." in str(number)

num1 = 10
num2 = "0.820"
num3 = 10.0

print(f"{num1} has decimal places: {has_decimal_places_str(num1)}")
print(f"{num2} has decimal places: {has_decimal_places_str(num2)}")
print(f"{num3} has decimal places: {has_decimal_places_str(num3)}")