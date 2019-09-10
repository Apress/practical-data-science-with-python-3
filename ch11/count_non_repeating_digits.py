import math

a, b = tuple(map(int, input().split()))

def variation_without_repetition(n, k):
    return math.factorial(n) // math.factorial(n - k)

# Finds how many numbers with non-repeating digits are present in [0, k].
def count_numbers_with_non_repeating_digits(k):
    if k < 0:
        return 0
    if k == 0:
        return 1

    # We can find most numbers using combinatorics.
    digits = str(k)
    num_digits = len(digits)
    first_digit = int(digits[0])
    span = 10 ** (num_digits - 1)
    
    s = (first_digit - 1) * variation_without_repetition(9, num_digits - 1)
    
    # We must take care of a lower interval regarding leading zeros.
    s += count_numbers_with_non_repeating_digits(span - 1)

    # We continue our search for the upper part.
    used_digits = {first_digit}
    t = num_digits == 1

    for i in range(1, num_digits):
        first_digit = int(digits[i])
        allowed_digits = set(range(first_digit + 1)) - used_digits
        v = variation_without_repetition(9 - i, num_digits - 1 - i)
        used_digits.add(first_digit)

        if first_digit not in allowed_digits:
            if len(allowed_digits) == 0 and i == 1:
                t = 0
            else:
                t += len(allowed_digits) * v
            break
        else:
            t += (len(allowed_digits) - (i != num_digits - 1)) * v                
    return s + t
    
print(count_numbers_with_non_repeating_digits(b) - \
      count_numbers_with_non_repeating_digits(a - 1))