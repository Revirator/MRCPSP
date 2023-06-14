from lab.environments import SlurmEnvironment


class DelftBlueEnvironment(SlurmEnvironment):
    MAX_TASKS = 1_000

    def __init__(
        self, 
        email=None, 
        account="innovation", 
        partition="compute", 
        time_limit_per_task=None, 
        memory_per_cpu=None,
        qos="normal"
    ):
        super().__init__(
            email=email, 
            extra_options=f"#SBATCH --account={account}", 
            partition=partition, 
            time_limit_per_task=time_limit_per_task, 
            memory_per_cpu=memory_per_cpu,
            qos=qos)

