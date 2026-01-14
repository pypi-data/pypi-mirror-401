import pytest

from angelq_client import ExperimentalSetup, AngelQClient

def test_dataclass():

    setup = ExperimentalSetup(
        qubo=[[1.0, -1.0], [-1.0, 2.0]],
        nqubits=2,
        shots=1000,
        experiments=10,
        algorithm="qaoa",
    )

    assert setup.algorithm == "qaoa"


def test_api_connection():

    setup = ExperimentalSetup(
        qubo=[[1.0, -1.0], [-1.0, 2.0]],
        nqubits=2,
        shots=1000,
        experiments=10,
        algorithm="qaoa",
    )

    client = AngelQClient(server="https://server.stratakis.eu", token="test_token")
    result = client.execute(setup)
    assert result == ""