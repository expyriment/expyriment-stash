import os
from glob import glob

from expyriment import control, design, io, misc, stimuli
from expyriment.design.extras import StimulationProtocol


# SETTINGS
BLOCK_LENGTH = 8  # In volumes
NR_REPETITIONS = 6  # For each block (rest and imagery)
TR = 2.0
SCAN_TRIGGER = misc.constants.K_5
SCAN_TRIGGER_LTP_ADDRESS = None  # None = USB (keyboard emulation)


# DESIGN
exp = design.Experiment("Motor Imagery (Swimming)")
control.initialize(exp)
protocol = StimulationProtocol("time")

fixcross = stimuli.FixCross()
fixcross.preload()
blocks = {"rest":[stimuli.TextLine("REST",
                                   text_size=70,
                                   text_colour=misc.constants.C_RED,
                                   text_font="monospace"),
                  stimuli.Audio("stimuli/rest.wav")],
          "swim":[stimuli.TextLine("SWIM",
                                   text_size=70,
                                   text_colour=misc.constants.C_GREEN,
                                   text_font="monospace"),
                  stimuli.Audio("stimuli/swim.wav")]}

for condition in blocks:
    protocol.add_condition(condition)
    blocks[condition][0].preload()
    blocks[condition][1].preload()

for repetition in range(NR_REPETITIONS):
    for condition in ("rest", "swim"):
        b = design.Block()
        b.set_factor("Condition", condition)
        t = design.Trial()
        t.add_stimulus(blocks[condition][0])
        t.add_stimulus(blocks[condition][1])
        b.add_trial(t)
        exp.add_block(b)
exp.add_block(exp.blocks[0].copy())


# IO
trigger = exp.keyboard  # For USB (keyboad emulation) trigger
#trigger = io.TriggerInput(io.ParallelPort(SCAN_TRIGGER_LTP_ADDRESS))  # For LTP trigger


# RUN
control.start()
stimuli.TextLine("Waiting for trigger...").present()
trigger.wait(SCAN_TRIGGER)  # Initial scanner sync
exp.clock.reset_stopwatch()
for block in exp.blocks:
    start = exp.clock.stopwatch_time
    block.trials[0].stimuli[1].play()
    exp.clock.wait((BLOCK_LENGTH * TR - TR/2) * 1000 - \
                   block.trials[0].stimuli[0].present(),
                   function=exp.keyboard.check)
    protocol.add_event(block.get_factor("Condition"), start,
                       exp.clock.stopwatch_time)
    trigger.wait(SCAN_TRIGGER)  # Sync to scanner for next block start

if not os.path.isdir("protocols"):
    os.mkdir("protocols")
protocol.export_to_brainvoyager(
        exp.name,
        "protocols"+os.path.sep+exp.name+"_"+"S"+repr(exp.subject).zfill(2))

control.end()
