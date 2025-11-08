import pygame
import sys
from utils.button import Button

def about(WIDTH, HEIGHT, sound_volume):
    pygame.init()
    pygame.display.set_caption("MAWIO")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # --- Background ---
    bg = pygame.image.load("assets/img/BG/menu_bg.png")
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

    # --- Fonts (scaled) ---
    font_title = pygame.font.Font(None, int(WIDTH * 0.06))
    font_text = pygame.font.Font(None, int(WIDTH * 0.035))

    # --- Buttons ---
    back_button = Button("Back", (WIDTH * 0.05, HEIGHT * 0.85), (WIDTH * 0.15, HEIGHT * 0.08))
    section_buttons = [
        Button("Controls", (WIDTH * 0.25, HEIGHT * 0.15), (WIDTH * 0.15, HEIGHT * 0.07)),
        Button("Team", (WIDTH * 0.45, HEIGHT * 0.15), (WIDTH * 0.15, HEIGHT * 0.07)),
        Button("Credits", (WIDTH * 0.65, HEIGHT * 0.15), (WIDTH * 0.15, HEIGHT * 0.07)),
    ]

    # --- Section data ---
    sections = {
        "Team": [
            "...",
            "..."
        ],
        "Credits": [
            "...",
            
        ],
        "Controls": [
            "W / UP ARROW          : Move Up",
            "S / DOWN ARROW    : Move Down",
            "A / LEFT ARROW       : Move Left",
            "D / RIGHT ARROW    : Move Right",
            "SPACE                         : Jump / Interact",
            "ESC                              : Pause",
        ]
    }

    # --- Default section ---
    current_section = "Controls"

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if back_button.is_clicked(mouse_pos):
                    print("Returning to main menu...")
                    return "menu", WIDTH, HEIGHT, sound_volume
                for btn in section_buttons:
                    if btn.is_clicked(mouse_pos):
                        current_section = btn.text
                        print(f"Switched to {current_section} section.")

        # --- Draw background ---
        screen.blit(bg, (0, 0))

        # --- Title ---
        title_text = font_title.render("About", True, (0, 0, 0))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT * 0.05))

        # --- Section buttons ---
        for btn in section_buttons:
            btn.draw(screen)

        # --- Content box ---
        content_y = HEIGHT * 0.3
        for line in sections[current_section]:
            text_surface = font_text.render(line, True, (0, 0, 0))
            screen.blit(text_surface, (WIDTH * 0.2, content_y))
            content_y += text_surface.get_height() + HEIGHT * 0.015

        # --- Back button ---
        back_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    return "menu", WIDTH, HEIGHT, sound_volume
