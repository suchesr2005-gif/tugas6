def get_label(nilai):
    if nilai >= 85: return 'A'
    elif nilai >= 80: return 'A-'
    elif nilai >= 70: return 'B+'
    elif nilai >= 65: return 'B-'
    elif nilai >= 60: return 'C+'
    elif nilai >= 55: return 'C'
    elif nilai >= 45: return 'D'
    else: return 'E'

def get_bobot(label):
    bobot = {'A':4,'A-':3.75,'B+':3.5,'B':3,'B-':2.75,'C+':2.5,'C':2,'D':1,'E':0}
    return bobot.get(label.upper(), "Label tidak valid")

def hitung_total_sks():
    jumlah_data = int(input("Jumlah Data: "))
    total_sks = 0

    for i in range(1, jumlah_data + 1):
        sks = int(input(f"sks {i}: "))
        total_sks += sks

    print(f"Total SKS: {total_sks}")
    return total_sks

def hitung_total_nilai(sks_list, nilai_list):
    total = 0
    for sks, nilai in zip(sks_list, nilai_list):
        label = get_label(nilai)
        bobot = get_bobot(label)
        total += sks * bobot
    return total

def hitung_ips(total_nilai, total_sks):
    return total_nilai / total_sks if total_sks > 0 else 0