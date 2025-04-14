import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns

# Wczytaj dane z CSV
df = pd.read_csv('data_pi_2.csv')


# Funkcja do obliczeń statystycznych
def compute_statistics(df, problem_size, scaling):
    subset = df[df['problem_size'] == problem_size]
    subset = subset[subset['scaling'] == scaling]
    stats = subset.groupby(['threads']).agg(
        mean_time=('time', 'mean'),
        std_time=('time', 'std'),
    ).reset_index()

    return stats


# Funkcja do obliczania przyspieszenia (speedup), efektywności (efficiency) i części sekwencyjnej (serial fraction)
def calculate_metrics(stats, scaling):
    # Przyspieszenie (Speedup)
    if scaling == 'weak':
        stats['speedup'] = stats['mean_time'].transform(lambda x: (x.iloc[0] * (x.index + 1)) / x)
    else:
        stats['speedup'] = stats['mean_time'].transform(lambda x: x.iloc[0] / x)

    # Efektywność (Efficiency)
    stats['efficiency'] = stats['speedup'] / stats['threads']
    print(stats['mean_time'])
    print(stats['speedup'])
    # Część sekwencyjna (Serial Fraction)
    stats['serial_fraction'] = stats['speedup'].transform(lambda x: (1 / x - 1 / (x.index + 1)) / (1 - 1 / (x.index + 1)))
    stats['serial_fraction'] = stats['serial_fraction']
    return stats


# L
# Przygotowanie wykresów
fig, axs = plt.subplots(2, 2, figsize=(15, 12))  # 4 wykresy na jednym zestawie
problem_sizes = [100000, 10000000, 1000000000]

# Zmienna do przechowywania wykresów dla różnych skalowań
scalings = ["strong", "weak"]

# Pętla po różnych typach skalowania
for scaling in scalings:
    # Nowe wykresy dla każdego skalowania (2x2)
    fig, axs = plt.subplots(2, 2, figsize=(15, 12))

    for i, problem_size in enumerate(problem_sizes):
        # Oblicz statystyki dla danego rozmiaru problemu i skalowania
        stats = compute_statistics(df, problem_size, scaling)
        stats = calculate_metrics(stats, scaling)
        print(f"Obliczenia dla {scaling} skalowania, Problem size {problem_size}")
        print(stats)

        # Zależność czasu od liczby procesorów (dodajemy do wykresu)
        axs[0, 0].errorbar(stats['threads'], stats['mean_time'], yerr=stats['std_time'], fmt='-o',
                           label=f'Problem size {problem_size}')

        # Zależność przyspieszenia (speedup) od liczby procesorów (dodajemy do wykresu)
        axs[0, 1].plot(stats['threads'], stats['speedup'], '-o', label=f'Problem size {problem_size}')

        # Zależność efektywności (efficiency) od liczby procesorów (dodajemy do wykresu)
        axs[1, 0].plot(stats['threads'], stats['efficiency'], '-o', label=f'Problem size {problem_size}')

        # Zależność części sekwencyjnej (serial fraction) od liczby procesorów (dodajemy do wykresu)
        axs[1, 1].plot(stats['threads'], stats['serial_fraction'], '-o', label=f'Problem size {problem_size}')

    # Ustawienia dla wykresów
    axs[0, 0].set_title(f'Czas vs Liczba procesorów ({scaling} scaling)')
    axs[0, 0].set_xlabel('Liczba procesorów')
    axs[0, 0].set_ylabel('Czas[s]')
    axs[0, 0].legend()

    axs[0, 1].set_title(f'Przyspieszenie vs Liczba procesorów ({scaling} scaling)')
    axs[0, 1].set_xlabel('Liczba procesorów')
    axs[0, 1].set_ylabel('Przyspieszenie (Speedup)')
    axs[0, 1].legend()

    axs[1, 0].set_title(f'Efektywność vs Liczba procesorów ({scaling} scaling)')
    axs[1, 0].set_xlabel('Liczba procesorów')
    axs[1, 0].set_ylabel('Efektywność')
    axs[1, 0].legend()

    axs[1, 1].set_title(f'Część sekwencyjna vs Liczba procesorów ({scaling} scaling)')
    axs[1, 1].set_xlabel('Liczba procesorów')
    axs[1, 1].set_ylabel('Część sekwencyjna')
    axs[1, 1].legend()

    # Dostosowanie układu wykresów
    plt.tight_layout()
    plt.show()
