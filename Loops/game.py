import pygame
import sys
from utils.gameFunc import draw, get_background, handle_move
from utils.button import Button
from entity.terrain import Terrain
from level.level import Level1, Level2, Level3
from entity.player import Player
from entity.proj import Proj
from entity.enemy import Enemy, MeleeEnemy, RangeEnemy
from entity.coin import Coin # Add Coin
from entity.container import Container # Add Container
from entity.star import Star # Add Star

FPS = 60

def game(WIDTH, HEIGHT, sound_volume, level=1):
    
    pygame.init()
    pygame.display.set_caption("MAWIO")

    BASE_WIDTH, BASE_HEIGHT = 1280, 720  # internal 16:9 resolution
    base_surface = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    setting = False

    # --- Load background and gear icon ---
    bg_tiles, bg_image = get_background("Blue.png", BASE_WIDTH, BASE_HEIGHT)
    bg_surface = pygame.Surface((WIDTH, HEIGHT))
    for pos in bg_tiles:
        bg_surface.blit(bg_image, pos)
    
    gear_img = pygame.image.load("assets/img/icon/setting.png").convert_alpha()
    gear_size = int(BASE_WIDTH * 0.04)
    gear_img = pygame.transform.scale(gear_img, (gear_size, gear_size))
    gear_rect = gear_img.get_rect(topright=(BASE_WIDTH - 20, 20))

    # --- Settings data ---
    resolutions = [
        (640, 360),
        (854, 480),
        (960, 540),
        (1024, 576),
        (1152, 648),
        (1280, 720)
    ]
    current_res_index = resolutions.index((WIDTH, HEIGHT)) if (WIDTH, HEIGHT) in resolutions else 5
    block_size = 64
    # --- Font ---
    font_size = int(BASE_WIDTH * 0.04)
    font = pygame.font.Font(None, font_size)

    # --- Settings buttons ---
    def make_settings_buttons():
        return (
            Button("Back", (BASE_WIDTH // 2 - int(BASE_WIDTH * 0.1), int(BASE_HEIGHT * 0.8)), (BASE_WIDTH * 0.2, BASE_HEIGHT * 0.08)),
            Button("Return to Menu", (BASE_WIDTH // 2 - int(BASE_WIDTH * 0.1), int(BASE_HEIGHT * 0.9)), (BASE_WIDTH * 0.25, BASE_HEIGHT * 0.08)),
            Button(f"{resolutions[current_res_index][0]}x{resolutions[current_res_index][1]}",
                   (BASE_WIDTH // 2 - BASE_WIDTH * 0.1, BASE_HEIGHT * 0.4), (BASE_WIDTH * 0.25, BASE_HEIGHT * 0.08)),
            Button("-", (BASE_WIDTH // 2 - BASE_WIDTH * 0.15, BASE_HEIGHT * 0.55), (BASE_WIDTH * 0.06, BASE_WIDTH * 0.06)),
            Button("+", (BASE_WIDTH // 2 + BASE_WIDTH * 0.09, BASE_HEIGHT * 0.55), (BASE_WIDTH * 0.06, BASE_WIDTH * 0.06))
        )

    back_button, menu_button, res_button, vol_minus, vol_plus = make_settings_buttons()
    
    def load_level(level):
        print(f"Loading level {level}...")
        if level == 1:
            return Level1()
        elif level == 2:
            return Level2()
        elif level == 3:
            return Level3()
        else:
            print("No more levels! Returning to menu.")
            return None
            
    
    
    tiles = load_level(level)
        
    # Coin
    coins_spawn = tiles.coins
    for coin in coins_spawn:
        coin.adj_vol(sound_volume)
    
    # Container
    containers_spawn = tiles.containers

    player = Player(tiles.spawn[0], tiles.spawn[1], 50, 50)
    terrain_positions = tiles.get_terrain()
        
    camera_x = 0
    camera_y = 32
    
    Nor_enemies = []
    Spe_enemies = []
    Nor_enemies.append(MeleeEnemy(200, 600, 32, 32, False))
    Nor_enemies.append(RangeEnemy(300, 600, 32, 32,False))
    Spe_enemies.append(MeleeEnemy(200, 500, 32, 32, True))
    Spe_enemies.append(RangeEnemy(300, 500, 32, 32,True))

    nor_projs = []
    spe_projs = []
    
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if setting:
                        setting = False
                    else:
                        return "menu", WIDTH, HEIGHT, sound_volume, 1
                
                elif event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()
                elif event.key == pygame.K_h:
                    player.shoot(nor_projs, spe_projs, setting)
                elif event.key == pygame.K_TAB or event.key == pygame.K_u:
                    setting = not setting
                
                #dev cheat
                elif event.key == pygame.K_p:
                    if level < 3:
                        level += 1
                        print(f"Level increased to {level}")
                        return "game", WIDTH, HEIGHT, sound_volume, level
                    else:
                        print("Reached final level, returning to menu...")
                        return "menu", WIDTH, HEIGHT, sound_volume, 1

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                # Adjust mouse for scale
                scale_x = BASE_WIDTH / WIDTH
                scale_y = BASE_HEIGHT / HEIGHT
                adj_mouse = (mouse_pos[0] * scale_x, mouse_pos[1] * scale_y)

                if setting:
                    if back_button.is_clicked(adj_mouse):
                        setting = False
                    elif menu_button.is_clicked(adj_mouse):
                        return "menu", WIDTH, HEIGHT, sound_volume, 1
                    elif res_button.is_clicked(adj_mouse):
                        current_res_index = (current_res_index + 1) % len(resolutions)
                        WIDTH, HEIGHT = resolutions[current_res_index]
                        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                        res_button.text = f"{WIDTH}x{HEIGHT}"
                    elif vol_minus.is_clicked(adj_mouse):
                        sound_volume = max(0, sound_volume - 10)
                        for coin in coins_spawn:
                            coin.adj_vol(sound_volume)
                    elif vol_plus.is_clicked(adj_mouse):
                        sound_volume = min(100, sound_volume + 10)
                        for coin in coins_spawn:
                            coin.adj_vol(sound_volume)
                else:
                    if gear_rect.collidepoint(adj_mouse):
                        setting = True
        keys = pygame.key.get_pressed()
                
        # --- Smart camera follow with 30px dead zone ---
        DEAD_ZONE = 30
        SMOOTHNESS = 0.1  # smaller = smoother (slower), larger = snappier




        # Calculate distance from current camera center to player center
        dx = player.rect.centerx - (camera_x + BASE_WIDTH // 2)


        # Only move camera if player leaves dead zone or to slowly recenter when stopped
        if abs(dx) > DEAD_ZONE:
            camera_x += dx * SMOOTHNESS
        else:
            # Slowly move toward player even when inside dead zone (gentle recenter)
            camera_x += dx * (SMOOTHNESS / 5)

        # Clamp camera to level bounds
        # Clamp camera to level bounds
        camera_x = max(0, min(camera_x, tiles.map_size[0] - BASE_WIDTH))
        
        player.loop(FPS)
        if not setting:
            for enemy in Nor_enemies:
                enemy.update(nor_projs, spe_projs, setting)
            for proj in (nor_projs):
                proj.update(terrain_positions, player, Nor_enemies, Spe_enemies)
                if proj.destroyed == True:
                    nor_projs.remove(proj)
                    break
                if proj.rect.x<-100 or proj.rect.x > tiles.map_size[0]:
                    nor_projs.remove(proj)
        for proj in (spe_projs):
            proj.update(terrain_positions, player, Nor_enemies, Spe_enemies)
            if proj.destroyed == True:
                    spe_projs.remove(proj)
                    break
            if proj.rect.x<-100 or proj.rect.x > tiles.map_size[0]:
                spe_projs.remove(proj)
                print("removed spe")

        handle_move(player, terrain_positions)
        # solid_objects = terrain_positions + containers_spawn
        # handle_move(player, solid_objects)
        
        for enemy in Spe_enemies:
            enemy.update(nor_projs, spe_projs, setting)
        for enemy in Nor_enemies:
            if enemy.HP ==0:
                Nor_enemies.remove(enemy)
        for enemy in Spe_enemies:
            if enemy.HP ==0:
                Spe_enemies.remove(enemy)
        
        # --- Smooth the coin collecting action ---
        for coin in coins_spawn[:]:
            coin.update(player)
            if coin.collected:
                tiles.coins.remove(coin)
        
        # --- Drawing ---
        draw(base_surface, bg_surface, setting, gear_img, gear_rect, BASE_WIDTH, BASE_HEIGHT, font, sound_volume, back_button, menu_button, res_button, vol_minus, vol_plus, WIDTH, HEIGHT, screen, terrain_positions, camera_x, camera_y, player, nor_projs, spe_projs, Nor_enemies, Spe_enemies, coins_spawn, containers_spawn)

        pygame.display.flip()

    pygame.quit()
