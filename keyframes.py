from dataclasses import dataclass
from collections import defaultdict
import bisect
import json

@dataclass(order=True)
class Keyframe:
    time: float
    score: tuple[int, int]
    player: str
    action: str

class KeyframeStore:
    def __init__(self):
        self.keyframes: list[Keyframe] = []

        # Indexes (with time-ordered lists)
        self.by_time = defaultdict(list)
        self.by_player = defaultdict(list)
        self.by_action = defaultdict(list)
        self.by_player_action = defaultdict(list)

    def _sorted_insert(self, lst, item):
        # Insert into list `lst` preserving time order
        bisect.insort(lst, item)

    def add(self, kf: Keyframe):
        self._sorted_insert(self.keyframes, kf)
        self._sorted_insert(self.by_time[kf.time], kf)
        self._sorted_insert(self.by_player[kf.player], kf)
        self._sorted_insert(self.by_action[kf.action], kf)
        self._sorted_insert(self.by_player_action[(kf.player, kf.action)], kf)

    def export_json(self, filename: str):
        data = [
            {
                "time": kf.time,
                "team_1_score": kf.score[0],
                "team_2_score": kf.score[1],
                "player": kf.player,
                "action": kf.action
            }
            for kf in self.keyframes
        ]
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

    def import_json(self, filename: str):
        with open(filename) as f:
            data = json.load(f)
        for entry in data:
            kf = Keyframe(
                time=entry["time"],
                score=(entry["team_1_score"], entry["team_2_score"]),
                player=entry["player"],
                action=entry["action"]
            )
            self.add(kf)

