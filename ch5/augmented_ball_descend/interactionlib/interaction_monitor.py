"""
Monitors whether the user is selecting an area on the image or has chosen the
starting position.
"""

from ipywidgets import Textarea
import matplotlib.pyplot as plt

class InteractionMonitor:
    """
    Detects mouse events to figure our what is a user doing.

    Args:
    fig: the matplotlib figure to monitor.
    info_area: the external informational area whose value needs to be updated.
    auto_stop_interaction: should interaction stop (when True) after selecting
    the starting position or not.
    """

    def __init__(self, fig: plt.Figure, info_area: Textarea,
                 auto_stop_interaction: bool = True):
        self._fig = fig
        self._info_area = info_area
        self._auto_stop_interaction = auto_stop_interaction
        self._cids = None
        self._selecting = False
        self._clicked = False
        self._clicked_position = None

    def _on_click(self, event):
        self._clicked = True

    def _on_release(self, event):
        if not self._selecting:
            self._clicked_position = (int(event.ydata), int(event.xdata))
            self._info_area.value = str(self._clicked_position)
            if self._auto_stop_interaction:
                self.stop()

        self._selecting = False
        self._clicked = False

    def _on_motion(self, event):
        self._selecting = self._clicked

    @property
    def clicked_position(self):
        """Returns the clicked data position on the map."""
        return self._clicked_position

    def start(self):
        """Starts monitoring mouse events on figure."""
        self._cids = [
            self._fig.canvas.mpl_connect('button_press_event', self._on_click),
            self._fig.canvas.mpl_connect('button_release_event', self._on_release),
            self._fig.canvas.mpl_connect('motion_notify_event', self._on_motion)]

    def stop(self):
        """Closes the figure and stops the interaction."""
        plt.close(self._fig)
