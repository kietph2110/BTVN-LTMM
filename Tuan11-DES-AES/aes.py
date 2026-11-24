# Thuat toan AES-128 - ma hoa / giai ma 1 khoi 128 bit
# In ra state sau tung buoc cua tung vong

import sys

SBOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16,
]

# S-box nguoc: tinh tu SBOX
INV_SBOX = [0] * 256
for i in range(256):
    INV_SBOX[SBOX[i]] = i

RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]


# ===== Ham tien ich =====

def hex_to_bytes(h):
    return [int(h[i:i + 2], 16) for i in range(0, len(h), 2)]


def bytes_to_hex(b):
    return "".join("%02x" % x for x in b)


# state la ma tran 4x4, state[hang][cot]
# 16 byte dau vao duoc xep theo cot
def bytes_to_state(b):
    return [[b[r + 4 * c] for c in range(4)] for r in range(4)]


def state_to_bytes(s):
    return [s[r][c] for c in range(4) for r in range(4)]


def print_states(titles, states):
    # in nhieu ma tran canh nhau cho gon
    print("    " + "".join("%-15s" % t for t in titles))
    for r in range(4):
        line = "    "
        for s in states:
            line += "%-15s" % " ".join("%02x" % s[r][c] for c in range(4))
        print(line)


# ===== Nhan trong GF(2^8) =====

def xtime(a):
    a = a << 1
    if a & 0x100:
        a ^= 0x11b
    return a


def gmul(a, b):
    res = 0
    while b:
        if b & 1:
            res ^= a
        a = xtime(a)
        b >>= 1
    return res


# ===== Mo rong khoa =====

def key_expansion(key_hex, verbose=True):
    key = hex_to_bytes(key_hex)
    w = []
    for i in range(4):
        w.append(key[4 * i:4 * i + 4])

    if verbose:
        print("Khoa K =", key_hex)
        for i in range(4):
            print("  w[%2d] = %s" % (i, bytes_to_hex(w[i])))

    for i in range(4, 44):
        temp = w[i - 1][:]
        if i % 4 == 0:
            rot = temp[1:] + temp[:1]
            sub = [SBOX[x] for x in rot]
            rc = [RCON[i // 4 - 1], 0, 0, 0]
            temp = [sub[j] ^ rc[j] for j in range(4)]
            if verbose:
                print("  --- i=%d: RotWord=%s  SubWord=%s  Rcon=%s  -> %s"
                      % (i, bytes_to_hex(rot), bytes_to_hex(sub), bytes_to_hex(rc), bytes_to_hex(temp)))
        new = [w[i - 4][j] ^ temp[j] for j in range(4)]
        w.append(new)
        if verbose:
            print("  w[%2d] = w[%2d] xor temp = %s" % (i, i - 4, bytes_to_hex(new)))

    # gom 4 word thanh 1 khoa vong
    round_keys = []
    for r in range(11):
        k = w[4 * r] + w[4 * r + 1] + w[4 * r + 2] + w[4 * r + 3]
        round_keys.append(bytes_to_state(k))

    if verbose:
        print()
        for r in range(11):
            print("  Khoa vong %2d: %s" % (r, bytes_to_hex(state_to_bytes(round_keys[r]))))
    return round_keys


# ===== 4 phep bien doi =====

def sub_bytes(s):
    return [[SBOX[s[r][c]] for c in range(4)] for r in range(4)]


def inv_sub_bytes(s):
    return [[INV_SBOX[s[r][c]] for c in range(4)] for r in range(4)]


def shift_rows(s):
    # hang r dich trai r byte
    return [s[r][r:] + s[r][:r] for r in range(4)]


def inv_shift_rows(s):
    return [s[r][4 - r:] + s[r][:4 - r] for r in range(4)]


def mix_columns(s):
    out = [[0] * 4 for _ in range(4)]
    for c in range(4):
        a = [s[r][c] for r in range(4)]
        out[0][c] = gmul(a[0], 2) ^ gmul(a[1], 3) ^ a[2] ^ a[3]
        out[1][c] = a[0] ^ gmul(a[1], 2) ^ gmul(a[2], 3) ^ a[3]
        out[2][c] = a[0] ^ a[1] ^ gmul(a[2], 2) ^ gmul(a[3], 3)
        out[3][c] = gmul(a[0], 3) ^ a[1] ^ a[2] ^ gmul(a[3], 2)
    return out


def inv_mix_columns(s):
    out = [[0] * 4 for _ in range(4)]
    for c in range(4):
        a = [s[r][c] for r in range(4)]
        out[0][c] = gmul(a[0], 14) ^ gmul(a[1], 11) ^ gmul(a[2], 13) ^ gmul(a[3], 9)
        out[1][c] = gmul(a[0], 9) ^ gmul(a[1], 14) ^ gmul(a[2], 11) ^ gmul(a[3], 13)
        out[2][c] = gmul(a[0], 13) ^ gmul(a[1], 9) ^ gmul(a[2], 14) ^ gmul(a[3], 11)
        out[3][c] = gmul(a[0], 11) ^ gmul(a[1], 13) ^ gmul(a[2], 9) ^ gmul(a[3], 14)
    return out


def add_round_key(s, k):
    return [[s[r][c] ^ k[r][c] for c in range(4)] for r in range(4)]


# ===== Ma hoa =====

def encrypt(plain_hex, rk, verbose=True):
    s = bytes_to_state(hex_to_bytes(plain_hex))
    if verbose:
        print("Vong 0:")
        start = s
        s = add_round_key(s, rk[0])
        print_states(["Input", "Round key 0", "AddRoundKey"], [start, rk[0], s])
        print()

    for r in range(1, 11):
        start = s
        s1 = sub_bytes(s)
        s2 = shift_rows(s1)
        if r != 10:
            s3 = mix_columns(s2)
        else:
            s3 = s2  # vong cuoi khong co MixColumns
        s = add_round_key(s3, rk[r])

        if verbose:
            print("Vong %d:" % r)
            titles = ["Start", "SubBytes", "ShiftRows"]
            states = [start, s1, s2]
            if r != 10:
                titles.append("MixColumns")
                states.append(s3)
            titles += ["Round key %d" % r, "AddRoundKey"]
            states += [rk[r], s]
            print_states(titles, states)
            print("    -> %s" % bytes_to_hex(state_to_bytes(s)))
            print()

    return bytes_to_hex(state_to_bytes(s))


# ===== Giai ma =====

def decrypt(cipher_hex, rk, verbose=True):
    s = bytes_to_state(hex_to_bytes(cipher_hex))
    if verbose:
        print("Vong 0:")
        start = s
        s = add_round_key(s, rk[10])
        print_states(["Input", "Round key 10", "AddRoundKey"], [start, rk[10], s])
        print()

    for r in range(9, -1, -1):
        start = s
        s1 = inv_shift_rows(s)
        s2 = inv_sub_bytes(s1)
        s3 = add_round_key(s2, rk[r])
        if r != 0:
            s = inv_mix_columns(s3)
        else:
            s = s3

        if verbose:
            print("Vong %d:" % (10 - r))
            titles = ["Start", "InvShiftRows", "InvSubBytes", "Round key %d" % r, "AddRoundKey"]
            states = [start, s1, s2, rk[r], s3]
            if r != 0:
                titles.append("InvMixColumns")
                states.append(s)
            print_states(titles, states)
            print("    -> %s" % bytes_to_hex(state_to_bytes(s)))
            print()

    return bytes_to_hex(state_to_bytes(s))


def main():
    # test vector mac dinh: vi du trong sach Stallings
    key = "0f1571c947d9e8590cb7add6af7f6798"
    plain = "0123456789abcdeffedcba9876543210"
    expected = "ff0b844a0853bf7c6934ab4364148fb9"

    if len(sys.argv) >= 3:
        key = sys.argv[1].lower()
        plain = sys.argv[2].lower()
        expected = sys.argv[3].lower() if len(sys.argv) >= 4 else None

    print("=" * 70)
    print("AES-128 - MO RONG KHOA")
    print("=" * 70)
    rk = key_expansion(key)

    print()
    print("=" * 70)
    print("AES-128 - MA HOA")
    print("=" * 70)
    cipher = encrypt(plain, rk)

    print("=" * 70)
    print("AES-128 - GIAI MA")
    print("=" * 70)
    back = decrypt(cipher, rk)

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
