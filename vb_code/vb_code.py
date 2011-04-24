# -*- coding: utf-8 -*-

def vb_decode(lst):
    decoded = 0
    offset  = 0
    for x in reversed(lst):
        decoded += (x & 127) << offset
        if x & 128 == 0:
            break
        offset += 7
    return decoded

def trailing_zero(x, max = 32):
    ans = 0
    for i in range(0, max):
        if x & 1:
            ans = i
        x >>= 1
    return ans

def vb_encode(x):
    lst = []
    for i in range(0, int(trailing_zero(x) / 8) + 1):
        lst.insert(0, (x & 127) | 128)
        x >>= 7
    lst.insert(0, x & 127)
    return lst

if __name__ == "__main__":
    def lst_to_s(lst):
        return ", ".join(["{0:08b}".format(x) for x in lst])

    def test(lst):
        print("decoding " + lst_to_s(lst))
        print("=>       {0:032b}, {1}".format(decode(lst), decode(lst)))

    test([0b00000001, 0b10000010])
    test([0b00000001, 0b00000010])
