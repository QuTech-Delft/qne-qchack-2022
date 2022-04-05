from netqasm.logging.glob import get_netqasm_logger
from netqasm.sdk.external import NetQASMConnection, Socket

from epr_socket import DerivedEPRSocket as EPRSocket

logger = get_netqasm_logger()


def main(app_config=None, key_length=16):
    # Socket for classical communication
    socket = Socket("bob", "alice", log_config=app_config.log_config)
    # Socket for EPR generation
    epr_socket = EPRSocket("alice")

    bob = NetQASMConnection(
        app_name=app_config.app_name,
        log_config=app_config.log_config,
        epr_sockets=[epr_socket],
    )

    with bob:
        # IMPLEMENT YOUR SOLUTION HERE
        logger.info("IMPLEMENT YOUR SOLUTION HERE")

    # RETURN THE SECRET KEY HERE
    return {
        "secret_key": None,
    }


if __name__ == "__main__":
    main()
