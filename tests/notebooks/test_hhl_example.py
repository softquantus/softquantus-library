from tests.utils_for_testbook import (
    validate_quantum_program_size,
    validate_quantum_model,
    wrap_testbook,
)
from testbook.client import TestbookNotebookClient


@wrap_testbook("hhl_example", timeout_seconds=800)
def test_notebook(tb: TestbookNotebookClient) -> None:
    # the `qmod`s and `qprog`s are defined in a function.
    # need to rewrite the notebook in order to test it

    # test notebook content
    for fidelity_softqlib, fidelity_qiskit in zip(
        tb.ref("softqlib_fidelities"),
        tb.ref("qiskit_fidelities"),
    ):
        assert fidelity_softqlib >= fidelity_qiskit - 0.02

    for depth_softqlib, depth_qiskit in zip(
        tb.ref("softqlib_depths"),
        tb.ref("qiskit_depths"),
    ):
        assert depth_softqlib < depth_qiskit
