import os

name_outlet = "erp-streamer"
id_outlet = 'erp-streamer'
type_outlet = 'EEG'

name_inlet = "scab-c_marker"

channels = ['F3', 'Fz', 'F4', 'C3', 'Cz', 'C4', 'P3', 'Pz', 'P4']
fs = 1000

markers = dict()
markers['target'] = ['11']
markers['nontarget'] = ['1']

#length_erp = 300
erp = [0.0 for m in range(300)] + [2.0 for m in range(200)]

#print(erp)

