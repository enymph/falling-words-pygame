from random import *
import pygame
import sys
import os
import random

pygame.init()

random_sound = 0


def game():

    keyboard_sound = pygame.mixer.Sound('Assets/sounds/keyboard.wav')
    fail_sound = pygame.mixer.Sound('Assets/sounds/fail.wav')
    success_sound = pygame.mixer.Sound('Assets/sounds/success.wav')

    y = 0
    X, Y = 618, 900
    FPS = 60
    y1 = -100

    HEALTH = 3
    HEALTH_LEFT = HEALTH

    end = 25

    random_words = []
    words = []
    i = -1
    total_words = end + HEALTH

    with open('assets/wordlist.txt', 'r') as f:

        words = f.readlines()
        words = [word.strip() for word in words if len(
            word.strip()) > 5 and len(word.strip()) < 12]
        # words = [word.strip() for word in words]

        while i != total_words:

            random_words.append(words[randint(0, len(words))])
            i += 1

    user_input = ''
    random_word = random_words[0]

    text_white = (245, 245, 245)
    white = (243, 229, 210)
    white2 = (243, 229-100, 210-100)
    white3 = (243, 229-150, 210-150)
    win_color = (140, 255, 113)
    lose_color = (255, 70, 70)
    black = (0, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 128)
    red = (255, 0, 0)
    font = pygame.font.Font('assets/retro.ttf', 26)

    display = pygame.display.set_mode((X, Y))
    pygame.display.set_caption('Falling Words')

    text = font.render(user_input, True, text_white, black)
    textRect = text.get_rect()
    textRect.center = (X // 2, Y // 2)

    falling_word = font.render(random_word, True, text_white, black)
    falling_word_rect = falling_word.get_rect()
    falling_word_rect.center = (X // 2, Y // 2)

    status = font.render(
        "Words: " + str(end - total_words + HEALTH_LEFT) + "/" + str(end), True, black)
    statusRect = status.get_rect()
    statusRect.center = (X // 2, Y // 2)

    text4 = font.render("Health: " + str(HEALTH_LEFT), True, black)
    text4Rect = text4.get_rect()
    text4Rect.center = (X // 2, Y // 2)

    display.fill(white)
    pygame.draw.line(display, blue, (0, 0), (X, Y))
    arrow = pygame.image.load('assets/arrow.png')
    arrow = pygame.transform.scale(arrow, (int(X/10), int(Y/10)))

    restart_text = font.render('press <R> to restart', True, black, white)
    win_text = font.render("You Win!", True, black, white)
    lose_text = font.render("You Lost!", True, black, white)

    bg_colors = [white, white2, white3]

    F_KEYS = [pygame.K_F1, pygame.K_F2, pygame.K_F3, pygame.K_F4, pygame.K_F5, pygame.K_F6,
              pygame.K_F7, pygame.K_F8, pygame.K_F9, pygame.K_F10, pygame.K_F11, pygame.K_F12]
    non_letters = [pygame.K_RETURN, pygame.K_BACKSPACE, pygame.K_DELETE, pygame.K_SPACE, pygame.K_CAPSLOCK, pygame.K_LMETA, pygame.K_RMETA, pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_LALT, pygame.K_RALT, pygame.K_LCTRL,
                   pygame.K_RCTRL, pygame.K_TAB, pygame.K_PRINTSCREEN, pygame.K_SCROLLLOCK, pygame.K_BREAK, pygame.K_INSERT, pygame.K_HOME, pygame.K_PAGEUP, pygame.K_PAGEDOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN] + F_KEYS

    clock = pygame.time.Clock()
    speed = 2

    while True:
        play_music()
        current_color = bg_colors[-HEALTH_LEFT]
        display.fill(current_color)
        pygame.draw.line(display, blue, (0, Y-32), (X, Y-32))
        y += speed
        clock.tick(FPS)

        display.blit(text, ((X-text.get_width())//2, Y-32))
        display.blit(falling_word, ((X-falling_word.get_width())//2, y))
        display.blit(status, (0, 0))
        display.blit(text4, (0, 32))
        display.blit(arrow, ((X-arrow.get_width()-80, y1)))
        pygame.display.update()
        y1 -= 12

        while total_words - HEALTH_LEFT == 0:

            display.fill(win_color)

            display.blit(win_text, ((X-win_text.get_width())//2, Y//2-42))
            display.blit(
                restart_text, ((X-restart_text.get_width())//2, Y//2+10))

            pygame.display.update()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_r:
                        return game()

                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            random_sound.stop()

        while HEALTH_LEFT == 0:

            display.fill(lose_color)

            display.blit(
                lose_text, ((X-lose_text.get_width())//2, Y//2-42))

            display.blit(
                restart_text, ((X-restart_text.get_width())//2, Y//2+10))

            pygame.display.update()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_r:

                        game()

            random_sound.stop()

        if y+64 > Y:

            y = 0
            HEALTH_LEFT -= 1
            y1 = -100
            text4 = font.render("Health: " + str(HEALTH_LEFT), True, black)
            text4Rect = text4.get_rect()
            text4Rect.center = (X // 2, Y // 2)
            random_word = random_words[-total_words]
            total_words -= 1
            falling_word = font.render(random_word, True, text_white, black)
            display.blit(falling_word, ((X-falling_word.get_width())//2, 0))
            fail_sound.play()

        if random_word < user_input:
            text = font.render(user_input, True, red, black)
            display.blit(text, ((X-text.get_width())//2, Y-32))

        if random_word == user_input:
            text = font.render(user_input, True, green, black)
            display.blit(text, ((X-text.get_width())//2, Y-32))

        if random_word == user_input and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                y = 0
                user_input = ''
                random_word = random_words[-total_words]
                total_words -= 1
                falling_word = font.render(
                    random_word, True, text_white, black)
                display.blit(
                    falling_word, ((X-falling_word.get_width())//2, 0))
                status = font.render(
                    "Words: " + str(end - total_words + HEALTH_LEFT) + "/" + str(end), True, black)
                text = font.render(user_input, True, text_white, black)
                display.blit(text, ((X-text.get_width())//2, Y-32))
                success_sound.play()

            if (total_words-HEALTH_LEFT) % 5 == 0 and total_words-HEALTH_LEFT < end:
                arrow = pygame.transform.scale(
                    arrow, (int(X/10), int(Y/10)))
                speed = increase_speed(speed)

                if total_words-HEALTH_LEFT != 0:
                    y1 = Y

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    user_input = ''
                    text = font.render(user_input, True, text_white, black)
                    display.blit(text, ((X-text.get_width())//2, Y-32))

                elif event.key == pygame.K_BACKSPACE:

                    user_input = user_input[:-1]
                    text = font.render(user_input, True, text_white, black)
                    display.blit(text, ((X-text.get_width())//2, Y-32))

                elif event.key not in non_letters:

                    user_input += str(pygame.key.name(event.key))
                    keyboard_sound.play()
                    text = font.render(user_input, True, text_white, black)
                    display.blit(text, ((X-text.get_width())//2, Y-32))


def increase_speed(speed):

    speed += 1.1

    return speed


i = 0

musics = []


for filename in os.scandir("Assets/musics"):
    if filename.is_file():
        musics.append(filename.path)

random_nums = random.sample(range(len(musics)), len(musics))


def play_music():

    global i
    global random_nums
    global random_sound
    pygame.mixer.init()

    pygame.mixer.set_num_channels(2)

    voice = pygame.mixer.Channel(0)

    if not voice.get_busy():

        random_sound = pygame.mixer.Sound(musics[random_nums[i]])
        pygame.mixer.Sound.play(random_sound)
        i += 1
        if i == len(random_nums):
            i = 0
            random_nums = random.sample(range(len(musics)), len(musics))


game()
