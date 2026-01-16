"""JupyterLab extension backend for the Etiq Copilot.

This module serves as the server-side component for the Etiq Copilot JupyterLab
extension. It establishes a communication channel (`Comm`) with the frontend
to provide code analysis, testing, and recommendation features directly within
the Jupyter environment.

The core logic is encapsulated in the `EtiqExtension` class, which manages
application state (such as the code scan cache), initializes necessary services
(like recommenders and code scanners), and handles incoming messages from the
client. It uses a dispatcher pattern to route actions from the frontend to the
appropriate handler functions.

It integrates with IPython through the standard `load_ipython_extension` and
`unload_ipython_extension` functions, which register and unregister the comm
target, respectively.
"""

from __future__ import annotations

import os
import uuid
import traceback
from typing import TYPE_CHECKING, Any
from typing_extensions import TypeAlias


from etiq_copilot.engine.telemetry import get_anonymous_user_id
from etiq_copilot.engine.daemons.utils import (
    send_stored_telemetry_to_dashboard,
)
from etiq_copilot.engine.telemetry import Telemetry
from etiq_copilot.engine.daemons.full.daemon import DaemonContext, handle_message
from etiq_copilot.engine.daemons.utils import SendJsonProtocol

# Allow pydantic-ai models to run within Jupyter's async code.
import nest_asyncio
nest_asyncio.apply()

if TYPE_CHECKING:
    from ipykernel.comm import Comm
    from ipykernel.zmqshell import ZMQInteractiveShell as InteractiveShell

CommMsg: TypeAlias = dict[str, Any]

try:
    from ._version import __version__
except ImportError:
    __version__ = "dev"


# Set up telemetry
telemetry = Telemetry(
    etiq_token=os.getenv("ETIQ_TOKEN") or "",
    user_id=get_anonymous_user_id(),
    session_id=uuid.uuid4(),
)


class EtiqExtension(SendJsonProtocol):
    """The EtiqExtension class.

    This class is the entry point for the Etiq extension. It is responsible for
    creating the CodeScanner, RecommenderRepository, and RCARecommender. It also sets up
    the action handlers and failure names.
    """

    def __init__(self, telemetry: Telemetry, comm: Comm) -> None:
        """Initialize the EtiqExtension class.

        Args:
            telemetry: The telemetry object used for sending telemetry data.
            comm: The Comm object used for sending and receiving messages.

        """
        self.comm = comm
        self.context = DaemonContext(publisher=self, telemetry=telemetry)

    def send_json(self, obj) -> None:
        self.comm.send(obj)

    def handle_message(self, msg: CommMsg) -> None:
        action_dict = msg["content"]["data"]
        try:
            handle_message(action_dict, self.context)
        except Exception:
            self.send_json({"type": "exception", "exception": traceback.format_exc()})


def comm_target(comm: Comm, _: CommMsg) -> None:
    """Handle comm_open messages from frontend."""
    extension_instance = EtiqExtension(comm=comm, telemetry=telemetry)
    comm.on_msg(extension_instance.handle_message)


# This function is required by jupyter lab and is not unused!
def _jupyter_labextension_paths() -> list[dict[str, str]]:
    return [{"src": "labextension", "dest": "jupyterlab-etiq"}]


def load_ipython_extension(ipython: InteractiveShell) -> None:
    # Register comm for communicating with frontend
    """Load the IPython extension.

    This function registers the comm target "debug_vis_comm" from the IPython kernel's
    comm manager, allowing the frontend to communicate with the backend.

    Args:
        ipython (InteractiveShell): The IPython InteractiveShell instance.

    """
    ipython.kernel.comm_manager.register_target("debug_vis_comm", comm_target)
    send_stored_telemetry_to_dashboard(telemetry=telemetry)


def unload_ipython_extension(ipython: InteractiveShell) -> None:
    """Unload the IPython extension.

    This function un-registers the comm target "debug_vis_comm" from the IPython kernel's
    comm manager.

    Args:
        ipython (InteractiveShell): The IPython InteractiveShell instance.

    """
    ipython.kernel.comm_manager.unregister_target("debug_vis_comm")
    send_stored_telemetry_to_dashboard(telemetry=telemetry)
