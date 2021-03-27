import pygame
import sys  # pylint: disable=unused-import
import random  # pylint: disable=unused-import


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 420))
    screen.blit(floor_surface, (floor_x_pos + 288, 420))


def create_pipe():
    random_pipe_position = random.choice(pipe_height)
    bottom_new_pipe = pipe_surface.get_rect(midtop=(350, random_pipe_position))
    top_new_pipe = pipe_surface.get_rect(
        midbottom=(350, random_pipe_position-130))
    return bottom_new_pipe, top_new_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2.88
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 420:
        death_sound.play()
        return False

    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(124, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(
            f'score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(
            f'score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(
            f'high score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(144, 400))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


pygame.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=512)
pygame.init()
screen = pygame.display.set_mode((288, 512), 0, 32)
clock = pygame.time.Clock()
game_font = pygame.font.Font(
    r".\game soure material\Font\04b19.ttf", 20)

# game variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

bg_surface = pygame.image.load(
    r".\game soure material\sprites\background-day.png"
)

floor_surface = pygame.image.load(
    r".\game soure material\sprites\base.png"
)
floor_x_pos = 0

# Bird
bird_downflap = pygame.image.load(
    r".\game soure material\sprites\bluebird-downflap.png")
bird_midflap = pygame.image.load(
    r".\game soure material\sprites\bluebird-midflap.png")
bird_upflap = pygame.image.load(
    r".\game soure material\sprites\bluebird-upflap.png")
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(124, 256))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)
# bird_surface = pygame.image.load(
#     r".\game soure material\sprites\bluebird-midflap.png")
# bird_rect = bird_surface.get_rect(center=(50, 256))

pipe_surface = pygame.image.load(
    r".\game soure material\sprites\pipe-green.png")
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1000)
pipe_height = [200, 250, 300, 350, 400]

game_over_surface = pygame.image.load(
    r".\game soure material\sprites\message.png")
game_over_rect = game_over_surface.get_rect(center=(144, 256))

flap_sound = pygame.mixer.Sound(r'.\game soure material\audio\wing.wav')
death_sound = pygame.mixer.Sound(r'.\game soure material\audio\hit.wav')
score_sound = pygame.mixer.Sound(r'.\game soure material\audio\point.wav')
score_sound_countdown = 100


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active == True:
                bird_movement = 0
                bird_movement -= 6
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (124, 256)
                bird_movement = 0
                score = 0
                score_sound_countdown = 100

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))

    if game_active:
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # score
        score += 0.011
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown == 0:
            score_sound.play()
            score_sound_countdown = 100

    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # Floor
    draw_floor()
    floor_x_pos -= 0.5
    if floor_x_pos < -288:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(90)
