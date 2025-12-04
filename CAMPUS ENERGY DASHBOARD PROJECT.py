#CAMPUS ENERGY DASHBOARD PROJECT

import os
import pandas as pd
import matplotlib.pyplot as plt


# LOADING AND COMBINING CSV FILES

def load_data(folder="DATA"):
    data_list = []

    for file in os.listdir(folder):
        if file.endswith(".csv"):
            path = os.path.join(folder, file)
            print(os.listdir("C:/Users/Nimarta/Desktop/DATA"))

            try:
                df = pd.read_csv(path)

                # Adding building name from file name
                df["building"] = file.replace(".csv", "")

                # Converting timestamp to datetime
                df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

                data_list.append(df)

            except:
                print(f"Error reading {file}")

    if data_list:
        return pd.concat(data_list, ignore_index=True)
    else:
        return pd.DataFrame()


# OOP CLASSES

class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh


class Building:
    def __init__(self, name):
        self.name = name
        self.readings = []

    def add_reading(self, timestamp, kwh):
        self.readings.append(MeterReading(timestamp, kwh))

    def total_usage(self):
        return sum(r.kwh for r in self.readings)


class BuildingManager:
    def __init__(self):
        self.buildings = {}

    def load_from_dataframe(self, df):
        for _, row in df.iterrows():
            name = row["building"]

            if name not in self.buildings:
                self.buildings[name] = Building(name)

            self.buildings[name].add_reading(row["timestamp"], row["kwh"])



# CALCULATIONS

def daily_totals(df):
    df = df.set_index("timestamp")
    return df["kwh"].resample("D").sum()

def weekly_totals(df):
    df = df.set_index("timestamp")
    return df["kwh"].resample("W").sum()

def building_summary(df):
    return df.groupby("building")["kwh"].agg(["sum", "mean", "min", "max"])



def create_dashboard(df):
    plt.figure(figsize=(12, 10))

    #  Daily Line Chart
    plt.subplot(3, 1, 1)
    plt.plot(daily_totals(df))
    plt.title("Daily Electricity Usage")
    plt.ylabel("kWh")

    #  Weekly Bar Chart
    plt.subplot(3, 1, 2)
    weekly = weekly_totals(df)
    plt.bar(weekly.index, weekly.values)
    plt.title("Weekly Electricity Usage")
    plt.ylabel("kWh")

    #  Scatter Plot of All Readings
    plt.subplot(3, 1, 3)
    plt.scatter(df["timestamp"], df["kwh"])
    plt.title("All Meter Readings")
    plt.xlabel("Time")
    plt.ylabel("kWh")

    plt.tight_layout()
    plt.savefig("dashboard.png")
    print("Dashboard saved as dashboard.png")



# SAVING OUTPUTS

def save_outputs(df):

    # Saving cleaned data
    df.to_csv("cleaned_energy_data.csv", index=False)
    print("Saved cleaned_energy_data.csv")

    # Saving building summary
    summary = building_summary(df)
    summary.to_csv("building_summary.csv")
    print("Saved building_summary.csv")

    # creating  text report
    total = df["kwh"].sum()
    highest = summary["sum"].idxmax()
    peak_time = df.loc[df["kwh"].idxmax(), "timestamp"]

    with open("summary.txt", "w") as f:
        f.write("CAMPUS ENERGY REPORT\n")
        f.write("-----------------------------\n")
        f.write(f"Total Campus Consumption: {total} kWh\n")
        f.write(f"Highest Consuming Building: {highest}\n")
        f.write(f"Peak Load Timestamp: {peak_time}\n")

    print("Saved summary.txt")

# MAIN PROGRAM

def main():
    print("Loading data...")
    df = load_data("C:/Users/Nimarta/Desktop/DATA")

    if df.empty:
        print("No CSV files found. Add files in /data folder.")
        return

    print("Creating building objects...")
    manager = BuildingManager()
    manager.load_from_dataframe(df)

    print("Generating dashboard...")
    create_dashboard(df)

    print("Saving outputs...")
    save_outputs(df)

    print("\nAll tasks completed successfully!")


if __name__ == "__main__":
    main()
