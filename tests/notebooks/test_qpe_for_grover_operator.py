from tests.utils_for_testbook import (
    validate_quantum_program_size,
    validate_quantum_model,
    wrap_testbook,
)
from testbook.client import TestbookNotebookClient

import itertools


@wrap_testbook(
    "qpe_for_grover_operator", timeout_seconds=3600
)  # bump from 1000  # bump from 2000
def test_notebook(tb: TestbookNotebookClient) -> None:
    # test models
    for qmod in itertools.chain(
        tb.ref("qmods"),
        tb.ref("qmods_width"),
        tb.ref("qmods_cx"),
    ):
        validate_quantum_model(qmod)

    # test quantum programs
    """
    softqlib depths: [866, 2596, 6056, 12976, 26816]
    softqlib cx_counts: [513, 1544, 3600, 7713, 15929]
    softqlib widths: [6, 7, 8, 9, 10]
    """
    for qprog, e_width, e_depth in zip(
        tb.ref_pydantic("qprogs_width"),
        tb.ref("softqlib_widths_ae_opt_width"),
        tb.ref("softqlib_depths_ae_opt_width"),
    ):
        validate_quantum_program_size(
            qprog,
            expected_width=int(e_width * 1.5),
            expected_depth=int(e_depth * 1.5),
        )
    """
    softqlib depths: [426, 1272, 2926, 6196, 13015]
    softqlib cx_counts: [241, 722, 1664, 3523, 7384]
    softqlib widths: [15, 18, 21, 24, 27]
    """
    for qprog, expected_max_width, e_depth in zip(
        tb.ref_pydantic("qprogs_cx"),
        tb.ref("qmods_cx_max_width"),
        tb.ref("softqlib_depths_ae_opt_depth_max_width"),
    ):
        validate_quantum_program_size(
            qprog,
            expected_width=expected_max_width,
            expected_depth=int(e_depth * 1.5),
        )

    # test notebook content
    for depth_softqlib_optimize_depth, depth_softqlib_optimize_width, depth_qiskit in zip(
        tb.ref("softqlib_depths_ae_opt_depth_max_width"),
        tb.ref("softqlib_depths_ae_opt_width"),
        tb.ref("qiskit_depths_ae"),
    ):
        assert (
            depth_softqlib_optimize_depth < depth_softqlib_optimize_width < depth_qiskit
        )
