import csv
import logging

from lab.reports import Report
from lab import tools


class CsvReport(Report):
    def __init__(self, attributes=None, filter=None, delimiter=',', **kwargs):
        self.attributes = tools.make_list(attributes)
        self.output_format = format
        self.toc = True
        self.run_filter = tools.RunFilter(filter, **kwargs)

        self.delimiter = delimiter


    def write(self):
        with open(self.outfile, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=self.delimiter)

            writer.writerow(self.attributes)

            for run in self.props.values():
                row = [get_attribute_value(attribute, run) for attribute in self.attributes]
                writer.writerow(row)

        logging.info(f"Wrote file://{self.outfile}")


def get_attribute_value(attribute: str, run_props: dict) -> str:
    if attribute in run_props:
        return str(run_props[attribute])

    return ""


