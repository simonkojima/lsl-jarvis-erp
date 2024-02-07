import os
import sys
import mne
import matplotlib.pyplot as plt

from mne_import_xdf import read_raw_xdf

home_dir = os.path.expanduser('~')
pyerp_dir = os.path.join(home_dir, "git", "pyerp", "src")

sys.path.append(pyerp_dir)
import pyerp

raw = read_raw_xdf("sub-virtual_ses-S001_task-oddball_run-002_eeg.xdf")
#raw.filter(l_freq=1, h_freq = 40)

events, event_id = mne.events_from_annotations(raw)
print(event_id)

epochs = mne.Epochs(raw, events, dict(target=event_id['11'], nontarget=event_id['1']), tmin = -0.1, tmax = 1.0, baseline = None, preload=True)

print(epochs)
print(epochs.ch_names)

fig = pyerp.plot_2ch_tnt(epochs)
plt.show()