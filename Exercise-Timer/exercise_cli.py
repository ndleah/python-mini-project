import click
import time as t
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

pygame.mixer.init()

def play_audio_start():
    start_audio = pygame.mixer.Sound("beep_start.mp3")
    start_audio.play()
    pygame.time.wait(int(start_audio.get_length() * 1000)) 

def play_audio_stop():
    stop_audio = pygame.mixer.Sound("beep_stop.mp3")
    stop_audio.play()
    pygame.time.wait(int(stop_audio.get_length() * 1000)) 
    
    
@click.command()
@click.option('--time', '-t', default=10, help='Time you want to exercise')
@click.option('--interval', '-i', default=3, help='Interval you want for exercise')
@click.option('--reps', '-r', default=5, help='Reps you want to do')
def exercise(time:int, interval:int, reps:int):
    for _ in range(reps):
        print('Interval')
        t.sleep(interval)
        print('Start')
        play_audio_start()
        t.sleep(time)
        print('Stop')
        play_audio_stop()
        t.sleep(interval)
        reps -= 1
        if reps != 0:
            print(f'Reps left: {reps}')
        else:
            print("Finished")
            finish_audio = pygame.mixer.Sound("beep_finish.mp3")
            finish_audio.play()
            pygame.time.wait(int(finish_audio.get_length() * 1500)) 

if __name__ == '__main__':
    exercise()
