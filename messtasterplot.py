import csv
import datetime
import matplotlib
matplotlib.use("Agg")  # GUI-freies Backend
import matplotlib.pyplot as plt

def plot_tod_csv(filename, output_png="plot.png"):
    times = []
    values = []

    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            if len(row) != 2:
                continue

            timestamp_str = row[0].replace("TOD#", "").strip()

            # Millisekunden ergänzen, falls sie fehlen
            if "." not in timestamp_str:
                timestamp_str += ".000"

            value = float(row[1].replace(",", "."))

            # Zu datetime parsen
            t = datetime.datetime.strptime(timestamp_str, "%H:%M:%S.%f")

            times.append(t)
            values.append(value)

    # Zeiten in Sekunden umrechnen
    t0 = times[0]
    seconds = [(t - t0).total_seconds() for t in times]

    # Plot erstellen
    plt.figure(figsize=(10, 5))
    plt.plot(seconds, values)
    plt.xlabel("Zeit [s]")
    plt.ylabel("Wert")
    plt.title("Plot aus TOD-CSV")
    plt.grid(True)
    plt.tight_layout()

    # Direkt als PNG speichern
    plt.savefig(output_png)
    print(f"Plot gespeichert als {output_png}")

# Beispielaufruf
plot_tod_csv(r".\data\2025-12-08-16_46_44_Wegmessung.csv", "wegmessung_plot.png")
