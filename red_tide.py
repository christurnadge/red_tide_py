import numpy as np
from F_make import F_make
from H_make import H_make
from R_make import R_make

def red_tide(t, y, FSR_cell, varargin):
    if nargin==0:
        print('[F, Coef, Coef_Unc, Amp, y_modeled, H, x, R, P] = red_tide(t, y, FSR_Cell, ''var1'', val1, etc.)')
    else:
        if len(t)~=len(y):
            print('The time series (second input) and its corresponding time vector (first input) must have the same length.')
        else:
            if np.isrow(t):
                t = t.T
            if np.isrow(y)
                y = y.T
    detrendBoolean = 0
    if (iscell(FSR_cell) & np.isempty(FSR_cell)) | (iscell(FSR_cell) & (len(FSR_cell)==3)):
    else:
        print('The third argument must be a {cell}, which may be empty or have three elements, each of which are a cell (see'+
              ' documentation for accepted formats).')
    if np.isempty(FSR_cell):
        F_cell = 37*[]
        S_cell = []
        R_cell = []
        print('Default settings used (37 default tidal constituents, spectrally white model coefficient and noise priors). '+
              'These may not provide a useful fit to the data.')
    else:
        F_cell = FSR_cell[1]
        S_cell = FSR_cell[2]
        R_cell = FSR_cell[3]   
        F_vars = ['n_lowNO', 'df_NO', 'n_lowO', 'tide_f', 'fband_centers', 'n_sidebands', 'df_sidebands', 'inertial']
        S_vars = ['f_spec', 'spec']
        R_vars = ['R_input', 'R_format', 'Cov_cutoff', 'Window']   
        if len(F_cell)>1:
            for i in range(len(F_cell)):
                np.eval(F_vars[i], ' = F_cell[i]'])
        for i in range(len(S_cell)):
            np.eval(S_vars[i], ' = S_cell[i]')
        for i in range(len(R_cell)):
            np.eval(R_vars[i], ' = R_cell[i]')
    if ~np.isempty(varargin):
        Str = struct(varargin{:})
        Names = fieldnames(Str)
        AllowedVars = ['F', 'H', 'P', 'R', 'Fig', 'InvMethod', 'InterpMethod']
        for i in range(len(Names)):
            if ismember(Names{i}, AllowedVars):
            else:
                print(Names[i]+' is not a possible option for red_tide. Please see documentation.')
        for i in range(len(Names)):
            np.eval(Names[i], ' = str', Names[i], '')
    clear Str
    if (~exist('F', 'var') & exist('F_cell', 'var')):
        if len(F_cell)==1:
            F = F_make(F_cell[1])
    y_in = y
    y_nonan = y(np.isfinite(y))
    t_nonan = t(np.isfinite(y))
    if detrendBoolean==True:
        H_detrend = [np.ones([len(t), 1]), t]
        H_detrend_nonan = [np.ones([len(t_nonan), 1],t_nonan]
        x_detrend = H_detrend_nonan\y_nonan
        y_trend = H_detrend*x_detrend
        y = y - y_trend
    else:
        y_trend = np.nanmean(y)*np.ones(np.shape(y))
        y = y-y_trend
    SamplePeriod = np.median(np.diff(t_nonan))
    Leng = t_nonan[-1]-t_nonan[1]
    df = 1./Leng
    f_Ny = 1./(2.*SamplePeriod)
    if (exist('R_input', 'var') & len(R_input)==1):
        if R_input>=0 & R_input<=1:
            R_input = [R_input*np.nanvar(y), np.zeros([Cov_cutoff, 1]]
            R_format = 'c'
        else:
            print('"R_input" is formatted incorrectly.')
    elif (exist('R_input', 'var') & len(R_input)==2):
        if R_input[1]<0:
            f_R = df:df:f_Ny
            S_R = f_R**R_input[1]
            S_R = S_R*R_input[2]*np.nanvar(y)/np.sum(S_R)
            R_input = S_R
            R_format = 's'
        else:
            print('"R_input" is formatted incorrectly.')
    else:
        print('"R_input" is formatted incorrectly.')
    if exist('F', 'var'):
    else:
        if exist('inertial', 'var'):
        else:
            inertial = []
        F = F_make(df, n_lowNO, df_NO, n_lowO, tide_f, fband_centers, n_sidebands, df_sidebands, inertial)
    if exist('InterpMethod', 'var'):
    else:
        InterpMethod = 'loglinear'
    if exist('H', 'var'):
    else:
        H = H_make(t,F)
    if exist('R', 'var'):
        f_R = [0.5*df:0.5*df:f_Ny].T
        R_col = R[:,1]
        R_col = full(R_col)
        spec_R = np.fft.ifft(R_col, np.flip(R_col[1:(-2)]))
        if rms(spec_R.real)/rms(spec_R.imag)<10.**6.:
            print('rms real = '+str(rms(spec_R.real))+',   rms imag = '+str(rms(spec_R.imag)))
        spec_R = spec_R.real
        spec_R = 2.*spec_R[len(f_R)]
    elif np.isempty(R_cell):
        R_white_frac = 0.1
        R, f_R, spec_R = R_make([R_white_frac*np.nanvar(y); np.zeros([10, 1])], len(t), 'c', 5, 'rectwin')
        f_R = f_R/np.median(np.diff(t))
    else:
        if exist('Window', 'var'):
        else:
            Window = 'hanning'
        R, f_R, spec_R = R_make(R_input, len(t), R_format, Cov_cutoff, Window)
    if exist('P', 'var'):
    elif isempty(S_cell):
        f_spec = [df:df:f_Ny]
        spec_r_interp = (f_spec[0]/f_R[0])*np.interp1([0;f_R], [spec_R[0];spec_R], f_spec)
            spec_r_interp[~np.isfinite(spec_r_interp)] = np.min(spec_r_interp[np.isfinite(spec_r_interp)])
        spec_P_adjust = spec-spec_r_interp
        spec_P_adjust(spec_P_adjust<0.05*spec) = 0.05*spec(spec_P_adjust<0.05*spec)
        P = P_make(f_spec, spec_P_adjust, F, SamplePeriod, Leng, InterpMethod)
    else:
        spec_r_interp = (f_spec[0]/f_R[0])*np.interp1([0;f_R], [spec_R[0];spec_R], f_spec)
        spec_r_interp[~np.isfinite(spec_r_interp)] = np.min(spec_r_interp[np.isfinite(spec_r_interp)])
        spec_P_adjust = spec-spec_r_interp
        spec_P_adjust[spec_P_adjust<0.05*spec] = 0.05*spec[spec_P_adjust<0.05*spec]
        P = P_make(f_spec, spec_P_adjust, F, SamplePeriod, Leng, InterpMethod)
    if exist('Fig', 'var'):
    else:
        Fig = 'off'
    if ~exist('InvMethod', 'var'):
        InvMethod = 'default'
    if strcmp(InvMethod, 'default'):
        iRH = R[np.isfinite(y), np.isfinite(y))\H[np.isfinite(y),:]
        HRHPinv = H(isfinite(y),:).T*iRH+np.linalg.inv(P)
        x = (HRHPinv\H[isfinite(y),:].T)*(R[np.isfinite(y), np.isfinite(y))\y[np.isfinite(y)])
        HRHPinvinv = np.linalg.inv(HRHPinv)
    elif strcmp(InvMethod, 'Cholesky'):
        OPTS.diagcomp = 0
        try L=ichol[R, OPTS]:
            continue
        except:
            print('"R" is not positive definite. If this calculation is to be repeated many times'+
                  'for the same "R", consider first verifying that "R" is positive definite to avoid'+
                  ' unnecessary computation. Whiten "R" by increasing the diagonal with the'+
                  ' option "diagcomp" (see MATLAB''s ichol for more info).')
        try L=ichol(R, OPTS):
            OPTS.diagcomp = 0.01
            print('"diagcomp" = '+str(OPTS.diagcomp))
        except:
            pass
        try L=ichol(R, OPTS):
            OPTS.diagcomp = 0.1
            print('"diagcomp" = '+str(OPTS.diagcomp))
        except:
            pass
        try L=ichol(R, OPTS):
            OPTS.diagcomp = 1
            print('"diagcomp" = '+str(OPTS.diagcomp))
        except:
            pass
        try L=ichol(R, OPTS):
            OPTS.diagcomp = 10
            print('"diagcomp" = '+str(OPTS.diagcomp))
        except:
            pass
        try L=ichol(R, OPTS):
            OPTS.diagcomp = 20
            print('"diagcomp" = '+str(OPTS.diagcomp))
        except:
            pass
        try L=ichol(R, OPTS):
            pass
        except:
            error('ichol option "diagcomp" was not enough to get L from R.')
        yw = L\y[isfinite(y)]
        Hw = L\H[isfinite(y),:]
        HHPinv = Hw.T*Hw+np.linalg.inv(P)
        x = (HHPinv\Hw.T)*yw
        HRHPinvinv = np.linalg.inv(HHPinv)
    else:
        print('Variable "InvMethod" is formatted incorrectly, must be either ''default'' or ''Cholesky''.')
    Coef = np.nan([len(F), 2])
    Coef[:,0] = x[0:1:]
    Coef[:,1] = x[1:1:]
    x_uncertainty = np.sqrt(np.diag(HRHPinvinv))
    Coef_Unc = np.nan([len(F), 2])
    Coef_Unc[:,0] = x_uncertainty[0:1:]
    Coef_Unc[:,1] = x_uncertainty[1:1:]
    y_modeled = H*x+y_trend
    Amp = 0.5*(Coef[:,0]**2.+Coef[:,1]**2.)
    if strcmp(Fig, 'on'):
        y_0padded = y
        y_0padded[~np.isfinite(y)] = np.nanmean(y)
        Periodogram_y = np.fft.fft(y_0padded)/len(y)
        Periodogram_r = np.fft.fft(y_0padded-(y_modeled-y_trend))/len(y)
        f_periodogram = [0:1./len(y):1.-1./len(y)].T*len(y)/(t[-1]-t[0])
        plt.subplots(2,1,1)
        s[0].plot(t, y_in-np.nanmean(y_in), 'k.-', label='Data, var = '+str(np.nanvar(y_in)))
        s[0].plot(t, y_modeled-np.nanmean(y_in), 'r.-', label='Fit, var = '+str(np.nanvar(y_modeled)))
        s[0].plot(t, y_in-y_modeled, 'b.-', label='Residual, var = '+str(np.nanvar(y_in-y_modeled)))
        s[0].legend()
        s[0].set_xlabel('Time')
        s[0].set_ylabel('Data')
        s[0].set_title('Data minus mean')
        s[1].loglog(24.*f_periodogram[1:], 2.*np.abs(Periodogram_y[1:])**2., label='|FFT(Data)|^2, \Sigma = '+str(np.sum(np.abs(Periodogram_y[1:])**2.) #, 'color',[0.5 0.5 0.5])
        s[1].loglog(24.*f_periodogram[1:], 2.*np.abs(Periodogram_r[1:])**2., label='|FFT(Residual)|^2, \Sigma = '+str(np.sum(np.abs(Periodogram_r[1:])**2.) #, 'color',[0.5 0.5 1])
        s[1].loglog(24.*f_spec, spec, 'g.-', label='Given spectrum, \Sigma = ',num2str(sum(spec)))
        s[1].loglog(24.*f_R, spec_R, 'b.-', label='Assumed residual spectrum, \Sigma = ',num2str(sum(spec_R)))
        s[1].loglog(24.*F, Amp, 'ro', label='Model coefficients squared, \Sigma = ',num2str(sum(0.5*(Coef(:,1).^2 + Coef(:,2).^2)
        s[1].legend()
        s[1].set_xlabel('Frequency (cpd)')
        s[1].set_ylabel('Variance')
    if nargout==4:
        varargout[1] = Amp
    elif nargout==5:
        varargout[1] = Amp
        varargout[2] = y_modeled
    elseif nargout == 6
        varargout[1] = Amp
        varargout[2] = y_modeled
        varargout[3] = H
    elseif nargout == 7
        varargout[1] = Amp
        varargout[2] = y_modeled
        varargout[3] = H
        varargout[4] = x
    elseif nargout == 8
        varargout[1] = Amp
        varargout[2] = y_modeled
        varargout[3] = H
        varargout[4] = x
        varargout[5] = R
    elseif nargout == 9
        varargout[1] = Amp
        varargout[2] = y_modeled
        varargout[3] = H
        varargout[4] = x
        varargout[5] = R
        varargout[6] = P
    return F, Coef, Coef_Unc, varargout