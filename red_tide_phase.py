import numpy as np

def red_tide_phase(X_Coef, varargin):
    if nargin==1:
        phaseSIN = np.atan2( X_Coef[:,1], X_Coef[:,0])
        phaseCOS = np.atan2(-X_Coef[:,0], X_Coef[:,1])
    elif nargin==2:
        F = varargin[1][1]
        Dateformat = varargin[1][2]
        T0 = varargin[1][3]
        T0_new = varargin[1][4]
        t0 = datenum(T0, Dateformat)
        t0_new = datenum(T0_new, Dateformat)
        dt_hours = (t0-t0_new)*24
        phaseSIN = np.mod(np.atan2( X_Coef[:,1],X_Coef[:,0])+dt_hours*2.*np.pi*F, 2.*np.pi)
        phaseCOS = np.mod(np.atan2(-X_Coef[:,0],X_Coef[:,1])+dt_hours*2.*np.pi*F, 2.*np.pi)
    else:
        print('Incorrect number of inputs, please see documentation.')
    return phaseSIN, phaseCOS 