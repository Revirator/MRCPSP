#! /usr/bin/env python

from lab.parser import Parser


if __name__ == "__main__":
    parser = Parser()

    parser.add_pattern("benchmark", r".*solving_([jmnr][0-9]+_[0-9]+).*$", \
                       type=str, flags="M", required=False, file="driver.log")
    parser.add_pattern("status", r"^s ([A-Z]+)$", type=str, flags="M", required=False, file="run.log")
    parser.add_pattern("wall_time", r"^w ([0-9\.]+m?s)$", type=str, flags="M", required=False, file="run.log")
    parser.add_pattern("cpu_time", r"^c ([0-9\.]+m?s)$", type=str, flags="M", required=False, file="run.log")
    parser.add_pattern("number_of_decisions", r"^d ([0-9]+)$", type=int, flags="M", required=False, file="run.log")

    parser.parse()

