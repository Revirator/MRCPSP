import platform
import reader
import reader_mmlib
import os
import sys
import time
from pathlib import Path
from pysat.formula import WCNF
from pysat.pb import PBEnc, EncType
from pysat.card import CardEnc


def encode_mmrpscp(filepath):
    """Encode the MRCPSP instance, located at that filepath, into MaxSAT.

    Args:
        filepath (String): Filepath to a *.mm file.

    Returns:
        WCNF: Weighted propositional formula in CNF.
    """
    start = time.time()
    
    if path.__contains__("mmlib"):
        N_ACT, N_RR_RES, N_NRR_RES, HORIZON, SUCC, MODES, MDUR, RR, RR_CAP, NRR, NRR_CAP = reader_mmlib.read(filepath)
    else:
        N_ACT, N_RR_RES, N_NRR_RES, HORIZON, SUCC, MODES, MDUR, RR, RR_CAP, NRR, NRR_CAP = reader.read(filepath)

    formula = WCNF()
    # append comments that the solver can use to obtain domain-specific knowledge about the problem
    formula.comments.append("c MRCPSP")
    formula.comments.append(f"c {N_ACT} {HORIZON}")
    mode = 0
    for i in range(N_ACT):
        for k in range(MODES[i]):
            mode += 1
            formula.comments.append(f"c {mode} {MDUR[i][k] + 1}")

    literal = 0
    # m_i,k = True if Activity i is executed in Mode k
    m_variables = [[literal := literal + 1 for _ in range(MODES[i])] for i in range(N_ACT)]
    # s_i,t = True if Activity i starts at Time t
    s_variables = [[literal := literal + 1 for _ in range(HORIZON + 1)] for _ in range(N_ACT)]
    # x_i,k,t = True if Activity i is executed in Mode k and is running at Time t
    x_variables = [[[literal := literal + 1 for _ in range(HORIZON)] for _ in range(MODES[i])] for i in range(N_ACT)]
    formula.nv = literal

    # add mode selection constraints
    for m in m_variables:
        # each Activity can be executed in exactly one mode
        clauses = CardEnc.equals(lits=m, bound=1, top_id=formula.nv)
        formula.extend(clauses)

    # add starting times constraints
    for i in range(N_ACT):
        # each Activity can start exactly once
        # NOTE: 'atleast' leads to better performance but the intermediate solutions that the solver finds will be incorrect
        clauses = CardEnc.equals(lits=s_variables[i], bound=1, top_id=formula.nv)
        formula.extend(clauses)

    # add completion constraints
    for i in range(N_ACT):
        for k in range(MODES[i]):
            # if Activity i is executed in Mode k with Duration d, then it must start with enough time left to finish (dummy UB)
            clause = [-m_variables[i][k]] + [s_variables[i][t] for t in range(HORIZON + 1 - MDUR[i][k])]
            formula.append(clause)

    # add precedence constraints
    for i in range(N_ACT):
        for j in SUCC[i]:
            for k in range(MODES[i]):
                for t in range(0, HORIZON + 1):
                    # if Activity j starts at Time t, then Activity i can start in Mode k with Duration d at the latest at t - d
                    clause = [-s_variables[j][t], -m_variables[i][k]] \
                        + [s_variables[i][t_prime] for t_prime in range(t + 1 - MDUR[i][k])]
                    formula.append(clause)

    # add consistency constraints 
    for i in range(1, N_ACT - 1):
        for k in range(MODES[i]):
            for t in range(HORIZON + 1 - MDUR[i][k]):
                # if Activity i starts at Time t in Mode k with Duration d, then it should be running from i to d (incl.)
                for t_prime in range(MDUR[i][k]):
                    clause = [-s_variables[i][t], -m_variables[i][k], x_variables[i][k][t + t_prime]]
                    formula.append(clause)

    # add non-renewable resources constraint
    for r in range(N_NRR_RES):
        modes = []
        resource_requirements = []
        for i in range(1, N_ACT - 1):
            for k in range(MODES[i]):
                if NRR[i][k][r] > 0:
                    modes.append(m_variables[i][k])
                    resource_requirements.append(NRR[i][k][r])
        if len(modes) > 0:
            clauses = PBEnc.atmost(lits=modes, weights=resource_requirements, bound=NRR_CAP[r], top_id=formula.nv, encoding=EncType.bdd)
            formula.extend(clauses)

    # add renewable resources constraint
    for r in range(N_RR_RES):
        for t in range(HORIZON):
            activities = []
            resource_requirements = []
            for i in range(1, N_ACT - 1):
                for k in range(MODES[i]):
                    if RR[i][k][r] > 0:
                        activities.append(x_variables[i][k][t])
                        resource_requirements.append(RR[i][k][r])
            if len(activities) > 0:
                clauses = PBEnc.atmost(lits=activities, weights=resource_requirements, bound=RR_CAP[r], top_id=formula.nv, encoding=EncType.bdd)
                formula.extend(clauses)

    # add objective function (makespan = cost - 1)
    for t in range(HORIZON + 1):
        formula.append([-s_variables[N_ACT - 1][t]], t + 1)

    print(f"Encoding took: {round(time.time() - start, 2)}s")
    return formula


if __name__ == "__main__":
    RUN_ON_CLUSTER = platform.node().startswith("login")
    OUTPUT_DIR = Path(__file__).parent.resolve().__str__() if not RUN_ON_CLUSTER else \
        "/scratch/" + os.environ.get("USER")
    OUTPUT_DIR += "/encodings/"
    filepath = sys.argv[1]

    path = filepath.split("/")
    dir = path[-2]
    filename = path[-1].split(".")[0]

    # preserve same folder structure as the 'instances' folder
    if dir != "instances":
        OUTPUT_DIR += f"{dir}/"

    formula = encode_mmrpscp(filepath)
    formula.to_file(OUTPUT_DIR + f"{filename}.wcnf")
