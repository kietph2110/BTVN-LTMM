# Thuat toan DES - ma hoa / giai ma 1 khoi 64 bit
# In ra gia tri trung gian cua tung buoc de kiem tra voi bai tren lop

import sys

# ===== Cac bang hoan vi =====

# Hoan vi khoi dau IP
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

# Hoan vi ket thuc IP^-1
IP_INV = [40, 8, 48, 16, 56, 24, 64, 32,
          39, 7, 47, 15, 55, 23, 63, 31,
          38, 6, 46, 14, 54, 22, 62, 30,
          37, 5, 45, 13, 53, 21, 61, 29,
          36, 4, 44, 12, 52, 20, 60, 28,
          35, 3, 43, 11, 51, 19, 59, 27,
          34, 2, 42, 10, 50, 18, 58, 26,
          33, 1, 41, 9, 49, 17, 57, 25]

# Mo rong E: 32 bit -> 48 bit
E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1]

# Hoan vi P sau S-box
P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]

# PC-1: 64 bit khoa -> 56 bit (bo bit chan le)
PC1 = [57, 49, 41, 33, 25, 17, 9,
       1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27,
       19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15,
       7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29,
       21, 13, 5, 28, 20, 12, 4]

# PC-2: 56 bit -> 48 bit khoa con
PC2 = [14, 17, 11, 24, 1, 5,
       3, 28, 15, 6, 21, 10,
       23, 19, 12, 4, 26, 8,
       16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55,
       30, 40, 51, 45, 33, 48,
       44, 49, 39, 56, 34, 53,
       46, 42, 50, 36, 29, 32]

# So bit dich trai moi vong
SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# 8 hop S
SBOX = [
    # S1
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    # S2
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    # S3
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    # S4
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    # S5
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    # S6
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    # S7
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    # S8
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]],
]


# ===== Ham tien ich =====

def hex_to_bits(h):
    # chuoi hex -> list bit (0/1)
    bits = []
    for c in h:
        v = int(c, 16)
        for i in range(3, -1, -1):
            bits.append((v >> i) & 1)
    return bits


def bits_to_hex(bits):
    s = ""
    for i in range(0, len(bits), 4):
        v = bits[i] * 8 + bits[i + 1] * 4 + bits[i + 2] * 2 + bits[i + 3]
        s += "%X" % v
    return s


def bits_to_str(bits, group=4):
    # in dang nhi phan, tach nhom cho de doc
    s = ""
    for i in range(len(bits)):
        if i > 0 and i % group == 0:
            s += " "
        s += str(bits[i])
    return s


def permute(bits, table):
    # bang hoan vi danh so tu 1
    return [bits[i - 1] for i in table]


def xor(a, b):
    return [x ^ y for x, y in zip(a, b)]


def shift_left(bits, n):
    return bits[n:] + bits[:n]


# ===== Sinh 16 khoa con =====

def generate_keys(key_hex, verbose=True):
    key = hex_to_bits(key_hex)
    k56 = permute(key, PC1)
    C = k56[:28]
    D = k56[28:]

    if verbose:
        print("Khoa K     =", key_hex)
        print("K (bin)    =", bits_to_str(key, 8))
        print("PC-1(K)    =", bits_to_str(k56, 7))
        print("C0 =", bits_to_str(C, 7), " (%s)" % bits_to_hex(C))
        print("D0 =", bits_to_str(D, 7), " (%s)" % bits_to_hex(D))
        print()

    keys = []
    for i in range(16):
        C = shift_left(C, SHIFTS[i])
        D = shift_left(D, SHIFTS[i])
        k = permute(C + D, PC2)
        keys.append(k)
        if verbose:
            print("Vong %2d: dich %d bit" % (i + 1, SHIFTS[i]))
            print("  C%-2d = %s  (%s)" % (i + 1, bits_to_str(C, 7), bits_to_hex(C)))
            print("  D%-2d = %s  (%s)" % (i + 1, bits_to_str(D, 7), bits_to_hex(D)))
            print("  K%-2d = %s  (%s)" % (i + 1, bits_to_str(k, 6), bits_to_hex(k)))
    return keys


# ===== Ham F =====

def f_function(R, K, verbose=True):
    ER = permute(R, E)
    x = xor(ER, K)

    out = []
    for i in range(8):
        block = x[i * 6:(i + 1) * 6]
        row = block[0] * 2 + block[5]
        col = block[1] * 8 + block[2] * 4 + block[3] * 2 + block[4]
        val = SBOX[i][row][col]
        for j in range(3, -1, -1):
            out.append((val >> j) & 1)

    result = permute(out, P)

    if verbose:
        print("    E(R)       =", bits_to_str(ER, 6), " (%s)" % bits_to_hex(ER))
        print("    E(R) xor K =", bits_to_str(x, 6), " (%s)" % bits_to_hex(x))
        print("    S-box out  =", bits_to_str(out, 4), " (%s)" % bits_to_hex(out))
        print("    F = P(S)   =", bits_to_str(result, 4), " (%s)" % bits_to_hex(result))
    return result


# ===== Ma hoa / giai ma =====

def des(block_hex, keys, decrypt=False, verbose=True):
    if decrypt:
        keys = keys[::-1]

    bits = hex_to_bits(block_hex)
    ip = permute(bits, IP)
    L = ip[:32]
    R = ip[32:]

    if verbose:
        print("Input      =", block_hex)
        print("IP         =", bits_to_str(ip, 4), " (%s)" % bits_to_hex(ip))
        print("L0 =", bits_to_hex(L), "  R0 =", bits_to_hex(R))
        print()

    for i in range(16):
        if verbose:
            print("Vong %d:  K%d = %s" % (i + 1, i + 1, bits_to_hex(keys[i])))
        F = f_function(R, keys[i], verbose)
        newR = xor(L, F)
        L = R
        R = newR
        if verbose:
            print("    L%-2d = %s   R%-2d = %s" % (i + 1, bits_to_hex(L), i + 1, bits_to_hex(R)))
            print()

    # vong cuoi doi cho L, R
    pre = R + L
    out = permute(pre, IP_INV)
    if verbose:
        print("R16L16     =", bits_to_hex(pre))
        print("IP^-1      =", bits_to_str(out, 8))
        print("Output     =", bits_to_hex(out))
    return bits_to_hex(out)


def main():
    # test vector mac dinh (vi du trong sach Stallings / tren lop)
    key = "133457799BBCDFF1"
    plain = "0123456789ABCDEF"
    expected = "85E813540F0AB405"

    if len(sys.argv) >= 3:
        key = sys.argv[1].upper()
        plain = sys.argv[2].upper()
        expected = sys.argv[3].upper() if len(sys.argv) >= 4 else None

    print("=" * 70)
    print("DES - SINH KHOA CON")
    print("=" * 70)
    keys = generate_keys(key)

    print()
    print("=" * 70)
    print("DES - MA HOA")
    print("=" * 70)
    cipher = des(plain, keys)

    print()
    print("=" * 70)
    print("DES - GIAI MA")
    print("=" * 70)
    back = des(cipher, keys, decrypt=True)

    print()
    print("=" * 70)
    print("KET QUA")
    print("=" * 70)
    print("Plaintext  :", plain)
    print("Key        :", key)
    print("Ciphertext :", cipher)
    if expected:
        print("Mong doi   :", expected, "->", "DUNG" if cipher == expected else "SAI")
    print("Giai ma    :", back, "->", "DUNG" if back == plain else "SAI")


if __name__ == "__main__":
    main()
