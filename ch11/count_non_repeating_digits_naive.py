a, b = tuple(map(int, input().split()))

count = 0
for i in range(a, b + 1):
    s = str(i)
    if len(set(s)) == len(s):
        count += 1
        
print(count)