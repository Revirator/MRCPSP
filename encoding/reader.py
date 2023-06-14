def read(filepath):
    """Parses the contents of an *.mm file at the provided location and returns them
    as MRCPSP instance.

    Args:
        filepath (String): Filepath to a *.mm file that needs to be parsed.

    Returns:
        N_ACT (int): number of activities (incl. start and end).
        N_RR_RES (int): number of renewable resources.
        N_NRR_RES (int): number of non-renewable resources.
        HORIZON (int): planning horizon.
        SUCC (list(list(int))): successors of activity.
        MODES (list(int)): number of modes per activity.
        MDUR (list(list(int))): duration of modes per activity.
        RR (list(list(list(int)))): renewable resource requirements per mode per activity.
        RR_CAP (list(int)): capacities per renewable resource.
        NRR (list(list(list(int)))): non-renewable resource requirements per mode per activity.
        NRR_CAP (list(int)): capacities per non-renewable resource.
    """
    lines = open(filepath, 'r').readlines()
    curr = 5
    N_ACT = int(lines[curr].split()[-1])
    curr += 1
    HORIZON = int(lines[curr].split()[-1])
    curr += 2      
    N_RR_RES = int(lines[curr].split()[-2])
    curr += 1
    N_NRR_RES = int(lines[curr].split()[-2])
    curr += 9

    MODES = []
    SUCC = []  
    for _ in range(N_ACT):
        line = lines[curr].split()
        MODES.append(int(line[1]))
        succ = [int(line[i]) - 1 for i in range(3, len(line))]
        SUCC.append(succ)
        curr += 1

    curr += 4
    NRR = []
    RR = []
    MDUR = []
    for i in range(N_ACT):
        mdur = []
        rr_m = []
        nrr_m = []
        for _ in range(MODES[i]):
            nrr = []
            rr = []
            line = lines[curr].split()
            for j in range(N_NRR_RES, 0, -1):
                nrr.append(int(line[-j]))
            for j in range(N_RR_RES + N_NRR_RES, N_NRR_RES, -1):
                rr.append(int(line[-j]))
            nrr_m.append(nrr)
            rr_m.append(rr)
            mdur.append(int(line[-(N_RR_RES + N_NRR_RES + 1)]))
            curr += 1
        NRR.append(nrr_m)
        RR.append(rr_m)
        MDUR.append(mdur)

    curr += 3
    RR_CAP = []
    NRR_CAP = []
    for i, cap in enumerate(lines[curr].split()):
        if i < N_RR_RES:
            RR_CAP.append(int(cap))
        else:
            NRR_CAP.append(int(cap))

    return N_ACT, N_RR_RES, N_NRR_RES, HORIZON, SUCC, MODES, MDUR, RR, RR_CAP, NRR, NRR_CAP