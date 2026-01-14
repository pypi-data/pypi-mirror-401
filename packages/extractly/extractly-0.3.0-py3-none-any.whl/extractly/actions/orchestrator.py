import logging

from ..fields import FieldRepository
from ..schemas import FieldResponse
from .defaults import DEFAULT_ACTIONS
from .schemas import Action

logger = logging.getLogger(__name__)


class ActionService:
    """Central registry for action handlers."""

    def __init__(
        self,
        *,
        base_actions: list[Action] | None = None,
    ) -> None:
        self._actions: dict[str, Action] = {}
        self.register_many(base_actions or DEFAULT_ACTIONS)

    def register(
        self,
        action: Action,
        *,
        overwrite: bool = True,
    ) -> None:
        """Register a new action for the given action."""
        if not overwrite and action.name in self._actions:
            raise ValueError(
                f"Action already registered for '{action.name}'",
            )
        self._actions[action.name] = action

    def register_many(
        self,
        actions: list[Action],
        *,
        overwrite: bool = True,
    ) -> None:
        """Register multiple actions at once."""
        for action in actions:
            self.register(
                action,
                overwrite=overwrite,
            )

    def dispatch(
        self,
        field_response: FieldResponse,
        fields: FieldRepository,
    ) -> None:
        """Dispatch the field response to the appropriate action."""
        action_name = field_response.action
        action = self.get(action_name)
        if action is None:
            raise ValueError(f"Action not found for '{action_name}'")
        action.handler(
            field_response,
            fields,
        )

    def get(self, action_name: str) -> Action | None:
        """Retrieve an action by its action name."""
        return self._actions.get(action_name)

    def available_actions(self) -> tuple[str, ...]:
        """Return the tuple of registered action names."""
        return tuple(self._actions.keys())

    def available_actions_description(self) -> str:
        """Return a summary list of available actions and their descriptions."""
        lines = [
            f'- "{action.name}": {action.description}'
            for action in self._actions.values()
        ]
        return "\n".join(lines)

    @property
    def actions(self) -> list[Action]:
        """Return the list of registered actions."""
        return list(self._actions.values())
