n, m = map(int, input().split())
print(n, m)

for _ in range(m):
    s = input().split()
    u = int(s[0])
    v = int(s[1])

    print("%5d %5d" %(u, v), end = ' ')
    print(s[2])