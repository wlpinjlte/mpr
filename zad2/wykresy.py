import pandas as pd
import matplotlib.pyplot as plt

# Wczytanie danych
df = pd.read_csv("wy.csv")

# Iteracja po schedulerach i rozmiarach problemu
for scheduler in df['schedule'].unique():
    for size in df['size'].unique():
        df_sub = df[(df['schedule'] == scheduler) & (df['size'] == size)]

        # WYKRES 1: Czas vs liczba wątków
        plt.figure(figsize=(10, 6))
        for chunk in df_sub['chunk'].unique():
            df_chunk = df_sub[df_sub['chunk'] == chunk].sort_values('threads')
            plt.plot(df_chunk['threads'], df_chunk['avg_time'], marker='o', label=f'chunk={chunk}')

        plt.title(f'Czas wykonania vs liczba wątków\nScheduler: {scheduler}, Size: {size}')
        plt.xlabel('Liczba wątków')
        plt.ylabel('Średni czas [s]')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"time_vs_threads_{scheduler}_size{size}.png")
        plt.show()

        # WYKRES 2: Przyspieszenie vs liczba wątków
        plt.figure(figsize=(10, 6))
        for chunk in df_sub['chunk'].unique():
            df_chunk = df_sub[df_sub['chunk'] == chunk].sort_values('threads')
            baseline_time = df_chunk[df_chunk['threads'] == 1]['avg_time'].values[0]
            speedup = baseline_time / df_chunk['avg_time']
            plt.plot(df_chunk['threads'], speedup, marker='o', label=f'chunk={chunk}')

        plt.title(f'Przyspieszenie vs liczba wątków\nScheduler: {scheduler}, Size: {size}')
        plt.xlabel('Liczba wątków')
        plt.ylabel('Przyspieszenie (speedup)')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"speedup_vs_threads_{scheduler}_size{size}.png")
        plt.show()
