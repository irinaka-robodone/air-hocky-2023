from pigframe import *
from component import *

def create_hockey(world: World, x: int, y: int, color: int, 
                up: int, down: int, left: int, right: int, weight: int = 1,
                radius: int = 20) -> int:
    """Create a hockey entity.

    Args:
        world (World): The world to create the entity in.
        x (int): The x position of the entity.
        y (int): The y position of the entity.

    Returns:
        int: The entity id of created hockey.
    """
    entity = world.create_entity()
    world.add_component_to_entity(entity, Position, x = x, y = y)
    world.add_component_to_entity(entity, Velocity, x = 0, y = 0, weight = weight)
    world.add_component_to_entity(entity, Controlable, up = up, down = down, left = left, right = right)
    world.add_component_to_entity(entity, Collidable)
    world.add_component_to_entity(entity, Hockey, id = entity, color = color, radius = radius)
    world.add_component_to_entity(entity, Score)
    return entity

def create_puck(world: World, x: int, y: int, dx: int = 1, dy: int = 1, weight: int = 1,
                radius: int = 6) -> int:
    """Create a puck entity.

    Args:
        world (World): The world to create the entity in.
        x (int): The x position of the entity.
        y (int): The y position of the entity.
        dx (int, optional): The x velocity of the entity. Defaults to 1.
        dy (int, optional): The y velocity of the entity. Defaults to 1.
        speed (int, optional): The speed of the entity. Defaults to 1.
        radius (int, optional): The radius of the entity. Defaults to 6.

    Returns:
        int: The entity id of created puck.
    """
    entity = world.create_entity()
    # ポジションコンポーネントを追加する。
    world.add_component_to_entity(entity, Position, x = x, y = y)
    # ベロシティ(速度)コンポーネントを追加する。
    world.add_component_to_entity(entity, Velocity, x = dx, y = dy, weight = weight)
    # コライダブル(衝突可能)コンポーネントを追加する。
    world.add_component_to_entity(entity, Collidable)
    # パックコンポーネントを追加する。
    world.add_component_to_entity(entity, Puck, id = entity, radius = radius)
    # 作成したエンティティのIDを返す。
    return entity

def create_field(world: World, width: int = 580, height: int = 380, goal_width: int = 100) -> int:
    """Create a field entity.

    Args:
        world (World): The world to create the entity in.
        width (int, optional): The width of the entity. Defaults to 580.
        height (int, optional): The height of the entity. Defaults to 380.

    Returns:
        int: The entity id of created field.
    """
    entity = world.create_entity()
    world.add_component_to_entity(entity, Field, width = width, height = height, goal_width = goal_width)
    return entity

def create_play_status(world: World) -> int:
    """Create a play status entity which has Result component.

    Args:
        world (World): The world to create the entity in.

    Returns:
        int: The entity id of created play status.
    """
    entity = world.create_entity()
    world.add_component_to_entity(entity, Result)
    return entity