import os
import shutil
import subprocess
from typing import Dict, List, Optional

from test_case import TestCase

EXPERIMENT_NAME = "autocheck-experiment"
KEY_LENGTH = 16


class BasicProtocolsTestCase(TestCase):

    def __init__(self, key_length):
        super().__init__("Basic protocols", key_length)

    def _configure_test_case(self, experiment: Dict) -> None:
        pass

    def _verify_test_case(
            self,
            alice_secret_key: Optional[List[int]],
            bob_secret_key: Optional[List[int]]
    ) -> TestCase.Result:

        if alice_secret_key is None:
            return TestCase.Result(
                success=False,
                message=(
                    "Alice and/or Bob did not generate a secret key "
                    "even though no eavesdropper was present"
                ),
            )

        return TestCase.Result(success=True, message=None)


def run(test: TestCase, timeout: int = 60) -> bool:
    test.configure()

    result = subprocess.run(
        ["qne", "experiment", "run", "--timeout", str(timeout)],
        stdout=subprocess.DEVNULL,
    )
    if result.returncode != 0:
        raise RuntimeError("Experiment run failed")

    return test.verify()


def main():
    if os.path.exists(EXPERIMENT_NAME):
        shutil.rmtree(EXPERIMENT_NAME)

    result = subprocess.run(
        ["qne", "experiment", "create", EXPERIMENT_NAME, "qkd", "randstad"],
        stdout=subprocess.DEVNULL,
    )
    if result.returncode != 0:
        raise RuntimeError("Experiment creation failed")

    os.chdir(EXPERIMENT_NAME)

    success = run(BasicProtocolsTestCase(KEY_LENGTH))

    os.chdir("..")

    return success


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
