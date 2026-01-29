import numpy as np
from sklearn.linear_model import OrthogonalMatchingPursuit

from temporal_omp_aug import augment_dictionary_framewise

# Demo: 20 frames, each frame summarized by [Y, Cb, Cr]
rng = np.random.default_rng(7)
N = 20
series = rng.normal(size=(N, 3))
# Target between frames 5 and 6
target = series[5] + 0.2 * (series[6] - series[5])

X_aug, y_aug, gamma, meta = augment_dictionary_framewise(
    series, target, rho=0.02, tau=0.05, safety=1.25, gamma=None, mode="empirical"
)

omp = OrthogonalMatchingPursuit(n_nonzero_coefs=3)
omp.fit(X_aug, y_aug)
coef = omp.coef_
support = np.flatnonzero(coef)
print("Chosen support:", support)
print("gamma used:", gamma)
