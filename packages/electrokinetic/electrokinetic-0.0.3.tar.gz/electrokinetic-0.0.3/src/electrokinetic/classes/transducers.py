import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from pandas.util.version import Infinity

matplotlib.use("QtAgg")


class Transducer(object):
    def __init__(self, C0, Lm, Cm, Rm=0.0):
        self.C0 = C0
        self.Rm = Rm
        self.Lm = Lm
        self.Cm = Cm
        self.Ra = 0.0
        self.freq = None
        self.omega = None
        self.omega_s = None
        self.omega_p = None
        self.Q = None

        self.Z_total = None
        self.Z_tvs = None
        self.Y_total = None
        self.Y_tvs = None

    def calc_resonances(self, show=False):
        self.omega_s = np.sqrt(np.reciprocal(self.Lm*self.Cm))
        self.omega_p = self.omega_s * np.sqrt(1.0 + self.Cm/self.C0)
        if self.Rm > 0.0:
            self.Q = self.omega_s * (self.Lm /self.Rm)
        else:
            self.Q = np.inf
        if show:
            print(f"omega_s: {self.omega_s:.3f} rad/s, ({self.omega_s / (2 * np.pi):.3f} Hz)")
            print(f"omega_p: {self.omega_p:.3f} rad/s, ({self.omega_p / (2 * np.pi):.3f} Hz)")
            print(f"Q: {self.Q:.3f}")

    def bvd_simple(self):
        """calculates BVD model.

        Returns:

        """
        if self.freq is None:
            return None
        #f = np.asarray(self.freq)
        #scalar_input = False
        #if f.ndim == 0:
        #    f = f[np.newaxis]
        #    scalar_input = True

        omega = 2*np.pi*self.freq

        Z_C0 = 1j*(-np.reciprocal(omega*self.C0))
        self.Z_mech = np.ones_like(omega)*self.Rm + 1j*(omega*self.Lm - np.reciprocal(omega*self.Cm))
        self.Z_piezo = (self.Z_mech * Z_C0) / (self.Z_mech + Z_C0)
        self.Z_total = self.Z_piezo + np.ones_like(omega)*self.Ra

        #if scalar_input:
        #    return Z_total.item()
        #return Z_total

    def bvd_vs(self):
        """calculates BVD model.
        Returns:
        """
        if self.freq is None:
            return None
        #f = np.asarray(self.freq)
        #scalar_input = False
        #if f.ndim == 0:
        #    f = f[np.newaxis]
        #    scalar_input = True

        omega = 2*np.pi*self.freq

        factor = self.C0 + self.Cm - np.square(omega)*self.C0*self.Cm*self.Lm
        self.Z_tvs = 1.0 - np.square(omega)*self.Cm*self.Lm + 1j*omega*self.Ra*factor
        self.Z_tvs /= 1j*omega*factor

        #if scalar_input:
        #    return Z_tvs.item()
        #return Z_tvs

    def calculate_Y(self):
        """calculates current/voltage ratio from BVD model.
            i = 1/Z_total * v  ==> i/v = 1/Z_total = Y_total
        Returns:
        """
        if self.Z_total is not None:
            self.Y_total = np.reciprocal(self.Z_total)
        if self.Z_tvs is not None:
            self.Y_tvs = np.reciprocal(self.Z_tvs)

    def calculate_voltage_ratio(self):
        """calculates fraction of drive voltage over piezo voltage from BVD model.
            v_piezo = Z_piezo/Z_total * v  ==> v_piezo/v = Z_piezo/Z_total = Z_piezo*Y_total
        Returns:
        """
        if self.Y_total is not None:
            self.voltage_ratio = self.Z_piezo*self.Y_total

    def calculate_mech_current(self):
        """calculates i_mech over total voltage from BVD model.
            i_mech = v_piezo/Z_mech = Z_piezo/(Z_total*Z_mech) * v
            ==> i_mech/v = Z_piezo/(Z_total*Z_mech) = (Z_piezo/Z_mech) * Y_total
        Returns:
        """
        if self.Y_total is not None:
            self.i_mech = (self.Z_piezo/self.Z_mech) * self.Y_total

    def calculate_Ra(self, show=False):
        """calculates "ideal" value for Ra in BVD model.
        """
        arg = (self.Lm*self.Cm) / (self.C0*(4.0*self.C0 + self.Cm))
        self.Ra_mid = 2.0*np.sqrt(arg)
        if show:
            print(f"Ra_mid: {self.Ra_mid:.3f} Ohm")

    def plot_bvd(f, z):
        fig, ax = plt.subplots(2, 1, figsize=(6, 6))
        ax[0].semilogy(f, np.abs(z))
        ax[1].semilogy(f, np.imag(z))
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    tr = Transducer(C0=0.48e-6, Lm=0.50e-3, Cm=192e-9, Rm=0.0)
    tr.Ra = 1000.0
    tr.calc_resonances(show=True)
    tr.calculate_Ra(show=True)

    # f = np.logspace(3,5, 801)
    tr.freq = np.linspace(100,100000, 10001)

    tr.bvd_simple()
    tr.bvd_vs()
    tr.calculate_Y()
    tr.calculate_voltage_ratio()
    tr.calculate_mech_current()

    fig, ax = plt.subplots(4, 1, figsize=(6, 6), sharex=True, layout="constrained")
    ax[0].semilogy(tr.freq, np.abs(tr.Z_total), label="Z")
    # ax[0].semilogy(tr.freq, np.abs(tr.Z_tvs), 'r-', label="MVS")
    ax[0].set_ylabel("|Z|")
    ax0_r = ax[0].twinx()
    ax0_r.plot(tr.freq, np.angle(tr.Z_total, deg=True))
    # ax0_r.plot(tr.freq, np.angle(tr.Z_tvs, deg=True), 'r-')
    ax0_r.set_ylim(-100, 100)
    ax0_r.set_ylabel("phase ($\degree$)")
    ax[0].legend()

    ax[1].semilogy(tr.freq, np.abs(tr.Y_total), label="Y")
    # ax[1].semilogy(tr.freq, np.abs(tr.Y_tvs), 'r-', label="MVS")
    ax[1].set_ylabel("|Y| \n Ratio piezo current \n to drive voltage")
    ax1_r = ax[1].twinx()
    ax1_r.plot(tr.freq, np.angle(tr.Y_total, deg=True))
    # ax1_r.plot(tr.freq, np.angle(tr.Y_tvs, deg=True), 'r-')
    ax1_r.set_ylim(-100, 100)
    ax1_r.set_ylabel("phase ($\degree$)")

    ax[2].semilogy(tr.freq, np.abs(tr.voltage_ratio), label= "G")
    ax[2].set_ylabel("Ratio $v_{piezo}$ \n to drive voltage")


    ax[3].plot(tr.freq, np.abs(tr.i_mech), label="B")

    # ax[3].set_ylim(-100, 100)
    ax[3].set_xlabel("frequency (Hz)")
    # plt.tight_layout()
    plt.show()

    # plot_bvd(f, Z_tr)

