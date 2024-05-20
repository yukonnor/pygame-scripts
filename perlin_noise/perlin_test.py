# https://github.com/pvigier/perlin-numpy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from perlin_numpy import generate_perlin_noise_3d

np.random.seed(0)
noise = generate_perlin_noise_3d(
    (32, 40, 40), (1, 8, 8), tileable=(True, False, False)
    # (32, 256, 256), (1, 4, 4), tileable=(True, False, False)
)

fig = plt.figure()
images = [
    [plt.imshow(
        layer, cmap='gray', interpolation='lanczos', animated=True
    )]
    for layer in noise
]
animation_3d = animation.ArtistAnimation(fig, images, interval=50, blit=True)
plt.show()