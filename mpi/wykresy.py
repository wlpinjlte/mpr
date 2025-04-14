import pandas as pd
import matplotlib.pyplot as plt

# Wczytaj dane
df = pd.read_csv("results.csv")

# Czasowe kolumny + etykiety
time_metrics = ['total_time', 'fill_time', 'partition_time', 'sort_time', 'merge_time']
time_labels = {
    'total_time': 'Całkowity',
    'fill_time': 'Wypełnianie',
    'partition_time': 'Partycjonowanie',
    'sort_time': 'Sortowanie',
    'merge_time': 'Scalanie'
}

# Typy skalowania i rozmiary kubełków
scaling_types = df['scaling'].unique()
bucket_sizes = sorted(df['avg_bucket_size'].unique())

# Tworzymy osobne figury dla każdego typu skalowania
for scaling in scaling_types:
    fig, axes = plt.subplots(1, len(bucket_sizes), figsize=(15, 5), sharey=True)
    if len(bucket_sizes) == 1:
        axes = [axes]

    data_scaling = df[df['scaling'] == scaling]

    for ax, bucket in zip(axes, bucket_sizes):
        data_bucket = data_scaling[data_scaling['avg_bucket_size'] == bucket]
        data_bucket = data_bucket.sort_values('threads')

        for time_col in time_metrics:
            ax.plot(
                data_bucket['threads'],
                data_bucket[time_col],
                label=time_labels[time_col],
                linestyle='solid',
                marker='o'
            )

        ax.set_title(f"{bucket} liczb w kubełku")
        ax.set_xlabel("Liczba wątków")
        ax.grid(True)
        ax.legend(fontsize='small', title="Typ czasu")

    axes[0].set_ylabel("Czas [s]")
    plt.suptitle(f"Czasy wykonania vs Liczba wątków\nTyp skalowania: {scaling.upper()}")
    plt.tight_layout(rect=[0, 0.03, 1, 0.93])
    plt.show()