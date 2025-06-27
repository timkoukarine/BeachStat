import json 

class Keyframes:
    def __init__(self, keyframes=None):
        if keyframes:
            self.keyframes = keyframes
            return
        
        self.keyframes = {}
        
    def add_keyframe(self, keyframe):
        self.keyframes.update(keyframe)

    def to_json(self):
        return json.dumps(self.keyframes)

    @classmethod
    def from_json(cls, json_str):
        keyframes = json.loads(json_str)
        return cls(keyframes)
    

class Keyframe:
    def __init__(self, time: float, player=None, action=None, score: tuple = (0, 0)):
        self.time = time
        if player:
            self.player = player
            self.action = action
    
        self.team_1_score = score[0]
        self.team_2_score = score[1]


    def to_dict(self):
        return {
            'time': self.time,
            'score': (self.team_1_score, self.team_2_score),
            'player': self.player,
            'action': self.action
        }

