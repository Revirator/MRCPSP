import logging
import os
from typing import Callable, List

from lab.experiment import Experiment
from lab.tools import Properties


class SolverExperiment(Experiment):
    aggregate_statistics: List[Callable[[Properties], None]] = []

    def __init__(self, path=None, environment=None):
        super().__init__(path, environment)


    def add_aggregate_statistics(self, function: Callable[[Properties], None]):
        self.aggregate_statistics.append(function)


    def run_aggregate_statistics(self):
        props = self._load_data()
        if props is None:
            return

        for func in self.aggregate_statistics:
            func(props)

    
    def _load_data(self) -> Properties:
        props_file = os.path.join(self.eval_dir, "properties")
        logging.info("Reading properties file")
        props = Properties(filename=props_file)
        if not props:
            logging.critical(f"No properties found in {self.eval_dir}")
        logging.info("Reading properties file finished")
        return props

