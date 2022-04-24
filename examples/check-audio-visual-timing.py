#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2021-11-16 13:23:44 christophe@pallier.org>

''' Display a white square for 100ms and play a 100ms tone simultanously, every half second
in order to check timing with external equipment (oscilloscope, BlackBox ToolKit, ...) '''

from numpy import round
from expyriment import design, control, stimuli, misc

nTrials = 1000
frameRate = 1/60  # this is an assumption to check! See below
blankDuration = (frameRate * 18) * 1000
stimDuration = (frameRate * 12) * 1000
toneDuration = 100



exp = design.Experiment(name="Cross-modal-timing-test")

control.defaults.window_mode = 1  # 0 = FULLSCREEN
control.defaults.window_size = (1024, 768)
control.defaults.open_gl = 2  # blocking on the vertical sync retrace
control.defaults.audiosystem_buffer_size = 256  # should be large enough to avoid sound buffer underruns (check in Terminal)

control.initialize(exp)

##

bs = stimuli.BlankScreen()
square = stimuli.Rectangle((400, 400),
                               colour=(255, 255, 255),
                               position=(0, 200))
tone = stimuli.Tone(toneDuration, 440)

bs.preload()
square.preload()
tone.preload()

##

control.start(skip_ready_screen=True)
clock = misc.Clock()

exp.screen.clear()
bs.present(update=True)
nframe = 0

# Estimate the Frame Rate  (allowing to check if blocking on VSYNC)
clock.reset_stopwatch()
bs.present(update=True)
fps_estimation_duration = 2  # in s
while clock.stopwatch_time < fps_estimation_duration * 1000:
    bs.present(update=True)
    nframe += 1
FPS = nframe / fps_estimation_duration

square_nframes = int(round(stimDuration / (1000 / FPS)))
bs_nframes = int(round(blankDuration / (1000 / FPS)))

square_target_duration = 1000 / FPS * square_nframes
blank_target_duration = 1000 /FPS * bs_nframes
trial_target_duration = square_target_duration + blank_target_duration

exp.data.write_comment(f'--PARAMETERS')
exp.data.write_comment(f' Estimated FPS = {FPS}Hz')
exp.data.write_comment(f' Targeted Square duration = {round(square_target_duration, 2)} ({square_nframes} frames)')
exp.data.write_comment(f' Targeted Blanck duration = {round(blank_target_duration, 2)} ({bs_nframes} frames)')
exp.data.write_comment(f' Targeted Trial duration = {round(trial_target_duration, 2)} ({square_nframes + bs_nframes} frames)')


## 

def wait_nframes(nframes, FPS=FPS, margin=((1000 / FPS) * 0.5)):
    """Delay for a duration between (nframes - 1) and (nframes)."""
    delay = int((nframes * 1000 / FPS) - margin)
    clock.reset_stopwatch()
    while clock.stopwatch_time < delay:
        pass


##


# Display instructions
frame = stimuli.Canvas((800, 800))
msg = stimuli.TextScreen("",
                         f"""This script runs a loop in which a black screen is displayed, followed by a white rectangle and a pure tone.

This permits to check the timing with some external equipment
(an oscilloscope, the Blackbox toolkit, etc.).

The current parameters are:

FPS = {FPS} Hz
Blank duration = {round(blank_target_duration, 2)} ms
Square duration = {round(square_target_duration, 2)} ms
Tone duration = {toneDuration} ms
                         
Press any key for next screen (Later, to exit the program, just press 'Esc').""",
                         position=(0, -200))
msg.plot(frame)
square.plot(frame)
frame.present()
exp.keyboard.wait()
stimuli.TextScreen("",
                   "Press a key to start").present(clear=True, update=True)
exp.keyboard.wait()

exp.data.add_variable_names(['trial', 'squareOn', 'blankOn'])

itrial = 0
clock.reset_stopwatch()
while itrial < nTrials:  # or break when the Esc key is pressed
    bs.present(update=True)
    blankOn = clock.stopwatch_time
    wait_nframes(bs_nframes)
    square.present(update=True)
    squareOn = clock.stopwatch_time
    tone.present()
    itrial += 1
    exp.data.add([itrial, squareOn, blankOn])
    exp.keyboard.process_control_keys()
    wait_nframes(square_nframes)
    
control.end()
