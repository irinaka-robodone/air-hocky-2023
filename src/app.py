import pyxel
from pigframe import *

from entity import *
from component import *
from system import *
from screen import *
from triger import *
from font import BDFRenderer

P1KEYS = {
    "up": pyxel.KEY_W,
    "down": pyxel.KEY_S,
    "left": pyxel.KEY_A,
    "right": pyxel.KEY_D
}

P2KEYS = {
    "up": pyxel.KEY_UP,
    
    "down": pyxel.KEY_DOWN,
    "left": pyxel.KEY_LEFT,
    "right": pyxel.KEY_RIGHT
}

class App(World):
    def __init__(self) -> None:
        super().__init__()
        self.SCREEN_SIZE = (640, 480)
        self.GAME_TITLE = "エアホッケー"
        self.FPS = 60
        pyxel.init(self.SCREEN_SIZE[0], self.SCREEN_SIZE[1], title=self.GAME_TITLE, fps=self.FPS)
        self.font_s = BDFRenderer("assets/b14.bdf")
        self.font_m = BDFRenderer("assets/b16.bdf")
        self.font_l = BDFRenderer("assets/b24.bdf")
        pyxel.mouse(True)
        self.init()
        
    def run(self):
        pyxel.run(self.update, self.draw)
        
    def init(self):
        pass
    
    def update(self):
        self.process_systems()
        self.process_events()
        self.level_manager.process()
        
    def draw(self):
        pyxel.cls(1)
        self.process_screens()
    
def main():
    app = App()
    app.add_scenes(["title", "gwame", "result"])
    app.current_scene = "title"
    
    # エンティティの生成
    create_hockey(app, 100, 240, weight=20, color=2, score = 5, **P1KEYS)
    create_hockey(app, 540, 240, weight=20, color=3, score = 5, **P2KEYS)
    create_field(app, 580, 320, goal_width = 80)
    create_puck(app, app.SCREEN_SIZE[0]//2, app.SCREEN_SIZE[1]//2, dx=1, dy=1, weight=1, radius=6)
    create_play_status(app)
    
    # システム処理の登録
    app.add_system_to_scenes(SysInit, "title", 0)
    app.add_system_to_scenes(SysMove, "game", 4)
    app.add_system_to_scenes(SysControl, "game", 3)
    app.add_system_to_scenes(SysCollision, "game", 2)
    app.add_system_to_scenes(SysScore, "game", 1)
    
    # スクリーン処理の登録
    app.add_screen_to_scenes(ScTitle, "title")
    app.add_screen_to_scenes(ScHockey, "game", priority=1)
    app.add_screen_to_scenes(ScPuck, "game", priority=0)
    app.add_screen_to_scenes(ScField, "game", priority=-1)
    app.add_screen_to_scenes(ScInfo, "game", priority=-2)
    app.add_screen_to_scenes(ScResult, "result")
    
    # シーン遷移（シーンを変える処理）の登録
    app.add_scene_transition("title", "game", lambda: pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_RETURN))
    app.add_scene_transition("game", "result", lambda: triger_result(app))
    app.add_scene_transition("result", "title", lambda: pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_RETURN))
    
    app.run()

    
if __name__ == "__main__":
    main()