from netqasm.sdk.qubit import Qubit

class Eve:

    def __init__(self):
        pass

    def eavesdrop(self, qubit: Qubit):
        # When measuring make sure to use `inplace=True` when calling
        # `qubit.measure(inpace=True)` so that the qubit is still available when
        # delivered to the application. Otherwise, the qubit is released.
        pass
