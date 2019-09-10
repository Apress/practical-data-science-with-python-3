def count_occurrences_digit_naive(k, n):
    k = str(k)
    count = 0
    for i in range(n + 1):
        count += str(i).count(k)
    return count

if __name__ == '__main__':
    k, n = tuple(map(int, input().split()))
    print(count_occurrences_digit_naive(k, n))
