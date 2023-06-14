from pathlib import Path
import platform
import os

from lab.environments import LocalEnvironment
from lab.experiment import Experiment

from framework.environments import DelftBlueEnvironment
from framework.experiment import SolverExperiment
from framework.reports import CsvReport


SCRIPT_DIR = Path(__file__).parent.resolve()

# Indicates whether the experiment is run locally or on a cluster.
RUN_ON_CLUSTER = platform.node().startswith("login")


# The attributes which are put into the report. These are gathered by parsers 
# during the 'fetch' step or the 'parse_again' step.
ATTRIBUTES = []

# Describe the environment on which the experiment is run. By default, the
# following are implemented:
#   - lab.environments.LocalEnvironment
#   - lab.environments.SlurmEnvironment
#   - framework.environments.DelftBlueEnvironment (a SlurmEnvironment 
#         specifically for DelftBlue)
ENV = LocalEnvironment() if not RUN_ON_CLUSTER \
        else DelftBlueEnvironment(email=...,
                                  account=...,
                                  time_limit_per_task=...,
                                  memory_per_cpu=...)

# The folder in which experiment files are generated.
EXP_PATH = SCRIPT_DIR / "data" / "exp" if not RUN_ON_CLUSTER \
        else SCRIPT_DIR / "data" / "exp"

BENCHMARK_PATH = SCRIPT_DIR / "instances" if not RUN_ON_CLUSTER \
        else SCRIPT_DIR / "instances"

ENCODINGS_PATH = SCRIPT_DIR / "encodings" if not RUN_ON_CLUSTER \
        else "/scratch/" + os.environ.get("USER") + "/encodings"

# The parsers in the 'framework/parsers' directory, which you want to apply to
# the logs of the experiment.
# Values in this array should be just the stem of the file, so no directories
# and no '.py' suffix.
PARSERS = []


def add_runs(experiment: Experiment):
    for root, dirs, files in os.walk(BENCHMARK_PATH):
        if root == BENCHMARK_PATH.__str__():
            if not os.path.exists(ENCODINGS_PATH):
                os.mkdir(ENCODINGS_PATH)
            for dir in dirs:
                if not os.path.exists(ENCODINGS_PATH / dir):
                    os.mkdir(ENCODINGS_PATH / dir)
        for file in files:
            if not file.endswith("mm"):
                continue
            filepath = root.__str__() + "/" + file
            filename = file.split('.')[0]
            run = experiment.add_run()
            run.set_property("id", [f"{filename}"])
            run.add_command(f"encoding_{filename}", ["python3", f"{SCRIPT_DIR}/encoder.py", f"{filepath}"])


def runner():
    exp = SolverExperiment(environment=ENV, path=EXP_PATH)

    for parser in PARSERS:
        exp.add_parser(f"framework/parsers/{parser}.py")

    add_runs(exp)

    exp.add_step("build", exp.build)
    exp.add_step("start", exp.start_runs)
    exp.add_fetcher(name="fetch")
    exp.add_parse_again_step()

    # Add reporting steps to the experiment. By default, we give a CSV report of 
    # all the specified attributes. However, you can add more reports or replace
    # the one given here.
    exp.add_report(CsvReport(attributes=ATTRIBUTES), outfile="report.csv")

    exp.run_steps()


if __name__ == "__main__":
    runner()
