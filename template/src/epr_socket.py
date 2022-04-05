from contextlib import contextmanager
from typing import Optional, Callable, List, Tuple, Union, ContextManager

from netqasm.qlink_compat import TimeUnit, RandomBasis, EPRType, LinkLayerOKTypeM, LinkLayerOKTypeR
from netqasm.sdk.builder import EprKeepResult, EprMeasureResult
from netqasm.sdk.epr_socket import EPRSocket, EPRMeasBasis
from netqasm.sdk.futures import RegFuture
from netqasm.sdk.qubit import Qubit, FutureQubit

from eve import Eve


class DerivedEPRSocket(EPRSocket):

    def __init__(
            self,
            remote_app_name: str,
            epr_socket_id: int = 0,
            remote_epr_socket_id: int = 0,
            min_fidelity: int = 100,
    ):
        super().__init__(remote_app_name, epr_socket_id, remote_epr_socket_id, min_fidelity)
        self._eve = Eve()


    def create_keep(
        self,
        number: int = 1,
        post_routine: Optional[Callable] = None,
        sequential: bool = False,
        time_unit: TimeUnit = TimeUnit.MICRO_SECONDS,
        max_time: int = 0,
        min_fidelity_all_at_end: Optional[int] = None,
        max_tries: Optional[int] = None,
    ) -> List[Qubit]:

        qubits = super().create_keep(
            number,
            post_routine,
            sequential,
            time_unit,
            max_time,
            min_fidelity_all_at_end,
            max_tries,
        )

        for q in qubits:
            self._eve.eavesdrop(q)

        return qubits

    def create_keep_with_info(
        self,
        number: int = 1,
        post_routine: Optional[Callable] = None,
        sequential: bool = False,
        time_unit: TimeUnit = TimeUnit.MICRO_SECONDS,
        max_time: int = 0,
        min_fidelity_all_at_end: Optional[int] = None,
    ) -> Tuple[List[Qubit], List[EprKeepResult]]:

        qubits_with_info = super().create_keep_with_info(
            number,
            post_routine,
            sequential,
            time_unit,
            max_time,
            min_fidelity_all_at_end,
        )

        for q in qubits_with_info[0]:
            self._eve.eavesdrop(q)

        return qubits_with_info

    def create_measure(
        self,
        number: int = 1,
        time_unit: TimeUnit = TimeUnit.MICRO_SECONDS,
        max_time: int = 0,
        basis_local: EPRMeasBasis = None,
        basis_remote: EPRMeasBasis = None,
        rotations_local: Tuple[int, int, int] = (0, 0, 0),
        rotations_remote: Tuple[int, int, int] = (0, 0, 0),
        random_basis_local: Optional[RandomBasis] = None,
        random_basis_remote: Optional[RandomBasis] = None,
    ) -> List[EprMeasureResult]:
        raise NotImplementedError("Not available in the QKD challenge")

    def create_rsp(
        self,
        number: int = 1,
        time_unit: TimeUnit = TimeUnit.MICRO_SECONDS,
        max_time: int = 0,
        basis_local: EPRMeasBasis = None,
        rotations_local: Tuple[int, int, int] = (0, 0, 0),
        random_basis_local: Optional[RandomBasis] = None,
        min_fidelity_all_at_end: Optional[int] = None,
    ) -> List[EprMeasureResult]:
        raise NotImplementedError("Not available in the QKD challenge")

    def create(
        self,
        number: int = 1,
        post_routine: Optional[Callable] = None,
        sequential: bool = False,
        tp: EPRType = EPRType.K,
        time_unit: TimeUnit = TimeUnit.MICRO_SECONDS,
        max_time: int = 0,
        basis_local: EPRMeasBasis = None,
        basis_remote: EPRMeasBasis = None,
        rotations_local: Tuple[int, int, int] = (0, 0, 0),
        rotations_remote: Tuple[int, int, int] = (0, 0, 0),
        random_basis_local: Optional[RandomBasis] = None,
        random_basis_remote: Optional[RandomBasis] = None,
    ) -> Union[List[Qubit], List[EprMeasureResult], List[LinkLayerOKTypeM]]:
        if tp != EPRType.K:
            raise NotImplementedError("Only EPRType.K is available in the QKD challenge")

        qubits: List[Qubit] = super().create(  # type: ignore
            number,
            post_routine,
            sequential,
            tp,
            time_unit,
            max_time,
            basis_local,
            basis_remote,
            rotations_local,
            rotations_remote,
            random_basis_local,
            random_basis_remote,
        )

        for q in qubits:
            self._eve.eavesdrop(q)

        return qubits

    def create_context(
        self,
        number: int = 1,
        sequential: bool = False,
        time_unit: TimeUnit = TimeUnit.MICRO_SECONDS,
        max_time: int = 0,
    ) -> ContextManager[Tuple[FutureQubit, RegFuture]]:
        raise NotImplementedError("Not available in the QKD challenge")

    def recv_keep(
        self,
        number: int = 1,
        post_routine: Optional[Callable] = None,
        sequential: bool = False,
        min_fidelity_all_at_end: Optional[int] = None,
        max_tries: Optional[int] = None,
    ) -> List[Qubit]:

        qubits = super().recv_keep(
            number,
            post_routine,
            sequential,
            min_fidelity_all_at_end,
            max_tries,
        )

        for q in qubits:
            self._eve.eavesdrop(q)

        return qubits

    def recv_keep_with_info(
        self,
        number: int = 1,
        post_routine: Optional[Callable] = None,
        sequential: bool = False,
        min_fidelity_all_at_end: Optional[int] = None,
        max_tries: Optional[int] = None,
    ) -> Tuple[List[Qubit], List[EprKeepResult]]:

        qubits_with_info = super().recv_keep_with_info(
            number,
            post_routine,
            sequential,
            min_fidelity_all_at_end,
            max_tries,
        )

        for q in qubits_with_info[0]:
            self._eve.eavesdrop(q)

        return qubits_with_info

    def recv_measure(
        self,
        number: int = 1,
    ) -> List[EprMeasureResult]:
        raise NotImplementedError("Not available in the QKD challenge")

    def recv_rsp(
        self,
        number: int = 1,
        min_fidelity_all_at_end: Optional[int] = None,
        max_tries: Optional[int] = None,
    ) -> List[Qubit]:
        raise NotImplementedError("Not available in the QKD challenge")

    def recv_rsp_with_info(
        self,
        number: int = 1,
        min_fidelity_all_at_end: Optional[int] = None,
        max_tries: Optional[int] = None,
    ) -> Tuple[List[Qubit], List[EprKeepResult]]:
        raise NotImplementedError("Not available in the QKD challenge")

    def recv(
        self,
        number: int = 1,
        post_routine: Optional[Callable] = None,
        sequential: bool = False,
        tp: EPRType = EPRType.K,
    ) -> Union[List[Qubit], List[EprMeasureResult], List[LinkLayerOKTypeR]]:
        if tp != EPRType.K:
            raise NotImplementedError("Only EPRType.K is available in the QKD challenge")

        qubits: List[Qubit] = super().recv(  # type: ignore
            number,
            post_routine,
            sequential,
            tp,
        )

        for q in qubits:
            self._eve.eavesdrop(q)

        return qubits

    @contextmanager
    def recv_context(
        self,
        number: int = 1,
        sequential: bool = False,
    ):
        raise NotImplementedError("Not available in the QKD challenge")
