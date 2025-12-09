import csv
import datetime
import matplotlib
import os
matplotlib.use("Agg")  # GUI-freies Backend
import matplotlib.pyplot as plt

def plot_multiple_tod_csv_from_folder(folder_path, legends, output_png="wegmessung_plot.png"):
    # Alle CSV-Dateien im Ordner sammeln
    filenames = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(".csv")]

    if len(filenames) != len(legends):
        raise ValueError("Anzahl der Legenden muss gleich der Anzahl der CSV-Dateien im Ordner sein.")

    plt.figure(figsize=(10, 5))

    for file, label in zip(filenames, legends):
        times = []
        values = []

        with open(file, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                if len(row) != 2:
                    continue

                timestamp_str = row[0].replace("TOD#", "").strip()

                if "." not in timestamp_str:
                    timestamp_str += ".000"

                value = float(row[1].replace(",", "."))

                t = datetime.datetime.strptime(timestamp_str, "%H:%M:%S.%f")

                times.append(t)
                values.append(value)

        # Zeiten in Sekunden umrechnen
        t0 = times[0]
        seconds = [(t - t0).total_seconds() for t in times]

        plt.plot(seconds, values, label=label)

    plt.xlabel("Zeit [s]")
    plt.ylabel("Weg [mm]")
    plt.title("Kolbenposition bei Druckbelichtung mit 5% Intensität")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_png)
    print(f"Plot gespeichert als {output_png}")


# Beispielaufruf
folder = r".\data\01"  # Pfad zum Ordner mit den CSV-Dateien
legends = [
        "0.5 bar",
        "0 bar",
        "1 bar",
        "0.25 bar"
        # ... usw.
]
plot_multiple_tod_csv_from_folder(folder, legends)