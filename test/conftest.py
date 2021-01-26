import ctypes
import os.path
import signal
import subprocess
from distutils.version import LooseVersion
from time import sleep

import pytest


def _set_pdeathsig(sig=signal.SIGTERM):
    """help function to ensure once parent process exits, its childrent processes will automatically die"""

    def callable():
        libc = ctypes.CDLL("libc.so.6")
        return libc.prctl(1, sig)

    return callable


@pytest.fixture(scope="function")
def broker():
    try:
        # Actually mosquitto doesn't support -v param so let's stuff some junk - it will return the
        # version anyways.
        ret = subprocess.run(["mosquitto", "--foo"], check=False, capture_output=True)
    except OSError:
        pytest.skip("mosquitto not found on PATH - skipping broker related tests.")
    if ret.returncode != 3:
        pytest.skip("mosquitto not found on PATH - skipping broker related tests.")

    for line in ret.stdout.decode().splitlines():
        if "version" in line:
            *_, raw_version = line.rpartition(" ")
            version = LooseVersion(raw_version)
            if version < "2":
                pytest.skip("Mosquitto >=2.0.0 is required for the tests.")
            break

    config = os.path.abspath(os.path.join(os.path.dirname(__file__), "mqtt.conf"))

    process = subprocess.Popen(
        ["mosquitto", "-c", config],
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        preexec_fn=_set_pdeathsig(signal.SIGTERM),
        bufsize=-1,
    )

    sleep(1)

    yield

    process.kill()
    process.wait()
