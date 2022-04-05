import json
import os
import shutil
import subprocess

EXPERIMENT_NAME = "autocheck-experiment"
KEY_LENGTH = 16


def main():

    result = subprocess.run(
        ["qne", "experiment", "create", EXPERIMENT_NAME, "qkd", "randstad"],
        stdout=subprocess.DEVNULL,
    )
    if result.returncode != 0:
        raise RuntimeError("Experiment creation failed")

    os.chdir(EXPERIMENT_NAME)

    with open("experiment.json", "r") as f:
        experiment_inputs = json.load(f)

    variables = experiment_inputs["asset"]["application"]
    key_length_var = variables[0]["values"][0]
    assert key_length_var["name"] == "key_length"
    key_length_var["value"] = KEY_LENGTH

    with open("experiment.json", "w") as f:
        json.dump(experiment_inputs, f)

    result = subprocess.run(
        ["qne", "experiment", "run"],
        stdout=subprocess.DEVNULL,
    )
    if result.returncode != 0:
        raise RuntimeError("Experiment run failed")

    with open(f"results/processed.json", "r") as f:
        results = json.load(f)

    os.chdir("..")

    # Always only one round. Extract the results from the first round.
    app_results = results[0]["round_result"][0]
    alice_secret_key = app_results["app_alice"]["secret_key"]
    bob_secret_key = app_results["app_bob"]["secret_key"]

    if alice_secret_key is None:
        print(f"No secret key was returned")
        return False

    if len(alice_secret_key) != KEY_LENGTH:
        print(f"Secret key length does not match requested key length of {KEY_LENGTH}")
        return False

    if alice_secret_key != bob_secret_key:
        print(f"Secret keys do not match")
        return False

    print("Secret keys match and are of correct length!")
    return True


if __name__ == "__main__":
    if os.path.exists(EXPERIMENT_NAME):
        shutil.rmtree(EXPERIMENT_NAME)

    success = main()

    shutil.rmtree(EXPERIMENT_NAME)

    exit(0 if success else 1)
