from typing import Any, Optional

import numpy as np
from sklearn.preprocessing import normalize

__all__ = [
    "choose_gamma",
    "build_temporal_tags",
    "augment_dictionary_framewise",
    "augment_dictionary_pixelwise",
]


def choose_gamma(
    y: np.ndarray,
    X: np.ndarray,
    delta_w: float,
    tau: float = 0.05,
    safety: float = 1.25,
    mode: str = "global",
) -> float:
    """
    Compute a global scale gamma that guarantees a forward step in OMP under the inequality:
        alpha_t * gamma^2 * (w_{t+1} - w_t) > 2 * M_t
    where M_t bounds image-block correlations.

    Parameters
    ----------
    y : (P,) array
        Target vector (concatenated signal for the current sample/patch).
    X : (P, N) array
        Dictionary atoms as columns; should be column-normalized already or will be.
    delta_w : float
        Minimum forward increment, e.g., rho if w_t = 1 + rho t.
    tau : float, default=0.05
        Minimum coefficient magnitude considered meaningful.
    safety : float, default=1.25
        Multiplicative margin > 1.
    mode : {"global","empirical"}
        "global": uses ||y||_2 as a loose bound on M_t;
        "empirical": uses max_k |<y, x_k>| from the initial dictionary.

    Returns
    -------
    gamma : float
    """
    if mode == "empirical":
        # Ensure columns are normalized for a fair bound
        Xn = normalize(X, axis=0)
        M0 = float(np.max(np.abs(Xn.T @ y)))
    else:
        M0 = float(np.linalg.norm(y))
    if delta_w <= 0:
        raise ValueError("delta_w must be > 0 (use increasing weights w_t).")
    if tau <= 0:
        raise ValueError("tau must be > 0.")
    gamma = np.sqrt((2.0 * M0 * safety) / (tau * delta_w))
    return float(gamma)


def build_temporal_tags(N: int, rho: float = 0.02) -> tuple[np.ndarray, np.ndarray]:
    """
    Build two-hot temporal tags v_t = sqrt(w_t) e_t + sqrt(w_{t+1}) e_{t+1}
    with w_t = 1 + rho * t. Returns the tag matrix V whose column t is v_t,
    and the weight vector w (length N+1, with the last entry unused except for sqrt).

    Parameters
    ----------
    N : int
        Number of frames / atoms.
    rho : float, default=0.02
        Linear weight increment; also equals min (w_{t+1} - w_t).

    Returns
    -------
    V : (N, N) array
        Tag matrix; column t is v_t.
    w : (N+1,) array
        Weight schedule w_t = 1 + rho t.
    """
    if N <= 0:
        raise ValueError("N must be positive.")
    if rho <= 0:
        raise ValueError("rho must be > 0 for a strict forward advantage.")
    w = 1.0 + rho * np.arange(N + 1, dtype=float)  # w_0..w_N (w_N used only under sqrt)
    V = np.zeros((N, N), dtype=float)
    for t in range(N):
        V[t, t] += np.sqrt(w[t])
        if t + 1 < N:
            V[t + 1, t] += np.sqrt(w[t + 1])
    return V, w


def _prep_framewise_matrix(
    ycbcr_series: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Framewise representation: each frame is a 3-vector [Y, Cb, Cr].
    Input shape: (N_frames, 3). Returns X (3, N) and a normalizer for columns.

    Parameters
    ----------
    ycbcr_series : (N, 3) array
        Y, Cb, Cr per frame.

    Returns
    -------
    X : (3, N) array
        Columns are unit-norm 3D vectors per frame.
    norms : (N,) array
        Original column norms before normalization.
    """
    if ycbcr_series.ndim != 2 or ycbcr_series.shape[1] != 3:
        raise ValueError("Expected shape (N_frames, 3) for ycbcr_series.")
    X: np.ndarray = ycbcr_series.astype(float).T  # (3, N)
    norms = np.linalg.norm(X, axis=0) + 1e-12
    X = X / norms
    return X, norms


def augment_dictionary_framewise(
    ycbcr_series: np.ndarray,
    target_vec: np.ndarray,
    rho: float = 0.02,
    tau: float = 0.05,
    safety: float = 1.25,
    gamma: Optional[float] = None,
    mode: str = "global",
    renormalize: bool = True,
) -> tuple[np.ndarray, np.ndarray, float, dict[str, Any]]:
    """
    Build the augmented dictionary for OMP when each frame is a 3-vector [Y, Cb, Cr].

    Parameters
    ----------
    ycbcr_series : (N, 3) array
        Basis video reduced to framewise YCbCr triplets.
    target_vec : (3,) array
        Target frame triplet [Y, Cb, Cr] for the block you're encoding.
    rho, tau, safety, gamma, mode : see choose_gamma/build_temporal_tags
    renormalize : bool
        If True, column-normalize the augmented dictionary (recommended).

    Returns
    -------
    X_aug : ((3+N), N) array
        Augmented dictionary.
    y_aug : (3+N,) array
        Augmented target (zeros in tag coords).
    gamma : float
        The scale actually used.
    meta : dict
        Extra info: N, rho, delta_w, norms, V, w.
    """
    X, norms = _prep_framewise_matrix(ycbcr_series)  # (3, N)
    N = X.shape[1]

    # Target vector normalization to match dictionary scaling
    y = np.asarray(target_vec, dtype=float).reshape(3)
    y_norm = y / (np.linalg.norm(y) + 1e-12)

    V, w = build_temporal_tags(N, rho=rho)
    delta_w = float(np.min(np.diff(w)))  # equals rho

    if gamma is None:
        gamma = choose_gamma(y_norm, X, delta_w, tau=tau, safety=safety, mode=mode)

    X_aug = np.vstack([X, gamma * V])  # ((3+N), N)
    y_aug = np.concatenate([y_norm, np.zeros(N)])

    if renormalize:
        X_aug = normalize(X_aug, axis=0)

    meta = {
        "N": N,
        "rho": rho,
        "delta_w": delta_w,
        "norms": norms,
        "V": V,
        "w": w,
        "gamma": gamma,
    }
    return X_aug, y_aug, float(gamma), meta


def augment_dictionary_pixelwise(
    frames_ycbcr: np.ndarray,
    target_frame: np.ndarray,
    rho: float = 0.02,
    tau: float = 0.05,
    safety: float = 1.25,
    gamma: Optional[float] = None,
    mode: str = "global",
    renormalize: bool = True,
) -> tuple[np.ndarray, np.ndarray, float, dict[str, Any]]:
    """
    Pixelwise representation for completeness (if later you move from 3 features per frame to full images).
    Input frames shape: (N, H, W, 3). Target: (H, W, 3).
    This flattens to P = H*W*3 per column and applies the same temporal tags.

    Returns X_aug ((P+N), N), y_aug (P+N,), gamma, meta
    """
    if frames_ycbcr.ndim != 4 or frames_ycbcr.shape[-1] == 0:
        raise ValueError("frames_ycbcr must be (N, H, W, 3).")
    N, H, W, C = frames_ycbcr.shape
    if C != 3:
        raise ValueError("Expected 3 channels (YCbCr).")

    X: np.ndarray = frames_ycbcr.reshape(N, -1).T.astype(float)  # (P, N)
    X = normalize(X, axis=0)
    y: np.ndarray = target_frame.reshape(-1).astype(float)
    y = y / (np.linalg.norm(y) + 1e-12)

    V, w = build_temporal_tags(N, rho=rho)
    delta_w = float(np.min(np.diff(w)))

    if gamma is None:
        gamma = choose_gamma(y, X, delta_w, tau=tau, safety=safety, mode=mode)

    X_aug = np.vstack([X, gamma * V])  # ((P+N), N)
    y_aug = np.concatenate([y, np.zeros(N)])

    if renormalize:
        X_aug = normalize(X_aug, axis=0)

    meta = {
        "N": N,
        "rho": rho,
        "delta_w": delta_w,
        "H": H,
        "W": W,
        "V": V,
        "w": w,
        "gamma": gamma,
    }
    return X_aug, y_aug, float(gamma), meta
