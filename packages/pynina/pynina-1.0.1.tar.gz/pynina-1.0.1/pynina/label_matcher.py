from .nina_api import NinaAPI


class ActionLabelMatcher:
    """Class to match action labels with their codes."""

    def __init__(self, api: NinaAPI):
        """Initialize."""
        self._api: NinaAPI = api

        self._labels: dict[str, str] = {}

    @property
    def initiated(self) -> bool:
        """Check if matcher has been initiated."""
        return len(self._labels.items()) > 0

    async def init(self) -> None:
        """Update the labels."""
        self._labels = await self._api.get_labels()

    def match(self, code: str) -> str:
        """Match a code to a label."""
        return self._labels.get(code, code)
