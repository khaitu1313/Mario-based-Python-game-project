import pygame
import sys
from utils.button import Button

def menu(WIDTH, HEIGHT, sound_volume):
    pygame.init()
    pygame.display.set_caption("MAWIO")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    
    setting = False

    # --- Load background and gear icon ---
    bg = pygame.image.load("assets/img/BG/menu_bg.png")
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

    gear_img = pygame.image.load("assets/img/icon/setting.png")
    gear_size = int(WIDTH * 0.04)  # Scale gear icon based on width
    gear_img = pygame.transform.scale(gear_img, (gear_size, gear_size))
    gear_rect = gear_img.get_rect(topright=(WIDTH - 20, 20))

    # --- Helper to create scalable buttons ---
    def make_button(text, y_factor, width_factor=0.25, height_factor=0.08):
        """Make button centered horizontally, vertically positioned by y_factor of HEIGHT"""
        button_width = int(WIDTH * width_factor)
        button_height = int(HEIGHT * height_factor)
        x = WIDTH // 2 - button_width // 2
        y = int(HEIGHT * y_factor)
        return Button(text, (x, y), (button_width, button_height))

    # --- Buttons for main menu (scalable) ---
    buttons = [
        make_button("New Game", 0.40),
        make_button("About", 0.52),
        make_button("Exit", 0.64)
    ]

    # --- Settings menu state ---
    resolutions = [
        (640, 360),
        (854, 480),
        (960, 540),
        (1024, 576),
        (1152, 648),
        (1280, 720)
    ]
    current_res_index = 5  # default 1280x720

    # --- Font scaling ---
    font_size = int(WIDTH * 0.04)
    font = pygame.font.Font(None, font_size)

    # --- Settings buttons ---
    def make_settings_buttons():
        return (
            Button("Back", (WIDTH // 2 - int(WIDTH * 0.1), int(HEIGHT * 0.8)), (WIDTH * 0.2, HEIGHT * 0.08)),
            Button(f"{resolutions[current_res_index][0]}x{resolutions[current_res_index][1]}",
                   (WIDTH // 2 - WIDTH * 0.1, HEIGHT * 0.4), (WIDTH * 0.25, HEIGHT * 0.08)),
            Button("-", (WIDTH // 2 - WIDTH * 0.15, HEIGHT * 0.55), (WIDTH * 0.06, WIDTH * 0.06)),
            Button("+", (WIDTH // 2 + WIDTH * 0.09, HEIGHT * 0.55), (WIDTH * 0.06, WIDTH * 0.06))
        )

    back_button, res_button, vol_minus, vol_plus = make_settings_buttons()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                if setting:
                    # --- Settings Screen Logic ---
                    if back_button.is_clicked(mouse_pos):
                        setting = False

                    elif res_button.is_clicked(mouse_pos):
                        # Cycle through resolution options
                        current_res_index = (current_res_index + 1) % len(resolutions)
                        WIDTH, HEIGHT = resolutions[current_res_index]
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                        bg = pygame.transform.scale(pygame.image.load("assets/img/BG/menu_bg.png"), (WIDTH, HEIGHT))

                        # Recalculate scaling
                        gear_size = int(WIDTH * 0.04)
                        gear_img = pygame.transform.scale(pygame.image.load("assets/img/icon/setting.png"), (gear_size, gear_size))
                        gear_rect = gear_img.get_rect(topright=(WIDTH - 20, 20))
                        font_size = int(WIDTH * 0.04)
                        font = pygame.font.Font(None, font_size)

                        # Recreate buttons at new scale
                        buttons = [
                            make_button("New Game", 0.40),
                            make_button("About", 0.52),
                            make_button("Exit", 0.64)
                        ]
                        back_button, res_button, vol_minus, vol_plus = make_settings_buttons()

                    elif vol_minus.is_clicked(mouse_pos):
                        sound_volume = max(0, sound_volume - 10)

                    elif vol_plus.is_clicked(mouse_pos):
                        sound_volume = min(100, sound_volume + 10)

                else:
                    # --- Main Menu Logic ---
                    if gear_rect.collidepoint(mouse_pos):
                        setting = True

                    for button in buttons:
                        if button.is_clicked(mouse_pos):
                            if button.text == "New Game":
                                return "game", WIDTH, HEIGHT, sound_volume
                            elif button.text == "About":
                                return "about", WIDTH, HEIGHT, sound_volume
                            elif button.text == "Exit":
                                pygame.quit()
                                sys.exit()

        # --- Draw background ---
        screen.blit(bg, (0, 0))

        if setting:
            # Dim overlay
            dim_surface = pygame.Surface((WIDTH, HEIGHT))
            dim_surface.set_alpha(160)
            dim_surface.fill((0, 0, 0))
            screen.blit(dim_surface, (0, 0))

            # --- Layout ---
            center_x = WIDTH // 2
            label_x = WIDTH * 0.3
            control_x = WIDTH * 0.6
            line_gap = HEIGHT * 0.15

            title = font.render("Settings", True, (255, 255, 255))
            screen.blit(title, (center_x - title.get_width() // 2, HEIGHT * 0.1))

            # Resolution row
            res_label = font.render("Resolution:", True, (255, 255, 255))
            res_y = HEIGHT * 0.35
            screen.blit(res_label, (label_x - res_label.get_width() // 2, res_y))
            res_button.rect.center = (control_x, res_y + res_label.get_height() // 2)
            res_button.draw(screen)

            # Sound row
            sound_label = font.render("Sound:", True, (255, 255, 255))
            sound_y = res_y + line_gap
            screen.blit(sound_label, (label_x - sound_label.get_width() // 2, sound_y))
            vol_text = font.render(f"{sound_volume}%", True, (255, 255, 255))
            gap = WIDTH * 0.04
            vol_minus.rect.center = (control_x - vol_text.get_width() - gap, sound_y)
            vol_plus.rect.center = (control_x + vol_text.get_width() + gap, sound_y)
            vol_minus.draw(screen)
            vol_plus.draw(screen)
            screen.blit(vol_text, (control_x - vol_text.get_width() // 2, sound_y - vol_text.get_height() // 2))

            # Back button
            back_button.rect.center = (center_x, sound_y + line_gap * 1.5)
            back_button.draw(screen)

        else:
            # Draw gear icon (settings button)
            screen.blit(gear_img, gear_rect)

            # Draw main menu buttons
            for button in buttons:
                button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    return "menu", WIDTH, HEIGHT, sound_volume
