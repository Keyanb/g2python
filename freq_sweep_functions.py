def set_frequencies (f_1, f_3, phase):
    if f_1 < f_3:
        #must use raw
        f_raw_1 = int(67.10887 * f_1)
        f_raw_3 = int(67.10887 * f_3)
        f_raw_2 = f_raw_3 - f_raw_1

        f_src.set_freq_raw(0, f_raw_1)
        f_src.set_freq_raw(1, f_raw_2)        
        f_src.set_freq_raw(2, f_raw_3)
        f_src.set_freq_raw(3, f_raw_3)
        
        f_src.set_phase(3, phase)
        f_src.sync()
    else:
        return "frequency 1 too large"

def set_amplitudes (coil_drive, coil_offset):
    f_src.set_amp(0, 1)
    f_src.set_amp(1, 1)        
    f_src.set_amp(2, 1)
    f_src.set_amp(3, coil_drive)
    f_src.set_DC(3, coil_offset)
