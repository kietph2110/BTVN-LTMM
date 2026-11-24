# DES và AES-128

Cài đặt thuật toán DES và AES-128 bằng Python (không dùng thư viện mã hóa), in giá trị trung gian của từng bước để kiểm tra với ví dụ trên lớp.

## Chạy chương trình

```
python des.py
python aes.py
```

Chạy với test vector khác: `python des.py <key> <plaintext> [ciphertext mong đợi]`

```
python des.py 0E329232EA6D0D73 8787878787878787 0000000000000000
python aes.py 000102030405060708090a0b0c0d0e0f 00112233445566778899aabbccddeeff 69c4e0d86a7b0430d8cdb78070b4c55a
```

## Nội dung in ra

**DES**
- Sinh khóa: PC-1, C0/D0, Ci/Di sau mỗi lần dịch, 16 khóa con Ki (PC-2)
- Mã hóa: IP, L0/R0, mỗi vòng in E(R), E(R) xor K, đầu ra S-box, F = P(S), Li/Ri; cuối cùng là R16L16 và IP^-1
- Giải mã: giống mã hóa nhưng dùng khóa con theo thứ tự ngược

**AES-128**
- Mở rộng khóa: w[0..43], các bước RotWord / SubWord / Rcon, 11 khóa vòng
- Mã hóa: mỗi vòng in ma trận state sau SubBytes, ShiftRows, MixColumns, AddRoundKey
- Giải mã: InvShiftRows, InvSubBytes, AddRoundKey, InvMixColumns

## Bài tập trên lớp

**Tuần 11 - AES:** p = 0x...0011, k = 0x...0000 (bổ sung số 0 cho đủ 128 bit)

```
python aes.py 00000000000000000000000000000000 00000000000000000000000000000011
```

- Khóa con vòng 1: `62636363 62636363 62636363 62636363`
- Trạng thái sau vòng 1: `e0e138d9 01000000 01000000 01000000`

| State | SubBytes | ShiftRows | MixColumns | Round key 1 | Kết quả vòng 1 |
|---|---|---|---|---|---|
| 00 00 00 00 | 63 63 63 63 | 63 63 63 63 | 82 63 63 63 | 62 62 62 62 | e0 01 01 01 |
| 00 00 00 00 | 63 63 63 63 | 63 63 63 63 | 82 63 63 63 | 63 63 63 63 | e1 00 00 00 |
| 00 00 00 00 | 63 63 63 63 | 63 63 63 63 | 5b 63 63 63 | 63 63 63 63 | 38 00 00 00 |
| 00 00 00 11 | 63 63 63 82 | 82 63 63 63 | ba 63 63 63 | 63 63 63 63 | d9 00 00 00 |

Chi tiết đủ 10 vòng: `ketqua/aes_bai_tuan11.txt`

## Test vector khác

| Thuật toán | Key | Plaintext | Ciphertext | Kết quả |
|---|---|---|---|---|
| DES | 133457799BBCDFF1 | 0123456789ABCDEF | 85E813540F0AB405 | Đúng |
| DES | 0E329232EA6D0D73 | 8787878787878787 | 0000000000000000 | Đúng |
| AES-128 | 0f1571c947d9e8590cb7add6af7f6798 | 0123456789abcdeffedcba9876543210 | ff0b844a0853bf7c6934ab4364148fb9 | Đúng |
| AES-128 | 000102030405060708090a0b0c0d0e0f | 00112233445566778899aabbccddeeff | 69c4e0d86a7b0430d8cdb78070b4c55a | Đúng |

Kết quả chạy đầy đủ nằm trong thư mục `ketqua/`.
