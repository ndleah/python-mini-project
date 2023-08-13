import statistics

numbers = []
print("\nWrite a number list to calculate the Arithmetic Average, Standard Deviation, Mode, Median and Variance (Press Enter to stop): ")
while True:
    number = input("")
    if number == "":
        break
    numbers.append(int(number))


Avg = statistics.mean(numbers)
Mode = statistics.mode(numbers)
Deviation = statistics.stdev(numbers)
Median = statistics.median(numbers)
Variance = statistics.variance(numbers)

print("")
print(f"Full list = {numbers}\n")
print(f"Mode: {Mode}")
print(f"Median: {Median}")
print(f"Variance: {Variance}")
print(f"Arithmetic Average: {Avg}")
print(f"Standard Deviation: {Deviation}\n")
