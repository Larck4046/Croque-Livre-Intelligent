import scanner

while True:
    p = input()
    s = scanner(p)
    s.receiver()
    del s
    