import shlex
import pathlib
import subprocess
import threading


def run_command_line(command_line, timeout_sec=120):
    proc = subprocess.Popen(
        shlex.split(command_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    kill_proc = lambda p: p.kill()  # noqa E731
    timer = threading.Timer(timeout_sec, kill_proc, [proc])
    try:
        timer.start()
        binaryStdout, binaryStderr = proc.communicate()
        stdout = binaryStdout.decode("utf-8")
        stderr = binaryStderr.decode("utf-8")
    finally:
        timer.cancel()
    return stdout, stderr


def parse_salloc_stderr(stderr):
    job_id = None
    list_lines = stderr.split("\n")
    for line in list_lines:
        if line.startswith("salloc: Granted job allocation"):
            job_id = int(line.split(" ")[-1])
            break
    return job_id


def salloc(partition, exclusive=False):
    timeout_sec = 100
    salloc_command_line = f"salloc --no-shell -p {partition}"
    if exclusive:
        salloc_command_line += " --exclusive"
    stdout, stderr = run_command_line(salloc_command_line, timeout_sec)
    job_id = parse_salloc_stderr(stderr)
    if job_id is None:
        print(stdout)
        print(stderr)
    return job_id


def srun(job_id, command):
    timeout_sec = 10
    srun_command_line = f"srun --jobid {job_id} {command}"
    stdout, stderr = run_command_line(srun_command_line, timeout_sec)
    return stdout, stderr


def scancel(job_id):
    timeout_sec = 10
    scancel_command_line = f"scancel {job_id}"
    stdout, stderr = run_command_line(scancel_command_line, timeout_sec)


def submit_job_to_slurm(
    command_line,
    working_directory,
    nodes=1,
    core=4,
    time="2:00:00",
    host=None,
    queue="mx",
    name=None,
    mem=None,
    list_modules=None,
    asynchronous=True,
):
    slurm_id = None
    working_directory = pathlib.Path(working_directory)
    script_name = "slurm.sh"
    slurm_script_path = working_directory / script_name
    job_stdout_path = working_directory / "stdout.txt"
    job_stderr_path = working_directory / "stderr.txt"
    script = "#!/bin/bash -l\n"
    if name is not None:
        script += '#SBATCH --job-name="{0}"\n'.format(name)
    script += "#SBATCH --partition={0}\n".format(queue)
    if mem is None:
        mem = 8000  # 8 Gb memory by default
    script += f"#SBATCH --mem={mem}\n"
    script += f"#SBATCH --ntasks={nodes}\n"
    script += "#SBATCH --nodes=1\n"  # Necessary for not splitting jobs! See ATF-57
    script += f"#SBATCH --cpus-per-task={core}\n"
    script += f"#SBATCH --time={time}\n"
    script += f"#SBATCH --output={job_stdout_path}\n"
    script += f"#SBATCH --error={job_stderr_path}\n"
    script += f"#SBATCH --chdir={working_directory}\n"
    if list_modules is not None:
        for module_name in list_modules:
            script += f"module load {module_name}\n"
    script += command_line + "\n"
    with open(slurm_script_path, "w") as f:
        f.write(script)
    slurm_command = "sbatch --export None"
    if not asynchronous:
        slurm_command += " --wait"
    stdout, stderr = run_command_line(f"{slurm_command} {slurm_script_path}")
    if "Submitted batch job" in stdout:
        slurm_id = int(stdout.split("job")[1])
    return slurm_script_path, slurm_id, job_stdout_path, job_stderr_path


def split_at_equal(line, dict_line={}):
    if "=" in line:
        key, value = line.split("=", 1)
        if "=" in value:
            if " " in value:
                part1, part2 = value.split(" ", 1)
            elif "," in value:
                part1, part2 = value.split(",", 1)
            dict_line[key.strip()] = part1.strip()
            dict_line = split_at_equal(part2, dict_line=dict_line)
        else:
            dict_line[key.strip()] = value.strip()
    return dict_line


def parse_slurm_stat(slurmStat):
    list_lines = slurmStat.split("\n")
    dict_slurm_stat = {}
    for line in list_lines:
        if line != "":
            dictLine = split_at_equal(line)
            dict_slurm_stat.update(dictLine)
    return dict_slurm_stat


def get_slurm_stat(slurm_job_id):
    dict_stat = None
    stdout, stderr = run_command_line("scontrol show job {0}".format(slurm_job_id))
    if stderr is None or stderr == "":
        dict_stat = parse_slurm_stat(stdout)
    return dict_stat


def are_jobs_pending(partition_name=None):
    jobs_are_pending = False
    if partition_name is not None:
        stdout, stderr = run_command_line(
            "squeue -p {0} -t PENDING".format(partition_name)
        )
    else:
        stdout, stderr = run_command_line("squeue -t PENDING")
    list_lines = stdout.split("\n")
    no_pending = 0
    for line in list_lines:
        if "Resources" in line or "Priority" in line:
            no_pending += 1
    if no_pending > 2:
        jobs_are_pending = True
    return jobs_are_pending
