from abc import abstractmethod
from pathlib import Path
from typing import Dict, List
import logging

from lab.tools import Properties
import matplotlib.pyplot as plt
import numpy as np


class Aggregator:
    @abstractmethod
    def generate(self, props: Properties, outfile: Path):
        pass


class CactusPlot(Aggregator):
    def __init__(
            self, 
            group_by_key: str,
            completed_tag: str = "OPTIMAL"):
        self.group_by_key = group_by_key
        self.completed_tag = completed_tag


    def generate(self, props: Properties, outfile: Path):
        for label, y in self._process_data(props).items():
            x = list(range(1, len(y) + 1))
            plt.plot(x, y, label=label)

        plt.xlabel("Instances")
        plt.ylabel("Time (s)")
        plt.legend()
        plt.savefig(outfile, bbox_inches='tight')


    def _process_data(self, props: Properties) -> Dict[str, List[float]]:
        times = {}
        for run_id, run in props.items():
            if self.group_by_key not in run:
                logging.warn(f"'{self.group_by_key}' not present in run '{run_id}'. Skipping...")
                continue

            if run["status"] != self.completed_tag:
                status = run["status"]
                logging.info(f"'{run_id}' does not have status '{self.completed_tag}' but '{status}'. Skipping...")
                continue

            solve_time = float(run["solve_time"])
            if run[self.group_by_key] not in times:
                times[run[self.group_by_key]] = [solve_time]
            else:
                times[run[self.group_by_key]].append(solve_time)

        for group_key in times.keys():
            times[group_key].sort()
            times[group_key] = np.cumsum(times[group_key])

        return times

