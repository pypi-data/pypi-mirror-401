import time
import pytest
import shutil
import tempfile
import edna2.config

from edna2.utils import UtilsSlurm


def test_parse_salloc_stderr():
    stderr = """salloc: Pending job allocation 9420567
salloc: job 9420567 queued and waiting for resources
salloc: job 9420567 has been allocated resources
salloc: Granted job allocation 9420567
salloc: Nodes mxhpc3-2201 are ready for job
    """
    job_id = UtilsSlurm.parse_salloc_stderr(stderr)
    assert job_id == 9420567


@pytest.mark.skipif(
    not edna2.config.get_site().lower().startswith("esrf"),
    reason="Slurm exec test disabled when using non-ESRF config",
)
def test_salloc():
    partition = "mx"
    job_id = UtilsSlurm.salloc(partition=partition)
    assert job_id is not None
    UtilsSlurm.scancel(job_id)


@pytest.mark.skipif(
    not edna2.config.get_site().lower().startswith("esrf"),
    reason="Slurm exec test disabled when using non-ESRF config",
)
def test_srun():
    partition = "mx"
    job_id = UtilsSlurm.salloc(partition=partition)
    assert job_id is not None
    command = "whoami"
    stdout, stderr = UtilsSlurm.srun(job_id, command)
    assert stdout != ""
    assert stderr == ""
    command = "id"
    stdout, stderr = UtilsSlurm.srun(job_id, command)
    assert stdout != ""
    assert stderr == ""
    UtilsSlurm.scancel(job_id)


@pytest.mark.skipif(
    not edna2.config.get_site().lower().startswith("esrf"),
    reason="Slurm exec test disabled when using non-ESRF config",
)
def test_submit_job_to_slurm():
    command_line = "anode; xds"
    working_directory = tempfile.mkdtemp(
        dir="/data/scisoft/edna2", prefix="edna2_test_slurm_"
    )
    list_modules = ["ccp4", "xds"]
    slurm_script_path, slurm_id, job_stdout_path, job_stderr_path = (
        UtilsSlurm.submit_job_to_slurm(
            command_line=command_line,
            working_directory=working_directory,
            list_modules=list_modules,
            queue="nice",
        )
    )
    # Wait for stdout and stderr files
    start_time = time.time()
    while not job_stdout_path.exists() or not job_stderr_path.exists():
        time.sleep(1)
        if time.time() - start_time > 120:
            raise RuntimeError(
                f"Timeout while waiting for {job_stdout_path} and {job_stderr_path}"
            )
    with open(job_stdout_path) as f:
        job_stdout = f.read()
    assert slurm_script_path.exists()
    assert slurm_id is not None
    assert "ANODE - ANOmalous DEnsity analysis" in job_stdout
    assert "***** XDS *****" in job_stdout
    shutil.rmtree(working_directory)
