import pandas as pd
import matplotlib.pyplot as plt

# Wczytaj dane
df = pd.read_csv("results_.csv")

# Etykiety części algorytmu
time_labels = {
    'fill_time': 'Losowanie liczb',
    'partition_time': 'Rozdział liczb do kubełków',
    'sort_time': 'Sortowanie kubełków',
    'merge_time': 'Przepisanie kubełków',
    'total_time': 'Całość algorytmu'
}

time_metrics = list(time_labels.keys())
scaling_types = df['scaling'].unique()
bucket_sizes = sorted(df['avg_bucket_size'].unique())

# Funkcje obliczające metryki
def compute_speedup(df_sub, time_col, scaling):
    p = df_sub['threads']
    base_time = df_sub[df_sub['threads'] == 1][time_col].values[0]
    if scaling == 'weak':
        return (base_time / df_sub[time_col]) * p
    else:
        return base_time / df_sub[time_col]

def compute_efficiency(speedup, p):
    return speedup / p

def compute_serial_fraction(speedup, p):
    return ((1 / speedup) - (1 / p)) / (1 - (1 / p))

# Główna funkcja rysująca podwójne wykresy
def plot_double_metric(metric_name, compute_func, ylabel):
    for scaling in scaling_types:
        fig, axes = plt.subplots(1, len(bucket_sizes), figsize=(14, 5), sharey=True)
        fig.suptitle(f"{ylabel} — Skalowanie: {scaling.capitalize()}", fontsize=16)

        if len(bucket_sizes) == 1:
            axes = [axes]

        for ax, bucket in zip(axes, bucket_sizes):
            df_sub = df[(df['scaling'] == scaling) & (df['avg_bucket_size'] == bucket)].copy()
            p = df_sub['threads']
            for time_col in time_metrics:
                speedup = compute_speedup(df_sub, time_col, scaling)
                if metric_name == 'time':
                    y = df_sub[time_col]
                elif metric_name == 'speedup':
                    y = speedup
                elif metric_name == 'efficiency':
                    y = compute_efficiency(speedup, p)
                elif metric_name == 'serial':
                    y = compute_serial_fraction(speedup, p)

                ax.plot(p, y, marker='o', label=time_labels[time_col])

            ax.set_title(f"Rozmiar kubełka: {bucket}")
            ax.set_xlabel("Liczba wątków")
            ax.grid(True)
            if ax == axes[0]:
                ax.set_ylabel(ylabel)
            ax.legend(fontsize='small')

        plt.tight_layout(rect=[0, 0.03, 1, 0.92])
        plt.show()

# Tworzymy wykresy dla wszystkich metryk
plot_double_metric('time', None, 'Czas wykonania [s]')
plot_double_metric('speedup', compute_speedup, 'Przyspieszenie')
plot_double_metric('efficiency', compute_efficiency, 'Wydajność')
plot_double_metric('serial', compute_serial_fraction, 'Część sekwencyjna')