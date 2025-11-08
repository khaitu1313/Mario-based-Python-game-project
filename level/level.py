import pygame
from entity.terrain import Terrain
from entity.coin import Coin # Adding Coin
from entity.enemy import MeleeEnemy, RangeEnemy, Boss
from entity.container import Container
from entity.portal import Portal


TILE_SIZE = 64  # each block = 64x64 pixels


class Level:
    """Base class for all levels."""
    def __init__(self, level_id, spawn, map_size, terrain_matrix, coins=[], containers = []):
        self.level_id = level_id
        self.spawn = spawn
        self.coins = coins
        self.Enemies = []
        self.containers = containers

        # Add 1-block border around the terrain matrix
        self.terrain_matrix = self.add_border(terrain_matrix)

        # Automatically recalculate map size based on bordered matrix
        self.map_size = (
            len(self.terrain_matrix[0]) * TILE_SIZE,  # width
            len(self.terrain_matrix) * TILE_SIZE      # height
        )
        self.boss = None
    def add_border(self, matrix):
        """Add a 1-block thick border around the map."""
        if not matrix:
            return [[1]]

        rows = len(matrix)
        cols = len(matrix[0])

        # Create new bordered matrix
        bordered = [[1] * (cols + 2)]  # top border
        for row in matrix:
            bordered.append([1] + row + [1])  # left/right borders
        bordered.append([1] * (cols + 2))  # bottom border

        return bordered

    def get_terrain(self):
        """Convert terrain matrix into a list of Terrain objects."""
        terrain_list = []
        for row_index, row in enumerate(self.terrain_matrix):
            for col_index, tile in enumerate(row):
                if tile == 1:  # solid block
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE
                    terrain_list.append(Terrain(x, y, TILE_SIZE))
        return terrain_list
    def get_nor_enemies(self):
        return [e for e in self.Enemies if not e.special]
    def get_spe_enemies(self):
        return [e for e in self.Enemies if e.special]
    def print_coin(self):
        for coin in self.coins:
            coin.draw(screen, camera_x, camera_y)
            coin.update(player)
    def get_boss(self):
        return self.boss

# ===========================================================
#                        LEVEL 1
# ===========================================================
class Level1(Level):
    """Tutorial level: flat ground with raised platform."""
    def __init__(self):
        terrain_matrix = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        ]

        super().__init__(
            level_id=1,
            spawn=(100, 610),
            map_size=(5120, 704),
            terrain_matrix=terrain_matrix,
            coins = [
    Coin(400, 500, 100),
    Coin(600, 500, 100),
    Coin(900, 420, 100),
    Coin(1200, 420, 100),
    Coin(1600, 500, 100),
    Coin(1900, 500, 100),
    Coin(2500, 500, 100),
    Coin(2800, 500, 100)
],

containers = [
    Container(1000, 500, 100),
    Container(2200, 500, 100)
]

        )
        self.Enemies = []
        self.portal = Portal(5000, 576, 64, 96)
        



# ===========================================================
#                        LEVEL 2
# ===========================================================
class Level2(Level):
    """Main level: longer with small gaps and elevated platforms."""
    def __init__(self):
        terrain_matrix = [
            [0]*80 for _ in range(9)
        ]

        # Ground with gaps
        terrain_matrix.append([
            1 if not (10 <= i < 13 or 30 <= i < 33 or 55 <= i < 58) else 0
            for i in range(80)
        ])

        # Elevated platforms
        terrain_matrix[6][12:17] = [1]*5
        terrain_matrix[4][32:37] = [1]*5
        terrain_matrix[6][48:55] = [1]*8
        terrain_matrix[4][60:63] = [1]*3
        terrain_matrix[7][30] = 1
        terrain_matrix[6][60]=1
        terrain_matrix[5][50] = 1


        super().__init__(
            level_id=2,
            spawn=(150, 704 - 160),
            map_size=(5120, 704),
            terrain_matrix=terrain_matrix,
            coins = [
    Coin(750, 300, 100),
    Coin(1150, 300, 100),
    Coin(1800, 500, 100),
    Coin(2600, 420, 100),
    Coin(3400, 320, 100),
    Coin(4200, 500, 100),
    Coin(4800, 420, 100)
],

containers = [
    Container(1000, 300, 100),
    Container(3600, 320, 100)
]

        )
        self.Enemies = []
        self.Enemies.append(RangeEnemy( 61*64+24,384 ,40, 40, special=True, dir_Left=True))
        self.Enemies.append(RangeEnemy(11 * 64, 640, 40, 40, special=False, dir_Left=False))    # special guarding left of 1st pit
        self.Enemies.append(RangeEnemy(13 * 64+24, 640, 40, 40, special=False, dir_Left=True))   # normal right of 1st pit

        self.Enemies.append(RangeEnemy(31 * 64, 640, 40, 40, special=False, dir_Left=False))  # normal left of 2nd pit
        self.Enemies.append(RangeEnemy(33 * 64+24, 640, 40, 40, special=False, dir_Left=True))    # special right of 2nd pit

        self.Enemies.append(RangeEnemy(56 * 64, 640, 40, 40, special=False, dir_Left=False))   # special left of 3rd pit
        self.Enemies.append(RangeEnemy(58 * 64+24, 640, 40, 40, special=False, dir_Left=True))   # normal right of 3rd pit

        # Melee enemies roaming freely (some special)
        self.Enemies.append(MeleeEnemy(20 * 64, 576, 40, 40, special=False))   # normal between pit 1 & 2
        self.Enemies.append(MeleeEnemy(40 * 64, 576, 40, 40, special=True))    # special between pit 2 & 3
        self.Enemies.append(MeleeEnemy(62 * 64+90, 576, 40, 40, special=False))   # normal after pit 3
        self.Enemies.append(MeleeEnemy(62 * 64, 576, 40, 40, special=True)) 

        
        self.portal = Portal(5000, 512, 64, 96) 
    
# ===========================================================
#                        LEVEL 3
# ===========================================================
class Level3(Level):
    """Boss fight arena: smaller, flat with 3 left platforms."""
    def __init__(self):
        # 10 rows, 18 columns (1280x720 total)
        terrain_matrix = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # top platform
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],  # mid platform
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0],  # bottom platform
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],  # ground
        ]

        super().__init__(
            level_id=3,
            spawn=(100, 704 - 192),
            map_size=(1280, 720),
            terrain_matrix=terrain_matrix,
            coins=[
    Coin(200, 450, 100),
    Coin(400, 450, 100),
    Coin(280, 320, 100),
    Coin(250, 160, 100),
    Coin(700, 500, 100),
    Coin(900, 500, 100),
    Coin(1100, 300, 100),
],
containers=[
    Container(600, 496, 100),
]

        )
        self.boss = Boss(1100, 64, 240,240)
        self.portal = None