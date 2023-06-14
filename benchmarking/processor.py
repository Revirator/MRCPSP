import pandas as pd
import re
import os
import time
from pathlib import Path


def process():
    start = time.time()

    SCRIPT_DIR = Path(__file__).parent.resolve()
    EXP_DIR = SCRIPT_DIR / "data" / "exp"
    REPORT_CSV = SCRIPT_DIR / "data" / "exp-eval" / "report.csv"
    PROCESSED_CSV = SCRIPT_DIR / "data" / "exp-eval" / "processed.csv"
    R_SOLUTION = r"^o \d+"
    R_BENCHMARK = r".*solving_([jmnr][0-9]+_[0-9]+).*"

    df = pd.read_csv(REPORT_CSV)
    df.dropna(inplace=True)
    df["number_of_solutions"] = 0

    for root, _, files in os.walk(EXP_DIR):
        n_solutions = 0
        benchmark = ""
        for file in files:
            if file == "run.log":
                lines = open(root + "/" + file, 'r').readlines()
                for line in lines:
                    if re.match(R_SOLUTION, line):
                        n_solutions += 1
            if file == "driver.log":
                lines = open(root + "/" + file, 'r').readlines()
                for line in lines:
                    match = re.match(R_BENCHMARK, line)
                    if match:
                        benchmark = match.group(1)
                        break
        if benchmark != "":
            df.loc[df["benchmark"] == benchmark, 'number_of_solutions'] = n_solutions

    j20_df = process_by_benchmark(df, "j20")
    j30_df = process_by_benchmark(df, "j30")
    m5_df = process_by_benchmark(df, "m5")
    n3_df = process_by_benchmark(df, "n3")
    r5_df = process_by_benchmark(df, "r5")

    combined_df = pd.concat([j20_df, j30_df, m5_df, n3_df, r5_df])
    combined_df.to_csv(PROCESSED_CSV, index=False)

    print(f"Processing took: {round(time.time() - start, 2)}s")


def process_by_benchmark(df, benchmark):
    df_copy = df[df['benchmark'].str.startswith(benchmark)].copy()
    df_copy["benchmark"] = df_copy["benchmark"].map(lambda _: benchmark)
    df_copy["cpu_time"] = df["cpu_time"].map(lambda c: get_time(c))
    df_copy["wall_time"] = df["wall_time"].map(lambda w: get_time(w))
    statuses = df_copy["status"].value_counts().to_dict().__str__()
    df_copy.drop("status", axis=1, inplace=True)

    grouped_df = df_copy.groupby("benchmark").agg({"cpu_time": "mean", \
                                                   "wall_time": "mean", \
                                                   "number_of_solutions": "mean", \
                                                   "number_of_decisions": "mean"}).reset_index()
    grouped_df["cpu_time"] = grouped_df["cpu_time"].map(lambda t: round(t, 2))
    grouped_df["wall_time"] = grouped_df["wall_time"].map(lambda t: round(t, 2))
    grouped_df["number_of_solutions"] = grouped_df["number_of_solutions"].map(lambda s: int(s))
    grouped_df["number_of_decisions"] = grouped_df["number_of_decisions"].map(lambda d: int(d))
    grouped_df["statuses"] = statuses
    grouped_df = grouped_df.rename(columns={"cput_time": "average_cpu_time", \
                                            "wall_time": "average_wall_time", \
                                            "number_of_solutions": "average_number_of_solutions", \
                                            "number_of_decisions": "average_number_of_decisions"})
    return grouped_df


def get_time(time):
    if time[-2] == "m":
        return float(time[:-2]) / 1000
    return float(time[:-1])


if __name__ == "__main__":
    process()