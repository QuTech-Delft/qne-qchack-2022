from netqasm.sdk.qubit import Qubit

class Eve:

    def __init__(self):
        pass

    def eavesdrop(self, qubit: Qubit):
        # IMPLEMENT YOUR EAVESDROPPING CODE HERE
        #
        # This method is called for each qubit individually at both ends of the
        # connection. However, note that these will be actually two separate
        # instances of Eve - one at each end. Thus, whilst you can share state
        # from qubit to qubit, this state cannot be shared between the two ends
        # of the connection.
        #
        # When measuring make sure to use `inplace=True` when calling
        # `qubit.measure(inpace=True)` so that the qubit is still available when
        # delivered to the application. Otherwise, the qubit is released.
        pass
