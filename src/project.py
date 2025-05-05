import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 255, 0)
INPUT_COLOR = (255, 255, 255)
CURSOR_COLOR = (255, 255, 255)
FONT_SIZE = 17
INPUT_AREA_HEIGHT = 40
PADDING = 10

try:
    FONT = pygame.font.SysFont("Courier New", FONT_SIZE)
except pygame.error:
    FONT = pygame.font.Font(None, FONT_SIZE)

game_output_lines = []
current_input = ""

STATE_COMMAND = 0
STATE_CHOICE = 1
STATE_BANDIT_COMBAT = 2
STATE_GAME_OVER = 3
STATE_WIN = 4

SCENE_TRAIN_START = 0
SCENE_TRAIN_BANDITS = 1

player_hp = 10
bandit_count = 3
player_attack_dc = 10
bandit_attack_dc = 10
bandit_damage = 2
advantage_on_next_attack = False

current_scene = SCENE_TRAIN_START
game_state = STATE_COMMAND

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("TextBuster Terminal")

def draw_text(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    fontHeight = font.size("Tg")[1]

    lines = text.split('\n')
    rendered_lines = []

    for line in lines:
        words = line.split(' ')
        current_line = ''
        for word in words:
            if word and font.size(current_line + ' ' + word)[0] < rect.width:
                if current_line:
                    current_line += ' ' + word
                else:
                    current_line = word
            else:
                if current_line:
                    rendered_lines.append(current_line)
                current_line = word
        if current_line:
            rendered_lines.append(current_line)

    for render_line in rendered_lines:
        if y + fontHeight > rect.bottom:
            break

        if bkg:
            image = font.render(render_line, 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(render_line, aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

def add_output_line(line):
    game_output_lines.append(line)

def reset_game():
    global game_output_lines, current_input, current_scene, game_state
    global player_hp, bandit_count, advantage_on_next_attack
    game_output_lines.clear()
    current_input = ""
    current_scene = SCENE_TRAIN_START
    game_state = STATE_COMMAND
    player_hp = 10
    bandit_count = 3
    advantage_on_next_attack = False
    add_output_line("Starting a new game...")
    add_output_line("Hello, and welcome to TextBuster")
    add_output_line("To begin, type 'start' to begin your journey!")
    add_output_line("Type 'quit' to exit.")
    add_output_line("-" * 40)

def roll_d20(advantage=False, disadvantage=False):
    roll1 = random.randint(1, 20)
    if advantage:
        roll2 = random.randint(1, 20)
        add_output_line(f"Rolled {roll1} and {roll2} with advantage.")
        return max(roll1, roll2)
    elif disadvantage:
        roll2 = random.randint(1, 20)
        add_output_line(f"Rolled {roll1} and {roll2} with disadvantage.")
        return min(roll1, roll2)
    else:
        add_output_line(f"Rolled a {roll1}.")
        return roll1

def process_command(command):
    global game_state, current_scene, player_hp, bandit_count, advantage_on_next_attack
    command = command.lower().strip()

    try:
        if command == "quit":
            add_output_line("Exiting game...")
            pygame.quit()
            sys.exit()
        elif command == "help":
            if game_state == STATE_COMMAND:
                 add_output_line("Available commands: start, quit, help")
            elif game_state == STATE_CHOICE:
                if current_scene == SCENE_TRAIN_START:
                     add_output_line("Choices: 1 (Stand up), 2 (Look), 3 (Sit and Wait)")
                elif current_scene == SCENE_TRAIN_BANDITS:
                     add_output_line("Choices: 1 (Fight), 2 (Keep your head down), 3 (Play it cool)")
                else:
                     add_output_line("No specific choices available right now. Try a general command.")
            elif game_state == STATE_BANDIT_COMBAT:
                 add_output_line("Combat: Type 'attack' or 'fight' to attack!")
            elif game_state == STATE_GAME_OVER:
                 add_output_line("Type 'start' to play again or 'quit' to exit.")
            elif game_state == STATE_WIN:
                 add_output_line("Type 'start' to play again or 'quit' to exit.")
            return

        if game_state == STATE_GAME_OVER:
             if command == "start":
                 reset_game()
             else:
                 add_output_line(f"Game Over. Type 'start' to play again or 'quit' to exit.")
             return

        elif game_state == STATE_WIN:
             if command == "start":
                 reset_game()
             else:
                 add_output_line(f"You have won! Type 'start' to play again or 'quit' to exit.")
             return

        if game_state == STATE_COMMAND:
            if current_scene == SCENE_TRAIN_START:
                if command == "start":
                    add_output_line("You are aboard a train, waiting to return home... yet, something feels off")
                    add_output_line("What do you do?")
                    add_output_line("1. Stand up")
                    add_output_line("2. Look")
                    add_output_line("3. Sit and Wait")
                    game_state = STATE_CHOICE
                else:
                    add_output_line(f"Unknown command: '{command}'")

            elif current_scene == SCENE_TRAIN_BANDITS:
                 add_output_line(f"Unknown command in this situation: '{command}'")

        elif game_state == STATE_CHOICE:
            if current_scene == SCENE_TRAIN_START:
                if command in ["1", "stand up", "2", "look", "3", "sit and wait"]:
                    if command in ["1", "stand up"]:
                         add_output_line("You stand up and look around the train car.")
                    elif command in ["2", "look"]:
                         add_output_line("You look around from your seat. The other passengers seem unusually still.")
                    elif command in ["3", "sit and wait"]:
                         add_output_line("You decide to sit and wait, hoping things will return to normal.")
                         add_output_line("Nothing seems to happen immediately.")

                    add_output_line("Suddenly, the train car doors burst open!")
                    add_output_line("A group of rough-looking bandits enters, weapons drawn.")
                    add_output_line("What do you do?")
                    add_output_line("1. Fight")
                    add_output_line("2. Keep your head down")
                    add_output_line("3. Play it cool till they are closer.")
                    current_scene = SCENE_TRAIN_BANDITS
                    game_state = STATE_CHOICE
                else:
                    add_output_line(f"Invalid choice: '{command}'. Please enter 1, 2, or 3.")

            elif current_scene == SCENE_TRAIN_BANDITS:
                if command == "1" or command.lower() == "fight":
                    add_output_line("You rush forward, but the bandits are too quick!")
                    add_output_line("They easily overwhelm you. (GAME OVER!)")
                    game_state = STATE_GAME_OVER
                elif command == "2" or command.lower() == "keep your head down":
                    add_output_line("You try to make yourself small and hope the bandits don't notice you.")
                    add_output_line("They seem focused on something else for now...")
                    add_output_line("You see an opportunity to attack the bandit in the back.")
                    add_output_line("Type 'attack' to attempt a stealth attack with advantage.")
                    game_state = STATE_BANDIT_COMBAT
                    advantage_on_next_attack = True
                elif command == "3" or command.lower() == "play it cool" or command.lower() == "play it cool till they are closer":
                     add_output_line("You try to act casual, observing the bandits as they approach.")
                     add_output_line("They are getting closer...")
                     add_output_line("Type 'attack' to attack the closest bandit.")
                     game_state = STATE_BANDIT_COMBAT
                     advantage_on_next_attack = False
                else:
                     add_output_line(f"Invalid choice: '{command}'. Please enter 1, 2, or 3.")

        elif game_state == STATE_BANDIT_COMBAT:
            if command == "attack" or command.lower() == "fight":
                add_output_line("-" * 20)
                add_output_line("Combat Round!")

                add_output_line("You attack!")
                if advantage_on_next_attack:
                    player_roll = roll_d20(advantage=True)
                    advantage_on_next_attack = False
                else:
                    player_roll = roll_d20()

                if player_roll >= player_attack_dc:
                    add_output_line("Your attack hits!")
                    bandit_count -= 1
                    add_output_line(f"One bandit is defeated! ({bandit_count} remaining)")

                    if bandit_count <= 0:
                        add_output_line("You have defeated the bandits! (YOU WIN!)")
                        game_state = STATE_WIN
                        return
                else:
                    add_output_line("Your attack misses!")

                if bandit_count > 0:
                    add_output_line("The bandits attack!")
                    total_bandit_damage_this_round = 0
                    for i in range(bandit_count):
                        bandit_roll = roll_d20(disadvantage=True)
                        if bandit_roll >= bandit_attack_dc:
                            add_output_line(f"Bandit {i+1}'s attack hits!")
                            total_bandit_damage_this_round += bandit_damage
                        else:
                            add_output_line(f"Bandit {i+1}'s attack misses!")

                    if total_bandit_damage_this_round > 0:
                        player_hp -= total_bandit_damage_this_round
                        add_output_line(f"You take {total_bandit_damage_this_round} damage! ({player_hp} HP remaining)")

                    if player_hp <= 0:
                        add_output_line("You have been defeated by the bandits! (GAME OVER!)")
                        game_state = STATE_GAME_OVER
                        return

                if game_state == STATE_BANDIT_COMBAT:
                    add_output_line("-" * 20)
                    add_output_line("Combat continues. Type 'attack' to fight again!")

            else:
                add_output_line(f"Invalid combat command: '{command}'. Type 'attack' or 'fight'.")

    except Exception as e:
        add_output_line(f"An error occurred while processing your command: {e}")
        add_output_line("Please check your game logic for issues.")
        game_state = STATE_COMMAND

reset_game()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                current_input = current_input[:-1]
            elif event.key == pygame.K_RETURN:
                process_command(current_input)
                current_input = ""
            elif event.key == pygame.K_ESCAPE:
                running = False
            else:
                current_input += event.unicode

    screen.fill(BG_COLOR)

    output_area_rect = pygame.Rect(PADDING, PADDING, SCREEN_WIDTH - 2 * PADDING, SCREEN_HEIGHT - INPUT_AREA_HEIGHT - 3 * PADDING)

    line_height = FONT.size("Tg")[1] + abs(-2)
    max_visible_lines = output_area_rect.height // line_height if line_height > 0 else 0

    visible_output_lines = game_output_lines[-max_visible_lines:]

    full_output_text = "\n".join(visible_output_lines)

    draw_text(screen, full_output_text, TEXT_COLOR, output_area_rect, FONT)

    input_area_rect = pygame.Rect(PADDING, SCREEN_HEIGHT - INPUT_AREA_HEIGHT - PADDING, SCREEN_WIDTH - 2 * PADDING, INPUT_AREA_HEIGHT)
    pygame.draw.rect(screen, (30, 30, 30), input_area_rect)

    if game_state == STATE_COMMAND:
        prompt_text = "> "
    elif game_state == STATE_CHOICE:
        prompt_text = "Choice > "
    elif game_state == STATE_BANDIT_COMBAT:
        prompt_text = "Combat > "
    elif game_state == STATE_GAME_OVER:
        prompt_text = "Game Over > "
    elif game_state == STATE_WIN:
        prompt_text = "You Win > "
    else:
        prompt_text = "> "

    input_display_text = prompt_text + current_input
    input_text_surface = FONT.render(input_display_text, True, INPUT_COLOR)
    screen.blit(input_text_surface, (input_area_rect.left + PADDING, input_area_rect.top + PADDING))

    if pygame.time.get_ticks() % 1000 < 500:
        cursor_pos_x = input_area_rect.left + PADDING + FONT.size(input_display_text)[0]
        cursor_rect = pygame.Rect(cursor_pos_x, input_area_rect.top + PADDING, 2, FONT_SIZE)
        pygame.draw.rect(screen, CURSOR_COLOR, cursor_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
