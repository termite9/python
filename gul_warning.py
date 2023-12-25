import ctypes
import win32api
import win32con
import keyboard
import winsound
import re
import threading

# 한글 자음 및 모음 조합
hangul_combinations = [
    'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ',
    'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ',
    'ㅏ', 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ'
]


def play_warning_sound():
    # 경고음 재생 코드
    winsound.Beep(1000, 500)


# 첫 번째 키를 기억할 변수
first_key = None


def check_consecutive_hangul(key1, key2):
    # 연속된 두 키가 한글 자음이거나 모음인지 확인
    hangul_combination = key1 + key2
    return hangul_combination in hangul_combinations


def on_key_event(event):
    global first_key

    key = event.Key.lower() if hasattr(event, 'Key') else event

    if first_key is None:
        # 첫 번째 키 입력 기억
        first_key = key
    else:
        # 두 번째 키 입력
        if check_consecutive_hangul(first_key, key):
            # 연속된 두 키가 한글 자음이거나 모음인 경우 경고음 재생
            play_warning_sound()

        # 첫 번째 키 초기화
        first_key = None

# Windows의 경우 모든 입력 환경에서 키보드 이벤트 감지를 위한 후킹


def hook_keyboard():
    user32 = ctypes.windll.user32
    user32.SetWindowsHookExA.restype = ctypes.c_void_p
    hook = user32.SetWindowsHookExA(
        win32con.WH_KEYBOARD_LL, ctypes.windll.kernel32.GetModuleHandleW(
            None), 0, 0
    )
    if not hook:
        return
    msg = ctypes.wintypes.MSG()
    ctypes.windll.user32.GetMessageA(ctypes.byref(msg), 0, 0, 0)
    user32.UnhookWindowsHookEx(hook)


# 키보드 후킹을 백그라운드에서 실행
keyboard_thread = threading.Thread(target=hook_keyboard)
keyboard_thread.daemon = True
keyboard_thread.start()

# 특정 키 이벤트를 후킹하여 처리
keyboard.hook(on_key_event)

# 프로그램이 종료되기 전까지 대기합니다.
keyboard.wait('esc')
