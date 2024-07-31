import argparse
import os
import datetime
import time
import logging
from random import random as rand

import numpy as np

import pylsl

from utils import log
from utils.std import mkdir

def main(name,
         id,
         stream_type,
         srate,
         channels,
         name_inlet,
         target,
         erp):
    
    # fetch marker inlet
    is_searching = True
    while is_searching:
        streams = pylsl.resolve_streams(wait_time = 1)
        for stream in streams:
            if stream.name() == name_inlet:
                inlet = pylsl.StreamInlet(stream)
                is_searching = False
    
    erp = np.array(erp)
    length_erp = erp.size
    #print(inlet)
    #while True:
    #    sample, timestamp = inlet.pull_sample()
    #    print(sample)
    #    print(timestamp)

    #channel_names = ["Fp1", "Fp2", "C3", "C4", "Cz", "P3", "P4", "Pz", "O1", "O2"]
    n_channels = len(channels)

    info = pylsl.StreamInfo(name, stream_type, n_channels, srate, 'float32', id)

    # append some meta-data
    # https://github.com/sccn/xdf/wiki/EEG-Meta-Data
    #info.desc().append_child_value("manufacturer", name)
    chns = info.desc().append_child("channels")
    for chan_ix, label in enumerate(channels):
        ch = chns.append_child("channel")
        ch.append_child_value("label", label)
        ch.append_child_value("unit", "microvolts")
        ch.append_child_value("type", "EEG")
        ch.append_child_value("scaling_factor", "1")

    # next make an outlet; we set the transmission chunk size to 32 samples
    # and the outgoing buffer size to 360 seconds (max.)
    outlet = pylsl.StreamOutlet(info, 32, 360)

    if False:
        # It's unnecessary to check the info when the stream was created in the same scope; just use info.
        # Use this code only as a sanity check if you think something when wrong during stream creation.
        check_info = outlet.get_info()
        assert check_info.name() == name
        assert check_info.type() == stream_type
        assert check_info.channel_count() == len(channel_names)
        assert check_info.channel_format() == pylsl.cf_float32
        assert check_info.nominal_srate() == srate

    print("now sending data...")
    logger.debug("now sending data...")
    start_time = pylsl.local_clock()
    sent_samples = 0
    send_erp = False
    while True:
        sample, timestamp = inlet.pull_sample(timeout=0.01)
        if sample is not None:
            for mrk in sample:
                #if mrk in markers['target']:
                if mrk in target:
                    idx_erp = 0
                    if (idx_erp <= length_erp) and send_erp:
                        print("erp is overlapped. second erp is ignored.")
                        logger.debug("erp is overlapped. second erp is ignored.")
                    send_erp = True
                    mrk_erp = mrk
        elapsed_time = pylsl.local_clock() - start_time
        required_samples = int(srate * elapsed_time) - sent_samples
        if required_samples > 0:
            # make a chunk==array of length required_samples, where each element in the array
            # is a new random n_channels sample vector
            mychunk = list()
            for m in range(required_samples):
                t_vec = list()
                for n in range(n_channels):
                    val = rand()
                    if send_erp:
                        if idx_erp < length_erp:
                            val += erp[idx_erp]
                        else:
                            send_erp = False
                            print("ERP was sent for marker '%s'"%mrk_erp)
                            logger.debug("ERP was sent for marker '%s'"%mrk_erp)
                    t_vec.append(val)
                if send_erp:
                    idx_erp += 1
                mychunk.append(t_vec)
            #mychunk = [[rand()+1.0 for chan_ix in range(n_channels)]
            #           for samp_ix in range(required_samples)]
            #print(mychunk + 10)
            # Get a time stamp in seconds. We pretend that our samples are actually
            # 125ms old, e.g., as if coming from some external hardware with known latency.
            #stamp = pylsl.local_clock() - 0.125
            stamp = pylsl.local_clock()
            # now send it and wait for a bit
            # Note that even though `rand()` returns a 64-bit value, the `push_chunk` method
            #  will convert it to c_float before passing the data to liblsl.
            outlet.push_chunk(mychunk, stamp)
            sent_samples += required_samples
        time.sleep(0.02)


if __name__ == '__main__':
    import conf

    log_strftime = "%y-%m-%d_%H-%M-%S"
    datestr =  datetime.datetime.now().strftime(log_strftime) 
    log_fname = "%s.log"%datestr
    
    mkdir(conf.log_dir)

    log.set_logger(os.path.join(conf.log_dir, log_fname), True)

    logger = logging.getLogger(__name__)
    
    logger.debug("log file will be saved in %s"%str(os.path.join(conf.log_dir, log_fname)))

    parser = argparse.ArgumentParser()
    parser.add_argument('--name', default = "jarvis-erp", type = str)
    parser.add_argument('--id', default = 'jarvis-erp', type = str)
    parser.add_argument('--type', default = 'eeg', type = str)
    parser.add_argument('--channels', default=['F3', 'Fz', 'F4', 'C3', 'Cz', 'C4', 'P3', 'Pz', 'P4'], type = str, nargs='*')
    parser.add_argument('--fs', default = 1000, type = int)
    parser.add_argument('--markerinlet', default = "scab-c", type = str)
    parser.add_argument('--target', default = conf.target, type = str, nargs='*')
    
    args = parser.parse_args()
    
    for key in vars(args).keys():
        val = vars(args)[key]
        logger.debug("%s: %s"%(str(key), str(val)))

    main(name=args.name,
         id=args.id,
         stream_type=args.type,
         srate=args.fs,
         channels=args.channels,
         name_inlet = args.markerinlet,
         target=args.target,
         erp=conf.erp)