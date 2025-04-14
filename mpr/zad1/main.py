import matplotlib.pyplot as plt
import pandas as pd

# Wczytanie czterech plików CSV
data1 = pd.read_csv('bsend_vnode1.csv')
data2 = pd.read_csv('bsend_vnode56.csv')
data3 = pd.read_csv('isend_vnode1.csv')
data4 = pd.read_csv('isend_vnode56.csv')

# Tworzenie wykresu
plt.figure(figsize=(10, 8))

# Wykres 1 - CSV1
plt.scatter(data1['Size'], data1['Bandwidth'], color='blue', label='bsend vnode 1')
plt.plot(data1['Size'], data1['Bandwidth'], color='blue', alpha=0.5)

# Wykres 2 - CSV2
plt.scatter(data2['Size'], data2['Bandwidth'], color='green', label='bsend vnode 5 and 6')
plt.plot(data2['Size'], data2['Bandwidth'], color='green', alpha=0.5)

# Wykres 3 - CSV3
plt.scatter(data3['Size'], data3['Bandwidth'], color='red', label='isend vnode 1')
plt.plot(data3['Size'], data3['Bandwidth'], color='red', alpha=0.5)

# Wykres 4 - CSV4
plt.scatter(data4['Size'], data4['Bandwidth'], color='purple', label='isend vnode 5 and 6')
plt.plot(data4['Size'], data4['Bandwidth'], color='purple', alpha=0.5)

# Skala logarytmiczna
plt.xscale('log')
# plt.yscale('log')  # Jeśli chcesz także logarytmiczną oś Y, odkomentuj

# Tytuł i etykiety
plt.title('Size vs Bandwidth (Log Scale)')
plt.xlabel('Size (Log Scale) [Bit]')
plt.ylabel('Bandwidth [MB/s]')

# Legenda
plt.legend()

# Wyświetlenie wykresu
plt.tight_layout()
plt.show()
