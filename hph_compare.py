from hph import hph
import matplotlib.pyplot as plt

def hph_compare(H, P, X):
    HPH = hph(H,P)
    xcovX = np.xcov(X, 'unbiased')
    xcovX = np.flip(np.fft.fftshift(xcovX))
    xcovX = xcovX[1:((len(xcovX)+1)/2))
    f,s = plt.subplots()
    s.plot(HPH, '.-', label='HPH^T')
    s.plot(xcovX, '.-', label='covariance')
    s.legend()
    s.set_xlabel('lag')
    return