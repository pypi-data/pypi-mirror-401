from .mortalite_tablosu import mortalite_tablosu


L0 = 100000

def hesapla_yasam_tablosu():
    lx = []
    dx = []
    Dx = []
    qx_list = []
    Lx_list = []

    l_anlik = L0

    for satir in mortalite_tablosu:
        isim = satir["age"]
        qx = satir["qx"]
        px = 1 - qx

        qx_list.append(qx)


        lx.append(l_anlik)


        d_olen=l_anlik * qx
        dx.append(d_olen)


        Lx = l_anlik - d_olen / 2
        Lx_list.append(Lx)


        Dx.append(Lx)


        l_anlik = l_anlik * px


    Nx = []
    toplam = 0
    for val in reversed(Dx):
        toplam += val
        Nx.append(toplam)
    Nx.reverse()


    Sx = [l / L0 for l in lx]


    Mx = [dx[i] / Dx[i] if Dx[i] > 0 else 0 for i in range(len(dx))]



    Rx = [Nx[i] / lx[i] if lx[i] > 0 else 0 for i in range(len(lx))]

    return lx, dx, Dx, Nx, Sx, Mx, Rx

lx, dx, Dx, Nx, Sx, Mx, Rx = hesapla_yasam_tablosu()



yas = int(input("Yaş girin (0-100): "))

if yas < 0 or yas > 100:
    print("Yaş aralığı 0-100 olmalıdır.")
    exit()


satir = None

for r in mortalite_tablosu:
    if r["age"] == yas:
        satir = r
        break

qx = satir["qx"]
px = 1 - qx


i = yas

print("\n--- MORTALİTE DEĞERLERİ ---")
print(f"Yaş: {yas}")
print(f"qx (ölme olasılığı): {qx:.5f}")
print(f"px (hayatta kalma olasılığı): {px:.5f}")
print(f"lx (sağ kalan): {lx[i]:.2f}")
print(f"dx (ölen): {dx[i]:.2f}")
print(f"Dx (yaşam yılı): {Dx[i]:.2f}")
print(f"Nx (kalan toplam yaşam yılı): {Nx[i]:.2f}")
print(f"Sx (sağ kalma oranı): {Sx[i]:.5f}")
print(f"Mx (ölüm yoğunluğu): {Mx[i]:.5f}")
print(f"Rx (ömür beklentisi): {Rx[i]:.5f}")
