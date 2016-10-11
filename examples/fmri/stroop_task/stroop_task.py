import os

from expyriment import control, design, misc, io, stimuli
from expyriment.design.extras import StimulationProtocol


# SETTINGS
REPETITIONS = 25  # times 4 is total
TR = 2.0
SCAN_TRIGGER = misc.constants.K_5
SCAN_TRIGGER_LTP_ADDRESS = None  # None = USB (keyboard emulation)
BB_SERIAL_PORT_ADDRESS = None  # None = USB (keyboard emulation)
RESPONSE_LEFT = 49
RESPONSE_RIGHT = 50


# DESIGN
exp = design.Experiment("Stroop Task (Colour)")
exp.add_data_variable_names(["TrialID, Condition, Text, Colour, Key, RT, Correct"])
control.initialize(exp)

out_protocol = StimulationProtocol("time")
out_protocol.add_condition("congruent")
out_protocol.add_condition("incongruent")
out_protocol.add_condition("error")

fixcross = stimuli.FixCross()
fixcross.preload()

main = design.Block()
for r in range(REPETITIONS):
    for name in ("RED",
                 "GREEN"):
        for colour in (misc.constants.C_RED,
                       misc.constants.C_GREEN):
            trial = design.Trial()
            if (name == "RED" and colour == misc.constants.C_RED) or \
               (name == "GREEN" and colour == misc.constants.C_GREEN):
                trial.set_factor("Condition", "congruent")
            else:
                trial.set_factor("Condition", "incongruent")
            stim = stimuli.TextLine(name,
                                    text_size=70,
                                    text_font="monospace",
                                    text_colour=colour)
            stim.preload()
            trial.add_stimulus(stim)
            main.add_trial(trial)
main.shuffle_trials()
exp.add_block(main)


# IO
trigger = exp.keyboard  # For USB (keyboad emulation) trigger
#trigger = io.TriggerInput(io.ParallelPort(SCAN_TRIGGER_LTP_ADDRESS))  # For LTP trigger
bb = exp.keyboard  # For USB (keyboard emulation) responses
# bb = io.EventButtonBox(io.SerialPort(BB_SERIAL_PORT_ADDRESS))  # For serial port button box


# RUN
control.start()

in_protocol = StimulationProtocol("time")
in_protocol.import_from_brainvoyager(os.path.join(
    "timings",
    "S{0}.prt".format(str(exp.subject).zfill(2))))
exp.blocks[0] = in_protocol.get_as_experimental_block(block=exp.blocks[0])

stimuli.TextScreen(
    "Instructions",
    "Respond left for green colour, right for red colour.").present()
bb.wait()
stimuli.TextLine("Waiting for trigger...").present()
trigger.wait(SCAN_TRIGGER)  # Initial scanner sync
exp.clock.reset_stopwatch()
for trial in exp.blocks[0].trials:
    fixcross.present()
    trial.preload_stimuli()
    while exp.clock.stopwatch_time < trial.get_factor("begin") - (TR / 2) * 1000:
        pass
    trigger.wait(SCAN_TRIGGER)  # Sync scanner for each trial
    trial.stimuli[0].present()
    start = exp.clock.stopwatch_time
    key, rt = bb.wait([RESPONSE_LEFT, RESPONSE_RIGHT],
        duration=trial.get_factor("end") - trial.get_factor("begin"))
    fixcross.present()
    correct = True
    if rt is None:
        rt = 1500
        correct = False
    if (trial.stimuli[0].text_colour == misc.constants.C_GREEN and \
        key != RESPONSE_LEFT) or \
       (trial.stimuli[0].text_colour == misc.constants.C_RED and \
        key != RESPONSE_RIGHT):
        correct = False
    if correct:
        out_protocol.add_event(trial.get_factor("Condition"), start, start + rt)
    else:
        out_protocol.add_event("error", start, start + rt)
    exp.data.add([trial.id, trial.get_factor("Condition"),
        trial.stimuli[0].text, trial.stimuli[0].text_colour, key, rt, correct])
    trial.unload_stimuli()
fixcross.present()
exp.clock.wait(12500)

if not os.path.isdir("protocols"):
    os.mkdir("protocols")
out_protocol.export_to_brainvoyager(
        exp.name,
        "protocols"+os.path.sep+exp.name+"_"+"S"+repr(exp.subject).zfill(2))

control.end()
