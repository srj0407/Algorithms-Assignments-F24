import time
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import math
from algorithms import log
from algorithms import poly

# Function to generate test inputs
def generate_test_input(n, C):
    # Ensure days is never more than the number of counts
    days = random.randint(1, min(math.pow(10, 6), n))  # Cap days to be less than or equal to n
    avg_attendees_per_club = C // n
    try:
        club_count = list(np.random.randint(1, max(2 * avg_attendees_per_club, 2), size=(n,), dtype=np.uint64))
    except:
        club_count = [random.randint(1, max(2 * avg_attendees_per_club, 1)) for _ in range(n)]

    return days, club_count

# Use high-resolution timer for better accuracy
def measure_time_logarithmic(n, C):
    days, club_count = generate_test_input(n, C)
    start_time = time.perf_counter()  # High precision timer
    log(days, club_count)
    end_time = time.perf_counter()
    return end_time - start_time  # Return the time difference

def measure_time_polynomial(n, C):
    days, club_count = generate_test_input(n, C)
    start_time = time.perf_counter()  # High precision timer
    poly(days, club_count)
    end_time = time.perf_counter()
    return end_time - start_time  # Return the time difference


# Generate multiple input sizes and measure their times
input_sizes = []
polynomial_times = []
logrithmic_times_n = []
logrithmic_times_c = []

i = 1
while True:
    x = 200 * i
    input_sizes.append(x)

    total_time = 0

  # Measure time for the logarithmic complexity algorithm
    log_elapsed_time = measure_time_logarithmic(x, 100)
    logrithmic_times_n.append(log_elapsed_time)
    print(f"Logarithmic Algorithm - Input size n: {x}, Time taken: {log_elapsed_time:.6f} seconds")

    total_time += log_elapsed_time

    # Measure time for the logarithmic complexity algorithm
    log_elapsed_time = measure_time_logarithmic(100, 2**(x // 5))
    logrithmic_times_c.append(log_elapsed_time)
    print(f"Logarithmic Algorithm - Input size C: {x}, Time taken: {log_elapsed_time:.6f} seconds")

    total_time += log_elapsed_time

    # Measure time for the polynomial complexity algorithm
    poly_elapsed_time = 0
    # Run the polynomial algorithm multiple times for smaller inputs
    for _ in range(5):
        poly_elapsed_time += measure_time_polynomial(x, 100)
    poly_elapsed_time /= 5  # Take the average time

    polynomial_times.append(poly_elapsed_time)
    print(f"Polynomial Algorithm - Input size: {x}, Time taken: {poly_elapsed_time:.6f} seconds")

    total_time += poly_elapsed_time

    if total_time > 2.0:
        break

    i += 1

# Plotting the results for both algorithms
plt.plot(input_sizes, logrithmic_times_n, marker='o', linestyle='-', color='b', label='Logarithmic n (O(n log C))')
plt.xlabel('Input Size (n)')
plt.ylabel('Time Taken (seconds)')
plt.grid(True)
plt.legend()
plt.show()

plt.plot(input_sizes, logrithmic_times_c, marker='o', linestyle='-', color='b', label='Logarithmic c (O(n log C))')
plt.xlabel('Input Size (c)')
plt.ylabel('Time Taken (seconds)')
plt.grid(True)
plt.legend()
plt.show()

plt.plot(input_sizes, polynomial_times, marker='x', linestyle='--', color='r', label='Polynomial (O(n^2))')
plt.xlabel('Input Size (n)')
plt.ylabel('Time Taken (seconds)')
plt.grid(True)
plt.legend()
plt.show()