import keyboard
import winsound
import time
import pygame

pygame.mixer.init()
# pygame.mixer.music.load()
# pygame.mixer.music.play()
warning_sound = pygame.mixer.Sound("Ring01.wav")


def on_key_event(e):
    if e.event_type == keyboard.KEY_DOWN and e.name == 'w':
        # if e.event_type == keyboard.KEY_DOWN and e.name == 'q':

        print("키보드 아스키 코드 113(q)가 눌렸습니다.")
        # 여기에 원하는 동작을 추가하세요.
        warning_sound.play()


keyboard.hook(on_key_event)

# 프로그램이 종료되기 전까지 실행되도록 유지
keyboard.wait('esc')
