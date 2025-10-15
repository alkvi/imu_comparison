# Code from https://commons.wikimedia.org/wiki/File:AliasingSines.svg

from pylab import *
from numpy import *

# create a figure
figure(figsize=(7.5,2.5))

# x coords from -1 to 11
x_fine = linspace(-0.4, 10.4, 1000)
x_coarse = linspace(0, 10, 11)

# sinewave w/ freq=0.9
y1 = sin(2*pi * 0.9 * (x_fine-0.5))
plot( x_fine, y1, "-", color="red")

# sinewave w/ freq=0.1
y2 = sin(2*pi * 0.1 * (x_fine-0.5))
plot(x_fine, y2, "-", color="blue")

# show aliasing
y3 = sin(2*pi * 0.1 * (x_coarse-0.5))
plot( x_coarse, y3, "o", color="black" )
vlines( x_coarse, 0, y3, color="black" ) # add the "lollipop" points

# set window and tick labels
axis([-0.5, 10.5, -1.1, 1.1])
yticks((-1.0,0,1.0), ('',0,''))
xticks(linspace(0,10,11))
plt.show()