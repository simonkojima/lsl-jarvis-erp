import os

name_outlet = "jarvis-erp"
id_outlet = 'jarvis-erp'
type_outlet = 'EEG'

name_inlet = "scab-c"

channels = ['F3', 'Fz', 'F4', 'C3', 'Cz', 'C4', 'P3', 'Pz', 'P4']
fs = 1000

markers = dict()
markers['target'] = ['101', '102', '103', '104', '105', '106', '107', '108', '109']
markers['nontarget'] = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

#markers = dict()
#markers['target'] = ['11']
#markers['nontarget'] = ['1']

#length_erp = 300
erp = [0.0 for m in range(300)] + [2.0 for m in range(200)]

#print(erp)

