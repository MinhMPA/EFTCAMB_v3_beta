import numpy as np
import sys, platform, os
camb_path = os.path.realpath(os.path.join(os.getcwd(),'..'))
sys.path.insert(0,camb_path)
import camb
from camb import model, initialpower
print('Using CAMB %s installed at %s'%(camb.__version__,os.path.dirname(camb.__file__)))

# Set output path

out_file='./EFTCAMB_test_transfer_out.dat'

# Set global parameters

z=[0.,]
PL18_H0=67.32
PL18_ombh2=0.022383
PL18_omch2=0.12011
PL18_omnuh2=0.0006451439
# PL18_mnu=0.06
PL18_omk=0
PL18_tau=0.0543
PL18_As=2.101e-9
PL18_ns=0.96605
PL18_r=0

# Sample EFT parameters
## Manually set for now, later sample and test condition
EFT_w0=-1.028
EFT_Omega0=0.05283090606807964
EFT_gamma10=0.8961122668868023
EFT_gamma20=0.9398130537680877
EFT_gamma30=0.42330140115983217

# Flags to check for stability

## Currently default values
stability_flag ={
                'EFT_ghost_math_stability'   : False,\
                'EFT_mass_math_stability'    : False,\
                'EFT_ghost_stability'        : True,\
                'EFT_gradient_stability'     : True,\
                'EFT_mass_stability'         : True,\
                'EFT_additional_priors'      : True
                }

# Specify EFT model

pureEFT_params= {
                 'EFTflag': 1,\
                 'PureEFTmodel': 1,\
                 # not sure this flag would still work
                 # 'PureEFTHorndeski': True,\
                  # const w0, specify w0 below
                 'EFTwDE': 1,\
                 'EFTw0': EFT_w0,\
                  # not relevant, set to 0
                 'EFTwa':0,'EFTwn':0,'EFTwat':0, 'EFTw2':0, 'EFTw3':0,\
                  # const Omega0, specify Omega0 below
                 'PureEFTmodelOmega': 1,\
                 'EFTOmega0':EFT_Omega0,\
                 'EFTOmegaExp':0,\
                  # linear gamma1, set gamma10 below
                 'PureEFTmodelGamma1':1,\
                 'EFTGamma10': EFT_gamma10,\
                 'EFTGamma1Exp': 0,\
                  # linear gamma2, set gamma20 below
                 'PureEFTmodelGamma2':1,\
                 'EFTGamma20': EFT_gamma20,\
                 'EFTGamma2Exp': 0,\
                  # linear gamma3, set gamma30 below
                 'PureEFTmodelGamma3':1,\
                 'EFTGamma30': EFT_gamma30,\
                 'EFTGamma3Exp': 0,\
                 'PureEFTmodelGamma4':1,'EFTGamma40': -EFT_gamma30,'EFTGamma4Exp': 0,\
                 'PureEFTmodelGamma5':1,'EFTGamma50': 0.5*EFT_gamma30,'EFTGamma5Exp': 0,\
                 'PureEFTmodelGamma6':0,'EFTGamma60': 0,'EFTGamma6Exp': 0
                 }
pureEFT_params.update(stability_flag)

# Set up CAMB and evaluate model

pars = camb.CAMBparams(omnuh2=PL18_omnuh2)
pars.set_cosmology(H0=PL18_H0,\
        ombh2=model_ombh2, omch2=model_omch2,\
        omk=PL18_omk, tau=PL18_tau,\
        EFTCAMB_params=pureEFT_params) # H0 (or theta) must be set explicitely here
pars.InitPower.set_params(As=PL18_As, ns=PL18_ns, r=PL18_r)
pars.set_matter_power(kmax=2.0,redshifts=z)
pars.WantTransfer = True
pars.WantCls = False
results = camb.get_results(pars)
trans = results.get_matter_transfer_data()

kh=trans.transfer_data[model.Transfer_kh-1,:,0]
cdm_delta=trans.transfer_data[model.Transfer_cdm-1,:,0]
baryon_delta=trans.transfer_data[model.Transfer_b-1,:,0]

# Save output

np.savetxt(out_file,np.c_[kh,cdm_delta,baryon_delta])
