import logging
from pathlib import Path
import os

from lab import tools
from lab.experiment import Experiment

from framework.aggregators import Aggregator


class SolverExperiment(Experiment):
    def __init__(self, path=None, environment=None):
        super().__init__(path, environment)


    def add_aggregator(self, aggregator: Aggregator, outfile: str):
        def run_aggregator():
            props_file = os.path.join(self.eval_dir, "properties")
            logging.info("Reading properties file")
            props = tools.Properties(filename=props_file)
            if not props:
                logging.critical(f"No properties found in {self.eval_dir}")
                return
            logging.info("Reading properties file finished")

            aggregator.generate(props, Path(self.eval_dir) / outfile)

        self.add_step(outfile, run_aggregator)

