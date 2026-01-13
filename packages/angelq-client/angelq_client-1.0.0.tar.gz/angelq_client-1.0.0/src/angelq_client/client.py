from __future__ import annotations

from dataclasses import dataclass
from typing import List
from enum import Enum
import requests

class Algorithm(Enum):
    QAOA = "qaoa"
    VQE = "vqe"
    ANNEALING = "anneal"
    CVQE = "cvqe"


@dataclass
class ExperimentalSetup:
    qubo: List[List[float]]
    nqubits: int
    shots: int
    experiments: int
    algorithm: Algorithm

    def __post_init__(self):
        if self.nqubits <= 0:
            raise ValueError("nqubits must be positive")
        
        if self.shots <= 0 or self.experiments <= 0:
            raise ValueError("shots and experiments must be positive")

class AngelQClient:
    """
    Minimal client skeleton for the AngelQ API.

    This initial release exists to establish the 'angelq-client' name on PyPI.
    The API surface will expand in future releases.
    """
    
    def __init__(self, server: str, token: str):
        self.server = server
        self.token = token

    
    def ping(self) -> bool:
        """
        This function checks the connection to the AngelQ server.
        
        :return: True if the server responds with 'pong', False otherwise.
        :rtype: bool
        """

        r = requests.get(f"{self.server}/api/v1/system/ping", timeout=2)
        return r.status_code == 200 and r.json().get("result") == "pong"


    def execute(self, setup: ExperimentalSetup) -> dict:
        """
        Executes the given experimental setup on the AngelQ server.
        
        :param setup: The experimental setup to execute.
        :type setup: ExperimentalSetup
        :return: Returns the result from the server in json format.
        :rtype: dict
        """

        if not self.ping():
            raise ConnectionError("Could not connect to AngelQ server.")

        r = requests.post(
            f"{self.server}/api/v1/execute",
            json={
                "qubo": setup.qubo,
                "nqubits": setup.nqubits,
                "shots": setup.shots,
                "experiments": setup.experiments,
                "algorithm": setup.algorithm.value
            },
            headers={"Authorization": f"Bearer {self.token}"},
            timeout=5
        )

        if r.status_code != 200:
            raise ConnectionError("Could not execute on AngelQ server, status code: " + str(r.status_code))

        return r.json()


    def get_active(self) -> list[str]:
        """
        Returns a list of active experiments running on the AngelQ server.

        :return: A list of active experiment IDs.
        :rtype: list[str]
        """

        r = requests.get(
            f"{self.server}/api/v1/experiments/active",
            headers={"Authorization": f"Bearer {self.token}"},
            timeout=5
        )

        return r.json().get("result", [])


    def get_result(self, experiment_id: str) -> dict:
        """
        Retrieves the result of a specific experiment by its ID.

        :param experiment_id: The ID of the experiment to retrieve.
        :type experiment_id: str
        :return: The result of the experiment in json format.
        :rtype: dict
        """

        r = requests.get(
            f"{self.server}/api/v1/experiments/{experiment_id}/result",
            headers={"Authorization": f"Bearer {self.token}"},
            timeout=5
        )

        if r.status_code != 200:
            raise ConnectionError("Could not retrieve result from AngelQ server, status code: " + str(r.status_code))

        return r.json()
