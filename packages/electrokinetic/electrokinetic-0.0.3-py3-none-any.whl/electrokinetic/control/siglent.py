
from dataclasses import dataclass
from typing import List

import platform
import re

import pyvisa

# https://stackoverflow.com/questions/39041142/how-to-setup-pyvisa-exception-handler


def create_rm():
    print(f"PyVISA {pyvisa.__version__} @ {platform.architecture()}")
    rm = pyvisa.ResourceManager()
    print(f"Created Resource manager: {rm}")
    res_list = rm.list_resources()
    if rm.last_status == pyvisa.constants.StatusCode.error_resource_not_found:
        print(f"No resources found ({rm.last_status})")
    return rm, res_list


def open_res():
    rm = pyvisa.ResourceManager()
    try:
        rm.open_resource('COM1')
    except pyvisa.VisaIOError as e:
        print(e.args)
        print(rm.last_status)
        print(rm.visalib.last_status)


def create_rm2():
    rm2 = pyvisa.ResourceManager('@py')
    print(rm2)
    print(rm2.list_resources())
    inst = rm2.open_resource('USB0::0xF4EC::0x1102::SDG2XFBQ902631::INSTR')
    print(inst.query("*IDN?"))


@dataclass
class AWGData:
    """Class for keeping track of AWG state."""
    frequency: float = None
    rep_rate: float = None
    n_cycles: int = None
    amplitude: float = None
    n_cycles: int = None
    rep_rate: float = None
    mode: str = None
    output: bool = False

    def avg_power(self) -> float:
        return (self.n_cycles/self.frequency) * self.rep_rate


class SiglentAWG():
    def __init__(self, manager, visa_resource=None):
        data = AWGData()
        self.rm = manager
        self.res = visa_resource
        self.last_command = ""
        self.instr = self.rm.open_resource(self.res)
        # self.instr.read_termination = '\n'
        # self.instr.write_termination = '\n'
        print(f"*IDN?: {self.instr.query('*IDN?').strip()}")
        print(f"INSTR: {self.instr}")

    def awg_setup(self):
        self.instr.write(f"LAGG EN")         # English LAnGuaGe
        self.instr.write(f"NBFM PNT, DOT")   # number format : decimal point
        self.instr.write(f"NBFM SEPT, ON")   # number format: separator on
        self.instr.write(f"SCFG LAST")       # remember last setting on restart
        self.instr.write(f"BUZZ ON")         # buzzer on
        self.instr.write(f"SCSV 15")         # screen saver after 15 min.
        self.instr.write(f"ROSC INT")        # internal ref. osc.
        self.instr.write(f"VOLTPRT ON")      # voltage protection on

    def switch_output(self, channel, cmd, value=None):
        if channel in ["C1", "C2"]:
            if cmd in ["ON", "OFF"]:
                self.instr.write(f"{channel}:OUTP {cmd}")
            elif cmd == "LOAD" and value == "50" or value == "HZ":
                self.instr.write(f"{channel}:OUTP LOAD, {value}")
            elif cmd == "PLRT" and value == "INVT" or value == "NOR":
                self.instr.write(f"{channel}:OUTP PLRT, {value}")
        return None

    def query_output(self, channel):
        if channel in ["C1", "C2"]:
            return self.instr.query(f"{channel}:OUTP?").strip()
        else:
            return ""

    def set_burst(self, channel, parameter, value=None):
        if channel in ["C1", "C2"]:
            self.instr.write(f"{channel}:BTWV {parameter}, {value}")
        return None

    def query_burst(self, channel):
        if channel in ["C1", "C2"]:
            return self.instr.query(f"{channel}:BTWV?").strip()
        else:
            return ""

    def set_default_burst(self, channel):
        if channel in ["C1", "C2"]:
            self.instr.write(f"{channel}:BSWV WVTP, SINE")       # sine
            self.instr.write(f"{channel}:BSWV FRQ, 1010e3")      # frequency
            self.instr.write(f"{channel}:BSWV AMP, 40e-3")       # amplitude Vpp
            self.instr.write(f"{channel}:BSWV OFST, 0")          # offset 0 V

            self.instr.write(f"{channel}:BTWV TRSR, INT")        # internal trigger source
            self.instr.write(f"{channel}:BTWV TRMD, OFF")        # RISE, FALL, OFF
            self.instr.write(f"{channel}:BTWV GATE_NCYC, NCYC")  # burst with fixed # cycles
            self.instr.write(f"{channel}:BTWV TIME, 10")         # num. cycles
            self.instr.write(f"{channel}:BTWV PRD, 0.1")         # repetition period in s
            self.instr.write(f"{channel}:BTWV STPS, 0")          # start phase
            self.instr.write(f"{channel}:BTWV DLAY, 1e-6")       # delay 1 us
            self.instr.write(f"{channel}:BTWV STATE, ON")        # on=BURST, off=CW !

            # apparently, the BSWV setting also apply to burst mode,
            # so the commands below have no effect
            # self.instr.write(f"{channel}:BTWV CARR, FRQ, 2e6")  # 1 MHz
            # self.instr.write(f"{channel}:BTWV CARR, OFST, 0")  # 1 us
        return self.query_burst(channel)

    def parse_query(self, response: str):
        # Split `s` at ';', ',', or space
        # resp_list = [x.strip() for x in re.split(r'[,\s+ ]',response.strip())]
        resp_list = [x.strip() for x in re.split(r',|\s+', response.strip())]
        for i, r in enumerate(resp_list):
            match r:
                case "STATE":
                    print(f"STATE: {resp_list[i+1]}")
                case "PRD":
                    print(f"PRD: {resp_list[i+1]}")
                case "STPS":
                    pass
                case "DLAY":
                    pass
                case "TIME":
                    print(f"TIME: {resp_list[i+1]}")
                case "FRQ":
                    print(f"FRQ: {resp_list[i+1]}")
                case "AMP":
                    print(f"AMP: {resp_list[i+1]}pp")
                case "OFST":
                    print(f"OFST: {resp_list[i+1]}")
                case "PHSE":
                    pass
        return None

    def close(self):
        self.instr.close()


if __name__ == '__main__':
    rm, res = create_rm()
    for i, r in enumerate(res):
        print(f"{i}: {r}")

    awg = SiglentAWG(rm, res[0])
    print(awg.query_output("C1"))
    awg.awg_setup()
    response = awg.set_default_burst("C1")
    awg.parse_query(response)
    print(awg.query_burst("C1"))

    # awg.switch_output("C1","ON")
    print(awg.query_output("C1"))

