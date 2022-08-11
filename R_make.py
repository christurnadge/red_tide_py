import numpy as np

def R_make(IN, N, Format, varargin):
    if nargin==3:
        Cov_cutoff = len(IN)
        WindowF = 'rectwin'
    elif nargin==4:
        Cov_cutoff = varargin{1}
        WindowF = 'rectwin'
    elif nargin==5:
        Cov_cutoff = varargin{1}
        WindowF = varargin{2}
    else:
        print('Wrong number of inputs.')
    Window = eval([WindowF, '(Cov_cutoff*2-1)'])
    Window = Window[(Cov_cutoff):end]
    Window = Window.T
    if iscolumn(IN):
        IN = IN.T
    if strcmp(Format,'s') || strcmp(Format,'spec') || strcmp(Format,'spectrum'):
        S = [0, IN]
        SS = [S np.flip(S[2:-1])]
        fSS = np.fft.ifft(SS)/len(SS)
        if rms(fSS.real)<10000.*rms(fSS.imag):
            print('Non-trivial imaginary component to the Fourier transform of the given spectrum.')
        else:
            fSS = fSS.real
        C = fSS[1:Cov_cutoff]
        C = np.sum(S)*C/C[1]
        C = C*Window
        R = spdiags(repmat([np.flip(C[2:]), C], N, 1), [1-len(C):len(C)-1], speye(N))
    elif strcmp(Format,'c') || strcmp(Format,'cov') || strcmp(Format,'covariance'):
        C = IN[1:Cov_cutoff]
        C = C*Window
        R = spdiags(repmat([flip(C[2:]), C], N, 1), [1-len(C):len(C)-1], speye(N))
    else:
        print('Invalid second input "Format".')
    if nargout==3:
        freq = [1/(N-1):1/(N-1)]:0.5].T
        R_col = R[1:np.round(N), 1]
        R_col = full(R_col)
        S_R = np.fft.ifft([R_col; np.flip(R_col[2:-1])])
        if rms(S_R.real)/rms(S_R.imag)<10.**6.:
            print('rms real = '+str(rms(S_R.real))+',   rms imag = '+str(rms(S_R.imag))])
        S_R = S_R.real
        S_R = 2.*S_R[2:len(freq)+1]
        varargout{1} = freq
        varargout{2} = S_R
    else:
        print('Either 1 or 3 outputs expected (see documentation).')
    return R, varargout