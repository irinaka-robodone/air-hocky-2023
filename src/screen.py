import pyxel
from pigframe import *

from component import *

class ScTitle(Screen):
    def draw(self):
        text1 = "エアホッケー"
        self.world.font_l.draw_text(
            self.world.SCREEN_SIZE[0]//2 - len(text1)*24//2, self.world.SCREEN_SIZE[1]//2 - 30, text1, 7
        )
        
        text2 = "クリック/タップしてスタート"
        self.world.font_m.draw_text(
            self.world.SCREEN_SIZE[0]//2 - len(text2)*16//2, self.world.SCREEN_SIZE[1]//2 + 10, text2, pyxel.frame_count//8 % 16
        )
        
        text3 = "5点を先に取ったら勝ち"
        self.world.font_m.draw_text(
            self.world.SCREEN_SIZE[0]//2 - len(text3)*16//2, self.world.SCREEN_SIZE[1]//2 + 40, text3, 7
        )
        
class ScHockey(Screen):
    def draw(self):
        for ent, (hock, pos, vel) in self.world.get_components(Hockey, Position, Velocity):
            pyxel.circb(pos.x, pos.y, hock.radius, 7)
            pyxel.circ(pos.x, pos.y, hock.radius, hock.color)
            # pyxel.line(pos.x, pos.y, pos.x + vel.x * hock.radius, pos.y + vel.y * hock.radius, 7)
            
class ScPuck(Screen):
    def draw(self):
        for ent, (puck, pos, vel) in self.world.get_components(Puck, Position, Velocity):
            pyxel.circ(pos.x, pos.y, puck.radius, 13)
            pyxel.circb(pos.x, pos.y, puck.radius, 0)
            # pyxel.line(pos.x, pos.y, pos.x + vel.x * puck.radius, pos.y + vel.y * puck.radius, 0)
            
class ScField(Screen):
    def draw(self):
        for ent, (field) in self.world.get_component(Field):
            # ゲームフィールドの描画
            pyxel.rect(
                self.world.SCREEN_SIZE[0]//2 - field.width//2, 
                self.world.SCREEN_SIZE[1]//2 - field.height//2, field.width, field.height, 7
            )
            # ゲームフィールドの枠の描画
            pyxel.rectb(
                self.world.SCREEN_SIZE[0]//2 - field.width//2, 
                self.world.SCREEN_SIZE[1]//2 - field.height//2, field.width, field.height, 7
            )
            # 中央の先を描画
            pyxel.line(
                self.world.SCREEN_SIZE[0]//2, (self.world.SCREEN_SIZE[1] - field.height)//2,
                self.world.SCREEN_SIZE[0]//2, (self.world.SCREEN_SIZE[1] + field.height)//2, 13
            )
        
        count_hock = 0
        for ent, (hock) in self.world.get_component(Hockey):
            # 左のゴールの描画
            if count_hock == 0:
                pyxel.rect(
                    (self.world.SCREEN_SIZE[0] - field.width)//2 - 20, self.world.SCREEN_SIZE[1]//2 - field.goal_width//2,
                    20, field.goal_width, hock.color
                )
            # 右のゴールの描画
            elif count_hock == 1:
                pyxel.rect(
                    (self.world.SCREEN_SIZE[0] + field.width)//2, self.world.SCREEN_SIZE[1]//2 - field.goal_width//2,
                    20, field.goal_width, hock.color
                )
            count_hock += 1

class ScInfo(Screen):
    def draw(self):
        text1 = "Score"
        self.world.font_l.draw_text(
            self.world.SCREEN_SIZE[0]//2 - len(text1)*12//2, 8, text1, 7
        )
        text2 = "VS"
        self.world.font_m.draw_text(
            self.world.SCREEN_SIZE[0]//2 - len(text2)*8//2, 36, text2, 7
        )
        
        count_players = 0
        # プレイヤーの数だけスコアを描画する。
        for ent, (score) in self.world.get_component(Score):
            score_str = str(score.score)
            
            # 左のプレイヤーのスコアを描画
            if count_players == 0:
                self.world.font_l.draw_text(
                    self.world.SCREEN_SIZE[0]//2 - 80 - len(score_str)*12, 32, score_str, 7
                )
                
            # 右のプレイヤーのスコアを描画
            elif count_players == 1:
                self.world.font_l.draw_text(
                    self.world.SCREEN_SIZE[0]//2 + 80 - len(score_str)*12, 32, score_str, 7
                )
            # ここまでのプレイヤーの数をカウントする。
            count_players += 1

class ScResult(Screen):
    def draw(self):
        for _, (result) in self.world.get_component(Result):
            winner = str(result.names[result.winner]) + " の勝ち"
            score1 = str(result.scores[0])
            score2 = str(result.scores[1])
            
            self.world.font_l.draw_text(
                self.world.SCREEN_SIZE[0]//2 - len(winner)*24//2, self.world.SCREEN_SIZE[1]//2 - 40, winner, 7
            )
            
            text1 = "クリック/タップしてタイトルに戻る"
            self.world.font_m.draw_text(
                self.world.SCREEN_SIZE[0]//2 - len(text1)*16//2, self.world.SCREEN_SIZE[1]//2 + 40, text1, pyxel.frame_count//8 % 16
            )
            text2 = "VS"
            self.world.font_m.draw_text(
                self.world.SCREEN_SIZE[0]//2 - len(text2)*8//2, self.world.SCREEN_SIZE[1]//2 + 4, text2, 7
            )
            self.world.font_l.draw_text(
                self.world.SCREEN_SIZE[0]//2 - 80 - len(score1)*24//2, self.world.SCREEN_SIZE[1]//2, score1, 7
            )
            
            self.world.font_l.draw_text(
                self.world.SCREEN_SIZE[0]//2 + 80 - len(score2)*24//2, self.world.SCREEN_SIZE[1]//2, score2, 7
            )
            