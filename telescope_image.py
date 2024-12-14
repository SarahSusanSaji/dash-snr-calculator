import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
from astropy import units as u
#from photutils.background import Background2D, MedianBackground
from astropy.convolution import Gaussian2DKernel
import astropy.convolution.convolve as convolve
from astropy.visualization import (MinMaxInterval, SqrtStretch,LogStretch,ZScaleInterval,HistEqStretch,LinearStretch,
                                   PowerStretch,ImageNormalize,simple_norm)
from astropy.io import fits
from matplotlib.patches import Rectangle
from math import log, log10, ceil, floor, exp, sqrt
from scipy import integrate,interpolate
import numpy.random as random

# constants
c_km = 2.9979E5      # km/s
c = 2.9979E10       # cm/s
h = 6.626068E-27    # cm^2*g/s
k = 1.3806503E-16   # cm^2*g/(s^2*K)
Ang = 1E-8          # cm
mu = 1E-4           # cm
scale=0.8/3 #0.8 arcsecond divided by 3 pixels
darkcurrent = 0.002 #e- / s
readnoise = 5 # e-
readnoise=readnoise**2
itime=5
nframes=1

zp=43.6*u.ph*u.cm**-2*u.s**-1*u.Angstrom**-1

zp=zp.to(u.ph*u.m**-2*u.s**-1*u.micron**-1)

print('K band zeropoint =',zp)

input_scene=np.zeros([108,108]) # input scene array

#x,y positions of objects in array and their corresponding magnitudes
x_arr=random.randint(low=0,high=108,size=20)
y_arr=random.randint(low=0,high=108,size=20)
mag_arr=random.randint(low=8,high=9,size=20)

for xi,yi,magi in zip(x_arr,y_arr,mag_arr):
        mag=magi
        phot_flux=zp*10**(-0.4*mag) #ph/s/um/m2
        area=np.pi*(3.6**2-0.952**2)*u.m**2
        bw=0.41*u.micron #micron
        eff=0.6#efficieny
        det_flux=phot_flux*area*bw*eff #area*bw*eff
        #print(det_flux) #photons/sec
        input_scene[yi,xi]=det_flux.value


#Seeing kernel
gaussian_2D = Gaussian2DKernel(x_stddev=1,y_stddev=1,x_size=11,y_size=11)

object_data=convolve(input_scene,gaussian_2D)

%matplotlib inline
norm = simple_norm(object_data, 'log')
plt.imshow(object_data,norm=norm)
plt.show() # Convolved image

#Sky Background
backmag=13.4048 # Kband /arcsec^2
phot_flux=zp*10**(-0.4*backmag)*u.arcsecond**-2

phot_flux

sky_flux=phot_flux*area*bw*eff
sky_flux_per_pixel=sky_flux*scale*u.arcsec*scale*u.arcsec
sky_flux_per_pixel

sky_data=np.zeros([108,108])+sky_flux_per_pixel.value

object_sky_data=object_data+sky_data

plt.figure()
norm = simple_norm(object_sky_data, 'log')
plt.imshow(object_sky_data,norm=norm)
plt.show()

