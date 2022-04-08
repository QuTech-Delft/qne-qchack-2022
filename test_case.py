from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
from typing import Dict, List, Optional


class TestCase(ABC):

    @dataclass
    class Result:
        success: bool
        message: Optional[str]

    def __init__(self, name: str, key_length: int):
        self._name = name
        self._key_length = key_length

    def configure(self) -> None:
        with open("experiment.json", "r") as f:
            experiment = json.load(f)

        self._configure_key_length(experiment)
        self._configure_test_case(experiment)

        with open("experiment.json", "w") as f:
            json.dump(experiment, f)

    def _configure_key_length(self, experiment: Dict) -> None:
        key_length_var = experiment["asset"]["application"][0]["values"][0]
        assert key_length_var["name"] == "key_length"
        key_length_var["value"] = self._key_length

    @abstractmethod
    def _configure_test_case(self, experiment: Dict) -> None:
        raise NotImplementedError

    def verify(self) -> bool:
        with open(f"results/processed.json", "r") as f:
            results = json.load(f)

        round_result = results[0]["round_result"]
        if "error" in round_result:
            error = round_result["error"]
            exception = error["exception"]
            message = error["message"]
            self._print_result(TestCase.Result(success=False, message=f"{exception}: {message}"), 0)
            return False

        app_results = results[0]["round_result"][0]
        alice_secret_key = app_results["app_alice"]["secret_key"]
        bob_secret_key = app_results["app_bob"]["secret_key"]

        result = self._verify_test_case(alice_secret_key, bob_secret_key)

        if result.success:
            result = self._verify_key_match(alice_secret_key, bob_secret_key)

        epr_pairs = 0
        if result.success:
            instructions = results[0]["instructions"]
            entanglements = filter(
                lambda instr: (instr["command"] == "entanglement") and (instr["action"] == "success"),
                instructions,
            )
            epr_pairs = sum(1 for _ in entanglements)

        self._print_result(result, epr_pairs)
        return result.success

    def _verify_key_match(
            self,
            alice_secret_key: Optional[List[int]],
            bob_secret_key: Optional[List[int]]
    ) -> Result:
        if (alice_secret_key is not None) and (len(alice_secret_key) != self._key_length):
            return TestCase.Result(
                success=False,
                message="Alice's and/or Bob's secret key has incorrect length",
            )

        if alice_secret_key != bob_secret_key:
            return TestCase.Result(
                success=False,
                message="Alice's and Bob's secret keys do not match",
            )

        return TestCase.Result(success=True, message=None)


    @abstractmethod
    def _verify_test_case(
            self,
            alice_secret_key: Optional[List[int]],
            bob_secret_key: Optional[List[int]]
    ) -> Result:
        raise NotImplementedError

    def _print_result(self, result: Result, epr_pairs: int) -> None:
        print(
            f"{self._name} :: " + ("PASS" if result.success else "FAIL") + " :: " +
            (f"{epr_pairs} EPR pairs consumed" if result.success else result.message)
        )
