def setup():
    MAX_EXPONENT = 50

    # Holds the number of occurrences of digit k in [0, (10**i) - 1], i > 0. 
    # If the range is partial (first part of the composite key is False), then
    # leading zeros are omitted (this is a special case when k == 0).
    table_of_occurrences = {(False, 0): 0, (False, 1): 1, 
                             (True, 0): 0, (True, 1): 1}
    for i in range(2, MAX_EXPONENT + 1):
        table_of_occurrences[(True, i)] = i * 10**(i - 1)
        table_of_occurrences[(False, i)] = \
            10**(i - 1) + 10 * table_of_occurrences[(False, i - 1)] - 10 
    return table_of_occurrences
    
def count_occurrences_digit(k, n, table_of_occurrences=setup()):
    digits = str(n)
    num_digits = len(digits)
    count = 0
    is_first_digit = num_digits > 1

    for digit in map(int, digits):
        span = 10**(num_digits - 1)

        count += (digit - 1) * table_of_occurrences[(True, num_digits - 1)]
        count += table_of_occurrences[(k != 0 or not is_first_digit, num_digits - 1)]
           
        if digit > k:
            if k > 0 or not is_first_digit:
                count += span
        elif digit == k:
            count += (n % span) + 1

        num_digits -= 1
        is_first_digit = False
    return count

if __name__ == '__main__':
    k, n = tuple(map(int, input().split()))
    print(count_occurrences_digit(k, n))
