from pigframe import *

from component import *

def triger_result(world: World) -> bool:
    """トリガー関数: 結果画面へ遷移するかを判定する関数。
    
    Args:
        world (World): The world to process.
    """
    # スコアが0のプレイヤーがいたら結果ステートへ遷移（変化）する。
    _, (result) = world.get_component(Result)[0]
    print(result.scores)
    count_player = 0
    for ent, (score) in world.get_component(Score):
        if 4 < score.score:
            result.winner = count_player
            return True
        count_player += 1
    return False