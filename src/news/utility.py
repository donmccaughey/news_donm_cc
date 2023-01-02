def bisect(items, compare):
    begin = 0
    end = len(items)
    while begin < end:
        i = (begin + end) // 2
        if compare(items[i]):
            begin = i + 1
        else:
            end = i
    return begin
