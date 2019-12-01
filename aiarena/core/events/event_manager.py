from aiarena import settings
from aiarena.core.events.events import BotActivationStatusChangedEvent, MatchResultReceivedEvent, Event, EventType
from aiarena.core.utils import post_result_to_discord_bot, add_result_replay_file_to_season_archive


class EventManager:
    def __init__(self):
        self._EVENT_HANDLER_MAP = {
            EventType.MATCH_RESULT_RECEIVED: self._handle_match_result_received,
            EventType.BOT_ACTIVATION_STATUS_CHANGED: self._handle_bot_activation_status_changed
        }

    def broadcast_event(self, event: Event):
        self._EVENT_HANDLER_MAP[event.TYPE](event)

    def _handle_match_result_received(self, event: MatchResultReceivedEvent):
        if settings.POST_SUBMITTED_RESULTS_TO_ADDRESS and event.result.match.round is not None:
            post_result_to_discord_bot(event.result)
        add_result_replay_file_to_season_archive(event.result)


    # todo: change this to a generic bot updated event
    def _handle_bot_activation_status_changed(self, event: BotActivationStatusChangedEvent):
        pass


EVENT_MANAGER = EventManager()