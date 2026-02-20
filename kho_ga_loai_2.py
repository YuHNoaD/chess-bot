# -*- coding: utf-8 -*-
"""
Thông tin về khô gà loại 2 đè tem
"""

import sys
import io

# Set UTF-8 encoding for output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Thông tin cơ bản
thong_tin_co_ban = {
    "Ten": "Kho ga loai 2 de tem",
    "Ten tieng Anh": "Second-grade stamped dried chicken",
    "Phan loai": "Kho ga",
    "Loai": "Loai 2",
    "Dac diem": "De tem",
}

# Đặc điểm sản phẩm
dac_diem = {
    "Nguon goc": "Ga cong nghiep hoac ga lai",
    "Kich thuoc": "Nho hon loai 1",
    "Do day": "Mong hon loai 1",
    "Mau sac": "Vang nhat den vang dam",
    "Ket cau": "Kho, ngon",
    "Huong vi": "Man, ngot, thom",
}

# Quy trình sản xuất
quy_trinh = [
    "1. Lua chon ga",
    "2. So che va lam sach",
    "3. Tam uop gia vi",
    "4. Say kho",
    "5. Dong goi",
    "6. Dong tem kiem dinh",
]

# Giá cả (ước tính)
gia_ca = {
    "Gia ban le": "80.000 - 150.000 VND/kg",
    "Gia ban si": "70.000 - 120.000 VND/kg",
}

# Cách sử dụng
cach_su_dung = [
    "An truc tiep nhu snack",
    "Ngam nuoc cho mem roi che bien",
    "Xao rau cu",
    "Nau canh",
    "Lam topping cho mi/bun",
]

# Lưu ý bảo quản
luu_y = [
    "Bao quan noi kho rapo, thoang mat",
    "Tranh anh nang truc tiep",
    "Nhiet do phong: 20-25°C",
    "Han su dung: 6-12 thang",
    "Sau khi mo: Dung trong 1 thang",
]

# So sánh với loại 1
so_sanh = {
    "Loai 1": {
        "Kich thuoc": "Lon hon",
        "Do day": "Day hon",
        "Gia": "Cao hon",
        "Chat luong": "Tot hon",
    },
    "Loai 2": {
        "Kich thuoc": "Nho hon",
        "Do day": "Mong hon",
        "Gia": "Re hon",
        "Chat luong": "Kha",
    },
}

# Địa chỉ mua
dia_chi_mua = [
    "Cho truyen thong",
    "Sieu thi",
    "Cua hang thuc pham kho",
    "San thuong mai dien tu (Shopee, Lazada, Tiki)",
    "Facebook",
    "Website ban thuc pham",
]

# Lưu ý khi mua
luu_y_khi_mua = [
    "Kiem tra han su dung",
    "Kiem tra tem mac",
    "Kiem tra bao bi",
    "Kiem tra mau sac",
    "Kiem tra mui vi",
    "Chon noi uy tin",
]

print("="*60)
print("THONG TIN VE KHO GA LOAI 2 DE TEM")
print("="*60)
print()

print("THONG TIN CO BAN:")
for key, value in thong_tin_co_ban.items():
    print(f"  {key}: {value}")
print()

print("DAC DIEM SAN PHAM:")
for key, value in dac_diem.items():
    print(f"  {key}: {value}")
print()

print("QUY TRINH SAN XUAT:")
for buoc in quy_trinh:
    print(f"  {buoc}")
print()

print("GIA CA:")
for key, value in gia_ca.items():
    print(f"  {key}: {value}")
print()

print("CACH SU DUNG:")
for i, cach in enumerate(cach_su_dung, 1):
    print(f"  {i}. {cach}")
print()

print("LUU Y BAO QUAN:")
for i, luu in enumerate(luu_y, 1):
    print(f"  {i}. {luu}")
print()

print("SO SANH VOI LOAI 1:")
print("  Loai 1:")
for key, value in so_sanh["Loai 1"].items():
    print(f"    {key}: {value}")
print("  Loai 2:")
for key, value in so_sanh["Loai 2"].items():
    print(f"    {key}: {value}")
print()

print("DIA CHI MUA:")
for i, dia_chi in enumerate(dia_chi_mua, 1):
    print(f"  {i}. {dia_chi}")
print()

print("LUU Y KHI MUA:")
for i, luu in enumerate(luu_y_khi_mua, 1):
    print(f"  {i}. {luu}")
print()

print("="*60)