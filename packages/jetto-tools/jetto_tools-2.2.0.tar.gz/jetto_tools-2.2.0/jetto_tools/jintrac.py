import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.ticker import FormatStrFormatter
import matplotlib.ticker as mticker
import os, sys, io
from datetime import datetime
#jetto-python tools imports
import jetto_tools.binary as jbt
#Edge2D Tran files - path in bashrc file
#from pytran import Tran
#Import from results.py classes to parse
#EQDSK anf GRAY fort. files
from jetto_tools.results import JettoResults, EqdskFile, GrayFortFile
#gray.py plotting routines
from jetto_tools.analysis.gray import plot_analysis_1, plot_analysis_2
#TGLF spectrum plotting method
from jetto_tools.plot_growthrates_TCI import plot_growthrates_TCI
#Import multithreading methods
import threading
import time
import argparse
import struct

__all__ = ["jintrac"]

class jintrac():
    """
    Class to read and plot JINTRAC output.
    Written by Guillermo Suarez Lopez.
    """   

    def __init__(self, jetto_path=None, jetto_jsp=None,
                 user=None, database="iter", nshot=None, run=None,
                 backend="auto", data_version=None, out_memory=True):
        """
        backend: str - "hdf5" or "mdsplus"
        """   

        #Autodetect the JINTRAC backend
        #Standard output doesn't have /imasdb folder
        #HDF5 has a structure /imasdb/database/nshot/
        #MDSPLUS has a structure /imasdb/database/0/
        if backend=="auto":
            dir_list = os.listdir(jetto_path)
            if 'imasdb' in dir_list:
                imas_list = os.listdir(jetto_path+
                            '/imasdb/'+database+'/3')
                if nshot == int(imas_list[0]):
                    backend="hdf5"
                else:
                    backend="mdsplus"
            else:
                backend="std"

        self.jetto_path = jetto_path
        self.jetto_jsp = jetto_jsp
        self.sanco_files = []
        self.nshot = nshot
        self.coconut = False
        self.gray = False
        self.eqdsk = False
        self.out_memory = out_memory
        self.backend = backend
        if data_version is None:
            data_version = os.environ['IMAS_VERSION']
        self.data_version = data_version

        #Set default values for some flags
        self.jspfile = False
        self.jstfile = False
        self.ssp1file = False
        self.ssp2file = False
        self.ssp3file = False
        self.jse = False
        self.grid = False
        self.tci_asym = False

        #If user is None, points to the imasdb folder
        #in jetto_path. Othwerwise, you can provide the
        #full path to the user.
        if user is None:
            user = jetto_path+"/imasdb"

        if self.out_memory:
            self.out = {}

        #Read a Standard Output case
        if backend == "std":
            self._readjetto_standard()
            #If it's a Coconut run
            try:
                self._read_edge2d()
                self._read_eirene()
                self.coconut = True
            except:
                print(' - No TRAN file found - usual in JETTO runs '+\
                      'OR EPROC library could not be loaded')
            #Read output quantities to memory
            if out_memory:
                self._out_memory_standard()

        #Read an IMAS IDS case
        else:
            self._readjetto_imas(database, nshot, run, user, backend,
                                 data_version)
            #For the time being, parse edge quantities from
            #tran file and EPROC. Most edge IDS are not currently
            #written
            try:
                self._read_edge2d()
                self.coconut = True
            except:
                print(' - No TRAN file found - usual in JETTO runs '+\
                      'OR EPROC library could not be loaded')
            #Read output quantities to memory
            if out_memory:
                self._out_memory_imas()

        #Compute derived quantities
        try:
            self._calculate_derived_quantities()
        except:
            print(" - Derived quantities could not be calculated.")

        #A list of elements to match fully ionized species against
        # index 0 unused
        self.Z_to_element = [None,
            "H",  "He",
            "Li", "Be", "B",  "C",  "N",  "O",  "F",  "Ne",
            "Na", "Mg", "Al", "Si", "P",  "S",  "Cl", "Ar",
            "K",  "Ca", "Sc", "Ti", "V",  "Cr", "Mn", "Fe", "Co", "Ni",
            "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr",
            "Rb", "Sr", "Y",  "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd",
            "Ag", "Cd", "In", "Sn", "Sb", "Te", "I",  "Xe",
            "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd",
            "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu",
            "Hf", "Ta", "W",  "Re", "Os", "Ir", "Pt", "Au", "Hg",
            "Tl", "Pb", "Bi", "Po", "At", "Rn",
            "Fr", "Ra", "Ac", "Th", "Pa", "U",  "Np", "Pu", "Am", "Cm",
            "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr",
            "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn",
            "Nh", "Fl", "Mc", "Lv", "Ts", "Og"]

        return


    def _readjetto_standard(self):
        """
         Simulations which have not yet finished
         need to be read from the last written
         jetto.jspXX file, however, jetto.jst file
         is always readily available

         Full JETTO output namelists can be found in:
         https://git.iter.org/projects/SCEN/repos/jintrac-docs/
         browse/webpages/wiki/JETTO_ppfoutputs.md
        """

        #Reading JETTO .jsp file - Profiles
        if self.jetto_jsp:
            if "/" in self.jetto_jsp:
                jsp_file = self.jetto_path + self.jetto_jsp
            else:
                jsp_file = self.jetto_path + "/" + self.jetto_jsp
        else:
            jsp_file = self.jetto_path + "/jetto.jsp"
        print("JETTO .jsp file:" + str(jsp_file))

        self.jet = {}

        try:
            dataset_jsp = jbt.read_binary_file(jsp_file)
            self.dataset_jsp = dataset_jsp
            self.jet = dataset_jsp.copy()
            self.names_jsp = dataset_jsp.keys()
            self.jspfile = True
        except:
            print('  - No JETTO JSP file')

        #Reading JETTO .jse file - JETTO equilibrium data
        try:
            jse_file = self.jetto_path + "/jetto.jse"
            print("JETTO .jse file:" + str(jse_file))
            dataset_jse = jbt.read_binary_file(jse_file)
            self.dataset_jse = dataset_jse
            self.names_jse = dataset_jse.keys()
            self.dataset_jse["TIME_EQ"] = self.dataset_jse["TIME"]
            #TIME key is different from TIME in jetto.jsp,
            #but both have the same name.
            del self.dataset_jse["TIME"]
            self.jet.update(self.dataset_jse)
            self.jse = True
        except:
            print('  - No JETTO JSE file') 

        #Reading JETTO .jst file - Time traces
        #tvec1 - Time vector
        try:
            jst_file = self.jetto_path + "/jetto.jst"
            print("JETTO .jst file:" + str(jst_file))
            dataset_jst = jbt.read_binary_file(jst_file)
            self.dataset_jst = dataset_jst
            self.names_jst = dataset_jst.keys()
            self.jet.update(self.dataset_jst)
            self.jstfile = True
        except:
            print('  - No JETTO JST file')

        #Reading SANCO .sspX file - Profiles
        #Reading SANCO .sstX file - Time traces
        #The X corresponds to each impurity
        #added to the simulation.
        #These files contain several pinch
        #velocities/diffusivities each, where
        #each one is a different ionization state.
        try:
            ssp_file1 = self.jetto_path + "/jetto.ssp1"
            print("JETTO .ssp file:" + str(ssp_file1))
            sst_file1 = self.jetto_path + "/jetto.sst1"
            print("JETTO .sst file:" + str(sst_file1))
            dataset_ssp1 = jbt.read_binary_file(ssp_file1)
            self.dataset_ssp1 = dataset_ssp1
            self.names_ssp1 = list(dataset_ssp1.keys())
            dataset_sst1 = jbt.read_binary_file(sst_file1)
            self.dataset_sst1 = dataset_sst1
            self.names_sst1 = list(dataset_sst1.keys())
            self.ssp1file = True
        except:
            print(" - Could not read " + str(ssp_file1))
            print(" - Could not read " + str(sst_file1))
            self.ssp1file = False

        #ssp2
        try:
            ssp_file2 = self.jetto_path + "/jetto.ssp2"
            print("JETTO .ssp file:" + str(ssp_file2))
            sst_file2 = self.jetto_path + "/jetto.sst2"
            print("JETTO .sst file:" + str(sst_file2))
            dataset_ssp2 = jbt.read_binary_file(ssp_file2)
            self.dataset_ssp2 = dataset_ssp2
            self.names_ssp2 = dataset_ssp2.keys()
            dataset_sst2 = jbt.read_binary_file(sst_file2)
            self.dataset_sst2 = dataset_sst2
            self.names_sst2 = dataset_sst2.keys()
            self.ssp2file = True
        except:
            print(" - Could not read " + str(ssp_file2))
            print(" - Could not read " + str(sst_file2))
            self.ssp2file = False     

        #ssp3
        try:
            ssp_file3 = self.jetto_path + "/jetto.ssp3"
            print("JETTO .ssp file:" + str(ssp_file3))
            sst_file3 = self.jetto_path + "/jetto.sst3"
            print("JETTO .sst file:" + str(sst_file3))
            dataset_ssp3 = jbt.read_binary_file(ssp_file3)
            self.dataset_ssp3 = dataset_ssp3
            self.names_ssp3 = dataset_ssp3.keys()
            dataset_sst3 = jbt.read_binary_file(sst_file3)
            self.dataset_sst3 = dataset_sst3
            self.names_sst3 = dataset_sst3.keys()
            self.ssp3file = True
        except:
            print(" - Could not read " + str(ssp_file3))
            print(" - Could not read " + str(sst_file3))
            self.ssp3file = False

        return


    def _out_memory_standard(self):
        """ 
        Reads into a new data dictionary the standard
        output Database from JINTRAC

        Parameters
        ----------

        Output
        ----------

        Notes
        ----------
        """

        if self.jspfile:
            ##########
            #JETTO JSP
            ##########
            #These signals depend on time. The time vector might not
            #be available if, for instance, the simulation fails in the
            #first iterations. So I give the option not to read them
            #so we can use this routine to analyze the output also in
            #case of a run having an early failure.
            try:
                self.out["time"] = np.squeeze(self.jet["TIME"])
                if self.out["time"].size == 1:
                    self.out["tend"] = self.out["time"]
                else:
                    self.out["tend"] = self.out["time"][-1]
                self.out["time_derived"] = np.squeeze(self.jet["TVEC1"])
                self.out["Wth"] = self.jet["WTH"].ravel()
                #Total alpha power [MW] f(t)
                self.out["Palf"] = self.jet["PALF"].ravel()
            except:
                print(" - No time vector in jetto.jsp")
            self.out["R_omp"] = self.jet["R"]  #Outer Midplane Major radius
            R0_mesh = np.repeat(np.expand_dims(self.jet["R"][:,0], 1),
                                len(self.out["R_omp"][0,:]), 1)
            self.out["r_omp"] = self.jet["R"] - R0_mesh
            self.out["rho"] = self.jet["RHO"]  #JETTO label [m]
            self.out["rhot_norm"] = self.jet["XRHO"]
            self.out["Te"] = self.jet["TE"]
            self.out["Ti"] = self.jet["TI"]  #Ion temp [eV]
            self.out["Qe"] = self.jet["PEFL"]  #Electron heat flux as afo rho [W]
            self.out["Qi"] = self.jet["PIFL"]  #Ion heat flux as afo rho [W]
            self.out["ne"] = self.jet["NE"]
            self.out["pres"] = self.jet["PR"]    #Total pressure [Pa]
            self.out["De_eff"] = self.jet["DFI"] #D effective (I assume evolving ne) [m2/s]
            self.out["D1_eff"] = self.jet["D1"]  #Particle Diffusion (I assume species 1) [m2/s]
            self.out["D2_eff"] = self.jet["D2"]  #Particle Diffusion species 2 [m2/s]
            self.out["De_n"] = self.jet["DNCE"]  #NCLASS el. diffusivity [m2/s]
            self.out["D1_n"] = self.jet["DNCI"]  #NCLASS (main?) ion diffusivity [m2/s]
            self.out["D2_n"] = self.jet["DNC1"]  #NCLASS 2nd spec.+1 diffusivity (Idk what +1 means..)
            self.out["D1_t"] = self.jet["DTCI"]  #Maion ion TCI part. diff. [m2/s]
            self.out["D2_t"] = self.jet["DTC2"]  #2nd ion TCI part. diff. [m2/s]
            self.out["vnce"] = self.jet["VNCE"]  #NCLASS el. pinch velocity [m/s]
            self.out["v1_n"] = self.jet["VNCI"]  #NCLASS (main?) ion pinch velocity [m/s]
            self.out["v2_n"] = self.jet["VNC1"]  #NCLASS 2nd spec.+1 vel. (Idk what +1 means..)
            self.out["v_ware"] = self.jet["VW"]  #Ware pinch [m/2]
            self.out["v1_t"] = self.jet["VTCI"]  #Pinch velocity TCI main ion 1st species [m/s]
            self.out["v2_t"] = self.jet["VTC2"]  #Pinch velocity TCI 2nd species [m/s]
            self.out["niH"] = self.jet["NIH"]    #Hydrogen density [m-3]
            self.out["niD"] = self.jet["NID"]    #Deuterium density [m-3]
            self.out["niT"] = self.jet["NIT"]    #Tritium density [m-3]
            self.out["ni"] = self.jet["NI"]      #Total ion density [m-3]
            self.out["nN1"] = self.jet["N01"]    #Neutral density [m-3]
            self.out["nN2"] = self.jet["N02"]    #Neutral density [m-3]
            #Probably assumed the same for all ions:
            self.out["vtor"] = self.jet["VTOR"] #Toroidal velocity [m/s]
            self.out["vpol"] = self.jet["VPOL"] #Poloidal velocity [m/s]
            self.out["D_tormom"] = self.jet["CHIM"] #Toroidal momentum diffusivity [m2/s]
            self.out["v_tormom"] = self.jet["VINM"] #Toroidal momentum pinch [m/s]
            self.out["D_tormom_eff"] = self.jet["XMF"] #Effective Toroidal momentum diff [m2/s]
            self.out["jtor"] = self.jet["JZ"] #Total tor. current density [A/m2]
            self.out["jpar"] = self.jet["JP"] #Total par. current density [A/m2]
            self.out["jpar_Bs"] = self.jet["JZBS"] #Total (parallel = Bootstrap) current density [A/m2]
            self.out["jtor_ec"] = self.jet["JZEC"] #EC driven tor. current density [A/m2]
            self.out["qprof"] = self.jet["Q"]
            self.out["qshear"] = self.jet["SH"]
            self.out["res_par"] = self.jet["ETA"] #Parallel resistivity [Ohm * m]
            #These are volumetric integrals of the pellet source profile
            self.out["S0"] = self.jet["S0D"]  #Neutral Particle source from FRANTIC [s-1]
            self.out["S1_pel"] = self.jet["SPE1"] #Pellet source species 1 [s-1]
            self.out["S2_pel"] = self.jet["SPE2"] #Pellet source species 2 [s-1]
            self.out["rhotnbi"] = self.jet["XRHO"]
            self.out["SBD1"] = self.jet["SBD1"] #NBI part. source (spec 1)
            self.out["SBD2"] = self.jet["SBD2"] #NBI part. source (spec 2)
            self.out["Pnbi_i"] = self.jet["QNBI"] #[MW/m^3] Ion NBI heating         
            self.out["Pnbi_e"] = self.jet["QNBE"] #[MW/m^3] Electron NBI heating    
            self.out["Pnbi_itot"] = np.squeeze(self.jet["PNBI"]) #Total NBI power to ions [MW] f(t)
            self.out["Pnbi_etot"] = np.squeeze(self.jet["PNBE"]) #Total NBI power to elec [MW] f(t)
            self.out["Pnbi_tot"] = self.out["Pnbi_itot"]+self.out["Pnbi_etot"]
            self.out["rhotec"] = self.jet["XRHO"]
            self.out["Pecrh"] = self.jet["QECE"]   #ECRH power density [W/m3]
            self.out["Pec_tot"] = np.squeeze(self.jet["PECE"]) #Total power [W] f(t)
            self.out["Poh_tot"] = np.squeeze(self.jet["POH"]) #Ohmic heating [W] f(t)
            self.out["Palph_e"] = self.jet["QALE"] #[W/m^3] Alpha e- heating
            self.out["Palph_i"] = self.jet["QALI"] #[W/m^3] Alpha i+ heating
            self.out["Prad"] = self.jet["QRAD"] #[MW/m^3] Impurity radiation loss
            self.out["Psyn"] = self.jet["QSYR"] #[MW/m^3] Synchroton radiation

            #Interleaved grid for diffusivities
            self.out["rhot_Xs"] = 0.5*(self.out["rhot_norm"][:,1:]+\
                                        self.out["rhot_norm"][:,:-1])
            #From the JINTRAC Wiki, part written by Florian
            #JSP/XI is the sum of all XIj.
            #JSP/XI1: neoclassical Xi
            #JSP/XI2: Bohm part of Xi from Bohm/gyroBohm model
            #JSP/XI3: gyroBohm part of Xi from Bohm/gyroBohm model
            #JSP/XI4: Xi from NeoAlcator model
            #JSP/XI5: Xi from CDBM model
            #JSP/XI6: Xi from TCI
            self.out["Xe"] = self.jet["XE"] #Electron heat diffusivity
            self.out["Xi"] = self.jet["XI"] #Total Ion heat diffusivity
            self.out["Xe_neo"] = self.jet["XE1"]
            self.out["Xi_neo"] = self.jet["XI1"] 
            self.out["Xe_Bohm"] = self.jet["XE2"]
            self.out["Xi_Bohm"] = self.jet["XI2"] 
            self.out["Xe_GBohm"] = self.jet["XE3"]
            self.out["Xi_GBohm"] = self.jet["XI3"]
            self.out["Xe_turb"] = self.jet["XE6"]
            self.out["Xi_turb"] = self.jet["XI6"]

            self.out["Vol_rho"] = self.jet["VOL"] #Plasma volume [m^3]
            self.out["dVdrho"] = self.jet["DVEQ"] #dVol/drho [m2]

        ################
        #JETTO JST, f(t)
        ################
        if self.jstfile:
            #Pedestal quantities
            self.out["alpha_max_jetto_edge"] = self.jet["ALFM"].ravel()
            self.out["presped_th"] = self.jet["PPED"].ravel()
            self.out["Zeff"] = self.jet["ZEFF"]
            self.out["neped"] = self.jet["NEBA"].ravel() #ne(pedestal top)
            #I assume this is the volumetric average
            self.out["ne_avg"] = self.jet["NEAV"][0] #e- volume-averaged density [m-3]
            self.out["ne_lavg"] = self.jet["NEL"][0] #e- line-averaged density [m-3]
            self.out["n1_avg"] = self.jet["NI1"][0]  #ion 1 volume-averaged density [m-3]
            self.out["n2_avg"] = self.jet["NI2"][0]  #ion 2 volume-averaged density [m-3]
            #Greenwal density fraction [%]
            self.out["nGw"] = self.jet["NGRN"].ravel()
            self.out["fGw"] = self.jet["NGFR"].ravel()
            self.out["Teped"] = self.jet["TEBA"]/1.e3 #Te @ top of barrier [keV]
            #Some concentrations may not be available,
            #this depends on the impurities used in the run.
            #IMC# = <n_imp>/<ne> [%]
            try:
                self.out["IMC1"] = self.jet["IMC1"][0]
            except:
                self.out["IMC1"] = np.zeros_like(self.out["Zeff"])
            try:
                self.out["IMC2"] = self.jet["IMC2"][0]
            except:
                self.out["IMC2"] = np.zeros_like(self.out["Zeff"])
            try:
                self.out["IMC3"] = self.jet["IMC3"][0]
            except:
                self.out["IMC3"] = np.zeros_like(self.out["Zeff"])

            self.out["Prad_tot"] = self.jet["PRAD"].ravel()
            self.out["frad"] = self.jet["RDFR"].ravel()

            #Energy confinement time - ITER Definition [s]
            self.out["tau_e"] = np.squeeze(self.jet["TAUE"])

            #Fusion Q
            #self.out["Qfus"] = self.jet["QDT"][0]
            self.out["Qfus"] = self.jet["QFUS"][0]
 
            #Particle input (puff 1 and puff 2. Hopefully, total source)
            #Note: These are for main ion species.
            self.out["Spuff_i1_tot"] = np.squeeze(self.jet["PIN1"])
            self.out["Spuff_i2_tot"] = np.squeeze(self.jet["PIN2"])

            #Total plasma current [A]
            self.out["Ip"] = self.jet["CUR"].ravel()
            self.out["jpar_Bstot"] = np.squeeze(self.jet["CUBS"])
            self.out["jtor_ectot"] = np.squeeze(self.jet["CUEC"])
            self.out["jtor_nbitot"] = np.squeeze(self.jet["CUNB"])
            self.out["jtor_ictot"] = np.squeeze(self.jet["CURF"])
            #Vacuum toroifal fields 
            self.out["Btor"] = np.squeeze(self.jet["BTOR"]) #Btor(R=Raxis)
            self.out["Btor_geo"] = self.jet["BGEO"].ravel() #Btor(R=Rgeo)

            #Non-inductive current fraction [%]
            self.out["Jni"] = np.squeeze(self.jet["NIFR"])
            #Loop voltage
            self.out["Vloop"] = np.squeeze(self.jet["VLP"]) #[V]

            #Bnd. energy flux (el+io)
            self.out["Psep"] = self.jet["PSEP"]
            #L-H transition power [W]
            #I believe this quantity is only written if the
            #IPWDEP L-H transition switch is active
            #I checked against Martin scaling law (30.01.2025)
            #and this quantity doesnt include - Prad_tot.
            try:
                self.out["Plht"] = self.jet["PLHT"]
            except:
                pass

            #H-fact_IPB98(y,2) P=Psep
            self.out["H98_Psep"] = self.jet["H98Y"].ravel()
            #H-fact_IPB98(y,2) P=Pnet
            self.out["H98_Pnet"] = self.jet["H98Z"].ravel()
            #Total normalized beta - Standard definition [%]
            self.out["betaN"] = np.squeeze(self.jet["BNTT"])

            #Geometric quantities
            #{R,Z} positions of magnetic axis.
            self.out["Raxis"] = self.jet["RAXS"].ravel()
            self.out["Zaxis"] = self.jet["ZAXS"].ravel()
            #(max(Rmid)+min(Rmid))/2
            self.out["Rgeo"] = self.jet["RGEO"].ravel()
            #Triangularity at JSP/XPSI=0.95
            self.out["delta_trian"] = self.jet["D95"].ravel()
            self.out["Sur_t"] = self.jet["SURF"]

            #Control parameters
            self.out["dtmax"] = self.jet["DTMX"]

        ################
        #JETTO JSE, f(t)
        ################
        if self.jse:
            self.out["time_eq"] = self.jet["TIME_EQ"]
            self.out["Rbnd"] = self.jet["RBND"]
            self.out["Zbnd"] = self.jet["ZBND"]

        ###################
        #EQDSK file
        #Read it to get PFM
        ###################
        try:
            eqdsk = EqdskFile
            eqdsk = eqdsk.load(self.jetto_path+"/jetto.eqdsk_out")
            self.out["Rgrid"] = eqdsk.Rgrid
            self.out["Zgrid"] = eqdsk.Zgrid
            self.out["Psi"] = eqdsk.psirz
            self.out["Psi_n"] = eqdsk.psirz_n
            self.eqdsk = True
        except:
            print(" - No EQDSK file found")

        ###################
        #GRAY file
        ###################
        try:
            gray = GrayFortFile
            #gray_central_ray_coord
            gr = gray.load(self.jetto_path + "/gray_central_ray_coord")
            R_cr = []
            Z_cr = []
            for i in range(0, len(gr)):
                R_cr.append(np.array(gr[i].data["R"]))
                Z_cr.append(np.array(gr[i].data["z"]))
            self.out["R_cr"] = R_cr
            self.out["Z_cr"] = Z_cr
            self.gray = True
        except:
            print(" - No GRAY output files")

        ####################################################
        #Vessel and buffle coordinates parsed from grid file
        #For JETTO runs there will not be a grid file.
        ####################################################
        try:
            file = open(self.jetto_path + "/grid", mode="r")
            lines = file.readlines()
            file.close()
            for line in lines:
                line = line.split(',')
                line = [i.strip() for i in line]
            idx_ves = None
            idx_buf = None
            for ii in range (0, len(lines)):
                if 'NVES' in lines[ii]:
                    idx_ves = ii
                if 'NBUFLE' in lines[ii]:
                    idx_buf = ii
            #If there is information about the vessel, read it
            if idx_ves:
                nvessel = int(lines[idx_ves+1])
                Rves = np.array([], dtype="f8")
                Zves = np.array([], dtype="f8")
                for jj in range(0,50):
                    Rves_tmp = lines[idx_ves+3+jj].replace('\n','').split(' ')
                    while '' in Rves_tmp:
                        Rves_tmp.remove('')
                    Rves = np.append(Rves, Rves_tmp).astype("f8")
                    if len(Rves) == nvessel:
                        break
                for zz in range(0,50):
                    Zves_tmp = lines[idx_ves+jj+zz+5].replace('\n','').split(' ')
                    while '' in Zves_tmp:
                        Zves_tmp.remove('')
                    Zves = np.append(Zves, Zves_tmp).astype("f8")
                    if len(Zves) == nvessel:
                        break
                self.out["nvessel"] = nvessel
                self.out["Rvessel"] = np.hstack((Rves, Rves[0]))
                self.out["Zvessel"] = np.hstack((Zves, Zves[0]))
                
            #If there is information about the buffle, read it
            if idx_buf:
                nbuffle = int(lines[idx_buf+1])
                Rbuf = np.array([], dtype="f8")
                Zbuf = np.array([], dtype="f8")
                for jj in range(0,50):
                    Rbuf_tmp = lines[idx_buf+3+jj].replace('\n','').split(' ')
                    while '' in Rbuf_tmp:
                        Rbuf_tmp.remove('')
                    Rbuf = np.append(Rbuf, Rbuf_tmp).astype("f8")
                    if len(Rbuf) == nbuffle:
                        break
                for zz in range(0,50):
                    Zbuf_tmp = lines[idx_buf+jj+zz+5].replace('\n','').split(' ')
                    while '' in Zbuf_tmp:
                        Zbuf_tmp.remove('')
                    Zbuf = np.append(Zbuf, Zbuf_tmp).astype("f8")
                    if len(Zbuf) == nbuffle:
                        break
                self.out["nbuffle"] = nbuffle
                self.out["Rbuffle"] = np.hstack((Rbuf, Rbuf[0]))
                self.out["Zbuffle"] = np.hstack((Zbuf, Zbuf[0]))
            self.grid = True
        except:
            print(" - No grid file found - usual in JETTO runs")

        #####################################
        #SANCO Impurity specific Profile data
        #####################################
        if self.ssp1file:
            #Find the number of charged states/bundles
            Ds = [int(x[2:]) for x in self.names_ssp1 if "ZQ" in x]
            ns_ssp1 = np.max(Ds)

            self.out["srhot"] = self.dataset_ssp1["XRHO"]
            self.out["t_sanco"] = np.squeeze(self.dataset_ssp1["TIME"])
            ni_ssp1 = np.zeros_like(self.dataset_ssp1["N1"])
            niZi2_ssp1 = np.zeros_like(self.dataset_ssp1["N1"]) 
            ne_ssp1 = np.zeros_like(self.dataset_ssp1["N1"])
            Dn_ssp1 = np.zeros_like(self.dataset_ssp1["D1"])
            vn_ssp1 = np.zeros_like(self.dataset_ssp1["V1"])
            #Sum over all the bundles
            for bb in range(1, ns_ssp1+1):
                ni_ssp1 = ni_ssp1 + self.dataset_ssp1["N"+str(bb)]
                niZi2_ssp1 = niZi2_ssp1 + self.dataset_ssp1["N"+str(bb)]*\
                             self.dataset_ssp1["Z"+str(bb)]**2.0
                ne_ssp1 = ne_ssp1 + self.dataset_ssp1["N"+str(bb)]*\
                          self.dataset_ssp1["Z"+str(bb)]
                Dn_ssp1 = Dn_ssp1 + self.dataset_ssp1["D"+str(bb)]*\
                          self.dataset_ssp1["N"+str(bb)]
                vn_ssp1 = vn_ssp1 + self.dataset_ssp1["V"+str(bb)]*\
                          self.dataset_ssp1["N"+str(bb)]

            #Weighted average over the bundles
            self.out["ni_ssp1"] = ni_ssp1
            self.out["niZi2_ssp1"] = niZi2_ssp1
            self.out["ne_ssp1"] = ne_ssp1
            self.out["Dn_ssp1"] = Dn_ssp1/ni_ssp1
            self.out["vn_ssp1"] = vn_ssp1/ni_ssp1

            #External neutral influx [m-2 s-1]
            self.out["Sn_spp1"] = self.dataset_sst1["INFL"]

        if self.ssp2file:
            #Find the number of charged states/bundles
            Ds = [int(x[2:]) for x in self.names_ssp2 if "ZQ" in x]
            ns_ssp2 = np.max(Ds)

            self.out["srhot"] = self.dataset_ssp2["XRHO"]
            self.out["t_sanco"] = np.squeeze(self.dataset_ssp2["TIME"])
            ni_ssp2 = np.zeros_like(self.dataset_ssp2["N1"])
            niZi2_ssp2 = np.zeros_like(self.dataset_ssp2["N1"]) 
            ne_ssp2 = np.zeros_like(self.dataset_ssp2["N1"])
            Dn_ssp2 = np.zeros_like(self.dataset_ssp2["D1"])
            vn_ssp2 = np.zeros_like(self.dataset_ssp2["V1"])
            #Sum over all the bundles
            for bb in range(1, ns_ssp2+1):
                ni_ssp2 = ni_ssp2 + self.dataset_ssp2["N"+str(bb)]
                niZi2_ssp2 = niZi2_ssp2 + self.dataset_ssp2["N"+str(bb)]*\
                             self.dataset_ssp2["Z"+str(bb)]**2.0
                ne_ssp2 = ne_ssp2 + self.dataset_ssp2["N"+str(bb)]*\
                          self.dataset_ssp2["Z"+str(bb)]
                Dn_ssp2 = Dn_ssp2 + self.dataset_ssp2["D"+str(bb)]*\
                          self.dataset_ssp2["N"+str(bb)]
                vn_ssp2 = vn_ssp2 + self.dataset_ssp2["V"+str(bb)]*\
                          self.dataset_ssp2["N"+str(bb)]

            #Weighted average over the bundles
            self.out["ni_ssp2"] = ni_ssp2
            self.out["niZi2_ssp2"] = niZi2_ssp2
            self.out["ne_ssp2"] = ne_ssp2
            self.out["Dn_ssp2"] = Dn_ssp2/ni_ssp2
            self.out["vn_ssp2"] = vn_ssp2/ni_ssp2

            #External neutral influx [m-2 s-1]
            self.out["Sn_spp2"] = self.dataset_sst2["INFL"]

        if self.ssp3file:
            #Find the number of charged states/bundles
            Ds = [int(x[2:]) for x in self.names_ssp3 if "ZQ" in x]
            ns_ssp3 = np.max(Ds)

            self.out["srhot"] = self.dataset_ssp3["XRHO"]
            self.out["t_sanco"] = np.squeeze(self.dataset_ssp3["TIME"])
            ni_ssp3 = np.zeros_like(self.dataset_ssp3["N1"])
            niZi2_ssp3 = np.zeros_like(self.dataset_ssp3["N1"]) 
            ne_ssp3 = np.zeros_like(self.dataset_ssp3["N1"])
            Dn_ssp3 = np.zeros_like(self.dataset_ssp3["D1"])
            vn_ssp3 = np.zeros_like(self.dataset_ssp3["V1"])
            #Sum over all the bundles
            for bb in range(1, ns_ssp3+1):
                ni_ssp3 = ni_ssp3 + self.dataset_ssp3["N"+str(bb)]
                niZi2_ssp3 = niZi2_ssp3 + self.dataset_ssp3["N"+str(bb)]*\
                             self.dataset_ssp3["Z"+str(bb)]**2.0
                ne_ssp3 = ne_ssp3 + self.dataset_ssp3["N"+str(bb)]*\
                          self.dataset_ssp3["Z"+str(bb)]
                Dn_ssp3 = Dn_ssp3 + self.dataset_ssp3["D"+str(bb)]*\
                          self.dataset_ssp3["N"+str(bb)]
                vn_ssp3 = vn_ssp3 + self.dataset_ssp3["V"+str(bb)]*\
                          self.dataset_ssp3["N"+str(bb)]

            #Weighted average over the bundles
            self.out["ni_ssp3"] = ni_ssp3
            self.out["niZi2_ssp3"] = niZi2_ssp3
            self.out["ne_ssp3"] = ne_ssp3
            self.out["Dn_ssp3"] = Dn_ssp3/ni_ssp3
            self.out["vn_ssp3"] = vn_ssp3/ni_ssp3

            #External neutral influx [m-2 s-1]
            self.out["Sn_spp3"] = self.dataset_sst3["INFL"]

        #####################
        #NEO 2D Impurity data
        #####################
        try:
            self._read_tci_asym()
            self.tci_asym = True
        except:
            print(" - No TCI_asym file found")

        return


    def _read_tci_asym(self):
        """
        Reads the file TCI_asym.dat produced by 
        2D TCI codes, such as NEO.
        Returns 2D density profiles.

        Parameters
        ----------

        Notes
        ----------
        This is a python adaptation of a routine
        already written in Matlab by F. Casson.

        Routine reads output generated by:
        jetto/tci/transport/src/TCI_asymmetry.F90
          SUBROUTINE OUTPUT_2D_DENS(dens2d,profiles)

        Assumes the binary was written using 8-byte reals
        (float64) and Fortran column-major array ordering.
        """
       
        tci_asym_file = os.path.join(self.jetto_path, "TCI_asym.dat")
        dat = {"file": tci_asym_file}

        if os.path.exists(dat["file"]):
            dat["date"] = datetime.fromtimestamp(os.path.getmtime(dat["file"]))
        else:
            raise FileNotFoundError(f"Cannot find {dat['file']}")

        time_list = []
        R_list, Z_list, B2D_list, rho_list = [], [], [], []
        dens_dict = {}

        with open(dat["file"], "rb") as fid:
            while True:
                try:
                    #Read time
                    n1 = np.fromfile(fid, dtype=np.int32, count=1)
                    if n1.size == 0:  # EOF
                        break
                    time_val = np.fromfile(fid, dtype=np.float64, count=1)[0]
                    time_list.append(time_val)

                    #Read nions / ntheta / nr
                    np.fromfile(fid, dtype=np.int32, count=2)
                    nions = np.fromfile(fid, dtype=np.int32, count=1)[0]
                    if nions < 10:
                        dat["nions_neo"] = nions
                        np.fromfile(fid, dtype=np.int32, count=2)
                        ntheta = np.fromfile(fid, dtype=np.int32, count=1)[0]
                    else:
                        ntheta = nions
                    dat["ntheta"] = ntheta

                    np.fromfile(fid, dtype=np.int32, count=2)
                    nr = np.fromfile(fid, dtype=np.int32, count=1)[0]
                    dat["nr"] = nr

                    #Theta grid
                    np.fromfile(fid, dtype=np.int32, count=2)
                    theta = np.fromfile(fid, dtype=np.float64, count=ntheta)
                    dat.setdefault("theta", theta)

                    #Rho grid
                    np.fromfile(fid, dtype=np.int32, count=2)
                    rho = np.fromfile(fid, dtype=np.float64, count=nr)
                    rho_list.append(rho)

                    #{R} grid coordinates
                    np.fromfile(fid, dtype=np.int32, count=2)
                    R = np.fromfile(fid, dtype=np.float64, count=nr*ntheta)
                    R = R.reshape((nr, ntheta), order='F')
                    R_list.append(R)

                    #{Z} grid coordinates
                    np.fromfile(fid, dtype=np.int32, count=2)
                    Z = np.fromfile(fid, dtype=np.float64, count=nr*ntheta)
                    Z = Z.reshape((nr, ntheta), order='F')
                    Z_list.append(Z)

                    #B2D
                    np.fromfile(fid, dtype=np.int32, count=2)
                    B2D = np.fromfile(fid, dtype=np.float64, count=nr*ntheta)
                    B2D = B2D.reshape((nr, ntheta), order='F')
                    B2D_list.append(B2D)

                    #Ion charge states and densities
                    for k in range(1, nions+1):
                        np.fromfile(fid, dtype=np.int32, count=2)
                        is_val = np.fromfile(fid, dtype=np.int32, count=1)[0]
                        np.fromfile(fid, dtype=np.int32, count=2)
                        z_charge = np.fromfile(fid, dtype=np.float64, count=1)[0]
                        dat[f"z_{is_val}"] = z_charge

                        np.fromfile(fid, dtype=np.int32, count=2)
                        dens = np.fromfile(fid, dtype=np.float64, count=nr*ntheta)
                        #use 'C' to match Fortran array constructor
                        dens = dens.reshape((nr, ntheta), order='C')
                        dens_dict.setdefault(is_val, []).append(dens)

                    np.fromfile(fid, dtype=np.int32, count=1)

                except Exception:
                    break

        #Convert lists to arrays
        dat["time_neo"] = np.array(time_list)
        dat["Rneo"] = np.stack(R_list, axis=2)
        dat["Zneo"] = np.stack(Z_list, axis=2)
        dat["B2D"] = np.stack(B2D_list, axis=2)
        dat["rho_neo"] = np.stack(rho_list, axis=1)

        #Convert dens_dict to dat entries
        dat["dens_1"] = np.stack(dens_dict.get(1, [np.zeros((nr, ntheta))]), axis=2)
        dat["dens_2"] = np.stack(dens_dict.get(2, [np.zeros((nr, ntheta))]), axis=2)
        for k, dens_list in dens_dict.items():
            if k > 2:
                dat[f"dens_{k}"] = np.stack(dens_list, axis=2)

        #Add first column to close circular theta loop
        for key in ["Rneo", "Zneo", "B2D"] + [f"dens_{i}" for i in range(1, nions+1)]:
            if key in dat:
                dat[key] = np.concatenate((dat[key], dat[key][:, 0:1, :]), axis=1)

        #Tungsten asymmetry
        mid = int(np.ceil(dat["ntheta"] / 2 + 0.1))
        lfs = 1

        dat["asym_W"], dat["dens_W"] = np.nan, np.nan
        for i in range(2, 6):
            if dat.get(f"z_{i}") == 74:
                dat["asym_W"] = \
                (dat[f"dens_{i}"][:, mid, :] - dat[f"dens_{i}"][:, lfs, :]) / \
                (dat[f"dens_{i}"][:, mid, :] + dat[f"dens_{i}"][:, lfs, :])
                dat["dens_W"] = dat[f"dens_{i}"]
                break

        #Hydrogen asymmetry
        if nions in [3, 4, 5]:
            idx = {3: 3, 4: 4, 5: 5}[nions]
            if dat.get(f"z_{idx}") == 1:
                dat["asym_H"] =\
                    (dat[f"dens_{idx}"][:, mid, :] - dat[f"dens_{idx}"][:, lfs, :]) /\
                    (dat[f"dens_{idx}"][:, mid, :] + dat[f"dens_{idx}"][:, lfs, :])
                dat["xH_lfs"] = dat[f"dens_{idx}"][:, lfs, :]/dat["dens_1"][:, lfs, :]
                dat["dens_H"] = dat[f"dens_{idx}"]
        else:
            dat["asym_H"] = np.full_like(dat["asym_W"], np.nan)
            dat["xH_lfs"] = np.full_like(dat["asym_W"], np.nan)
            dat["dens_H"] = np.full_like(dat["dens_1"], np.nan)

        #Flux-surface averages (mean over all theta and time)
        try:
            dat["fsa_H"] = np.mean(dat["dens_H"], axis=1)
            dat["xH_fsa"] = np.mean(dat["dens_H"], axis=1)/\
                            np.mean(dat["dens_1"], axis=1)
        except Exception:
            pass

        dat["rmin"] = (dat["Rneo"][:, mid, :] - dat["Rneo"][:, 0, :]) /\
                      (dat["Rneo"][:, mid, :] + dat["Rneo"][:, 0, :])
        dat["rova"] = dat["rmin"][:, -1] / dat["rmin"][-1, -1]
        dat["Bc"] = 0

        #Append NEO data to output dictionary
        self.out.update(dat)

        return dat


    def _readjetto_imas(self, database, nshot, run, user, backend, 
                        data_version):
        """
         Reads IMAS Output from JETTO using the IMAS
         module

         Stored in /imasdb/3/0/0/
         shot number = first 5 numbers without following 0s
         run number for output - 2
         Database - 'iter'
         USER - Directory of the Database or 'public'
         for the general one
        """

        #IMAS module - To handle IDS output
        try:
            import imas
        except ImportError:
            print(' - IMAS Module could not be loaded.'+\
            ' Output IDS cannot be read!')
            if (self.backend=="hdf5") or (self.backend=="mdsplus"):
                return
        
        if backend == "mdsplus":
            imas_backend = imas.imasdef.MDSPLUS_BACKEND
        elif backend == "hdf5":
            imas_backend = imas.imasdef.HDF5_BACKEND

        input = imas.DBEntry(imas_backend, database, nshot,
                             run, user_name=user,
                             data_version=data_version)
        input.open()
        self.jet = input

        return


    def _out_memory_imas(self):
        """ 
        Reads into a new data dictionary the IMAS
        output Database from JINTRAC

        Parameters
        ----------

        Output
        ----------

        Notes
        ----------
        """

        ############
        #SUMMARY IDS
        ############
        #Load summary IDSs into memory with "get"
        summary = self.jet.get('summary')
        #Get IDS data
        self.out["data_dictionary"] = summary.ids_properties.version_put.data_dictionary
        self.out["access_layer"] = summary.ids_properties.version_put.access_layer
        self.out["time"] = summary.time
        self.out["nt"] = len(summary.time)
        #Set a dummy variable corresponding to the jetto.jst
        #timebase from the standard output.
        self.out["time_derived"] = self.out["time"]
        self.out["Wtot"] = summary.global_quantities.energy_total.value
        self.out["Wth"] = summary.global_quantities.energy_thermal.value
        self.out["Wdia"] = summary.global_quantities.energy_diamagnetic.value

        #Energy confinement time
        self.out["tau_e"] = summary.global_quantities.tau_energy.value
        #Total plasma current
        self.out["Ip"] = summary.global_quantities.ip.value
        self.out["jpar_Bstot"] = summary.global_quantities.current_bootstrap.value
        self.out["R0"] = summary.global_quantities.r0.value

        #Total EC power from all launchers [MW]
        n_ec_launchers = len(summary.heating_current_drive.ec)
        Pec_tot = 0
        jec_tot = 0
        for ll in range(0, n_ec_launchers):
            Pec_tot += summary.heating_current_drive.ec[ll].power.value
            jec_tot += summary.heating_current_drive.ec[ll].current.value
        self.out["Pec_tot"] = Pec_tot
        self.out["jtor_ectot"] = jec_tot

        #Total NBI (e+i) power from all beams [MW]
        n_nbi_beams = len(summary.heating_current_drive.nbi)
        Pnbi_tot = 0
        jnbi_tot = 0
        for ll in range(0, n_nbi_beams):
            Pnbi_tot += summary.heating_current_drive.nbi[ll].power.value
            jnbi_tot += summary.heating_current_drive.nbi[ll].current.value
        self.out["Pnbi_tot"] = Pnbi_tot
        self.out["jtor_nbitot"] = jnbi_tot

        self.out["Palf"] = summary.fusion.power.value
        self.out["Zeff"] = summary.volume_average.zeff.value #f(t)

        #Total IC (e+i) power from all antennas [MW]
        n_ic_ant = len(summary.heating_current_drive.ic)
        Pic_tot = 0
        jic_tot = 0
        for ll in range(0, n_ic_ant):
            Pic_tot += summary.heating_current_drive.ic[ll].power.value
            jic_tot += summary.heating_current_drive.ic[ll].current.value
        self.out["Pic_tot"] = Pnbi_tot
        self.out["jtor_ictot"] = jnbi_tot

        self.out["Palf"] = summary.fusion.power.value
        self.out["Zeff"] = summary.volume_average.zeff.value #f(t)

        #Line-averaged electron density [1e19 m-3]
        self.out["ne_lavg"] = summary.line_average.n_e.value

        #Gas injection rates [el/s]
        self.out["Spuff_H_tot"] = summary.gas_injection_rates.hydrogen.value
        if len(self.out["Spuff_H_tot"]) == 0:
            self.out["Spuff_H_tot"] = np.zeros(self.out["nt"])
        self.out["Spuff_D_tot"] = summary.gas_injection_rates.deuterium.value
        if len(self.out["Spuff_D_tot"]) == 0:
            self.out["Spuff_D_tot"] = np.zeros(self.out["nt"]) 
        self.out["Spuff_T_tot"] = summary.gas_injection_rates.tritium.value
        if len(self.out["Spuff_T_tot"]) == 0:
            self.out["Spuff_T_tot"] = np.zeros(self.out["nt"])
        self.out["Spuff_Ne_tot"] = summary.gas_injection_rates.neon.value
        if len(self.out["Spuff_Ne_tot"]) == 0:
            self.out["Spuff_Ne_tot"] = np.zeros(self.out["nt"])

        #########
        #WALL IDS
        #########
        #Wall contour
        try:
            self.out["Rvessel"] = self.jet.partial_get('wall',
                        'description_2d(0)/limiter/unit(0)/outline/r').T
            self.out["Zvessel"] = self.jet.partial_get('wall',
                        'description_2d(0)/limiter/unit(0)/outline/z').T
        except:
            print("- No wall IDS")

        ################
        #EQUILIBRIUM IDS
        ################
        #f(t)
        self.out["Vol_t"] = Vol_t = self.jet.partial_get('equilibrium',
                   'time_slice(:)/global_quantities(:)/volume').T
        #Outer midplane major radius [m]
        self.out["R_omp"] = self.jet.partial_get('equilibrium',
                    'time_slice(:)/profiles_1d/r_outboard').T
        rho_tor_norm_eq = self.jet.partial_get('equilibrium',
                             'time_slice(:)/profiles_1d/rho_tor_norm').T
        self.out["rho_tor_norm_eq"] = rho_tor_norm_eq
        Vol_rho = self.jet.partial_get('equilibrium',
                          'time_slice(:)/profiles_1d/volume').T
        self.out["Vol_rho"] = Vol_rho

        ds = rho_tor_norm_eq[:,1:]-rho_tor_norm_eq[:,:1]
        dV = (Vol_rho[:,1:]-Vol_rho[:,:-1])
        dVds = dV/ds
        #dVol/drho [m2]
        self.out["dVdrho"] = self.jet.partial_get('equilibrium',
                   'time_slice(:)/profiles_1d(:)/dvolume_drho_tor').T
        self.out["Sur_t"] = Vol_t = self.jet.partial_get('equilibrium',
                   'time_slice(:)/global_quantities(:)/surface').T

        #Btor(R=Raxis)
        self.out["Btor"] =\
        self.jet.partial_get('equilibrium',
        'time_slice(:)/global_quantities(:)/magnetic_axis/b_field_tor').T

        #2D profiles
        #{R,Z} coordinates of flux grid
        self.out["Rgrid"] = self.jet.partial_get('equilibrium',
                    'time_slice(:)/profiles_2d(0)/r').T
        self.out["Zgrid"] = self.jet.partial_get('equilibrium',
                    'time_slice(:)/profiles_2d(0)/z').T
        self.out["Psi"] = self.jet.partial_get('equilibrium',
                    'time_slice(:)/profiles_2d(0)/psi').T

        #Poloidal flux at the separatrix
        self.out["Psi_sep"] = self.jet.partial_get('equilibrium',
                    'time_slice(:)/boundary_separatrix/psi').T

        ##Interpolate {rsep, zsep} from 2D grid for last time point
        #cs = plt.contour(self.out["Rgrid"][-1,:,:], self.out["Zgrid"][-1,:,:],
        #                 self.out["Psi"][-1,:,:], [self.out["Psi_sep"][-1]])
        #p = cs.collections[0].get_paths()[0]
        #v = p.vertices
        #self.out["Rbnd"] = v[:,0]
        #self.out["Zbnd"] = v[:,1]

        ##################
        #CORE PROFILES IDS
        ##################
        cp = self.jet.get('core_profiles')
        self.out["rhot_norm"] = self.jet.partial_get('core_profiles',
                                'profiles_1d(:)/grid/rho_tor_norm').T
        #JETTO label [m]
        self.out["rho"] = self.jet.partial_get('core_profiles',
                          'profiles_1d(:)/grid/rho_tor').T
        #Use the rhot_norm coordinate
        self.out["srhot"] = self.out["rhot_norm"]
        self.out["Te"] = self.jet.partial_get('core_profiles',
                          'profiles_1d(:)/electrons/temperature').T
        self.out["ne"] = self.jet.partial_get('core_profiles',
                           'profiles_1d(:)/electrons/density').T

        ions = self.jet.partial_get('core_profiles',
                    'profiles_1d(:)/ion')
        nions = len(ions)
        self.out["niH"] = np.zeros_like(self.out["ne"])
        self.out["TiH"] = np.zeros_like(self.out["ne"])
        self.out["niD"] = np.zeros_like(self.out["ne"])
        self.out["TiD"] = np.zeros_like(self.out["ne"])
        self.out["niT"] = np.zeros_like(self.out["ne"])
        self.out["TiT"] = np.zeros_like(self.out["ne"])
        self.out["niHe"] = np.zeros_like(self.out["ne"])
        self.out["TiHe"] = np.zeros_like(self.out["ne"])
        self.out["niNe"] = np.zeros_like(self.out["ne"])
        self.out["TiNe"] = np.zeros_like(self.out["ne"])
        self.out["niW"] = np.zeros_like(self.out["ne"])
        self.out["TiW"] = np.zeros_like(self.out["ne"])
        self.out["vtor"] = np.zeros_like(self.out["ne"])
        for nn in range(0, nions):
            label = np.unique(self.jet.partial_get('core_profiles',
                              'profiles_1d(:)/ion('+str(nn)+')/label'))
            if label == 'H':
                self.out["niH"] = self.jet.partial_get('core_profiles',
                          'profiles_1d(:)/ion('+str(nn)+')/density').T
                self.out["TiH"] = self.jet.partial_get('core_profiles',
                          'profiles_1d(:)/ion('+str(nn)+')/temperature').T
                self.out["vtH"] = self.jet.partial_get('core_profiles',
                          'profiles_1d(:)/ion('+str(nn)+')/velocity_tor').T
                self.out["wtH"] = self.jet.partial_get('core_profiles',
                          'profiles_1d(:)/ion('+str(nn)+')/rotation_frequency_tor').T
                if np.any(self.out["vtH"]) is not None:       
                    self.out["vtor"] += self.out["vtH"]
            elif label == 'D':
                self.out["niD"] = self.jet.partial_get('core_profiles',
                          'profiles_1d(:)/ion('+str(nn)+')/density').T
                self.out["TiD"] = self.jet.partial_get('core_profiles',
                          'profiles_1d(:)/ion('+str(nn)+')/temperature').T
                self.out["vtD"] = self.jet.partial_get('core_profiles',
                          'profiles_1d(:)/ion('+str(nn)+')/velocity_tor').T
                self.out["wtD"] = self.jet.partial_get('core_profiles',
                          'profiles_1d(:)/ion('+str(nn)+')/rotation_frequency_tor').T
                if np.any(self.out["vtD"]) is not None:
                    self.out["vtor"] += self.out["vtD"]
            elif label == 'T':
                self.out["niT"] = self.jet.partial_get('core_profiles',
                          'profiles_1d(:)/ion('+str(nn)+')/density').T
                self.out["TiT"] = self.jet.partial_get('core_profiles',
                          'profiles_1d(:)/ion('+str(nn)+')/temperature').T
                self.out["vtT"] = self.jet.partial_get('core_profiles',
                          'profiles_1d(:)/ion('+str(nn)+')/velocity_tor').T
                self.out["wtT"] = self.jet.partial_get('core_profiles',
                          'profiles_1d(:)/ion('+str(nn)+')/rotation_frequency_tor').T
                if np.any(self.out["vtT"]) is not None:
                    self.out["vtor"] += self.out["vtT"]
            elif label == 'He':
                self.out["niHe"] = self.jet.partial_get('core_profiles',
                          'profiles_1d(:)/ion('+str(nn)+')/density').T
                self.out["TiHe"] = self.jet.partial_get('core_profiles',
                          'profiles_1d(:)/ion('+str(nn)+')/temperature').T
                self.out["vtHe"] = self.jet.partial_get('core_profiles',
                          'profiles_1d(:)/ion('+str(nn)+')/velocity_tor').T
                self.out["wtHe"] = self.jet.partial_get('core_profiles',
                          'profiles_1d(:)/ion('+str(nn)+')/rotation_frequency_tor').T
                if np.any(self.out["vtHe"]) is not None:
                    self.out["vtor"] += self.out["vtHe"]
            elif label == 'C':
                self.out["niC"] = self.jet.partial_get('core_profiles',
                          'profiles_1d(:)/ion('+str(nn)+')/density').T
                self.out["TiC"] = self.jet.partial_get('core_profiles',
                          'profiles_1d(:)/ion('+str(nn)+')/temperature').T
                self.out["vtC"] = self.jet.partial_get('core_profiles',
                          'profiles_1d(:)/ion('+str(nn)+')/velocity_tor').T
                self.out["wtC"] = self.jet.partial_get('core_profiles',
                          'profiles_1d(:)/ion('+str(nn)+')/rotation_frequency_tor').T
                if np.any(self.out["vtC"]) is not None:
                    self.out["vtor"] += self.out["vtC"]
            elif label == 'Ne':
                self.out["niNe"] = self.jet.partial_get('core_profiles',
                          'profiles_1d(:)/ion('+str(nn)+')/density').T
                self.out["TiNe"] = self.jet.partial_get('core_profiles',
                          'profiles_1d(:)/ion('+str(nn)+')/temperature').T
                self.out["vtNe"] = self.jet.partial_get('core_profiles',
                          'profiles_1d(:)/ion('+str(nn)+')/velocity_tor').T
                self.out["wtNe"] = self.jet.partial_get('core_profiles',
                          'profiles_1d(:)/ion('+str(nn)+')/rotation_frequency_tor').T
                if np.any(self.out["vtNe"]) is not None:
                    self.out["vtor"] += self.out["vtNe"]
            elif label == 'W':
                self.out["niW"] = self.jet.partial_get('core_profiles',
                          'profiles_1d(:)/ion('+str(nn)+')/density').T
                self.out["TiW"] = self.jet.partial_get('core_profiles',
                          'profiles_1d(:)/ion('+str(nn)+')/temperature').T
                self.out["vtW"] = self.jet.partial_get('core_profiles',
                          'profiles_1d(:)/ion('+str(nn)+')/velocity_tor').T
                self.out["wtW"] = self.jet.partial_get('core_profiles',
                          'profiles_1d(:)/ion('+str(nn)+')/rotation_frequency_tor').T
                if np.any(self.out["vtW"]) is not None:
                    self.out["vtor"] += self.out["vtW"]

        self.out["vtor"] = self.out["vtor"]/nions
        self.out["pres"] = self.jet.partial_get('core_profiles',
                                    'profiles_1d(:)/pressure_thermal(:)').T

        #Total toroidal current density = average(J_Tor/R) / average(1/R)
        #{dynamic} [A/m^2]
        self.out["jtor"] = self.jet.partial_get('core_profiles',
                                         'profiles_1d(:)/j_tor').T
        #Bootstrap current density = average(J_Bootstrap.B) / B0,
        #where B0 = Core_Profiles/Vacuum_Toroidal_Field/ B0
        self.out["jpar_Bs"] = self.jet.partial_get('core_profiles',
                                         'profiles_1d(:)/j_bootstrap').T
        self.out["qprof"] = self.jet.partial_get('core_profiles',
                                         'profiles_1d(:)/q').T
        #Magnetic shear
        self.out["qshear"] = self.jet.partial_get('core_profiles',
                                         'profiles_1d(:)/magnetic_shear').T
        #Vacuum Btor(R=Raxis)
        self.out["Btor_vac"] = self.jet.partial_get('core_profiles',
                                'vacuum_toroidal_field/b0(:)').T

        ########
        #NBI IDS
        ########
        n_units = self.jet.partial_get('nbi', 'unit')
        n_units = len(n_units)
        self.out["Pnbi_launched"] = np.zeros_like(self.out["time"])
        if n_units != 0:
            for uu in range(0, n_units):
                p_launched = self.jet.partial_get('nbi',
                            'unit('+str(uu)+')/power_launched/data')
                if p_launched is not None:
                    self.out["Pnbi_launched"] += p_launched
                t_nbi = self.jet.partial_get('nbi',
                            'unit('+str(uu)+')/power_launched/time')
            self.out["t_nbi"] = t_nbi

        ##################
        #EDGE PROFILES IDS
        ##################
        #JETTO simulations don't have the edge profiles IDS,
        #therefore, only read them if it's a Coconut simulation
        #if self.coconut:
            #self.out["time_e2d"] = self.jet.partial_get('edge_profiles',
            #                    'time(:)')
            #self.out["ne_edge"] = self.jet.partial_get('edge_profiles',
            #                    'profiles_1d(:)/electrons/density(:)')
            #self.out["Te_edge"] = self.jet.partial_get('edge_profiles',
            #                    'profiles_1d(:)/electrons/temperature(:)')

        #################
        #CORE SOURCES IDS
        #################
        #Cource sources identifiers
        # i1: 0 (unspecified) Unspecified source type
        # i1: 1	Total source; combines all sources
        # i1: 2 Source from Neutral Beam Injection
        # i1; 3 Sources from electron cyclotron heating and current drive
        # i1: 6 Sources from fusion reactions, e.g., alpha particle heating
        # i1: 7 Source from ohmic heating
        # i1: 108 (gas_puff) Gas puff
        #Rho of core_sources has the same dimmensionality
        #as rho from core_profiles, and the same values
        #(I compared them), so I assume they are the same
        #radial coordinate
        #rho = self.jet.partial_get('core_sources',
        #      'source(0)/profiles_1d(:)/grid/rho_tor_norm(:)')
        cs = self.jet.get('core_sources')
        for ss in range(0, len(cs.source)):
            #0 (unspecified) Unspecified source type
            if cs.source[ss].identifier.index == 0:
                self.out["S0"] = self.jet.partial_get('core_sources',
                'source(0)/profiles_1d(:)/ion(1)/particles(:)')

            #Total sources
            elif cs.source[ss].identifier.index == 1:
                self.out["rhot_tot"] = self.jet.partial_get('core_sources',
                'source('+str(ss)+')/profiles_1d(:)/grid/rho_tor_norm').T
                self.out["Ptot_e"] = self.jet.partial_get('core_sources',
                'source('+str(ss)+')/profiles_1d(:)/electrons/energy').T
                self.out["Ptot_i"] = self.jet.partial_get('core_sources',
                'source('+str(ss)+')/profiles_1d(:)/total_ion_energy').T

                #Loop over ions for particle sources
                #[part/s*m^3]
                #Total part. source
                ions = self.jet.partial_get('core_sources',
                    'source('+str(ss)+')/profiles_1d(:)/ion')
                nions = len(ions)
                for nn in range(0, nions):
                    label = np.unique(self.jet.partial_get('core_sources',
                            'source('+str(ss)+')/profiles_1d(:)/ion('+\
                            str(nn)+')/label'))[0]
                    if label == 'H':
                        self.out["Stot_H"] = self.jet.partial_get('core_sources',
                            'source('+str(ss)+')/profiles_1d(:)/ion('+
                            str(nn)+')/particles').T
                    if label == 'D':
                        self.out["Stot_D"] = self.jet.partial_get('core_sources',
                            'source('+str(ss)+')/profiles_1d(:)/ion('+
                            str(nn)+')/particles').T
                    elif label == 'T':
                        self.out["Stot_T"] = self.jet.partial_get('core_sources',
                            'source('+str(ss)+')/profiles_1d(:)/ion('+
                            str(nn)+')/particles').T
                    elif label == 'He':
                        self.out["Stot_He"] = self.jet.partial_get('core_sources',
                            'source('+str(ss)+')/profiles_1d(:)/ion('+
                            str(nn)+')/particles').T
                    elif label == 'Ne':
                        self.out["Stot_Ne"] = self.jet.partial_get('core_sources',
                            'source('+str(ss)+')/profiles_1d(:)/ion('+
                            str(nn)+')/particles').T

            #NBI sources
            elif cs.source[ss].identifier.index == 2:
                self.out["rhotnbi"] = self.jet.partial_get('core_sources',
                    'source('+str(ss)+')/profiles_1d(:)/grid/rho_tor_norm').T
                #[W/m3]
                self.out["Pnbi_e"] = self.jet.partial_get('core_sources',
                    'source('+str(ss)+')/profiles_1d(:)/electrons/energy').T
                self.out["Pnbi_i"] = self.jet.partial_get('core_sources',
                    'source('+str(ss)+')/profiles_1d(:)/total_ion_energy').T
                #[A/m^2]
                self.out["j_parallel_nbi"] = self.jet.partial_get('core_sources',
                    'source('+str(ss)+')/profiles_1d(:)/j_parallel').T
                #[kg/ms^2]
                self.out["mom_tor_nbi"] = self.jet.partial_get('core_sources',
                    'source('+str(ss)+')/profiles_1d(:)/momentum_tor').T

                #Loop over ions for particle sources
                #[part/s*m^3]
                #NBI part. source (spec 1)
                #SBD1 = self.jet.partial_get('core_sources',
                #       'source(2)/profiles_1d(:)/ion(1)/particles(:)')
                #NBI part. source (spec 2)
                #SBD2 = self.jet.partial_get('core_sources',
                #       'source(2)/profiles_1d(:)/ion(2)/particles(:)')
                ions = self.jet.partial_get('core_sources',
                    'source('+str(ss)+')/profiles_1d(:)/ion')
                nions = len(ions)
                for nn in range(0, nions):
                    label = np.unique(self.jet.partial_get('core_sources',
                            'source('+str(ss)+')/profiles_1d(:)/ion('+\
                            str(nn)+')/label'))
                    if label == 'D':
                        self.out["Snbi_D"] = self.jet.partial_get('core_sources',
                            'source('+str(ss)+')/profiles_1d(:)/ion('+
                            str(nn)+')/particles').T
                        #Assume for the time being D and T
                        self.out["SBD1"] = self.out["Snbi_D"]
                    elif label == 'T':
                        self.out["Snbi_T"] = self.jet.partial_get('core_sources',
                            'source('+str(ss)+')/profiles_1d(:)/ion('+
                            str(nn)+')/particles').T
                        #Assume for the time being D and T
                        self.out["SBD2"] = self.out["Snbi_T"]
                    elif label == 'He':
                        self.out["Snbi_He"] = self.jet.partial_get('core_sources',
                            'source('+str(ss)+')/profiles_1d(:)/ion('+
                            str(nn)+')/particles').T

            #ECRH sources
            elif cs.source[ss].identifier.index == 3:
                self.out["rhotec"] = self.jet.partial_get('core_sources',
                    'source('+str(ss)+')/profiles_1d(:)/grid/rho_tor_norm').T
                self.out["Pecrh"] = self.jet.partial_get('core_sources',
                    'source('+str(ss)+')/profiles_1d(:)/electrons/energy').T
                self.out["jpar_ec"] = self.jet.partial_get('core_sources',
                    'source('+str(ss)+')/profiles_1d(:)/j_parallel').T

            #Sources from fusion reactions, e.g., alpha particle heating
            elif cs.source[ss].identifier.index == 6:
                self.out["Palh_e"] = self.jet.partial_get('core_sources',
                        'source('+str(ss)+')/profiles_1d(:)/electrons/energy').T
                self.out["Palh_i"] = self.jet.partial_get('core_sources',
                        'source('+str(ss)+')/profiles_1d(:)/ions(0)/energy').T
                #Not populated
                #Palf = self.jet.partial_get('core_sources',
                #       'source(6)/global_quantities(:)/power')

            #Source from ohmic heating
            elif cs.source[ss].identifier.index == 7:
                self.out["Poh_e"] = self.jet.partial_get('core_sources',
                        'source('+str(ss)+')/profiles_1d(:)/electrons/energy').T
                if np.shape(self.out["Poh_e"])[0] != 0:
                    Poh_tot = np.zeros_like(self.out["time"])
                    for tt in range(0, np.shape(dVds)[0]):
                        Poh_tot[tt] = np.sum(self.out["Poh_e"][tt,1:]*dVds[tt,:]*ds[tt,:])
                    self.out["Poh_tot"] = np.squeeze(Poh_tot)

            #Radiation sources [W/m3]
            elif cs.source[ss].identifier.index == 200:
                self.out["rhotrad"] = self.jet.partial_get('core_sources',
                    'source('+str(ss)+')/profiles_1d(:)/grid/rho_tor_norm').T
                self.out["Prad"] = self.jet.partial_get('core_sources',
                    'source('+str(ss)+')/profiles_1d(:)/electrons/energy').T
                #I couldn't find an IDS for the total radited power as a 
                #function of time, so I compute the integral myself
                if np.shape(self.out["Prad"])[0] != 0:
                    Prad_tot = np.zeros_like(self.out["time"])
                    for tt in range(0, np.shape(dVds)[0]):
                        Prad_tot[tt] = np.sum(self.out["Prad"][tt,1:]*dVds[tt,:]*ds[tt,:])
                    self.out["Prad_tot"] = np.squeeze(Prad_tot)

        ###################
        #CORE TRANSPORT IDS
        ###################
        #model(i1)/identifier
        #Transport model identifiers
        #i1: 0 unspecified
        #i1: 1 Combination of data from available transport models.
        #i1: 2 Output from a transport solver
        #i3: 3 Background transport level, ad-hoc transport model,
        #      not directly related to a physics model
        #i4: 4 Transport specified by a database entry external to
        #      the dynamic evolution of the plasma
        #i5: 5 Neoclassical
        #i6: 6 Representation of turbulent transport
        nmodels = len(self.jet.partial_get('core_transport', 'model'))
        ct = self.jet.get('core_transport')
        for nn in range(0, nmodels):
            if ct.model[nn].identifier.name == 'combined':
                self.out["rhot_Xs"] = self.jet.partial_get('core_transport',
                       'model('+str(nn)+')/profiles_1d(:)/grid_flux/rho_tor_norm(:)').T
                #[m2/s]
                self.out["Xe"] = self.jet.partial_get('core_transport',
                       'model('+str(nn)+')/profiles_1d(:)/electrons/energy/d(:)').T
                self.out["Xi"] = self.jet.partial_get('core_transport',
                       'model('+str(nn)+')/profiles_1d(:)/total_ion_energy/d(:)').T
                #Electron effective diffusivity
                self.out["De_eff"] = self.jet.partial_get('core_transport',
                             'model('+str(nn)+')/profiles_1d(:)/electrons/particles/d(:)').T
                self.out["ve_eff"] = self.jet.partial_get('core_transport',
                             'model('+str(nn)+')/profiles_1d(:)/electrons/particles/v(:)').T          
                self.out["D1_eff"] = self.jet.partial_get('core_transport',
                             'model('+str(nn)+')/profiles_1d(:)/ions(0)/particles/d(:)').T
                self.out["v1_eff"] = self.jet.partial_get('core_transport',
                             'model('+str(nn)+')/profiles_1d(:)/ions(0)/particles/v(:)').T                  
                self.out["D2_eff"] = self.jet.partial_get('core_transport',
                             'model('+str(nn)+')/profiles_1d(:)/ions(1)/particles/d(:)').T
                self.out["v2_eff"] = self.jet.partial_get('core_transport',
                             'model('+str(nn)+')/profiles_1d(:)/ions(1)/particles/v(:)').T

                #Toroidal momentum transport
                self.out["D_tormom"] = self.jet.partial_get('core_transport',
                             'model('+str(nn)+')/profiles_1d(:)/momentum_tor/d(:)').T
                self.out["v_tormom"] = self.jet.partial_get('core_transport',
                             'model('+str(nn)+')/profiles_1d(:)/momentum_tor/v(:)').T

                #For some old runs, these IDS are not filled
                #Set the arrays to 0
                if np.any(self.out["De_eff"]==None):
                    self.out["De_eff"] = np.zeros_like(self.out["rhot_Xs"])
                    self.out["D1_eff"] = np.zeros_like(self.out["rhot_Xs"])
                    self.out["D2_eff"] = np.zeros_like(self.out["rhot_Xs"])

            #neoclassical
            if ct.model[nn].identifier.name == 'neoclassical':
                nions = len(self.jet.partial_get('core_transport', 'model('+\
                            str(nn)+')/profiles_1d(:)/ion'))
                for ll in range (0, nions):
                    label = np.unique(self.jet.partial_get('core_transport',
                            'model('+str(nn)+')/profiles_1d(:)/ion('+\
                            str(ll)+')/label'))
                    if label == 'H':
                        self.out["Dn_H"] = self.jet.partial_get('core_transport', 'model('+\
                                   str(nn)+')/profiles_1d(:)/ion('+str(ll)+')/particles/d').T
                        self.out["vn_H"] = self.jet.partial_get('core_transport', 'model('+\
                                   str(nn)+')/profiles_1d(:)/ion('+str(ll)+')/particles/v').T
                    if label == 'D':
                        self.out["Dn_D"] = self.jet.partial_get('core_transport', 'model('+\
                                   str(nn)+')/profiles_1d(:)/ion('+str(ll)+')/particles/d').T
                        self.out["vn_D"] = self.jet.partial_get('core_transport', 'model('+\
                                   str(nn)+')/profiles_1d(:)/ion('+str(ll)+')/particles/v').T
                    if label == 'T':
                        self.out["Dn_T"] = self.jet.partial_get('core_transport', 'model('+\
                                   str(nn)+')/profiles_1d(:)/ion('+str(ll)+')/particles/d').T
                        self.out["vn_T"] = self.jet.partial_get('core_transport', 'model('+\
                                   str(nn)+')/profiles_1d(:)/ion('+str(ll)+')/particles/v').T                                
                    if label == 'Ne':
                        self.out["Dn_Ne"] = self.jet.partial_get('core_transport', 'model('+\
                                    str(nn)+')/profiles_1d(:)/ion('+str(ll)+')/particles/d').T
                        self.out["vn_Ne"] = self.jet.partial_get('core_transport', 'model('+\
                                    str(nn)+')/profiles_1d(:)/ion('+str(ll)+')/particles/v').T
                    if label == 'W':
                        self.out["Dn_W"] = self.jet.partial_get('core_transport', 'model('+\
                                   str(nn)+')/profiles_1d(:)/ion('+str(ll)+')/particles/d').T
                        self.out["vn_W"] = self.jet.partial_get('core_transport', 'model('+\
                                   str(nn)+')/profiles_1d(:)/ion('+str(ll)+')/particles/v').T

            #turbulent
            if ct.model[nn].identifier.name == 'anomalous':
                nions = len(self.jet.partial_get('core_transport', 'model('+\
                            str(nn)+')/profiles_1d(:)/ion'))
                for ll in range (0, nions):
                    label = np.unique(self.jet.partial_get('core_transport',
                            'model('+str(nn)+')/profiles_1d(:)/ion('+\
                            str(ll)+')/label'))
                    if label == 'H':
                        self.out["Dt_H"] = self.jet.partial_get('core_transport', 'model('+\
                                   str(nn)+')/profiles_1d(:)/ion('+str(ll)+')/particles/d').T
                        self.out["vt_H"] = self.jet.partial_get('core_transport', 'model('+\
                                   str(nn)+')/profiles_1d(:)/ion('+str(ll)+')/particles/v').T
                    if label == 'D':
                        self.out["Dt_D"] = self.jet.partial_get('core_transport', 'model('+\
                                   str(nn)+')/profiles_1d(:)/ion('+str(ll)+')/particles/d').T
                        self.out["vt_D"] = self.jet.partial_get('core_transport', 'model('+\
                                   str(nn)+')/profiles_1d(:)/ion('+str(ll)+')/particles/v').T
                    if label == 'T':
                        self.out["Dt_T"] = self.jet.partial_get('core_transport', 'model('+\
                                   str(nn)+')/profiles_1d(:)/ion('+str(ll)+')/particles/d').T
                        self.out["vt_T"] = self.jet.partial_get('core_transport', 'model('+\
                                   str(nn)+')/profiles_1d(:)/ion('+str(ll)+')/particles/v').T                                
                    if label == 'Ne':
                        self.out["Dt_Ne"] = self.jet.partial_get('core_transport', 'model('+\
                                    str(nn)+')/profiles_1d(:)/ion('+str(ll)+')/particles/d').T
                        self.out["vt_Ne"] = self.jet.partial_get('core_transport', 'model('+\
                                    str(nn)+')/profiles_1d(:)/ion('+str(ll)+')/particles/v').T
                    if label == 'W':
                        self.out["Dt_W"] = self.jet.partial_get('core_transport', 'model('+\
                                   str(nn)+')/profiles_1d(:)/ion('+str(ll)+')/particles/d').T
                        self.out["vt_W"] = self.jet.partial_get('core_transport', 'model('+\
                                   str(nn)+')/profiles_1d(:)/ion('+str(ll)+')/particles/v').T

        ###################
        #FURTHER QUANTITIES
        ###################
        #I cannot find impurity concentrations as a function
        #of time (.jst output IMC1, IMC2, etc.), so I calculate
        #them here.
        ne_avg = np.zeros_like(Vol_t)
        niW_avg = np.zeros_like(Vol_t)
        niNe_avg = np.zeros_like(Vol_t)
        Pnbi_etot = np.zeros_like(self.out["time"])
        Pnbi_itot = np.zeros_like(self.out["time"])

        #It can be that the equilibrium and kinetic profiles have
        #different radial grids, for instance, when taking input IDS.
        #I need to check for this and interpolate, but for the time being,
        #I simply don't perform the calculations if the grids don't match.
        if np.shape(rho_tor_norm_eq)[1] == np.shape(self.out["ne"])[1]:
            for tt in range(0, np.shape(dVds)[0]):
                ne_avg[tt] = (1/Vol_t[tt]) * np.sum(self.out["ne"][tt,1:]*\
                             dVds[tt,:]*ds[tt,:])
                niNe_avg[tt] = (1/Vol_t[tt]) * np.sum(self.out["niNe"][tt,1:]*\
                               dVds[tt,:]*ds[tt,:])
                niW_avg[tt] = (1/Vol_t[tt]) * np.sum(self.out["niW"][tt,1:]*\
                              dVds[tt,:]*ds[tt,:])
                #Pnbi_etot[tt] = np.sum(self.out["Pnbi_e"][tt,1:]*\
                #                dVds[tt,:]*ds[tt,:])
                #Pnbi_itot[tt] = np.sum(self.out["Pnbi_i"][tt,1:]*\
                #                dVds[tt,:]*ds[tt,:])

            self.out["ne_avg"] = ne_avg
            self.out["niNe_avg"] = niNe_avg
            self.out["niW_avg"] = niW_avg
            self.out["IMC_Ne"] = (niNe_avg/ne_avg)*100
            self.out["IMC_W"] = (niW_avg/ne_avg)*100
            #self.out["Pnbi_etot"] = Pnbi_etot
            #self.out["Pnbi_itot"] = Pnbi_itot
        else:
            pass


        return

    def _calculate_derived_quantities(self):
        """
         Calculates derived quantities from IDS JINTRAC
         output. Since the JINTRAC IMAS driver does not
         fill every IDS that would mimic the standard output,
         we compute some useful quantities here.
        """

        if self.backend == "mdsplus" or self.backend == "hdf5":
            cp = self.jet.get('core_profiles')
            #Poloidal flux
            chi_pol = self.jet.partial_get('core_profiles',
                        'profiles_1d(:)/grid/psi(:)').T
            Vol_t = self.jet.partial_get('equilibrium',
                        'time_slice(:)/global_quantities(:)/volume').T
            Vol_rho = self.jet.partial_get('equilibrium',
                        'time_slice(:)/profiles_1d/volume').T           
            #This IDS is populated with a bunch of Nones..
            #rhop = self.jet.partial_get('core_profiles',
            #     'profiles_1d(:)/grid/rho_pol_norm(:)').T
            dVdchi = (Vol_rho[:,1:]-Vol_rho[:,:-1])/\
                     (chi_pol[:,1:]-chi_pol[:,:-1])
            chi_pol_axis = np.expand_dims(chi_pol[:,0], axis=1)
            chi_pol_axis = np.repeat(chi_pol_axis, np.shape(chi_pol)[1],
                                     axis=1)
            chi_pol_sepa = np.expand_dims(chi_pol[:,-1], axis=1)
            chi_pol_sepa = np.repeat(chi_pol_sepa, np.shape(chi_pol)[1],
                                     axis=1)
            rhop = np.sqrt(np.abs((chi_pol[:,:] - chi_pol_axis)/\
                              (chi_pol_sepa - chi_pol_axis)))                    
            r_omp = self.jet.partial_get('equilibrium',
                    'time_slice(:)/profiles_1d/r_outboard').T            
            pres = self.jet.partial_get('core_profiles',
                    'profiles_1d(:)/pressure_thermal(:)').T
            dpdrp = (pres[:,1:]-pres[:,:-1])/\
                    (rhop[:,1:]-rhop[:,:-1])
            dpdchi = (pres[:,1:]-pres[:,:-1])/\
                    (chi_pol[:,1:]-chi_pol[:,:-1])
            dpdV = (pres[:,1:]-pres[:,:-1])/\
                    (Vol_rho[:,1:]-Vol_rho[:,:-1])
            dpdr = (pres[:,1:]-pres[:,:-1])/\
                    (r_omp[:,1:]-r_omp[:,:-1])  
            dpdrt = (pres[:,1:]-pres[:,:-1])/\
                    (self.out["rhot_norm"][:,1:]-self.out["rhot_norm"][:,:-1])
            qprof = self.jet.partial_get('core_profiles',
                    'profiles_1d(:)/q').T 
            summary = self.jet.get('summary')
            B0 = self.jet.partial_get('core_profiles',
                    'vacuum_toroidal_field/b0(:)').T
            R0 = summary.global_quantities.r0.value
            mu0 = 4*np.pi*1.e-7
            eps = (r_omp-R0)/R0
            B0_1 = np.repeat(np.expand_dims(B0,axis=1),
                        np.shape(dpdrp[-1,:]),axis=1)
            alpha_ballooning = dpdrp* (-2.*mu0*(qprof[:,:-1]**2.0) /\
                           (eps[:,:-1]*B0_1**2.0))
            alpha_cyl = dpdr* (-2.*mu0*R0*(qprof[:,:-1]**2.0) /\
                           (B0_1**2.0))
            alpha_miller = (-2.*dVdchi/(2.*np.pi)**2.0) *\
                            np.sqrt(Vol_rho[:,1:]/(2.*(np.pi**2.0)*R0))*\
                            mu0 * dpdchi
            alpha_mishka =\
            (1/2.*mu0*r_omp[:,1:]**2.0)*(-4.* ((qprof[:,:-1]**2.0)/(eps[:,1:]*B0_1**2.0))*\
                        np.sqrt(Vol_rho[:,:-1]) * dpdV)

            #alpha jetto
            #jetto/alfcalc.f
            #ALFVAL(J) = P8*1.E-7 * (RMAEQ2(J)-RMJT)**2
            #* ABS( (GRDPE(J)+GRDPI(J))/GRDPSI(J)/BPAEQ2(J) )/ ANORM
            B0_2 = np.ones_like(r_omp)*B0[-1]
            B_theta = r_omp/(R0+r_omp)*(B0_2/qprof)

            alpha_jetto = 0.5* mu0 * (r_omp[:,:-1]**2.0) *\
                        np.abs(dpdchi * 1/B_theta[:,:-1])

            self.out['alpha_ballooning'] = alpha_ballooning
            self.out["alpha_jetto"] = alpha_jetto
            #Maximum critical pressure gradients
            self.out["alpha_max_ballooning_edge"] =\
            np.squeeze(np.max(self.out["alpha_ballooning"][:,-100:], axis=1))
            self.out["alpha_max_jetto_edge"] =\
                                    np.max(alpha_jetto[:,-100:], axis=1)
            self.out["alpha_max_mishka_edge"] = np.max(alpha_mishka[:,-100:], axis=1)

            #plt.figure()
            #plt.plot(r_omp[-1,1:], alpha_ballooning[-1,:], label="alpha_ballooning")
            #plt.plot(r_omp[-1,1:], alpha_cyl[-1,:], c="red", label="alpha cyl")
            #plt.plot(r_omp[-1,1:], alpha_miller[-1,:], c="brown", label="alpha miller")
            #plt.plot(r_omp[-1,1:], alpha_jetto[-1,:], c="green", label="alpha jetto")
            #plt.plot(r_omp[-1,1:], alpha_mishka[-1,:], c="orange", label="alpha mishka")
            #plt.legend()
            #plt.show()

            #Greenwald fraction
            #Should be included in Summary IDS, but it's not :)
            r_omp = self.jet.partial_get('equilibrium',
                        'time_slice(:)/profiles_1d/r_outboard').T
            Ip = self.jet.partial_get('equilibrium',
                        'time_slice(:)/global_quantities/ip').T
            r_minor = self.jet.partial_get('equilibrium',
                        'time_slice(:)/boundary/minor_radius').T
            ne_lavg = summary.line_average.n_e.value
            surf = np.pi * r_minor**2.0
            nGw = np.abs((Ip/1.e6)/surf)
            #[%]
            self.out["fGw"] = np.abs(ne_lavg/(1.e20*nGw))*100

            #Fusion Q
            self.out["Paux"] = (self.out["Pnbi_tot"] + self.out["Pec_tot"])
            self.out["Qfus"] = self.out["Palf"]*5/(self.out["Paux"])

            #Martin L-H transition power scaling
            self.out["Plht"] = 0.0488 * 1e6 * ((self.out["ne_lavg"]/1e20)**0.72) *\
                               (np.abs(self.out["Btor"])**0.8) * (self.out["Sur_t"]**0.94)

        #Wth
        drho = self.out["rho"][:,1:] - self.out["rho"][:,:-1]
        array = np.zeros(len(self.out["time"]))
        drho = np.hstack((np.expand_dims(array.T, axis=1), drho))
        #The ETB is especified at 8cm width. Interpolate the rho
        #value so I know where the pedestal is. Since jetto.jsp
        #does not output the minor radius at Z=Zaxis, interpolate
        #from the major radius instead as an approximation
        rhotn_etb = np.interp(np.array([np.max(self.out['R_omp'][-1,:])-0.08]),
                              self.out['R_omp'][-1,:], self.out['rhot_norm'][-1,:])
        idx_etb = np.argmin((self.out["rhot_norm"][-1,:] - rhotn_etb)**2.0)

        self.out["Wth_ped"] = 3/2. * \
        np.sum(((self.out["ne"]*self.out["Te"] + self.out["niH"]*self.out["Ti"] +\
                 self.out["niD"]*self.out["Ti"]+ self.out["niT"]*self.out["Ti"]) *\
                 self.out["dVdrho"]*drho)[:,idx_etb:], axis=1)
        #Convert to MJ
        self.out["Wth_ped"] *= (1.380649e-23 / 8.617333262e-5) / 1.e6

        self.out["Wth_cal"] = 3/2. * \
        np.sum(((self.out["ne"]*self.out["Te"] + self.out["niH"]*self.out["Ti"] +\
                 self.out["niD"]*self.out["Ti"]+ self.out["niT"]*self.out["Ti"]) *\
                 self.out["dVdrho"]*drho), axis=1)
        #Convert to MJ
        self.out["Wth_cal"] *= (1.380649e-23 / 8.617333262e-5) / 1.e6

        #Saarelma pedestal scaling
        #T_(e,ped,top)^target = 4.37e3 δ^1.69 Bgeo^0.41 Ip^1.44 
        #                       n_(e,ped,top)^(−0.6) Rgeo^(−2.1)
        #delta = (2Rgeo - Rtop - Rbottom)/2a
        Teped_saarelma = 4.37e3 * (self.out["delta_trian"]**1.69) *\
        (np.abs(self.out["Btor_geo"])**0.41) * (np.abs(self.out["Ip"])**1.44) *\
        (self.out["neped"]**(-0.6)) * (self.out["Rgeo"]**(-2.1))
        self.out["Teped_saarelma"] = Teped_saarelma

        return


    def _read_edge2d(self):
        """ 
        Reads EDGE2D TRAN output files

        Parameters
        ----------

        Output
        ----------

        Notes
        ----------
         JINTRAC Wiki EPROC page
         https://users.euro-fusion.org/pages/data-cmg/
         wiki/EPROC_Python_module.html

         Note: Using EPROC requires preloading JINTRAC
         modules, i.e.:
         module use #HOME/jintrac/$JINVER/modules
         module load jintrac
         This will automatically load compatible IMAS,
         Python, IPython and Viz libraries.

         Available rows to read (from row.py):
         xx = Absolute row number.
         OT = Outer target
         IT = Inner Target
         IMP = Inner mid-plane.
         OMP = Outer mid-plane.

         Some EPROC Nomenclature
         Every output is a Struct, you can see what is
         inside the structure with the command dir(Struct)
         To access one of the quantities just do quant.field
          ep.row - Will read along a row
          ep.ring - Will read along a ring
           - To read along a ring use ep.ring(tran, quantity, 'SX')
             where 'X' is the ring index.
          ep.data - Will fetch particular data
          ep.volint - Will compute vol. integral btw. 2 rings
          OT - Will read along Outer target
          IT - Will read along Inner target
          OMP - Will read along Outer Midplane
          IMP - Will read along Inner Midplane
        """

        #EPROC is used to read EDGE2D data. EPROC lives in the JINTRAC
        #repo. The user needs to add EPROC to the PYTHONPATH to be able
        #to import the module successfully. Alternatively, the user can
        #preload a JINTRAC version. However, we make EPROC optional in
        #case a JINTRAC installation does not exist.
        try:
            import eproc as ep
        except ImportError:
            print(' - EPROC Module could not be loaded.'+\
           ' EDGE2D will not be read!')

        nt = 0
        #Use the tran file generated by JINTRAC
        tran_file = self.jetto_path + "/tran"
        varnames = dir(ep.names(tran_file))
        nt = ep.data(tran_file,'TVEC').nPts
        #If tran file does not exist, look in the
        #directory for the last tranXX file.
        if nt==0:
            filelist = os.listdir(self.jetto_path)
            tranfiles = [i for i in filelist if "tran" in i and len(i) < 8]
            numbers = [int(i.replace("tran", "")) for i in tranfiles]
            maxnum = np.max(numbers)
            #TRAN files with number < 10 are named tran+0+num,
            #i.e. tran01, tran02, etc.
            if maxnum < 10:
                str_maxnum = "0" + str(maxnum)
            else:
                str_maxnum = str(maxnum)
            tran_file = self.jetto_path + "/tran" + str_maxnum

            #From the JINTRAC wiki. Arguments to this function.
            #prof = 1 will display profile names.
            #time = 1 will display time traces names.
            #flux = 1 will display Nimbus flux.
            #geom = 1 will display Geometry data.
            #sort = 1 will alphabetically sort signal names.
            varnames = ep.names(tran_file)

        #################################
        #Retrieve time trace signal names
        #################################
        varnames2 = ep.getnames(tran_file, 2).names
        descriptions2 = ep.getnames(tran_file, 2).description

        #Time base is in [ms]
        nt = ep.data(tran_file,'TVEC').nPts
        self.out["time_e2d"] = ep.data(tran_file,'TVEC').data[:nt]/1.e3

        #Maximum power density at the targets [W/m2] -> [MW/m2]
        self.out["Qmax_it"] = ep.data(tran_file,'QMAXIT').data[:nt]/1.e6
        self.out["Qmax_ot"] = ep.data(tran_file,'QMAXOT').data[:nt]/1.e6

        #Effective sputtering factors [Ne, W]
        self.out["Yeff_Ne"] = ep.data(tran_file,'YLDT_1').data[:nt]
        self.out["Yeff_W"] = ep.data(tran_file,'YLDT_2').data[:nt]

        #SOL gas puff - [ions/s as far as I can see]
        #EXTRA NEUTRAL FLUX
        self.out["Stot_main"] = ep.data(tran_file,'HEXTRA').data[:nt]
        #NE- EXTRA NEUTRAL IMPURITIES 
        self.out["Spuff_Ne_tot"] = ep.data(tran_file,'ZEXTRT_1').data[:nt]
        #W - EXTRA NEUTRAL IMPURITIES
        self.out["Spuff_W_tot"] = ep.data(tran_file,'ZEXTRT_2').data[:nt]

        #[eV]
        # These temperatures are at x=0 in the plate
        # (I verified it myself comparing against (TEVE, OT)
        # at Te_ot.xData = 0)
        Te_ot_t = ep.time(tran_file, 'TESOT')
        self.out["Te_ot_t"] = Te_ot_t.yData
        Ti_ot_t = ep.time(tran_file, 'TISOT')
        self.out["Ti_ot_t"] = Ti_ot_t.yData
        Te_it_t = ep.time(tran_file, 'TESIT')
        self.out["Te_it_t"] = Te_it_t.yData
        Ti_it_t = ep.time(tran_file, 'TISIT')
        self.out["Ti_it_t"] = Ti_it_t.yData

        #Electron Temperature [eV]
        Te_ot = ep.row(tran_file,'TEVE','OT')
        self.out['x_div_ot'] = np.array(Te_ot.xData)
        self.out['Te_ot'] = np.array(Te_ot.yData)
        Te_it = ep.row(tran_file,'TEVE','IT')
        self.out['x_div_it'] = np.array(Te_it.xData)
        self.out['Te_it'] = np.array(Te_it.yData)
        Te_im = ep.row(tran_file,'TEVE','IMP')
        self.out['x_im'] = np.array(Te_im.xData)
        self.out['Te_im'] = np.array(Te_im.yData)
        Te_om = ep.row(tran_file,'TEVE','OMP')
        self.out['x_om'] = np.array(Te_om.xData)
        self.out['Te_om'] = np.array(Te_om.yData)

        #Impurity densities
        n_imp1_im = ep.row(tran_file,'DENZ01', 'IMP')
        self.out["n_imp1_im"] = n_imp1_im.yData
        n_imp1_om = ep.row(tran_file,'DENZ01', 'OMP')
        self.out["n_imp1_om"] = n_imp1_om.yData
        n_imp1_it = ep.row(tran_file,'DENZ01', 'IT')
        self.out["n_imp1_it"] = n_imp1_it.yData
        n_imp1_ot = ep.row(tran_file,'DENZ01', 'OT')
        self.out["n_imp1_ot"] = n_imp1_ot.yData

        #########
        #Geometry
        #########
        #PFM
        self.out["Psi_e2d"] = ep.data(tran_file,'PSI').data
        #The mesh is composed of two main regions, the SOL and
        #the private flux region, each with different structures.
        #However, in the geometry data, we only get the {R,Z}
        #positions of all the points in the mesh. To build a 2D
        #grid array, it's easier to call RMESH and ZMESH using
        #ep.ring and pad with masked/NaN values the difference
        #in points between SOL and PFR.
        self.out['Rmesh'] = ep.data(tran_file,'RMESH').data
        self.out['Zmesh'] = ep.data(tran_file,'ZMESH').data
        self.out["npts_mesh"] = ep.data(tran_file,'RMESH').nPts
        mesh_geom = ep.geom(tran_file)
        #Mesh center
        self.out["R0_mesh"] = mesh_geom.r0
        self.out["Z0_mesh"] = mesh_geom.z0
        #Number of rings and rows
        self.out["nrings_mesh"] = nRings = mesh_geom.nRings
        self.out["nrows_mesh"] = nRows = mesh_geom.nRows

        #Mesh organized by rings
        npoints_sol = len(ep.ring(tran_file,'RMESH', 'S1').yData)
        Rmesh2D = np.zeros((nRings, npoints_sol))
        Zmesh2D = np.zeros((nRings, npoints_sol))
        Psi2D = np.zeros((nRings, npoints_sol))
        for i in range(0, nRings):
            Ri = np.array(ep.ring(tran_file,'RMESH', 'S'+str(i)).yData)
            Zi = np.array(ep.ring(tran_file,'ZMESH', 'S'+str(i)).yData)
            Psi_i = np.array(ep.ring(tran_file,'PSI', 'S'+str(i)).yData)
            if len(Ri) < npoints_sol:
                npoints_pfr = len(Ri)
                Rmesh2D[i,:npoints_pfr] = Ri
                Rmesh2D[i,npoints_pfr:] = np.nan
                Zmesh2D[i,:npoints_pfr] = Zi
                Zmesh2D[i,npoints_pfr:] = np.nan
                Psi2D[i,:npoints_pfr] = Psi_i
                Psi2D[i,npoints_pfr:] = np.nan
            else:
                Rmesh2D[i,:] = Ri
                Zmesh2D[i,:] = Zi
                Psi2D[i,:] = Psi_i

        self.out["Rmesh2D_rings"] = Rmesh2D
        self.out["Zmesh2D_rings"] = Zmesh2D
        self.out["Psi2D_rings"] = Psi2D

        #Mesh organized by rows
        npoints_sol = len(ep.row(tran_file,'RMESH', '0').yData)
        Rmesh2D = np.zeros((nRows, npoints_sol))
        Zmesh2D = np.zeros((nRows, npoints_sol))
        Psi2D = np.zeros((nRows, npoints_sol))
        for i in range(0, nRows):
            Ri = np.array(ep.row(tran_file,'RMESH', str(i)).yData)
            Zi = np.array(ep.row(tran_file,'ZMESH', str(i)).yData)
            Psi_i = np.array(ep.row(tran_file,'PSI', str(i)).yData)
            if len(Ri) < npoints_sol:
                npoints_pfr = len(Ri)
                Rmesh2D[i,:npoints_pfr] = Ri
                Rmesh2D[i,npoints_pfr:] = np.nan
                Zmesh2D[i,:npoints_pfr] = Zi
                Zmesh2D[i,npoints_pfr:] = np.nan
                Psi2D[i,:npoints_pfr] = Psi_i
                Psi2D[i,npoints_pfr:] = np.nan
            else:
                Rmesh2D[i,:] = Ri
                Zmesh2D[i,:] = Zi
                Psi2D[i,:] = Psi_i

        self.out["Rmesh2D_rows"] = Rmesh2D
        self.out["Zmesh2D_rows"] = Zmesh2D
        self.out["Psi2D_rows"] = Psi2D

#        #Reading EDGE2D tran file
#        #Names from compare_e2d.py in jintrac's python folder  
#        names =\
#        ["da", "den", "denel", "denptot", "denztot", "dha", "dm",
#         "dperp", "jtargi", "pmach", "prehyd", "pretot", "soun",
#         "souz", "sqehrad", "sqezrad", "tev", "teve", "totpden",
#         "vpi", "vpinch", "vro", "vtri", "zeff"]
#
#        nitems = len(names)
#        data = []
#
#        for item in range(nitems):
#            try:
#                #npts = eproc.data(file1, names[item]).nPts
#                npts = len(tran1.tran[names[item].upper()]['data'])
#                if npts != 0:
#                    #data1.append((eproc.data(file1, names[item])).data
#                    data1.append(tran1.tran[names[item].upper()]['data'])
#                    #data2.append((eproc.data(file2, names[item])).data)
#                    data2.append(tran2.tran[names[item].upper()]['data'])
#                #Deals with empty / non-existent dataset
#                else:
#                    data1.append([])
#                    data2.append([])
#                    
#            except KeyError:
#                if verbosity > 1:
#                    print(names[item].upper(),
#                          "missing from tran file")
#                data1.append([])
#                data2.append([])

        return
    
    def _read_eirene(self):
        """
        Reads EIRINE files

        Parameters
        ----------

        Output
        ----------

        Notes
        ----------
        I implement this routine so far to check the EIRINE grid.
        Inspired by the routines in plote2deir by Derek Harting.
        """

        #Get EIRINE grid points stored in eirene.npco_char
        file = open(self.jetto_path + "/eirene.npco_char", mode="r")
        lines = file.readlines()
        file.close()

        self.out["npts_mesh_eirene"] = npts_mesh_eirene = int(lines[0])
        Rmesh_eirene = np.array([])
        Zmesh_eirene = np.array([])
        for ii in range (1, len(lines)):
            linetmp = lines[ii].replace('\n','').split(' ')
            while '' in linetmp:
                linetmp.remove('')
            Rmesh_eirene = np.hstack((Rmesh_eirene, float(linetmp[1])/100))
            Zmesh_eirene = np.hstack((Zmesh_eirene, float(linetmp[2])/100))

        self.out["Rmesh_eirene"] = Rmesh_eirene
        self.out["Zmesh_eirene"] = Zmesh_eirene

        #Get the indeces that compose every triangle in eirene.elemente
        file = open(self.jetto_path + "/eirene.elemente", mode="r")
        lines = file.readlines()
        file.close()
        self.out["nelements_eirene"] = nelements_eirene = int(lines[0])
        Triang_idxs = np.zeros([nelements_eirene, 3])
        for ii in range (1, len(lines)):
            linetmp = lines[ii].replace('\n','').split(' ')
            while '' in linetmp:
                linetmp.remove('')
            Triang_idxs[ii-1,:] = np.array([int(linetmp[1])-1,
                                  int(linetmp[2])-1, int(linetmp[3])-1])

        self.out["Rmesh_eirene"] = Rmesh_eirene
        self.out["Zmesh_eirene"] = Zmesh_eirene
        self.out["Triang_idxs"] = Triang_idxs

        return


    def plot_run(self, savefig=False):
        """
        Plots output parameters and profiles of interest from
        a JETTO/Coconut run.

        Parameters
        ----------
        savefig : Bool
            Whether to save the figures

        Notes
        ----------

        """

        #Make sure output quantities have been read into
        #memory
        if self.out_memory is False:
            if self.nshot is None:
                self._out_memory_standard()
            else:
                self._out_memory_imas()

        #General plot parameters
        plt.rcParams.update({'font.size': 12,
        'axes.xmargin':0, 'axes.ymargin':0.02})
        legend_fontsize = 10

        #List to append figures for GUI
        figures = []

        #Generic helper that attaches time_data + update_time to an axis
        def attach_time_dependent(ax, xt_list, yt_list, labels, time_array,
                                  linestyles, colors, fig=None, legend=True):

            """
            Multiple lines per axis, x and y vary with time.
            Fixed y-axis, dynamic legend showing timestamp.
            Updates figure suptitle with current time if fig is provided.

            Parameters
            ----------
            ax : matplotlib axis
            xt_list : list of 2D arrays (time x radial points)
            yt_list : list of 2D arrays (time x radial points)
            labels : list of strings
            time_array : array of time stamps
            colors : list of colors for each line (mandatory)
            fig : matplotlib figure (optional)
            """

            n_lines = len(labels)
            n_time_steps = len(time_array)

            #Compute global min/max for y-axis.
            #Exclude first time point as often values
            #can be very large.
            if len(yt_list[0][:,0]) > 1:
                y_min = 0.98*min([np.min(y[1:,:]) for y in yt_list])
                y_max = 1.02*max([np.max(y[1:,:]) for y in yt_list])
            else:
                y_min = 0.98*min([np.min(y) for y in yt_list])
                y_max = 1.02*max([np.max(y) for y in yt_list])
            ax.set_ylim(y_min, y_max)

            #Initialize lines at first frame
            lines = []
            for i, label in enumerate(labels):
                line, = ax.plot(xt_list[i][0,:], yt_list[i][0,:],
                                label=label, ls=linestyles[i], c=colors[i])
                lines.append(line)

            if legend:
                legend = ax.legend()

            def update_time(frame_idx, legend=legend):
                idx = min(frame_idx, n_time_steps - 1)
                current_time = time_array[idx]

                for line, x_arr, y_arr in zip(lines, xt_list, yt_list):
                    line.set_data(x_arr[idx, :], y_arr[idx, :])

                #Update legend labels with timestamp
                if legend: 
                    for leg_line, label in zip(legend.get_lines(), labels):
                        leg_line.set_label(f"{label} (t={current_time:.3f})")
                    ax.legend()  #Redraw legend

                #Update figure suptitle with time
                if fig and fig._suptitle:
                    #Keep the original title (before '|') stored separately
                    if not hasattr(fig, "_original_suptitle"):
                        fig._original_suptitle = fig._suptitle.get_text()
                    fig._suptitle.set_text(f"{fig._original_suptitle} | t = {current_time:.3f}")
                    fig.canvas.draw_idle()

            ax.time_data = list(range(n_time_steps))
            ax.update_time = update_time

            # Initialize at last frame
            update_time(n_time_steps - 1)


        def attach_time_dependent_contour(ax, X, Y, Z, time_array,
            levels=None, cmap="viridis", filled=True, fig=None,
            cb_size="10%", cb_pad=0.04, vmin=None, vmax=None):
            """
            Attach a time-dependent contour plot to a given axis, with
            a colorbar whose height matches the axis.

            Supports 2D or 3D arrays for X, Y, and Z. If 3D, the last
            dimension is interpreted as time. Can create filled (`contourf`)
            or line-only (`contour`) contours. Automatically attaches an
            `update_time` method to the axis for GUI sliders.

            Parameters
            ----------
            ax : matplotlib.axes.Axes
                Axis where the contour will be drawn.
            X, Y : array-like, shape (nx, ny) or (nx, ny, nt)
                Coordinate arrays for the contour. Can be 2D (static)
                or 3D (time-dependent).
            Z : array-like, shape (nx, ny, nt)
                Data array for the contour. If 3D, the last dimension
                is interpreted as time.
            time_array : array-like, shape (nt,)
                Array of time points corresponding to the third dimension
                of Z (and optionally X and Y).
            levels : int or array-like, optional
                Number of contour levels or explicit level values.
            cmap : str or Colormap, default 'viridis'
                Colormap for the contour.
            filled : bool, default True
                If True, creates a filled contour plot (`contourf`),
                otherwise line contours (`contour`).
            fig : matplotlib.figure.Figure, optional
                Figure containing the axis. Used to update the suptitle
                with the current time. If None, `ax.figure` is used.
            cb_size : str or float, default '10%'
                Width of the colorbar relative to the axis.
            cb_pad : float, default 0.04
                Padding between axis and colorbar.
            vmin, vmax : float, optional
                Global minimum and maximum values for contour color scaling.
                Defaults to min/max of Z.

            Returns
            -------
            contour : QuadContourSet
                The initial contour (or filled contour) object.
            cbar : matplotlib.colorbar.Colorbar
                The colorbar associated with the contour, with ticks
                rounded to 1 decimal and duplicates removed.

            Side Effects
            ------------
            Attaches the following attributes to `ax`:
                - ax.time_data : list of time indices (0..nt-1)
                - ax.update_time(frame_idx) : callable to update the
                contour for a given frame index. Can be used in GUI sliders.

            Notes
            -----
            - Automatically ensures that the time dimension of Z matches
            `time_array`. If Z has time as the first or second dimension,
            it is moved to the last dimension.
            - The initial contour is drawn at the last time frame.
            - Colorbar tick labels are rounded to 1 decimal place,
            and repeated values are removed.
            - If `fig` is provided and has a suptitle, it will update
            with the current time.
            """

            if fig is None:
                fig = ax.figure

            #Ensure shape: (nx, ny, nt)
            nt = Z.shape[2]
            if nt != len(time_array):
                # try to move time axis to last
                if Z.shape[0] == len(time_array):
                    Z = np.moveaxis(Z, 0, -1)
                elif Z.shape[1] == len(time_array):
                    Z = np.moveaxis(Z, 1, -1)
                else:
                    raise ValueError("Time dimension of Z doesn't match time_array length.")

            #Determine vmin/vmax if not supplied (global across time)
            if vmin is None:
                vmin = np.nanmin(Z)
            if vmax is None:
                vmax = np.nanmax(Z)
            #Create global levels (instead of integer levels)
            if isinstance(levels, int):
                levels = np.linspace(vmin, vmax, levels)

            #Initial frame (use last for consistency)
            idx0 = nt - 1
            X0 = X[:, :, idx0] if X.ndim == 3 else X
            Y0 = Y[:, :, idx0] if Y.ndim == 3 else Y
            Z0 = Z[:, :, idx0]

            #Create initial contour (keep reference)
            if filled:
                contour = ax.contourf(X0, Y0, Z0, levels=levels,
                                      cmap=cmap, vmin=vmin, vmax=vmax)
            else:
                contour = ax.contour(X0, Y0, Z0, levels=levels,
                                     cmap=cmap, vmin=vmin, vmax=vmax)

            #Create a colorbar axes sized to this axis using make_axes_locatable
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size=cb_size, pad=cb_pad)
            cbar = fig.colorbar(contour, cax=cax)
            #Round tick labels to one decimal place - scientific notation
            cbar.formatter = mticker.FormatStrFormatter('%.1f')
            #Optionally, tweak tick fontsize etc:
            cbar.update_ticks()
            #Remove repeated tick labels
            ticks = cbar.get_ticks()
            tick_labels = np.round(ticks, 1)  # round to 1 decimal
            #Keep only unique values in order
            _, unique_indices = np.unique(tick_labels, return_index=True)
            cbar.set_ticks(ticks[unique_indices])
            cbar.update_ticks()

            #Updater: replace collections and update colorbar mappable
            def update_time(frame_idx):
                nonlocal contour
                idx = min(frame_idx, nt - 1)
                curr_t = time_array[idx]
                X_t = X[:, :, idx] if X.ndim == 3 else X
                Y_t = Y[:, :, idx] if Y.ndim == 3 else Y
                Z_t = Z[:, :, idx]

                #Remove old contour collections
                try:
                    for coll in contour.collections:
                        coll.remove()
                except Exception:
                    pass

                #Draw new contour in same axis
                if filled:
                    new_contour = ax.contourf(X_t, Y_t, Z_t, levels=levels,
                                  cmap=cmap, vmin=vmin, vmax=vmax)
                else:
                    new_contour = ax.contour(X_t, Y_t, Z_t, levels=levels,
                                  cmap=cmap, vmin=vmin, vmax=vmax)

                #Replace reference
                contour = new_contour

                #Update the colorbar to reference the new mappable
                #and keep its axis size
                cbar.mappable = contour
                cbar.update_normal(contour)

                #Update suptitle if requested
                if fig and fig._suptitle:
                    if not hasattr(fig, "_original_suptitle"):
                        fig._original_suptitle = fig._suptitle.get_text()
                    fig._suptitle.set_text(f"{fig._original_suptitle} | t = {curr_t:.3f}")

                #Redraw
                fig.canvas.draw_idle()

            #Expose to GUI
            ax.time_data = list(range(nt))
            ax.update_time = update_time

            #Initialize to last frame
            update_time(nt - 1)

            return contour, cbar

        ####################
        #JSP file - Profiles
        #[time, rho]
        ####################
        if self.jspfile:
            fig, ax = plt.subplots(figsize=(12,7), nrows=3, ncols=3,
                                sharex=True)
            if self.jstfile:
                fig.suptitle("JSP file")

            time_data = fig.time_data = self.out["time"]
            x_data = [self.out["rhot_norm"], self.out["rhot_norm"],
                      self.out["rhot_norm"]]
            y_data = [self.out["ne"], self.out["niD"], self.out["niT"]]
            labels = [r"$n_e$", r"$n_{D}$", r"$n_{T}$"]
            linestyles = ["-", "-", "-"]
            colors = ["blue", "red", "orange"]
            attach_time_dependent(ax[0][0], x_data, y_data, labels, time_data,
                                  linestyles, colors, fig=fig)

            axy = ax[0][0].twinx()
            #Particle sources [part/m3]
            axy.plot(self.out["rhot_norm"][-1,:], self.out["S0"][-1,:],
                    c='#00ff3f')
            ##NBI spec 1
            #axy.plot(self.out["rhotnbi"][-1,:], self.out["SBD1"][-1,:],
            #         c="k", label=r"$S_{NBI, spec. 1}$")
            ##NBI spec 2
            #axy.plot(self.out["rhotnbi"][-1,:], self.out["SBD2"][-1,:],
            #         c="k", ls="--", label=r"$S_{NBI, spec. 2}$")
            #Pellets
            axy.plot(self.out["rhot_Xs"][-1,:], self.out["S1_pel"][-1,:],
                    c="green", ls="-")
            axy.plot(self.out["rhot_Xs"][-1,:], self.out["S2_pel"][-1,:],
                    c="green", ls="--")       
            
            legend_elements =\
            [Line2D([0], [0], c='blue', label=r"$n_e$"),
            Line2D([0], [0], c='red', label =r"$n_{D}$"), 
            Line2D([0], [0], c='orange', label=r"$n_{T}$"),
            Line2D([0], [0], c='#00ff3f', label=r"$S_{frantic}$"), 
            Line2D([0], [0], c='green', label=r"$S_{pel, \, 1}$"), 
            Line2D([0], [0], ls="--", c='green', label=r"$S_{pel, \, 2}$")]
            ax[0][0].legend(loc="best", fontsize=legend_fontsize,
                            ncol=2, handles=legend_elements)
            axy.set_ylabel(r"$S_{neutral} \, [1/m^3]$")

            #Particle diffusivities
            #Particle diffusion spec. 1 [m2/s]
            #Particle diffusion spec. 2 [m2/s]
            #NCLASS ion diffusivities
            #TCI - 1st species particle diffusivity
            #TCI - 2nd species particle diffusivity
            time_data = fig.time_data = self.out["time"]
            x_data = [self.out["rhot_Xs"], self.out["rhot_Xs"],
                    self.out["rhot_Xs"], self.out["rhot_Xs"],
                    self.out["rhot_Xs"], self.out["rhot_Xs"]]
            y_data = [self.out["D1_eff"], self.out["D2_eff"],
                    self.out["D1_n"], self.out["D2_n"],
                    self.out["D1_t"], self.out["D2_t"]]
            labels = [r"$\mathrm{D_{eff}^{1}}$", r"$\mathrm{D_{eff}^{2}}$",
                    r"$\mathrm{D_{1}^{Nclass}}$", r"$\mathrm{D_{2}^{Nclass}}$",
                    r"$\mathrm{D_{i}^{TCI-1}}$", r"$\mathrm{D_{part}^{TCI-2}}$"]
            linestyles = ["-", "-", "-.", "-.", ":", ":"]
            colors = ["red", "orange", "red", "orange", "red", "orange"]
            attach_time_dependent(ax[1][0], x_data, y_data, labels, time_data,
                                linestyles, colors, fig=fig)
            ax[1][0].legend(loc="upper left", fontsize=legend_fontsize,
                            ncol=3, columnspacing=0.8)

            #The ETB is especified at 8cm width. Interpolate the rho
            #value so I know where the pedestal is. Since jetto.jsp
            #does not output the minor radius at Z=Zaxis, interpolate
            #from the major radius instead as an approximation
            rhotn_etb = np.interp(np.array([np.max(self.out['R_omp'][-1,:])-0.08]),
                                self.out['R_omp'][-1,:], self.out['rhot_norm'][-1,:])
            idx_etb = np.argmin((self.out["rhot_norm"][-1,:] - rhotn_etb)**2.0)

            #Te
            x_data = [self.out["rhot_norm"]]
            y_data = [self.out["Te"]/1.e3]
            labels = [r"$T_e$",]
            linestyles = ["-"]
            colors = ["blue"]
            attach_time_dependent(ax[0][1], x_data, y_data, labels, time_data,
                                  linestyles, colors)
            ax[0][1].plot(self.out["rhot_norm"][0,:],
                        self.out["Te"][0,:]/1.e3,
                        ls="--", c="blue", alpha=0.5)

            if (self.backend=="std") and self.jspfile:
                time_data = fig.time_data = self.out["time"]
                x_data = [self.out["rhot_norm"][:,:-1], self.out["rhot_norm"][:,:-1]]
                #NCLASS first and second ion pinch velocities          
                y_data = [self.out["v1_n"], self.out["v2_n"]]
                labels = [r"$v_{i, 1}^{neo}$", r"$v_{i, 2}^{neo}$"]
                linestyles = ["-", "-"]
                colors = ["orange", "blue"]
                attach_time_dependent(ax[2][0], x_data, y_data, labels, time_data,
                                      linestyles, colors)

                #TCI first and second ion pinch velocities
                ax[2][0].plot(self.out["rhot_norm"][-1,:-1],
                            self.out["v1_t"][-1,:],
                            c="red", label=r"$v_{i, 1}^{turb}$")
                ax[2][0].plot(self.out["rhot_norm"][-1,:-1],
                            self.out["v2_t"][-1,:],
                            c="cyan", label=r"$v_{i, 2}^{turb}$")
                #Ware pinch
                ax[2][0].plot(self.out["rhot_norm"][-1,:-1],
                            self.out["v_ware"][-1,:],
                            c="k", label=r"$v_{ware}^{neo}$")
            else:
                main_ion_list = ["H","D","T"]
                colors_neo = ["orange", "cyan", "brown"]
                colors_turb = ["red", "blue", "green"]
                j=0
                for i in main_ion_list:
                    try:
                        ax[2][0].plot(self.out["rhot_norm"][-1,:],
                                    self.out["vn_"+i][-1,:],
                                    c=colors_neo[j],
                                    label=r"$v_{$"+i+r"$}^{Nclass}$")
                        ax[2][0].plot(self.out["rhot_norm"][-1,:],
                                    self.out["vt_"+i][-1,:],
                                    c=colors_turb[j],
                                    label=r"$v_{$"+i+r"$}^{turb}$")
                        ax[0][1].plot(self.out["rhot_norm"][0,:],
                                    self.out["Ti"+i][0,:]/1.e3,
                                    ls="--", c="orange")
                        ax[0][1].plot(self.out["rhot_norm"][-1,:],
                                    self.out["Ti"+i][-1,:]/1.e3,
                                    label="Ti", c="orange")
                        j+=1
                    except:
                        pass

            if (self.backend=="std") and self.jspfile:
                #Qi, Qe [W]
                time_data = fig.time_data = self.out["time"]
                x_data = [self.out["rhot_Xs"], self.out["rhot_Xs"]]
                y_data = [self.out["Qi"]/1.e6, self.out["Qe"]/1.e6]
                labels = [r"$Q_{i}$", r"$Q_{e}$"]
                linestyles = ["-", "-"]
                colors = ["red", "blue"]
                attach_time_dependent(ax[0][2], x_data, y_data, labels, time_data,
                                      linestyles, colors, fig=fig)

            #chi_e, chi_i [m2/s]
            time_data = fig.time_data = self.out["time"]
            x_data = [self.out["rhot_Xs"], self.out["rhot_Xs"]]
            y_data = [self.out["Xe"], self.out["Xi"]]
            labels = [r"$\chi_e$", r"$\chi_i$"]
            linestyles = ["-", "-"]
            colors = ["blue", "orange"]
            attach_time_dependent(ax[1][1], x_data, y_data, labels, time_data,
                                  linestyles, colors, fig=fig)

            #Rotation profiles
            time_data = fig.time_data = self.out["time"]
            x_data = [self.out["rhot_norm"], self.out["rhot_norm"]]
            y_data = [self.out["vtor"], self.out["vpol"]]
            labels = [r"$v^{\phi}$", r"$v^{\theta}$"]
            linestyles = ["-", "-"]
            colors = ["blue", "orange"]
            attach_time_dependent(ax[1][2], x_data, y_data, labels, time_data,
                                  linestyles, colors, fig=fig)
            ax[1][2].set_ylabel("v [m/s]")

            #Add all the heat diffusivity components
            #From the JINTRAC Wiki, part written by Florian
            #JSP/XI is the sum of all XIj.
            #JSP/XI1: neoclassical Xi
            #JSP/XI2: Bohm part of Xi from Bohm/gyroBohm model
            #JSP/XI3: gyroBohm part of Xi from Bohm/gyroBohm model
            #JSP/XI4: Xi from NeoAlcator model
            #JSP/XI5: Xi from CDBM model
            #JSP/XI6: Xi from TCI
            #if verbose:
            #    ax[1][1].plot(self.jet["XRHO"][-1,:-1],
            #                  self.jet["XI1"][-1,:], c="orange",
            #                  ls="--", label=r"$\chi_{i, neo}$")
            #    ax[1][1].plot(self.jet["XRHO"][-1,:-1],
            #                  self.jet["XI3"][-1,:], c="orange",
            #                  ls="-.", label=r"$\chi_{i, GB}$")
            #    ax[1][1].plot(self.jet["XRHO"][-1,:-1],
            #                  self.jet["XI6"][-1,:], c="orange",
            #                  ls="-.", label=r"$\chi_{i, TCI}$")

            #Total current density [A/m2]
            #Bootstrap current density [A/m2]
            time_data = fig.time_data = self.out["time"]
            x_data = [self.out["rhot_norm"], self.out["rhot_norm"]]
            y_data = [self.out["jtor"]/1.e3, self.out["jpar_Bs"]/1.e3]
            labels = [r"$j_{total}$", r"$j_{BS}$"]
            linestyles = ["-", "-"]
            colors = ["k", "green"]

            #Not yet implemented for IMAS Backend
            if self.backend=="std":
                #ECCD current density [A/m2]
                #NBI current density [A/m2]
                #ICRF current density [A/m2]
                x_data.extend([self.out["rhot_norm"], self.out["rhot_norm"],
                            self.out["rhot_norm"]])
                y_data.extend([self.jet["JZEC"]/1.e3, self.jet["JZNB"]/1.e3,
                            self.jet["JZRF"]/1.e3])
                labels.extend([r"$j_{ECCD}$", r"$j_{NBI}$", r"$j_{ICRF}$"])
                linestyles.extend(["-", "-", "-"])
                colors.extend(["blue", "orange", "red"])

            attach_time_dependent(ax[2][1], x_data, y_data, labels, time_data,
                                  linestyles, colors, fig=fig)

            #q-profile
            time_data = fig.time_data = self.out["time"]
            x_data = [self.out["rhot_norm"]]
            y_data = [self.out["qprof"]]
            labels = [r"$q_{prof}$"]
            linestyles = ["-"]
            colors = ["k"]
            attach_time_dependent(ax[2][2], x_data, y_data, labels, time_data,
                                  linestyles, colors, fig=fig)

            ax[2][0].legend(fontsize=legend_fontsize)
            ax[0][1].legend(fontsize=legend_fontsize)
            ax[0][2].legend(fontsize=legend_fontsize)
            ax[0][0].set_ylabel(r"$\mathrm{n \, [m^{-3}]}$")
            ax[1][0].set_ylabel(r"$\mathrm{D \, [m^2/s]}$")
            ax[2][0].set_ylabel(r"$\mathrm{v_{pinch} \, [m/s]}$")
            ax[0][1].set_ylabel(r"$\mathrm{T \,\, [keV]}$")
            ax[0][2].set_ylabel(r"$\mathrm{Q_{\mu} \, [MW]}$")        
            ax[1][1].set_ylabel(r"$\mathrm{\chi \, [m^2/s]}$")
            ax[2][1].set_ylabel(r"$\mathrm{j \, [kA/m^2]}$")
            ax[2][2].set_ylabel(r"$\mathrm{q_{prof}}$")
            ax[1][1].legend(fontsize=legend_fontsize)
            ax[2][1].legend(fontsize=legend_fontsize)
            ax[2][0].set_xlabel(r"$\mathrm{\rho_{\phi}}$")
            ax[2][1].set_xlabel(r"$\mathrm{\rho_{\phi}}$")
            ax[2][2].set_xlabel(r"$\mathrm{\rho_{\phi}}$")
            fig.tight_layout()
            plt.subplots_adjust(top=0.92)
            figures.append(fig)

            if savefig:
                plt.savefig("profiles.png")

        #################################
        #Time traces
        #  - Kinetic profiles (jetto.jsp)
        #################################
        if self.jstfile:
            fig, ax = plt.subplots(figsize=(10,8), nrows=4, ncols=3,
                                sharex=True)
            fig.suptitle("JST file")
            
            ax[0][0].plot(np.squeeze(self.out["time"]),
                          self.out["Te"][:,0]/1.e3,
                          c="blue", marker="o",
                          label=r"$\mathrm{T_{e,0}}$")

            if self.backend=="std":
                ax[0][0].plot(np.squeeze(self.out["time"]),
                              self.out["Ti"][:,0]/1.e3,
                              c="red", marker="o",
                              label=r"$\mathrm{T_{i,0}}$")
            else:
                try:
                    ax[0][0].plot(np.squeeze(self.out["time"]),
                                  self.out["TiH"][:,0]/1.e3,
                                  c="red", marker="o",
                                  label=r"$\mathrm{T_{i,0}}$")
                except:
                    pass
                try:
                    ax[0][0].plot(np.squeeze(self.out["time"]),
                                  self.out["TiD"][:,0]/1.e3,
                                  c="red", marker="o",
                                  label=r"$\mathrm{T_{i,0}}$")
                except:
                    pass
                try:
                    ax[0][0].plot(np.squeeze(self.out["time"]),
                                  self.out["TiT"][:,0]/1.e3,
                                  c="red", marker="o",
                                  label=r"$\mathrm{T_{i,0}}$")
                except:
                    pass

            ax[0][0].set_ylabel(r"$\mathrm{T \,\, [keV]}$")
            ax[0][0].ticklabel_format(useOffset=False)
            ax[0][0].legend(fontsize=legend_fontsize)
                
            #Maximum difference between adjacent points
            #in the electron density profile
            ne_diff = np.max(self.out["ne"][:,1:]-\
                            self.out["ne"][:,:-1], axis=1)
            ax[0][1].plot(np.squeeze(self.out["time"]),
                        self.out["ne"][:,0],
                        c="blue", marker="o",
                        label=r"$\mathrm{n_{e,0} \, [keV]}$")
            ax[0][1].plot(np.squeeze(self.out["time"]),
                        self.out["niD"][:,0],
                        c="red", marker="o",
                        label=r"$\mathrm{n_{D,0} \, [keV]}$")
            ax[0][1].plot(np.squeeze(self.out["time"]),
                        self.out["niT"][:,0],
                        c="orange", marker="o",
                        label=r"$\mathrm{n_{T,0} \, [keV]}$")
            label=r"$\mathrm{max(n_{e, i+1} - n_{e, i})"+\
                  r"\, [m^{-3}]}$"
            ax[0][1].plot(np.squeeze(self.out["time"]),
                        ne_diff, c="k", marker="o", label=label)  
            ax[0][1].ticklabel_format(useOffset=False)
            ax[0][1].legend(fontsize=legend_fontsize)

            #q-profile
            ax[0][2].plot(self.out["time"], self.out["qprof"][:,0],
                          marker="o", c='k', label=r"$q_0$")
            ax[0][2].legend(fontsize=legend_fontsize)

            ##  - Powers (jetto.jst)
            #ax[1][0].plot(self.out["time_derived"], self.out["Plht"].T/1.e6,
            #            marker="o", ls="--", c="cyan", label=r"$P_{LH}$")
            #ax[1][0].plot(self.jet["TVEC1"], self.jet["PTOT"].T/1.e6,
            #              marker="o", c="k", label=r"$P_{tot}$")
            #Pnet includes dW/dt. As the thermal energy content
            #stabilizes, Pnet -> Ptot.
            #ax[1][0].plot(self.jet["TVEC1"], self.jet["PNET"].T/1.e6,
            #              marker ="o", c="red",
            #              label=r"$P_{net} (+dW/dt)$")
            ax[1][0].plot(self.out["time_derived"], self.out["Pec_tot"]/1.e6,
                          marker ="o", c="blue", label=r"$P_{ecrh}$")
            #ax[1][0].plot(self.jet["TVEC1"], self.jet["PRF"].T/1.e6,
            #              marker ="o", c="brown", label=r"$P_{ICRH}$")
            ax[1][0].plot(self.out["time_derived"], self.out["Pnbi_tot"].T/1.e6,
                          marker="o", c="green", label=r"$P_{NBI}$")
            ax[1][0].plot(self.out["time_derived"],
                          np.abs(self.out["Prad_tot"].T)/1.e6,
                          marker="o", c="k", ls="--", label=r"$|P_{rad}|$")
            ax[1][0].plot(self.out["time_derived"], self.out["Palf"]/1.e6,
                          marker="o", c="magenta",
                          label=r"$P_{\alpha}$")
            ax[1][0].plot(self.out["time_derived"], self.out["Poh_tot"]/1.e6,
                          marker="o", c="0.5", label=r"$P_{\Omega}$")
            #ax[1][0].set_ylim(0., 1.2*np.max(self.jet["PNET"].T/1.e6))
            ax[1][0].ticklabel_format(useOffset=False)
            ax[1][0].legend(ncol=3, fontsize=legend_fontsize)
            ax[1][0].set_ylabel("P [MW]")

            #Radiated power fraction
            ax[2][0].plot(self.out["time_derived"], self.out["frad"]*100,
                          marker="o", c="blue", lw=2)
            ax[2][0].set_ylabel(r"$f_{rad} \, [\%]$")
            ax[2][0].set_ylim(0,100)

            #  - Heat fluxes (jetto.jsp)
    #        try:
    #            ax[2][0].plot(np.squeeze(self.jet["TIME"]),
    #                          np.max(self.jet["PIFL"], axis=1).T/1.e6,
    #                          marker="o", c="red",
    #                          label=r"$Q_{i, max}$")
    #            ax[2][0].plot(np.squeeze(self.jet["TIME"]),
    #                          np.max(self.jet["PEFL"], axis=1).T/1.e6,
    #                          marker="o", c="blue",
    #                          label=r"$Q_{e, max}$")
    #            ax[2][0].set_ylabel(r"$\mathrm{Q_{\mu} \, [MW]}$")
    #            ax[2][0].ticklabel_format(useOffset=False)
    #            ax[2][0].legend()
    #        except:
    #            print("Cannot use .jsp file in <<time>> mode")

            #Edge energy fluxes (jetto.jst)
            #ax[2][0].plot(np.squeeze(self.jet["TVEC1"]),
            #              np.squeeze(self.jet["PFIO"]).T/1.e6,
            #              marker="o", c="red",
            #              label=r"$Q_{i,B}$")
            #ax[2][0].plot(np.squeeze(self.jet["TVEC1"]),
            #              np.squeeze(self.jet["PFEL"]).T/1.e6,
            #              marker="o", c="blue",
            #              label=r"$Q_{e,B}$")
            #ax[2][0].set_ylabel(r"$\mathrm{Q_{\mu, B} \, [MW]}$")
            #ax[2][0].ticklabel_format(useOffset=False)
            #ax[2][0].legend(fontsize=legend_fontsize)

            #  - Particle sources (jetto.jst)
            #ax[1][1].plot(np.squeeze(self.jet["TVEC1"]),
            #              np.squeeze(self.jet["SIN1"]),
            #              c="blue", marker ="o",
            #              label=r"$S_{puff, spec. 1}$")
            #ax[1][1].plot(np.squeeze(self.jet["TVEC1"]),
            #              np.squeeze(self.jet["SIN2"]),
            #              c="blue", ls="--",
            #              marker ="o", label=r"$S_{puff, spec. 2}$")
            #ax[1][1].plot(np.squeeze(self.jet["TVEC1"]),
            #              np.squeeze(self.jet["SPEL"]), c="k",
            #              marker ="o", label=r"$S_{pellet}$")
            #ax[1][1].ticklabel_format(useOffset=False)
            #ax[1][1].set_ylabel(r"$\mathrm{S  \, [part/s]}$")
            #ax[1][1].legend(fontsize=legend_fontsize)

            #Greenwald fraction
            ax[1][1].plot(self.out["time_derived"],
                          self.out["fGw"], marker="o", lw=2)
            nesep_derived = np.interp(self.out["time_derived"],
                            self.out["time"], self.out["ne"][:,-1])
            ax[1][1].plot(self.out["time_derived"], 
                          (nesep_derived/self.out["nGw"])*100,
                          lw=2, marker="o", c="orange",
                          label=r"$f_{Gw}^{sep}$")
            ax[1][1].set_ylabel(r"$\mathrm{f_{Gw} \, [\%]}$")
            ax[1][1].legend(fontsize=legend_fontsize)
            
            #Plasma beta
            ax[1][2].plot(self.out["time_derived"], 
                          self.out["betaN"], lw=2, c="blue",
                          marker="o", label=r"$\beta_{N}$")
            ax[1][2].legend(fontsize=legend_fontsize)
            ax[1][2].set_ylabel(r"$\mathrm{\beta \, [\%]}$")

            #Capital fusion Q - Amplification factor
            ax[2][1].plot(np.squeeze(self.out["time_derived"]),
                        np.squeeze(self.out["Qfus"]),
                        c="blue", marker="o",
                        label=r"$Q_{fus}$")        
            ax[2][1].ticklabel_format(useOffset=False)
            ax[2][1].legend(fontsize=legend_fontsize)

            #H98 - Average of Pnet and Psep
            H98_avg = (self.out["H98_Pnet"]+self.out["H98_Psep"])/2.0
            ax[2][2].plot(self.out["time_derived"], H98_avg, lw=2,
                          marker="o", c="blue")
            ax[2][2].set_ylabel(r"$\mathrm{H_{98,\,avg}}$")

            #Impurity concentrations
            if "IMC1" in self.out.keys():
                ax[3][0].plot(np.squeeze(self.out["time_derived"]),
                            np.squeeze(self.out["IMC1"]),
                            c="blue", marker="o",
                            label=r"$c_{imp, 1}$")
            if "IMC2" in self.out.keys():
                ax[3][0].plot(np.squeeze(self.out["time_derived"]),
                            np.squeeze(self.out["IMC2"]),
                            c="orange", marker="o",
                            label=r"$c_{imp, 2}$")
            if "IMC3" in self.out.keys():
                ax[3][0].plot(np.squeeze(self.out["time_derived"]),
                            np.squeeze(self.out["IMC3"]),
                            c="red", marker="o",
                            label=r"$c_{imp, 3}$")        
            ax[3][0].set_ylabel(r"$\left< n_{imp} \right> /$"+\
                                r"$\left< n_e \right>$ [%]")
            ax[3][0].ticklabel_format(useOffset=False)
            ax[3][0].legend(fontsize=legend_fontsize)

            #Alpha - Normalized pressured at the ETB
            ax[3][1].plot(self.out["time_derived"], self.out["alpha_max_jetto_edge"],
                        c="blue", marker ="o", label=r"$max(\alpha)$")
            ax[3][1].set_ylabel(r"$\alpha$(ETB)")
            ax[3][1].ticklabel_format(useOffset=False)
            ax[3][1].legend(fontsize=legend_fontsize)
            #Zeff
            ax[3][2].plot(self.out["time_derived"],
                          np.squeeze(self.out["Zeff"]), 
                          marker="o", c="k")
            ax[3][2].set_ylabel(r"$\mathrm{Z_{eff}}$")
            ax[3][0].set_xlabel("time [s]")
            ax[3][1].set_xlabel("time [s]")
            ax[3][2].set_xlabel("time [s]")
            fig.tight_layout()
            plt.subplots_adjust(top=0.92)
            figures.append(fig)

        ##################################################
        #SSPX files - SANCO Impurity Profiles #[time, rho]
        #SSTX files - SANCO Impurity Profiles #[time, rho]
        ##################################################
        if "IMC1" in self.out.keys():
            #SSP1
            fig_prad, ax_prad =\
            plt.subplots(figsize=(10,4), nrows=1, ncols=2)
            ax_prad[0].set_xlabel(r"$\rho$")
            ax_prad[0].set_ylabel(r"$\mathrm{P_{rad} \, [MW/m^3]}$")
            ax_prad[0].ticklabel_format(useOffset=False)
            ax_prad[1].set_xlabel("time [s]")
            ax_prad[1].set_ylabel(r"$\mathrm{P_{rad} \,\, [MW]}$")
            ax_prad[1].ticklabel_format(useOffset=False)

            try:
                #Impurity name
                name_imp1 = self.dataset_ssp1["INFO"]["Z1"]["DESC"].split()[0]
                #Find the number of charged states
                Ds = [int(x[2:]) for x in self.names_ssp1 if "ZQ" in x]
                ns_ssp1 = np.max(Ds)
                nrows = int(np.ceil(ns_ssp1/6))
                ncols = np.min(np.array([6, ns_ssp1]))
                fig, ax = plt.subplots(figsize=(ncols*3, int(nrows*3)),
                          nrows=nrows, ncols=ncols, sharex=True)
                if nrows == 1:
                    ax = [ax]
                fig.suptitle("SANCO 1st impurity - " + str(name_imp1))

                for i in range(0, nrows):
                    for j in range(0, ncols):
                        sn = j + 1 + i*ncols
                        labeln = r"$\mathrm{n_{imp} \, [m^{-3}]}$"
                        labelD = r"$D$"
                        labelDn = r"$D_{neo}$"
                        labelv = r"$v$"
                        labelvn = r"$v_{neo}$"
                        time_data = fig.time_data = self.out["t_sanco"]
                        x_data = [self.dataset_ssp1["XRHO"]]
                        y_data = [self.dataset_ssp1["N"+str(sn)]]
                        labels = [labeln]
                        linestyles = ["-"]
                        colors = ["k"]
                        attach_time_dependent(ax[i][j], x_data, y_data, labels, time_data,
                                            linestyles, colors, fig=fig, legend=False)
                        legend_text = "Z="+\
                                     str(np.round(self.dataset_ssp1["Z"+str(sn)][0][-1],2))
                        ax[i][j].text(0.05, 0.9, legend_text,
                                     transform=ax[i][j].transAxes)

                        axy = ax[i][j].twinx()
                        time_data = fig.time_data = self.out["t_sanco"]
                        x_data = [self.dataset_ssp1["XRHO"], self.dataset_ssp1["XRHO"],
                                  self.dataset_ssp1["XRHO"], self.dataset_ssp1["XRHO"]]
                        y_data =\
                        [self.dataset_ssp1["D"+str(sn)], self.dataset_ssp1["DN"+str(sn)],
                         self.dataset_ssp1["V"+str(sn)], self.dataset_ssp1["VN"+str(sn)]]
                        labels = [labelD, labelDn, labelv, labelvn]
                        linestyles = ["-", "--", "-", "--"]
                        colors = ["blue", "blue", "red", "red"]
                        attach_time_dependent(axy, x_data, y_data, labels, time_data,
                                              linestyles, colors, fig=fig, legend=False)
                        axy.set_ylabel(r"$D \, [m^2/s], \, v \, [m/s]$")

                for j in range(0, ncols):
                    ax[nrows-1][j].set_xlabel(r"$\mathrm{\rho_{\phi}}$")

                handles1, labels1 = ax[0][0].get_legend_handles_labels()
                handles2, labels2 = axy.get_legend_handles_labels()
                handles = handles1 + handles2
                labels = labels1 + labels2
                fig.legend(handles, labels, loc='upper right',
                           bbox_to_anchor=(0.73, 0.96), ncol=5)

                ax_prad[0].plot(self.dataset_ssp1["XRHO"][0,:],
                                self.dataset_ssp1["PR"][0,:]/1.e6,
                                c="blue", ls='--')
                ax_prad[0].plot(self.dataset_ssp1["XRHO"][-1,:],
                                self.dataset_ssp1["PR"][-1,:]/1.e6,
                                c='blue', ls='-',
                                label=r"SANCO " + str(name_imp1))
                ax_prad[1].plot(self.dataset_sst1["TVEC1"],
                                self.dataset_sst1["PT"][-1,:]/1.e6,
                                c="blue", marker="o",
                                label=r"SANCO " + str(name_imp1))

                fig.tight_layout()
                #Leave 0.65 units of space for the title,
                #regardless of figure size.
                plt.subplots_adjust(top=(int(nrows*3)-1.05)/int(nrows*3),
                                    hspace=0.25)
                figures.append(fig)
                if savefig:
                    plt.savefig("ssp1.png")
            except:
                print(" - No SSP1 SANCO file")

            #SSP2
            try:
                #Impurity name
                name_imp2 = self.dataset_ssp2["INFO"]["Z1"]["DESC"].split()[0]
                #Find the number of charged states
                Ds = [int(x[2:]) for x in self.names_ssp2 if "ZQ" in x]
                ns_ssp2 = np.max(Ds)
                nrows = int(np.ceil(ns_ssp2/6))
                ncols = np.min(np.array([6, ns_ssp2]))
                fig, ax = plt.subplots(figsize=(ncols*3, int(nrows*3)),
                          nrows=nrows, ncols=ncols, sharex=True)
                if nrows == 1:
                    ax = [ax]
                fig.suptitle("SANCO 2nd impurity - " + str(name_imp2))

                for i in range(0, nrows):
                    for j in range(0, ncols):
                        sn = j + 1 + i*ncols
                        labeln = r"$\mathrm{n_{imp} \, [m^{-3}]}$"
                        labelD = r"$D$"
                        labelDn = r"$D_{neo}$"
                        labelv = r"$v$"
                        labelvn = r"$v_{neo}$"
                        time_data = fig.time_data = self.out["t_sanco"]
                        x_data = [self.dataset_ssp2["XRHO"]]
                        y_data = [self.dataset_ssp2["N"+str(sn)]]
                        labels = [r"$\mathrm{n_{imp} \, [m^{-3}]}$"]
                        linestyles = ["-"]
                        colors = ["k"]
                        attach_time_dependent(ax[i][j], x_data, y_data, labels, time_data,
                                            linestyles, colors, fig=fig, legend=False)
                        legend_text = "Z="+\
                                     str(np.round(self.dataset_ssp2["Z"+str(sn)][0][-1],2))
                        ax[i][j].text(0.05, 0.9, legend_text,
                                     transform=ax[i][j].transAxes)

                        axy = ax[i][j].twinx()
                        time_data = fig.time_data = self.out["t_sanco"]
                        x_data = [self.dataset_ssp2["XRHO"], self.dataset_ssp2["XRHO"],
                                  self.dataset_ssp2["XRHO"], self.dataset_ssp2["XRHO"]]
                        y_data =\
                        [self.dataset_ssp2["D"+str(sn)], self.dataset_ssp2["DN"+str(sn)],
                         self.dataset_ssp2["V"+str(sn)], self.dataset_ssp2["VN"+str(sn)]]
                        labels = [labelD, labelDn, labelv, labelvn]
                        linestyles = ["-", "--", "-", "--"]
                        colors = ["blue", "blue", "red", "red"]
                        attach_time_dependent(axy, x_data, y_data, labels, time_data,
                                            linestyles, colors, fig=fig, legend=False)
                        axy.set_ylabel(r"$D \, [m^2/s], \, v \, [m/s]$")
                        axy.legend(fontsize=legend_fontsize, loc="lower left")

                for j in range(0, ncols):
                    ax[nrows-1][j].set_xlabel(r"$\mathrm{\rho_{\phi}}$")

                handles1, labels1 = ax[0][0].get_legend_handles_labels()
                handles2, labels2 = axy.get_legend_handles_labels()
                handles = handles1 + handles2
                labels = labels1 + labels2
                fig.legend(handles, labels, loc='upper right',
                           bbox_to_anchor=(0.73, 0.96), ncol=5)

                ax_prad[0].plot(self.dataset_ssp2["XRHO"][0,:],
                                self.dataset_ssp2["PR"][0,:]/1.e6,
                                c="orange", ls='--')
                ax_prad[0].plot(self.dataset_ssp2["XRHO"][-1,:],
                                self.dataset_ssp2["PR"][-1,:]/1.e6,
                                c='orange', ls='-',
                                label=r"SANCO " + str(name_imp2))
                ax_prad[1].plot(self.dataset_sst2["TVEC1"],
                                self.dataset_sst2["PT"][-1,:]/1.e6,
                                c="orange", marker="o",
                                label=r"SANCO " + str(name_imp2))

                fig.tight_layout()
                #Leave 0.65 units of space for the title,
                #regardless of figure size.
                plt.subplots_adjust(top=(int(nrows*3)-1.05)/int(nrows*3),
                                    hspace=0.25)
                figures.append(fig)
                if savefig:
                    plt.savefig("ssp2.png")
            except:
                print(" - No SSP2 SANCO file")

            #SSP3
            try:
                #Impurity name
                name_imp3 = self.dataset_ssp3["INFO"]["Z1"]["DESC"].split()[0]
                #Find the number of charged states
                Ds = [int(x[2:]) for x in self.names_ssp3 if "ZQ" in x]
                ns_ssp3 = np.max(Ds)
                nrows = int(np.ceil(ns_ssp3/6))
                ncols = np.min(np.array([6, ns_ssp3]))
                fig, ax = plt.subplots(figsize=(ncols*3, int(nrows*3)),
                          nrows=nrows, ncols=ncols, sharex=True)
                if nrows == 1:
                    ax = [ax]
                fig.suptitle("SANCO 3rd impurity - " + str(name_imp3))
                #plt.subplots_adjust(wspace=0.6, left=0.05, right=0.95)

                for i in range(0, nrows):
                    for j in range(0, ncols):
                        sn = j + 1 + i*ncols
                        labeln = r"$\mathrm{n_{imp} \, [m^{-3}]}$"
                        labelD = r"$D$"
                        labelDn = r"$D_{neo}$"
                        labelv = r"$v$"
                        labelvn = r"$v_{neo}$"
                        time_data = fig.time_data = self.out["t_sanco"]
                        x_data = [self.dataset_ssp3["XRHO"]]
                        y_data = [self.dataset_ssp3["N"+str(sn)]]
                        labels = [r"$\mathrm{n_{imp} \, [m^{-3}]}$"]
                        linestyles = ["-"]
                        colors = ["k"]
                        attach_time_dependent(ax[i][j], x_data, y_data, labels, time_data,
                                            linestyles, colors, fig=fig, legend=False)
                        legend_text = "Z="+\
                                     str(np.round(self.dataset_ssp3["Z"+str(sn)][0][-1],2))
                        ax[i][j].text(0.05, 0.9, legend_text,
                                     transform=ax[i][j].transAxes)

                        axy = ax[i][j].twinx()
                        time_data = fig.time_data = self.out["t_sanco"]
                        x_data = [self.dataset_ssp3["XRHO"], self.dataset_ssp3["XRHO"],
                                  self.dataset_ssp3["XRHO"], self.dataset_ssp3["XRHO"]]
                        y_data =\
                        [self.dataset_ssp3["D"+str(sn)], self.dataset_ssp3["DN"+str(sn)],
                         self.dataset_ssp3["V"+str(sn)], self.dataset_ssp3["VN"+str(sn)]]
                        labels = [labelD, labelDn, labelv, labelvn]
                        linestyles = ["-", "--", "-", "--"]
                        colors = ["blue", "blue", "red", "red"]
                        attach_time_dependent(axy, x_data, y_data, labels, time_data,
                                            linestyles, colors, fig=fig, legend=False)
                        axy.set_ylabel(r"$D \, [m^2/s], \, v \, [m/s]$")
                        axy.legend(fontsize=legend_fontsize, loc="lower left")

                for j in range(0, ncols):
                    ax[nrows-1][j].set_xlabel(r"$\mathrm{\rho_{\phi}}$")

                handles1, labels1 = ax[0][0].get_legend_handles_labels()
                handles2, labels2 = axy.get_legend_handles_labels()
                handles = handles1 + handles2
                labels = labels1 + labels2
                fig.legend(handles, labels, loc='upper right',
                           bbox_to_anchor=(0.73, 0.96), ncol=5)

                ax_prad[0].plot(self.dataset_ssp3["XRHO"][0,:],
                                self.dataset_ssp3["PR"][0,:]/1.e6,
                                c="red", ls='--')
                ax_prad[0].plot(self.dataset_ssp3["XRHO"][-1,:],
                                self.dataset_ssp3["PR"][-1,:]/1.e6,
                                c='red', ls='-',
                                label=r"SANCO " + str(name_imp3))
                ax_prad[1].plot(self.dataset_sst3["TVEC1"],
                                self.dataset_sst3["PT"][-1,:]/1.e6,
                                c="red", marker="o",
                                label=r"SANCO " + str(name_imp3))

                fig.tight_layout()
                #Leave 0.65 units of space for the title,
                #regardless of figure size.
                plt.subplots_adjust(top=(int(nrows*3)-1.05)/int(nrows*3),
                                    hspace=0.25)
                figures.append(fig)
                if savefig:
                    plt.savefig("ssp3.png")
            except:
                self.ssp3file = False
                print(" - No SSP3 SANCO file")

            #Legends for the impurity plots
            fig_prad.tight_layout()
            ax_prad[0].legend(fontsize=legend_fontsize)
            ax_prad[1].legend(fontsize=legend_fontsize)

        ###################################
        #2D TCI plots - Usually from NEO
        #TCI_asym.dat file output
        ###################################
        if self.tci_asym:
            fig, ax = plt.subplots(1, self.out["nions_neo"]+1,
                      figsize=(3.5*self.out["nions_neo"], 5))
            fig.suptitle("2D NEO")

            #B2D field
            contour, cbar =\
            attach_time_dependent_contour(ax[0], self.out["Rneo"], self.out["Zneo"],
            self.out["B2D"], self.out["time_neo"], fig=fig, filled=True, levels=200, 
            cmap='viridis', cb_pad=0.04)
            ax[0].plot(self.out["Rneo"][:, :, 0].T, self.out["Zneo"][:, :, 0].T,
                       c="k", alpha=0.5, lw=0.3)
            ax[0].plot(self.out["Rneo"][:, :, 0], self.out["Zneo"][:, :, 0],
                       c="k", alpha=0.5, lw=0.3)
            ax[0].set_title("Magnetic Field B2D")
            ax[0].set_xlabel("R [m]")
            ax[0].set_ylabel("Z [m]")
            ax[0].set_aspect("equal", adjustable="box")

            #Density of species
            for i in range(1, self.out["nions_neo"]+1):
                vmin = self.out["dens_"+str(i)].min()
                vmax = self.out["dens_"+str(i)].max()
                max_abs = max(abs(vmin), abs(vmax))
                if max_abs != 0:
                    exponent = int(np.floor(np.log10(max_abs)))
                else:
                    exponent = 0
                contour, cbar =\
                attach_time_dependent_contour(ax[i], self.out["Rneo"], self.out["Zneo"],
                self.out["dens_"+str(i)]/10**exponent, self.out["time_neo"], fig=fig,
                filled=True, levels=200, cmap='viridis', cb_pad=0.04)
                ax[i].plot(self.out["Rneo"][:, :, 0].T, self.out["Zneo"][:, :, 0].T,
                           c="k", alpha=0.5, lw=0.3)
                ax[i].plot(self.out["Rneo"][:, :, 0], self.out["Zneo"][:, :, 0],
                           c="k", alpha=0.5, lw=0.3)
                element = self.Z_to_element[int(self.out["z_"+str(i)])]
                ax[i].set_title(r"$ n_i^{" + element + r'} \, [\times \, 10^{' +\
                                str(exponent) + r'}]$')
                ax[i].set_xlabel("R [m]")
                ax[i].set_ylabel("Z [m]")
                ax[i].set_aspect("equal", adjustable="box")

            plt.tight_layout()
            plt.subplots_adjust(wspace=0.75, left=0.06, right=0.94, top=0.85)
            figures.append(fig)

        ###################################
        #Mag. Equilibrium and wall elements
        #Current sources (jetto.jst file)
        ###################################
        fig = plt.figure(figsize=(14,5))
        fig.suptitle("Magnetic equilibrium")
        gs = fig.add_gridspec(2,4)
        ax_eq = fig.add_subplot(gs[:, 0])
        ax_eq.set_aspect("equal")
        ax_eq.set_xlabel("R [m]")
        ax_eq.set_ylabel("Z [m]")
        ax2 = fig.add_subplot(gs[0, 1])
        ax3 = fig.add_subplot(gs[1, 1])
        ax4 = fig.add_subplot(gs[0, 2])
        axy4 = ax4.twinx()
        ax5 = fig.add_subplot(gs[1, 2])
        ax6 = fig.add_subplot(gs[0, 3])

        if self.jse:
            ax_eq.scatter(self.out["Rbnd"][-1,:],
                          self.out["Zbnd"][-1,:], c="k", s=10)

        #PLot some flux surfaces
        if self.backend == "std" and self.eqdsk == False:
            pass
        else:
            ax_eq.contour(self.out["Rgrid"], self.out["Zgrid"],
                          self.out["Psi_n"], np.array([0.1, 0.3,
                          0.5, 0.7, 0.9, 0.99999]), colors="k")

        if self.jstfile:
            ax_eq.scatter(self.out["Raxis"][-1], self.out["Zaxis"][-1],
                          c="k", marker="x")

        #Plot ray for GRAY if available
        if self.gray:
            for i in range(0, len(self.out["R_cr"])):
                ax_eq.plot(self.out["R_cr"][i], self.out["Z_cr"][i],
                        lw=2, c="blue")

        #Plot EDGE2D grid
        if self.coconut:
            npts = self.out["npts_mesh"]
            #Rings
            ax_eq.plot(self.out["Rmesh2D_rings"].T, -1.*self.out["Zmesh2D_rings"].T,
                    c='blue', alpha=0.8, lw=0.3)
            #Rows
            ax_eq.plot(self.out["Rmesh2D_rows"].T, -1.*self.out["Zmesh2D_rows"].T,
                    c='k', alpha=0.8, lw=0.3)

        #Plot wall elements
        #These are read from the "grid" file
        if self.coconut and self.grid:
            ax_eq.plot(self.out["Rvessel"], -1.*self.out["Zvessel"],
                       lw="2", c="k")
            ax_eq.set_xlim(np.min(self.out["Rvessel"]-0.1),
                           np.max(self.out["Rvessel"][:npts]+1.4))
            ax_eq.set_ylim(np.min(self.out["Zvessel"][:npts]-0.05),
                           np.max(self.out["Zvessel"][:npts]+0.2))
            #Some machines, i.e. JET do not have a buffle
            try:
                ax_eq.plot(self.out["Rbuffle"], -1.*self.out["Zbuffle"],
                           lw="2", c="k")
            except:
                pass

        #Plor EIRENE grid
        if self.coconut:
            ax_eq.triplot(self.out["Rmesh_eirene"], self.out["Zmesh_eirene"],
                       self.out["Triang_idxs"], c="green", lw="0.3")

            ax_eq.plot(np.array([]), np.array([]), c="blue", label="EDGE2D grid")
            ax_eq.plot(np.array([]), np.array([]), c="green", label="EIRENE grid")
            ax_eq.legend(loc="lower right")

        #q-profile
        if self.jspfile:
            axy = ax2.twinx()
            axy.plot(self.out["rhot_norm"][-1,:], self.out["qprof"][-1,:],
                    label=r"$q_{prof}$", c="blue")
            axy.set_ylabel("$q_{prof}$")
            axy.yaxis.label.set_color("blue")
            axy.set_ylim(0, np.max(self.out["qprof"][-1,:]))
            axy.plot((0,1), (1,1), ls="--", c="k")
            #Toroidal current density [A/m2]
            ax2.plot(self.out["rhot_norm"][-1,:],
                    self.out["jtor"][-1,:]/1.e3,
                    c="k")     
            ax2.set_ylabel(r"$\mathrm{j^{\phi} \, [kA/m^2]}$")

        #Total current as afo time
        if self.jstfile:
            ax3.plot(self.out["time_derived"], self.out["Ip"].T/1.e6,
                     c="k", ls="--", label=r"$\mathrm{I_{tot}}$")
            #Total BS current as afo time
            ax3.plot(self.out["time_derived"], self.out["jpar_Bstot"].T/1.e6,
                     label=r"$\mathrm{I_{BS}}$")
            #EC current as afo time
            ax3.plot(self.out["time_derived"], self.out["jtor_ectot"].T/1.e6,
                     c="blue", label=r"$\mathrm{I_{EC}}$")
            #NBI current drive
            ax3.plot(self.out["time_derived"], self.out["jtor_nbitot"].T/1.e6,
                     c="orange", label=r"$\mathrm{I_{NBI}}$")
            #IRCF current drive
            ax3.plot(self.out["time_derived"], self.out["jtor_ictot"].T/1.e6,
                     c="red", label=r"$\mathrm{I_{ICRF}}$")
            ##LH current drive
            #ax[1].plot(self.jet["TVEC1"], self.jet["CULH"].T/1.e6,
            #           c="green", label=r"$\mathrm{I_{LH}}$")
            ##Electron Berstein wave
            #ax[1].plot(self.jet["TVEC1"], self.jet["CUEB"].T/1.e6,
            #           c="cyan", label=r"$\mathrm{I_{EBW}}$")
            #B^{phi} at R=R_axis
            ax4.plot(self.out["time_derived"], self.out["Btor"],
                     c="blue")
            axy4.plot(self.out["time_derived"], self.out["Raxis"],
                      c="black")
            #Loop voltage
            ax5.plot(self.out["time_derived"], self.out["Vloop"])
        #Parallel resistivity
        if self.jspfile:
            ax6.plot(self.out["rhot_norm"][0,:], self.out["res_par"][0,:]*1.e6,
                    ls="--", c="black")
            ax6.plot(self.out["rhot_norm"][-1,:], self.out["res_par"][-1,:]*1.e6,
                    c="blue")
            ax6.set_xlabel(r"$\rho_{\phi}$")
            ax6.set_ylabel(r"$\eta_{\parallel} \, [\mu\Omega \cdot m]$")
        ax2.set_xlabel(r"$\rho_{\phi}$")
        ax3.set_xlabel("time [s]")
        ax3.set_ylabel("I [MA]")
        ax3.legend(fontsize=legend_fontsize)
        ax4.set_xlabel("time [s]")
        axy4.set_ylabel(r"$R_{axis} \, [m]$")
        axy4.yaxis.label.set_color("blue")
        ax4.set_ylabel(r"$B^{\phi}_{plas} (R=R_{axis}) \, [T]$")
        ax5.set_xlabel("time [s]")
        ax5.set_ylabel(r"$V_{loop} \, [V]$")
        fig.tight_layout()
        plt.subplots_adjust(left=0.08, wspace=1, top=0.90)
        figures.append(fig)

        ################################
        #Heating Source Profiles [MW/m3]
        #Radiation profiles
        ################################
        if self.jspfile:
            fig, ax = plt.subplots(nrows=1, ncols=1)
            plt.subplots_adjust(left=0.12, right=0.95)
            fig.suptitle("Heating source profiles")

            time_data = fig.time_data = self.out["time"]
            x_data = [self.out["rhot_norm"], self.out["rhot_norm"],
                    self.out["rhot_norm"], self.out["rhot_norm"],
                    self.out["rhot_norm"], self.out["rhot_norm"],
                    self.out["rhot_norm"]]
            y_data = [self.out["Pecrh"]/1.e6, self.out["Pnbi_i"]/1.e6,
                    self.out["Pnbi_e"]/1.e6, self.out["Palph_i"]/1.e6,
                    self.out["Palph_e"]/1.e6, np.abs(self.out["Prad"])/1.e6,
                    np.abs(self.out["Psyn"])/1.e6]
            labels = [r"$Q_{ECRH}$", r"$Q_{NBI}^{i}$", r"$Q_{NBI}^{e}$",
                    r"$Q_{\alpha}^{i}$", r"$Q_{\alpha}^{e}$", r"$|Q_{rad}|$",
                    r"$|Q_{sync}|$"]
            linestyles = ["-", "-", "-", "-", "-", "--", "--"]
            colors = ["blue", "orange", "cyan", "red", "royalblue", "k", "silver"]
            attach_time_dependent(ax, x_data, y_data, labels, time_data, 
                                linestyles, colors, fig=fig)
            
            #ax.plot(self.jet["XRHO"][-1,:], self.jet["QRFE"][-1,:]/1.e6,
            #        lw=2, label=r"$P^e_{ICRH}$")
            #ax.plot(self.jet["XRHO"][-1,:], self.jet["QRFI"][-1,:]/1.e6,
            #        lw=2, label=r"$P^i_{ICRH}$")
            ax.set_xlabel(r"$\mathrm{\rho_{\phi}}$")
            ax.set_ylabel(r"$\mathrm{P_{aux}, \, |P_{rad}| \, [MW/m^3]}$")
            ax.legend(fontsize=legend_fontsize)
            fig.tight_layout()
            figures.append(fig)

        ##################################
        #EDGE2D Output from TRAN fiels/IDS
        ##################################
        if self.coconut:
            fig, ax = plt.subplots(figsize=(6,6), nrows=1, ncols=1,
                                  sharex=True)
            fig.suptitle("Target temperatures")
            plt.subplots_adjust(wspace=0.5, top=0.91, bottom=0.05,
                                left=0.1, right=0.95)
            ax.plot(self.out['x_div_it'], self.out['Te_it'],
                    c='blue', label=r'$T_{e, \, IT}$')
            ax.plot(self.out['x_div_ot'], self.out['Te_ot'],
                    c='red', label=r'$T_{e, \, OT}$')
            ax.legend()
            ax.set_xlabel("Plate distance [m]")
            ax.set_ylabel(r"$\mathrm{T_{e} \, [eV]}$")
            fig.tight_layout()
            figures.append(fig)

        ##################################
        #Time traces of control parameters
        ##################################
        if "IMC1" in self.out.keys():
            fig, ax = plt.subplots(nrows=1, ncols=1)
            fig.suptitle("Control Parameters")
            ax.scatter(self.out["time_derived"], self.out["dtmax"],
                       c="k", s=20, label=r"$dt_{max}$")
            ax.legend()
            ax.set_xlabel("time [s]")
            fig.tight_layout()
            figures.append(fig)

        return figures


    def plot_postprocessed(self, savefig=False):
        """
        Plots postprocessed quantities from a JETTO/Coconut run.

        Parameters
        ----------
        savefig : Bool
            Whether to save the figures

        Notes
        ----------
        Call here external user-contributed routines
        and store the output plots to be displayed into the GUI.
        """

        #General plot parameters
        plt.rcParams.update({'font.size': 12,
        'axes.xmargin':0, 'axes.ymargin':0.02})
        legend_fontsize = 10

        #List to append figures for GUI
        figures = []

        #STEP-relevant quantities
        fig, ax = plt.subplots(figsize=(7,7), nrows=1, ncols=1,
                               sharex=True)
        fig.suptitle("STEP-specific parameters")

        #Net electric power
        C0 = 85.1 #[MW]
        C1 = 2.11 #EC efficiency
        C2 = 0.357 #Pfus efficiency
        Pnetele = -C0 - C1*self.out["Pec_tot"]/1.e6 + C2*self.out["Palf"]*5/1.e6
        ax.plot(self.out["time_derived"], Pnetele)
        ax.set_xlabel("time [s]")
        ax.set_ylabel(r"$\mathrm{P_{net, \, ele} \, [MW]}$")
        fig.tight_layout()
        fig.subplots_adjust(top=0.92)
        figures.append(fig)

        #Add plots from gray.py
        #For the time being, analysis_1 re-reads JETTO data,
        #which needs to be removed.
        try:
            res = JettoResults(path=self.jetto_path, run=None,
                  device=None, spn=None)
            self.res = res
            times = res.get_eqdsk_times()
            self.out["times_eqdsk"] = times
            if len(times) > 0:
                tend = times[-1]
            else:
                tend = None

            def make_gray_figure1(time):
                fig_gray1 = plot_analysis_1(self.res, self.dataset_jsp,
                                            self.dataset_jst, time)
                base_title = "GRAY Analysis 1"
                # Store the clean title before modifying the visible one
                if not hasattr(fig_gray1, "_original_suptitle"):
                    fig_gray1._original_suptitle = base_title
                if fig_gray1._suptitle:
                    fig_gray1._suptitle.set_text(f"{base_title} | t = {time:.3f}")
                else:
                    fig_gray1.suptitle(f"{base_title} | t = {time:.3f}")
                return fig_gray1

            def make_gray_figure2(time):
                fig_gray2 = plot_analysis_2(self.res, self.dataset_jsp,
                                            self.dataset_jst, time)
                base_title = "GRAY Analysis 2"
                if not hasattr(fig_gray2, "_original_suptitle"):
                    fig_gray2._original_suptitle = base_title
                if fig_gray2._suptitle:
                    fig_gray2._suptitle.set_text(f"{base_title} | t = {time:.3f}")
                else:
                    fig_gray2.suptitle(f"{base_title} | t = {time:.3f}")
                fig_gray2._original_suptitle = base_title
                return fig_gray2

            first_fig_gray1 = make_gray_figure1(tend)
            first_fig_gray2 = make_gray_figure2(tend)

            #Store metadata so GUI can attach a time slider
            figures.append({
                "figure": first_fig_gray1,
                "dynamic": True,
                "times": times,
                "update_func": make_gray_figure1})
            figures.append({
                "figure": first_fig_gray2,
                "dynamic": True,
                "times": times,
                "update_func": make_gray_figure2})
        except:
            print(" - Could not plot GRAY Analysis")

        #Add TCI plots
        try:
            self.xhros = [0.1, 0.5, 0.9]
            self.kygrid_range = [0.1, 30]
            def make_tci_figure(time):
                fig_tci = plot_growthrates_TCI(self.dataset_jsp, time,
                          self.xhros, self.kygrid_range, None)
                base_title = "TGLF Spectra"
                #Store the clean title before modifying the visible one
                if not hasattr(fig_tci, "_original_suptitle"):
                    fig_tci._original_suptitle = base_title
                if fig_tci._suptitle:
                    fig_tci._suptitle.set_text(f"{base_title} | t = {time:.3f}")
                else:
                    fig_tci.suptitle(f"{base_title} | t = {time:.3f}")
                return fig_tci

            tend = self.out["time"][-1]
            first_fig_tci = make_tci_figure(tend)

            #Store metadata so GUI can attach a time slider
            figures.append({
                "figure": first_fig_tci,
                "dynamic": True,
                "times": self.out["time"],
                "update_func": make_tci_figure})
        except:
            print(" - Could not plot TGLF spectra")

        return figures


class PlotGUI(tk.Tk):
    """
    GUI Wrapper of plot_run()

    Parameters
    ----------

    Notes
    ----------

    """

    def __init__(self, producer=None):
        super().__init__()
        self.title("JINTRAC output v. 0.2")
        self.geometry("1400x900")

        self.last_folder = None
        self.producer = producer
        self.figures = []
        self.current_index = 0

        #Left frame for plot selection
        self.tab_frame = ttk.Frame(self, width=600)
        self.tab_frame.grid(row=0, column=0, sticky="ns")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)  #right panel expands

        #Button to select folder and reload PlotProducer
        self.folder_button = ttk.Button(self.tab_frame, text="Select Folder",
                             command=self.select_folder)
        self.folder_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        #Update button
        self.update_button = ttk.Button(
            self.tab_frame,
            text="Update Plots",
            command=self.update_current_folder,
            state="disabled")  # enabled after first load
        self.update_button.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="ew")

        #Listbox for raw data plots
        self.tab_listbox = tk.Listbox(self.tab_frame)
        self.tab_listbox.grid(row=2, column=0, sticky="nswe", padx=5, pady=5)
        self.tab_frame.rowconfigure(2, weight=1)
        self.tab_frame.columnconfigure(0, weight=1)
        self.tab_listbox.bind("<<ListboxSelect>>", self.change_plot)

        #Decorative separator for Post-processed section
        separator_frame = ttk.Frame(self.tab_frame)
        separator_frame.grid(row=3, column=0, sticky="ew", padx=5, pady=(10,5))

        separator_line_left = ttk.Separator(separator_frame, orient="horizontal")
        separator_line_left.pack(side="left", fill="x", expand=True, padx=(0,5))

        separator_label =\
        ttk.Label(separator_frame, text="Post-processed", font=("Arial", 11, "bold"))
        separator_label.pack(side="left")

        separator_line_right = ttk.Separator(separator_frame, orient="horizontal")
        separator_line_right.pack(side="left", fill="x", expand=True, padx=(5,0))

        #Listbox for post-processed plots
        self.postproc_listbox = tk.Listbox(self.tab_frame)
        self.postproc_listbox.grid(row=4, column=0, sticky="nswe", padx=5, pady=(0,5))
        self.tab_frame.rowconfigure(4, weight=1)
        self.postproc_listbox.bind("<<ListboxSelect>>", self.change_postproc_plot)

        #Initialize tab titles
        self.tab_titles = []
        self.loading_widgets = []

        #Right frame for plot display
        self.display_frame = tk.Frame(self, bg="#d9d9d9")
        self.display_frame.grid(row=0, column=1, sticky="nsew")
        self.display_frame.rowconfigure(0, weight=1)  # canvas row expands
        self.display_frame.rowconfigure(1, weight=0)  # controls row fixed
        self.display_frame.columnconfigure(0, weight=1)

        #Initialize attributes
        self.canvas_frame = None
        self.controls_frame = None
        self.canvas = None
        self.toolbar = None
        self.time_slider = None

        #Bind resize event to redraw the plot
        self.display_frame.bind("<Configure>", self.on_resize)

        #Close figures when closing GUI
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        #Create a place to store callback IDs
        self._shutting_down = False
        self._after_ids = set()

        #Initially no plots — wait until folder selected
        if self.producer:
            figures = self.producer.plot_run()
            self._on_plots_loaded(figures)

    def _load_folder(self, folder_path):
        """Load or reload data from a given folder path."""
        self.last_folder = folder_path
        self.update_button.config(state="normal")

        #Clear right panel
        for child in self.display_frame.winfo_children():
            child.destroy()
        self.display_frame.configure(bg="#d9d9d9")

        #Close old figures
        for fig in self.figures:
            plt.close(fig)
        self.figures.clear()

        #Loading UI
        loading_frame = ttk.Frame(self.display_frame)
        loading_frame.place(relx=0.5, rely=0.4, anchor="center")

        static_label = ttk.Label(
            loading_frame, text="Loading Files", font=("Arial", 16))
        static_label.pack(side="left")

        #Dots label (for animation, right next to text)
        dots_label = ttk.Label(loading_frame, font=("Arial", 16))
        dots_label.pack(side="left")

        log_text = tk.Text(
            self.display_frame, height=10, wrap="word", state="disabled")
        log_text.place(
            relx=0.5, rely=0.55, anchor="n",
            relwidth=0.9, relheight=0.35)

        self.loading_widgets = [static_label, dots_label, log_text]

        # Redirect stdout/stderr
        redirector = self.TextRedirector(self, log_text)
        sys.stdout = redirector
        sys.stderr = redirector

        # Animate dots
        self._loading = True
        self._anim_step = 0
        dots_cycle = ["   ", ".  ", ".. ", "..."]

        def update_dots():
            if self._loading:
                dots_label.config(
                    text=dots_cycle[self._anim_step % len(dots_cycle)])
                self._anim_step += 1
                after_id = self.after(500, update_dots)
                self._after_ids.add(after_id)

        update_dots()

        #Background job
        def job():
            try:
                if self._shutting_down:
                    return

                mpl.use('Agg', force=True)
                self.producer = jintrac(
                    database="iter",
                    nshot=53298,
                    run=2,
                    jetto_path=folder_path,
                    backend="std",
                    data_version="3.39.0",
                    out_memory=True)

                #Re-check before scheduling GUI work
                if self._shutting_down:
                    return

                aid = self.after(0, lambda: self._create_figures_safe(self.producer))
                self._after_ids.add(aid)

            except Exception as e:
                if self._shutting_down:
                    return

                def fail(err=e):
                    if self._shutting_down:
                        return
                    sys.stdout = sys.__stdout__
                    sys.stderr = sys.__stderr__
                    messagebox.showerror("Error", str(err))
                    self._loading = False

                aid = self.after(0, fail)
                self._after_ids.add(aid)

        threading.Thread(target=job, daemon=True).start()

    def select_folder(self):
        folder_path = filedialog.askdirectory(title="Select Folder")
        if not folder_path:
            return
        self._load_folder(folder_path)

    def update_current_folder(self):
        """Reload data from the last selected folder."""
        if not self.last_folder:
            messagebox.showinfo(
                "No folder",
                "Please select a folder first.")
            return

        self._load_folder(self.last_folder)

    def _create_figures_safe(self, producer):
        """Runs in main thread, safe to create Matplotlib figures."""
        if self._shutting_down:
            return
        try:
            figures = producer.plot_run()  #NOW safe: executed in main thread
            self._on_plots_loaded(figures)
        except Exception as e:
            messagebox.showerror("Error creating figures", str(e))
            self._loading = False

    def _on_plots_loaded(self, figures):
        """Update GUI after plots are loaded (runs in main thread)."""
        # Stop loading animation
        self._loading = False

        dots_label = next((w for w in self.loading_widgets if isinstance(w, ttk.Label)), None)
        if dots_label:
            dots_label.config(text="")  # clear dots

        #Close old figures if any
        for fig in self.figures:
            plt.close(fig)
        self.figures = figures

        #Populate Listbox and display first plot
        self.current_index = 0
        self.tab_listbox.delete(0, tk.END)

        if not self.figures:
            messagebox.showerror("No plots", "No plots were generated for this run.")
            return

        #Store original suptitles for left panel
        self.tab_titles = []
        for i, fig in enumerate(self.figures):
            if fig._suptitle and not hasattr(fig, "_original_suptitle"):
                fig._original_suptitle = fig._suptitle.get_text()
            title = getattr(fig, "_original_suptitle", f"Plot {i+1}")
            self.tab_titles.append(title)
            self.tab_listbox.insert("end", title)

        #Adjust Listbox width to longest title
        max_length = max(len(title) for title in self.tab_titles)
        self.tab_listbox.config(width=max_length + 2)

        #Load post-processed plots (if available)
        self.postproc_listbox.delete(0, tk.END)
        self.postproc_titles = []
        self.postproc_figures = []

        if hasattr(self.producer, "plot_postprocessed"):
            try:
                postproc_results = self.producer.plot_postprocessed()
                if postproc_results:
                    self.postproc_figures = []
                    self.postproc_metadata = []
                    self.postproc_listbox.delete(0, tk.END)
                    self.postproc_titles = []

                    for i, entry in enumerate(postproc_results):
                        if isinstance(entry, dict):
                            fig = entry["figure"]
                            dynamic = entry.get("dynamic", False)
                            times = entry.get("times", None)
                            update_func = entry.get("update_func", None)
                        else:
                            # backward compatibility
                            fig, dynamic, times, update_func = entry, False, None, None

                        #Determine clean title for GUI (remove "| t =" if present)
                        if hasattr(fig, "_original_suptitle"):
                            # Prefer explicitly stored clean title
                            title = fig._original_suptitle
                        else:
                            # Extract visible title, but strip any time suffix
                            if hasattr(fig, "_suptitle") and fig._suptitle:
                                raw_title = fig._suptitle.get_text()
                                title = raw_title.split("|")[0].strip()
                            else:
                                title = f"Post {i+1}"
                                fig.suptitle(title)
                            # Store the stripped title for next time
                            fig._original_suptitle = title

                        # Store for GUI display (clean title only)
                        self.postproc_titles.append(title)
                        self.postproc_listbox.insert("end", title)

                        #Append to internal lists
                        self.postproc_figures.append(fig)
                        self.postproc_metadata.append({
                            "dynamic": dynamic,
                            "times": times,
                            "update_func": update_func})

                    # Adjust Listbox width to longest title
                    max_length_post = max(len(t) for t in self.postproc_titles)
                    self.postproc_listbox.config(width=max_length_post + 1)

            except Exception as e:
                print(f"Warning: failed to load post-processed plots: {e}")
        else:
            self.postproc_figures = []


        #NOW it’s safe to destroy the loading widgets
        for w in self.loading_widgets:
            w.destroy()

        #NOW reset stdout/stderr back to normal
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        #Display first plot
        self.display_plot(self.current_index)

    class TextRedirector(io.StringIO):
        def __init__(self, gui, widget):
            super().__init__()
            self.gui = gui
            self.widget = widget

        def write(self, msg):
            aid = self.gui.after(0, lambda m=msg: self._append(m))
            self.gui._after_ids.add(aid)

        def flush(self):
            pass

        def _append(self, msg):
            try:
                self.widget.configure(state="normal")
                self.widget.insert("end", msg)
                self.widget.see("end")
                self.widget.configure(state="disabled")
            except tk.TclError:
                pass

    def display_plot(self, index):
        """
        Defines the plots shown on the right panel

        Parameters
        ----------

        Notes
        ----------

        """

        fig = self.figures[index]

        #Destroy previous frames
        if self.canvas_frame:
            self.canvas_frame.destroy()
        if self.controls_frame:
            self.controls_frame.destroy()
        self.canvas = None
        self.toolbar = None
        self.time_slider = None

        #Canvas frame
        self.canvas_frame = ttk.Frame(self.display_frame)
        self.canvas_frame.grid(row=0, column=0, sticky='nsew')
        self.canvas_frame.rowconfigure(0, weight=1)
        self.canvas_frame.columnconfigure(0, weight=1)

        #Create new canvas
        self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, sticky='nsew')
        self.canvas.draw_idle()
        fig.canvas = self.canvas  #Attach for update_time

        #Controls frame (toolbar + slider)
        self.controls_frame = ttk.Frame(self.display_frame)
        self.controls_frame.grid(row=1, column=0, sticky='ew')
        self.controls_frame.columnconfigure(0, weight=1)

        #Add Matplotlib navigation toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.controls_frame)
        self.toolbar.update()
        self.toolbar.grid(row=0, column=0, sticky='ew')

        time_axes = []
        max_len = 0
        for ax in fig.get_axes():
            if hasattr(ax, 'time_data') and hasattr(ax, 'update_time'):
                time_axes.append(ax)
                max_len = max(max_len, len(ax.time_data))

        #If any subplot has time-dependent data, add slider
        if time_axes and max_len > 1:
            #Artificial resolution for smooth sliding
            self.slider_resolution = 10000  
            self.time_slider = ttk.Scale(self.controls_frame,
                                         from_=0,
                                         to=self.slider_resolution,
                                         orient='horizontal',
                                         command=self.update_time_plot)
            self.time_slider.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
            self.time_slider.set(self.slider_resolution)  #Start at last time point

            # Save references for update
            fig._time_axes = time_axes
            fig._max_time_len = max_len

    def update_time_plot(self, val):
        """Update all time-dependent subplots for the selected time index.
        This function is called every time the slider is moved. To ensure
        smoothness, replotting only happens every 16 ms."""
        slider_val = float(val)
        fig = self.figures[self.current_index]

        if hasattr(fig, '_time_axes'):
            #Map slider value (0..resolution) to index (0..max_time_len-1)
            idx = int((slider_val/self.slider_resolution) * (fig._max_time_len - 1))

            #Cancel any pending redraws
            if hasattr(self, "_redraw_after_id"):
                aid = self.after_cancel(self._redraw_after_id)
                self._after_ids.add(aid)

            def do_redraw():
                for ax in fig._time_axes:
                    tlen = len(ax.time_data)
                    safe_index = min(idx, tlen - 1)  # don’t go out of range
                    ax.update_time(safe_index)
                fig.canvas.draw_idle()

            #Only redraw every 16 ms (60fps)
            aid = self._redraw_after_id = self.after(16, do_redraw)
            self._after_ids.add(aid)

    def change_plot(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            self.current_index = index
            self.display_plot(index)

    def display_plot_from_figure(self, fig):
        """Display a given Matplotlib figure directly in the display frame."""
        if self.canvas_frame:
            self.canvas_frame.destroy()
        if self.controls_frame:
            self.controls_frame.destroy()

        self.canvas_frame = ttk.Frame(self.display_frame)
        self.canvas_frame.grid(row=0, column=0, sticky='nsew')
        self.canvas_frame.rowconfigure(0, weight=1)
        self.canvas_frame.columnconfigure(0, weight=1)

        self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
        self.canvas.draw_idle()

        self.controls_frame = ttk.Frame(self.display_frame)
        self.controls_frame.grid(row=1, column=0, sticky='ew')

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.controls_frame)
        self.toolbar.update()

    def change_postproc_plot(self, event):
        """
        Handle user selection in the post-processed plots listbox.
        Displays the selected post-processed figure in the right panel.
        If the figure is dynamic, shows the time slider for interactivity.
        """
        selection = event.widget.curselection()
        if not selection:
            return

        index = selection[0]

        # Ensure postprocessed figures exist
        if not hasattr(self, "postproc_figures") or not self.postproc_figures:
            return

        fig = self.postproc_figures[index]
        meta = self.postproc_metadata[index]

        # Destroy any existing plot display
        if self.canvas_frame:
            self.canvas_frame.destroy()
        if self.controls_frame:
            self.controls_frame.destroy()

        # Create new canvas
        self.canvas_frame = ttk.Frame(self.display_frame)
        self.canvas_frame.grid(row=0, column=0, sticky='nsew')
        self.canvas_frame.rowconfigure(0, weight=1)
        self.canvas_frame.columnconfigure(0, weight=1)

        self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
        self.canvas.draw_idle()

        # Create controls (toolbar + slider)
        self.controls_frame = ttk.Frame(self.display_frame)
        self.controls_frame.grid(row=1, column=0, sticky='ew')
        self.controls_frame.columnconfigure(0, weight=1)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.controls_frame)
        self.toolbar.update()
        self.toolbar.grid(row=0, column=0, sticky='ew')

        # If this plot is dynamic, add slider and enable live update
        if meta.get("dynamic", False):
            times = meta["times"]
            self.time_slider = ttk.Scale(
                self.controls_frame,
                from_=0,
                to=len(times) - 1,
                orient='horizontal',
                command=lambda val: self._update_dynamic_postproc_plot(meta, val)
            )
            self.time_slider.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
            self.time_slider.set(0)  # start at first time

            # Remember current figure for reuse (avoid recreation)
            self.current_dynamic_fig = fig
            self.current_postproc_time_idx = 0

        else:
            # Static plots — nothing else needed
            self.current_dynamic_fig = None

    def _update_dynamic_postproc_plot(self, meta, val):
        """Smoothly update the dynamic postprocessed figure when the slider moves.
        Throttles redraws to prevent flicker and excessive re-rendering."""
        idx = int(float(val))

        #Cancel any pending redraws if the slider is still moving
        if hasattr(self, "_redraw_after_id"):
            aid = self.after_cancel(self._redraw_after_id)
            self._after_ids.add(aid)

        #Schedule the actual redraw after 50 ms (20 fps)
        self._redraw_after_id =\
        self.after(50, lambda: self._refresh_dynamic_postproc_plot(meta, idx))
        self._after_ids.add(self._redraw_after_id)

    def _refresh_dynamic_postproc_plot(self, meta, idx):
        """Actually refresh the dynamic postprocessed figure with a new one."""
        times = meta["times"]
        update_func = meta["update_func"]
        time_point = times[idx]

        #Close and clean up any previous figure before generating a new one
        if hasattr(self, "current_dynamic_fig") and self.current_dynamic_fig:
            try:
                plt.close(self.current_dynamic_fig)
            except Exception:
                pass
            self.current_dynamic_fig = None

        #Safely replace only the canvas (not controls) ---
        if self.canvas:
            old_widget = self.canvas.get_tk_widget()
            old_widget.destroy()
            self.canvas = None

        #Generate a new figure for this time step
        new_fig = update_func(time_point)

        # Clean title handling (ensure GUI sidebar title stays clean)
        if hasattr(new_fig, "_original_suptitle"):
            base_title = new_fig._original_suptitle
        elif new_fig._suptitle:
            base_title = new_fig._suptitle.get_text().split("|")[0].strip()
            new_fig._original_suptitle = base_title
        else:
            base_title = ""

        #Update the visible figure title with current time
        if new_fig._suptitle:
            new_fig._suptitle.set_text(f"{base_title} | t = {time_point:.3f}")
        else:
            new_fig.suptitle(f"{base_title} | t = {time_point:.3f}")

        self.canvas = FigureCanvasTkAgg(new_fig, master=self.canvas_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
        self.canvas.draw_idle()

        # Remember slider position
        self.current_dynamic_fig = new_fig
        self.current_postproc_time_idx = idx

    def display_postproc_plot_with_slider(self):
        """
        Display a single post-processed plot with a time slider that updates
        the figure as the user moves the slider.
        """
        # Destroy previous frames
        if self.canvas_frame:
            self.canvas_frame.destroy()
        if self.controls_frame:
            self.controls_frame.destroy()

        self.canvas = None
        self.toolbar = None
        self.time_slider = None

        # Validate producer attributes
        if not hasattr(self.producer, "times") or not hasattr(self.producer, "make_postprocessed_plot"):
            messagebox.showerror("Error", "Producer missing 'times' or 'make_postprocessed_plot'.")
            return

        self.postproc_times = np.array(self.producer.times)
        self.current_postproc_idx = 0

        # Create initial figure
        initial_time = self.postproc_times[self.current_postproc_idx]
        fig = self.producer.make_postprocessed_plot(initial_time)

        # Create frame for canvas
        self.canvas_frame = ttk.Frame(self.display_frame)
        self.canvas_frame.grid(row=0, column=0, sticky='nsew')
        self.canvas_frame.rowconfigure(0, weight=1)
        self.canvas_frame.columnconfigure(0, weight=1)

        # Create the matplotlib canvas
        self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, sticky='nsew')
        self.canvas.draw_idle()

        # Controls (toolbar + slider)
        self.controls_frame = ttk.Frame(self.display_frame)
        self.controls_frame.grid(row=1, column=0, sticky='ew')
        self.controls_frame.columnconfigure(0, weight=1)

        # Matplotlib toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.controls_frame)
        self.toolbar.update()
        self.toolbar.grid(row=0, column=0, sticky='ew')

        # Time slider
        self.time_slider = ttk.Scale(
            self.controls_frame,
            from_=0,
            to=len(self.postproc_times) - 1,
            orient='horizontal',
            command=self.update_postproc_slider_plot)
        self.time_slider.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
        self.time_slider.set(0)

        # Display initial time in title
        fig.suptitle(f"Post-processed at t={initial_time:.3f}", fontsize=12)

        self.current_postproc_fig = fig

    def update_postproc_slider_plot(self, val):
        """
        Update the post-processed plot when the time slider is moved.

        Parameters
        ----------
        val : float
            The slider position (corresponding to index in self.postproc_times)
        """
        idx = int(float(val))
        if idx == getattr(self, "current_postproc_idx", None):
            return  # avoid unnecessary redraws

        self.current_postproc_idx = idx
        new_time = self.postproc_times[idx]

        # Generate new figure for this time
        new_fig = self.producer.make_postprocessed_plot(new_time)

        # Replace displayed canvas
        self.canvas_frame.destroy()
        self.canvas_frame = ttk.Frame(self.display_frame)
        self.canvas_frame.grid(row=0, column=0, sticky='nsew')
        self.canvas_frame.rowconfigure(0, weight=1)
        self.canvas_frame.columnconfigure(0, weight=1)

        self.canvas = FigureCanvasTkAgg(new_fig, master=self.canvas_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
        self.canvas.draw_idle()

        new_fig.suptitle(f"Post-processed at t={new_time:.3f}", fontsize=12)
        self.current_postproc_fig = new_fig

    def on_resize(self, event):
        if self.canvas:
            #Make the plot scale with the frame,
            self.canvas.get_tk_widget().config(width=event.width,
                 height=event.height)
            self.canvas.draw_idle()

    def on_close(self):
        self._shutting_down = True

        #Cancel all scheduled after() callbacks
        for aid in list(self._after_ids):
            try:
                self.after_cancel(aid)
            except Exception:
                pass

        self._after_ids.clear()

        #Restore stdout/stderr
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        if self.canvas_frame:
            self.canvas_frame.destroy()
        if self.controls_frame:
            self.controls_frame.destroy()
        for fig in self.figures:
            plt.close(fig)
        self.destroy()

        #Hard exit fallback (prevents zombie processes)
        os._exit(0)

def main():
    parser = argparse.ArgumentParser(description="JINTRAC GUI or debug runner")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Run in debug mode (no GUI, outputs to terminal)")
    parser.add_argument(
        "--path",
        type=str, default="./",
        help="Path to JETTO output folder")
    args = parser.parse_args()

    if args.debug:
        # --- DEBUG MODE ---
        print("Running JINTRAC in debug mode (no GUI)...")

        # Initialize your producer exactly as the GUI would
        producer = jintrac(
            database="iter",
            nshot=53298,
            run=2,
            jetto_path=args.path,
            backend="std",
            data_version="3.39.0",
            out_memory=True)

        #Run the postprocessing and print diagnostic info
        print("Generating main plots...")
        figs = producer.plot_run()

        print(f"Generated {len(figs)} base figures.")

        #Optionally: generate postprocessed plots
        if hasattr(producer, "plot_postprocessed"):
            postproc = producer.plot_postprocessed()
            print(f"Generated {len(postproc)} postprocessed figures.")
        else:
            print("No postprocessed plots available.")

        print("Debug run complete.")
        return
    else:
        #NORMAL GUI MODE - No producer at startup
        app = PlotGUI()
        app.mainloop()

if __name__ == "__main__":
    main()
