"""
1.「ｘ」 パックとホッケーがあたったら跳ね返るしくみ
1. 「」ゲームの初期化
1. 「×」ホッケーを動かす仕組み
1. 「」パックを動かす仕組み
1. 「ｘ」スコアを加算する仕組み（勝利判定も）
"""
from pigframe import *
import pyxel

from component import *

class SysMove(System):
    def __init__(self, world: World, priority: int, **kwargs) -> None:
        super().__init__(world)
        self.world = world

    def process(self):
        # フィールドコンポーネントを1つ取得する。
        _, (field) = self.world.get_component(Field)[0]
        # 位置と速度コンポーネントを持つエンティティを取得して、移動処理を行う。
        for ent, (pos, vel) in self.world.get_components(Position, Velocity):
            # 速度（vel）を使って位置（pos）を更新する。
            
            pos.x += vel.x
            pos.y += vel.y
            
            vel.x *= 0.95
            vel.y *= 0.95
            
            # ゴールに入ったときはパックの跳ね返りを行わない。
            # 左のゴールに入ったときの例外処理。
            if (self.world.SCREEN_SIZE[0] - field.width)//2 - 20 < pos.x < (self.world.SCREEN_SIZE[0] - field.width)//2:
                if (self.world.SCREEN_SIZE[1]//2 - field.goal_width//2) < pos.y < (self.world.SCREEN_SIZE[1]//2 + field.goal_width//2):
                    continue
            
            # 右のゴールに入ったときの例外処理。
            if (self.world.SCREEN_SIZE[0] + field.width)//2 < pos.x < (self.world.SCREEN_SIZE[0] + field.width)//2 + 20:
                if (self.world.SCREEN_SIZE[1]//2 - field.goal_width//2) < pos.y < (self.world.SCREEN_SIZE[1]//2 + field.goal_width//2):
                    continue
            
            # フィールドの外に出ないようにする。
            # 左右（x方向）の壁に当たったら進む向き（vel.x）を逆にして跳ね返す。
            if pos.x < (self.world.SCREEN_SIZE[0] - field.width)//2 or \
                pos.x > (self.world.SCREEN_SIZE[0] + field.width)//2:
                vel.x *= -1
            # 上下（y方向）の壁に当たったら進む向き（vel.y）を逆にして跳ね返す。
            if pos.y < (self.world.SCREEN_SIZE[1] - field.height)//2 or \
                pos.y > (self.world.SCREEN_SIZE[1] + field.height)//2:
                vel.y *= -1
            
            # 左右（x方向）の壁に当たったら位置（pos.x）をフィールド内に戻す。
            if pos.x < (self.world.SCREEN_SIZE[0] - field.width)//2:
                pos.x = (self.world.SCREEN_SIZE[0] - field.width)//2
            if pos.x > (self.world.SCREEN_SIZE[0] + field.width)//2:
                pos.x = (self.world.SCREEN_SIZE[0] + field.width)//2
            # 上下（y方向）の壁に当たったら位置（pos.y）をフィールド内に戻す。
            if pos.y < (self.world.SCREEN_SIZE[1] - field.height)//2:
                pos.y = (self.world.SCREEN_SIZE[1] - field.height)//2
            if pos.y > (self.world.SCREEN_SIZE[1] + field.height)//2:
                pos.y = (self.world.SCREEN_SIZE[1] + field.height)//2

class SysControl(System):
    def __init__(self, world: World, priority: int, **kwargs) -> None:
        super().__init__(world)
        self.world = world
    
    def process(self):
        for ent, (pos, vel, cont) in self.world.get_components(Position, Velocity, Controlable):
            vel.x = 0
            vel.y = 0
            
            if pyxel.btnp(cont.up)or pyxel.btnp(cont.down)\
                or pyxel.btnp(cont.left)or pyxel.btnp(cont.right):
                pass
            
            if pyxel.btn(cont.left):
                vel.x = -4
                vel.x *= 1.01
            if pyxel.btn(cont.right):
                vel.x = 4
                vel.x *= 1.01
            if pyxel.btn(cont.up):
                vel.y = -4
                vel.y *= 1.01
            if pyxel.btn(cont.down):
                vel.y = 4
                vel.y *= 1.01
                
class SysCollision(System):
    def __init__(self, world: World, priority: int, **kwargs) -> None:
        super().__init__(world)
        self.world = world
    
    def process(self):
        for ent1, (pos1, vel1, coll1) in self.world.get_components(Position, Velocity, Collidable):
            for ent2, (pos2, vel2, coll2) in self.world.get_components(Position, Velocity, Collidable):
                if ent1 == ent2:
                    continue
                if abs(pos1.x-pos2.x) < 20 and abs(pos1.y-pos2.y) < 20:
                    print(vel1.x)
                    vel1.x = (vel2.x * vel2.weight + vel1.x * vel1.weight)/vel1.weight
                    vel1.y = (vel2.y * vel2.weight + vel1.y * vel1.weight)/vel1.weight
                    vel2.x = (vel1.x * vel1.weight + vel2.x * vel2.weight)/vel2.weight
                    vel2.y = (vel1.y * vel1.weight + vel2.y * vel2.weight)/vel2.weight
                    print(vel1.x)
                    break
                
                
class SysScore(System):
    def __init__(self, world: World, priority: int, **kwargs) -> None:
        super().__init__(world)
        self.world = world
    
    def process(self):
        # フィールドコンポーネントを1つ取得する。
        _, (field) = self.world.get_component(Field)[0]
        _, (result) = self.world.get_component(Result)[0]
        # パックが自分のゴールに入ったら相手のスコアを加算する。
        player_entites = [ent for ent, (_, _) in self.world.get_components(Hockey, Score)]
        for _, (pos, vel, puck) in self.world.get_components(Position, Velocity, Puck):
            count_hock = 0
            shooted = False
            for player_ent, (hock, score) in self.world.get_components(Hockey, Score):
                # 左のゴールの判定
                if count_hock == 0:
                    if ((self.world.SCREEN_SIZE[0] - field.width)//2 - 20 < pos.x < (self.world.SCREEN_SIZE[0] - field.width)//2) \
                    and ((self.world.SCREEN_SIZE[1]//2 - field.goal_width//2) < pos.y < (self.world.SCREEN_SIZE[1]//2 + field.goal_width//2)):
                        opponent_score = self.world.get_entity_object(player_entites[count_hock-1])[Score]
                        opponent_score.score += 1
                        result.scores[player_entites[count_hock - 1]] = opponent_score.score
                        shooted = True
                        
                # 右のゴールの判定
                elif count_hock == 1:
                    if ((self.world.SCREEN_SIZE[0] + field.width)//2 < pos.x < (self.world.SCREEN_SIZE[0] + field.width)//2 + 20) \
                    and ((self.world.SCREEN_SIZE[1]//2 - field.goal_width//2) < pos.y < (self.world.SCREEN_SIZE[1]//2 + field.goal_width//2)):
                        opponent_score = self.world.get_entity_object(player_entites[count_hock-1])[Score]
                        opponent_score.score += 1
                        result.scores[player_entites[count_hock - 1]] = opponent_score.score
                        shooted = True
                
                # パックがゴールに入ったら、パックをフィールドの中央に戻す。
                if shooted:
                    pos.x = self.world.SCREEN_SIZE[0]//2
                    pos.y = self.world.SCREEN_SIZE[1]//2
                    # パックの速度をシュートされたときと逆にする。
                    vel.x *= -1
                    vel.y *= -1
                    # パックの速度を少し上げる。
                    vel.x *= 1.1
                    vel.y *= 1.1
                    return
                    
                # ここまでのホッケーの数をカウントする。
                count_hock += 1
                
class SysInit(System):
    def __init__(self, world: World, priority: int, **kwargs) -> None:
        super().__init__(world)
        self.world = world
    
    def process(self):
        # 結果を初期化する
        _, (result) = self.world.get_component(Result)[0]
        result.winner = None
        
        result.scores = {
            0: 0,
            1: 0
        }
        
        for _,(score) in self.world.get_component(Score):
            score.score = 0
            
        for _,(vel) in self.world.get_component(Velocity):
            vel.x = 1
            vel.y = 1