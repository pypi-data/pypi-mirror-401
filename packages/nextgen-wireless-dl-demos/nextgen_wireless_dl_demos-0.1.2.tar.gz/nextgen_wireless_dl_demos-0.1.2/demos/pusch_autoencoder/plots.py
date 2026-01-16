# SPDX-License-Identifier: MIT
# Copyright (c) 2025–present Srikanth Pagadarai

"""
Visualization script for PUSCH autoencoder results.

This script generates publication-quality plots comparing the trained
autoencoder against baseline LMMSE performance for 32 BS antenna configuration:

1. **BLER Comparison**: Baseline (perfect/imperfect CSI) vs trained autoencoder
2. **BER Comparison**: Bit error rate analysis
3. **Training Loss Curve**: BCE loss evolution during training
4. **Constellation Evolution**: Intermediate snapshots at checkpoints
5. **Final Constellation**: Standard 16-QAM vs trained geometry
6. **Constellation Overlay**: Initial vs final with bit pattern labels

Prerequisites
-------------
Before running this script, you must have generated:

1. ``results/baseline_results_ant{num_bs_ant}.npz`` - from baseline.py
2. ``results/inference_results_ant{num_bs_ant}.npz`` - from inference.py
3. ``results/training_data_ant{num_bs_ant}.npz`` - from training.py
4. ``results/PUSCH_autoencoder_weights_ant{num_bs_ant}`` - from training.py
5. Checkpoint files at iterations 1000, 2000, 3000, 4000 (optional)

Output
------
All plots are saved to ``results/`` directory:

- ``bler_plot_{num_bs}bs_{num_bs_ant}bs_ant_x_{num_ue}ue_{num_ue_ant}ue_ant.png``: BLER comparison
- ``ber_plot_{num_bs}bs_{num_bs_ant}bs_ant_x_{num_ue}ue_{num_ue_ant}ue_ant.png``: BER comparison
- ``training_loss_ant{num_bs_ant}.png``: Loss curve with best iteration marked
- ``constellation_normalized_ant{num_bs_ant}.png``: Final trained vs standard 16-QAM
- ``constellation_overlay_ant{num_bs_ant}.png``: Initial vs final with bit labels
- ``constellation_iter_{N}_ant{num_bs_ant}.png``: Intermediate constellation snapshots

Usage
-----
Run from the repository root after baseline.py, training.py, and inference.py::

    python -m demos.pusch_autoencoder.plots

Interpretation Guide
--------------------
**BLER Plot**:

- Perfect CSI curve shows theoretical upper bound
- Gap between perfect and imperfect CSI is the "CSI penalty"
- Autoencoder should approach or exceed imperfect CSI baseline

**BER Plot**:

- Shows bit-level error rate (finer granularity than BLER)
- Useful for understanding uncoded performance
- Lower BER generally correlates with lower BLER after decoding

**Constellation Plot**:

- Significant point movement indicates channel adaptation
- Points should remain roughly symmetric (balanced I/Q)
- Minimum distance between points affects high-SNR performance
"""

import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from demos.pusch_autoencoder.src.config import Config

# get directory name of file
DEMO_DIR = os.path.dirname(os.path.abspath(__file__))


# =============================================================================
# Constellation Utilities
# =============================================================================
def normalize_constellation(points_r, points_i):
    """
    Apply centering and power normalization to constellation points.

    This matches the normalization in ``PUSCHTrainableTransmitter.get_normalized_constellation()``,
    ensuring consistent visualization regardless of how raw variables have drifted.

    Parameters
    ----------
    points_r : np.ndarray
        Real parts of constellation points.
    points_i : np.ndarray
        Imaginary parts of constellation points.

    Returns
    -------
    np.ndarray, complex128
        Normalized constellation with zero mean and unit average power.
    """
    points = points_r + 1j * points_i

    # Center: remove DC offset for balanced I/Q
    points = points - np.mean(points)

    # Normalize: scale to unit average power for fair comparison
    energy = np.mean(np.abs(points) ** 2)
    points = points / np.sqrt(energy)

    return points


def standard_16qam():
    """
    Generate standard Gray-coded 16-QAM constellation.

    Returns
    -------
    np.ndarray, complex128
        16 constellation points with unit average power.
    """
    levels = np.array([-3, -1, 1, 3])
    real, imag = np.meshgrid(levels, levels)
    points = (real.flatten() + 1j * imag.flatten()) / np.sqrt(10)
    return points


# Reference constellation for comparison
standard_const = standard_16qam()


# =========================================================================
# Configuration
# =========================================================================
_cfg = Config()
num_bs_ant = _cfg.num_bs_ant
batch_size = _cfg.batch_size
num_ue = _cfg.num_ue
num_ue_ant = _cfg.num_ue_ant
num_bs = _cfg.num_bs

ant_suffix = f"_ant{num_bs_ant}"

# =========================================================================
# Load Results Data
# =========================================================================
# Baseline results (from baseline.py)
baseline_path = os.path.join(DEMO_DIR, "results", f"baseline_results{ant_suffix}.npz")
if not os.path.exists(baseline_path):
    print(
        f"Warning: {baseline_path} not found. "
        f"Run baseline.py first. Skipping {num_bs_ant} antenna plots."
    )

# Autoencoder inference results (from inference.py)
inference_path = os.path.join(DEMO_DIR, "results", f"inference_results{ant_suffix}.npz")
if not os.path.exists(inference_path):
    print(
        f"Warning: {inference_path} not found. "
        f"Run inference.py first. Skipping {num_bs_ant} antenna plots."
    )

baseline_data = np.load(baseline_path)
inference_data = np.load(inference_path)
inference_ebno_db = inference_data["ebno_db"]


ebno_db = baseline_data["ebno_db"]
bler = baseline_data[
    "bler"
]  # Shape: [2, num_snr_points] - [perfect_csi, imperfect_csi]
inference_bler = inference_data["bler"]

# =========================================================================
# BLER Comparison Plot
# =========================================================================
# Compare baseline LMMSE (perfect/imperfect CSI) against trained autoencoder

# Extrapolate baseline at -0.5, 0.5, 1.5 dB for main plot
extra_ebno = np.array([-0.5, 0.5, 1.5])
extra_bler = np.zeros((2, len(extra_ebno)))  # [perfect_csi, imperfect_csi]

for idx in range(2):  # For both perfect and imperfect CSI
    extra_bler[idx] = np.interp(extra_ebno, ebno_db, bler[idx])

# Combine original and extrapolated points
combined_ebno = np.sort(np.concatenate([ebno_db, extra_ebno]))
combined_bler = np.zeros((2, len(combined_ebno)))
for idx in range(2):
    combined_bler[idx] = np.interp(combined_ebno, ebno_db, bler[idx])

fig, ax = plt.subplots(figsize=(8, 6))

# Main plot: zoomed view (-1 to 2 dB)
for idx, csi_label in enumerate(["(Perfect CSI)", "(Imperfect CSI)"]):
    # Filter points in range [-1, 2]
    mask = (combined_ebno >= -1) & (combined_ebno <= 2)
    ax.semilogy(
        combined_ebno[mask],
        combined_bler[idx][mask],
        marker="o",
        linestyle="-",
        label=f"Conventional Detector {csi_label}",
    )

ax.semilogy(
    inference_ebno_db,
    inference_bler,
    marker="x",
    linestyle="-",
    label="Neural MIMO Detector (Imperfect CSI)",
)
ax.set_xlabel("Eb/N0 [dB]")
ax.set_ylabel("BLER")
ax.set_title(f"PUSCH - BLER vs Eb/N0 ({num_bs_ant} BS Antennas)")
ax.set_xlim([-1, 2])
ax.grid(True, which="both")
ax.legend(loc="lower left", framealpha=0.7)

# Inset: full baseline range (-2 to 9 dB)
ax_inset = inset_axes(ax, width="40%", height="40%", loc="upper right")

for idx, csi_label in enumerate(["(Perfect CSI)", "(Imperfect CSI)"]):
    ax_inset.semilogy(
        ebno_db,
        bler[idx],
        marker="o",
        linestyle="-",
        linewidth=1,
        markersize=3,
    )

ax_inset.set_xlim([-2, 9])
ax_inset.set_xlabel("Eb/N0 [dB]", fontsize=8)
ax_inset.set_ylabel("BLER", fontsize=8)
ax_inset.tick_params(labelsize=7)
ax_inset.grid(True, which="both", alpha=0.3)
ax_inset.patch.set_alpha(0.7)  # Make inset background translucent

outfile = os.path.join(
    DEMO_DIR,
    "results",
    f"bler_plot_{num_bs}bs_{num_bs_ant}bs_ant_x_{num_ue}ue_{num_ue_ant}ue_ant.png",
)
fig.savefig(outfile, dpi=300, bbox_inches="tight")
plt.close(fig)
print(f"Saved BLER plot to {outfile}")

# =========================================================================
# BER Comparison Plot
# =========================================================================
# Compare baseline LMMSE (perfect/imperfect CSI) against trained autoencoder
# BER provides finer granularity than BLER for understanding bit-level performance
if "ber" in baseline_data and "ber" in inference_data:
    ber = baseline_data[
        "ber"
    ]  # Shape: [2, num_snr_points] - [perfect_csi, imperfect_csi]
    inference_ber = inference_data["ber"]

    # Extrapolate baseline at -0.5, 0.5, 1.5 dB for main plot
    extra_ebno = np.array([-0.5, 0.5, 1.5])
    extra_ber = np.zeros((2, len(extra_ebno)))  # [perfect_csi, imperfect_csi]

    for idx in range(2):  # For both perfect and imperfect CSI
        extra_ber[idx] = np.interp(extra_ebno, ebno_db, ber[idx])

    # Combine original and extrapolated points
    combined_ebno = np.sort(np.concatenate([ebno_db, extra_ebno]))
    combined_ber = np.zeros((2, len(combined_ebno)))
    for idx in range(2):
        combined_ber[idx] = np.interp(combined_ebno, ebno_db, ber[idx])

    fig, ax = plt.subplots(figsize=(8, 6))

    # Main plot: zoomed view (-1 to 2 dB)
    for idx, csi_label in enumerate(["(Perfect CSI)", "(Imperfect CSI)"]):
        # Filter points in range [-1, 2]
        mask = (combined_ebno >= -1) & (combined_ebno <= 2)
        ax.semilogy(
            combined_ebno[mask],
            combined_ber[idx][mask],
            marker="o",
            linestyle="-",
            label=f"Conventional Detector {csi_label}",
        )

    ax.semilogy(
        inference_ebno_db,
        inference_ber,
        marker="x",
        linestyle="-",
        label="Neural MIMO Detector (Imperfect CSI)",
    )
    ax.set_xlabel("Eb/N0 [dB]")
    ax.set_ylabel("BER")
    ax.set_title(f"PUSCH - BER vs Eb/N0 ({num_bs_ant} BS Antennas)")
    ax.set_xlim([-1, 2])
    ax.grid(True, which="both")
    ax.legend(loc="lower left", framealpha=0.7)

    # Inset: full baseline range (-2 to 9 dB)
    ax_inset = inset_axes(ax, width="40%", height="40%", loc="upper right")

    for idx, csi_label in enumerate(["(Perfect CSI)", "(Imperfect CSI)"]):
        ax_inset.semilogy(
            ebno_db,
            ber[idx],
            marker="o",
            linestyle="-",
            linewidth=1,
            markersize=3,
        )

    ax_inset.set_xlim([-2, 9])
    ax_inset.set_xlabel("Eb/N0 [dB]", fontsize=8)
    ax_inset.set_ylabel("BER", fontsize=8)
    ax_inset.tick_params(labelsize=7)
    ax_inset.grid(True, which="both", alpha=0.3)
    ax_inset.patch.set_alpha(0.7)  # Make inset background translucent

    ber_outfile = os.path.join(
        DEMO_DIR,
        "results",
        f"ber_plot_{num_bs}bs_{num_bs_ant}bs_ant_x_{num_ue}ue_{num_ue_ant}ue_ant.png",
    )
    fig.savefig(ber_outfile, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved BER plot to {ber_outfile}")
else:
    print(
        f"Warning: BER data not found in baseline or inference results. "
        f"Skipping BER plot for {num_bs_ant} antennas."
    )

# =========================================================================
# Load Training Data
# =========================================================================
training_data_path = os.path.join(DEMO_DIR, "results", f"training_data{ant_suffix}.npz")
if os.path.exists(training_data_path):
    training_data = np.load(training_data_path)
    loss_history = training_data["loss_history"]
    init_constellation = training_data["init_constellation"]
    final_constellation = training_data["final_constellation"]
    learned_permutation = training_data["learned_permutation"]
    has_learnable_labeling = bool(training_data["has_learnable_labeling"])

    # =====================================================================
    # Training Loss Plot
    # =====================================================================
    iterations_range = np.arange(len(loss_history))

    plt.figure(figsize=(10, 5))
    plt.plot(iterations_range, loss_history, linewidth=0.8)
    plt.xlabel("Iteration")
    plt.ylabel("Loss")
    plt.title(f"Training Loss ({num_bs_ant} BS Antennas)")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()

    loss_outfile = os.path.join(DEMO_DIR, "results", f"training_loss{ant_suffix}.png")
    plt.savefig(loss_outfile, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved loss plot to {loss_outfile}")

    # =====================================================================
    # Constellation Overlay Plot (Initial vs Final with Bit Labels)
    # =====================================================================
    # Create inverse mapping: which bit pattern is at each constellation point?
    inv_perm = np.empty_like(learned_permutation)
    for bit_pattern, const_idx in enumerate(learned_permutation):
        inv_perm[const_idx] = bit_pattern

    fig, ax = plt.subplots(figsize=(7, 7))

    ax.scatter(
        init_constellation.real,
        init_constellation.imag,
        s=25,
        marker="o",
        label="Initial",
        alpha=0.5,
    )
    ax.scatter(
        final_constellation.real,
        final_constellation.imag,
        s=40,
        marker="x",
        label="Trained",
        linewidths=2,
    )

    # Add bit pattern labels to trained constellation points
    for const_idx in range(len(final_constellation)):
        bit_pattern = inv_perm[const_idx]
        label = format(bit_pattern, "04b")
        ax.annotate(
            label,
            (final_constellation[const_idx].real, final_constellation[const_idx].imag),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=8,
            color="darkred",
            weight="bold",
            bbox=dict(
                boxstyle="round,pad=0.3", facecolor="white", alpha=0.7, edgecolor="none"
            ),
        )

    ax.axhline(0.0, linewidth=0.5, color="gray", linestyle="-")
    ax.axvline(0.0, linewidth=0.5, color="gray", linestyle="-")
    ax.set_aspect("equal", "box")
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.3)

    labeling_type = "Learned labeling" if has_learnable_labeling else "Fixed Gray"
    ax.set_title(
        f"Constellation: initial vs trained ({num_bs_ant} BS ant)\n{labeling_type}",
        fontsize=11,
    )
    ax.set_xlabel("In-phase")
    ax.set_ylabel("Quadrature")
    ax.legend(loc="upper right")

    fig.tight_layout()
    overlay_path = os.path.join(
        DEMO_DIR, "results", f"constellation_overlay{ant_suffix}.png"
    )
    plt.savefig(overlay_path, dpi=150)
    plt.close(fig)
    print(f"Saved constellation overlay plot to {overlay_path}")

    # =====================================================================
    # Labeling Matrix Visualization
    # =====================================================================
    if (
        "init_labeling_matrix" in training_data
        and "final_labeling_matrix" in training_data
    ):
        init_labeling = training_data["init_labeling_matrix"]
        final_labeling = training_data["final_labeling_matrix"]

        fig, axes = plt.subplots(1, 3, figsize=(16, 5))

        # Left: Initial labeling matrix (identity/Gray)
        im1 = axes[0].imshow(init_labeling, cmap="Blues", aspect="auto", vmin=0, vmax=1)
        axes[0].set_title(
            "Initial Labeling Matrix\n(Identity/Gray Coding)", fontsize=11
        )
        axes[0].set_xlabel("Constellation Point Index")
        axes[0].set_ylabel("Bit Pattern (Decimal)")
        axes[0].set_xticks(np.arange(16))
        axes[0].set_yticks(np.arange(16))

        # Add bit pattern labels on y-axis
        bit_labels = [format(i, "04b") for i in range(16)]
        axes[0].set_yticklabels(bit_labels, fontsize=8)

        # Add grid
        axes[0].set_xticks(np.arange(16) - 0.5, minor=True)
        axes[0].set_yticks(np.arange(16) - 0.5, minor=True)
        axes[0].grid(
            which="minor", color="gray", linestyle="-", linewidth=0.5, alpha=0.3
        )

        plt.colorbar(im1, ax=axes[0], fraction=0.046, pad=0.04)

        # Middle: Final learned labeling matrix
        im2 = axes[1].imshow(
            final_labeling, cmap="Blues", aspect="auto", vmin=0, vmax=1
        )
        axes[1].set_title("Learned Labeling Matrix\n(After Training)", fontsize=11)
        axes[1].set_xlabel("Constellation Point Index")
        axes[1].set_ylabel("Bit Pattern (Decimal)")
        axes[1].set_xticks(np.arange(16))
        axes[1].set_yticks(np.arange(16))
        axes[1].set_yticklabels(bit_labels, fontsize=8)

        axes[1].set_xticks(np.arange(16) - 0.5, minor=True)
        axes[1].set_yticks(np.arange(16) - 0.5, minor=True)
        axes[1].grid(
            which="minor", color="gray", linestyle="-", linewidth=0.5, alpha=0.3
        )

        plt.colorbar(im2, ax=axes[1], fraction=0.046, pad=0.04)

        # Right: Difference (absolute change)
        diff = np.abs(final_labeling - init_labeling)
        im3 = axes[2].imshow(diff, cmap="Reds", aspect="auto", vmin=0, vmax=1)
        axes[2].set_title("Labeling Change\n|Final - Initial|", fontsize=11)
        axes[2].set_xlabel("Constellation Point Index")
        axes[2].set_ylabel("Bit Pattern (Decimal)")
        axes[2].set_xticks(np.arange(16))
        axes[2].set_yticks(np.arange(16))
        axes[2].set_yticklabels(bit_labels, fontsize=8)

        axes[2].set_xticks(np.arange(16) - 0.5, minor=True)
        axes[2].set_yticks(np.arange(16) - 0.5, minor=True)
        axes[2].grid(
            which="minor", color="gray", linestyle="-", linewidth=0.5, alpha=0.3
        )

        plt.colorbar(im3, ax=axes[2], fraction=0.046, pad=0.04)

        # Add overall title
        labeling_changed = not np.array_equal(learned_permutation, np.arange(16))
        change_status = "Adapted from Gray" if labeling_changed else "Remained at Gray"
        fig.suptitle(
            f"Bit-to-Symbol Labeling Matrix ({num_bs_ant} BS Ant) - {change_status}",
            fontsize=13,
            fontweight="bold",
        )

        fig.tight_layout(rect=[0, 0, 1, 0.96])
        labeling_path = os.path.join(
            DEMO_DIR, "results", f"labeling_matrix{ant_suffix}.png"
        )
        plt.savefig(labeling_path, dpi=150)
        plt.close(fig)
        print(f"Saved labeling matrix plot to {labeling_path}")

        # Print analysis of labeling changes
        if labeling_changed:
            num_changed = np.sum(learned_permutation != np.arange(16))
            print(
                f"  Labeling analysis: {num_changed}/16 bit patterns mapped to different points"
            )
            print(f"  Total change magnitude: {np.sum(diff):.2f}")
else:
    print(f"Warning: {training_data_path} not found, skipping training-related plots.")

# =========================================================================
# Load Final Trained Weights
# =========================================================================
final_weights_path = os.path.join(
    DEMO_DIR, "results", f"PUSCH_autoencoder_weights{ant_suffix}"
)
if not os.path.exists(final_weights_path):
    print(f"Warning: {final_weights_path} not found, skipping constellation plots.")

with open(final_weights_path, "rb") as f:
    final_weights = pickle.load(f)

# =========================================================================
# Display Correction Scale Values
# =========================================================================
# These scales indicate how much the neural network deviates from classical LMMSE:
# - Values near 0: Neural corrections have minimal effect (classical dominates)
# - Large values: Neural network significantly modifies classical estimates
if "rx_weights" in final_weights:
    rx_weights = final_weights["rx_weights"]
    # Weight ordering matches PUSCHNeuralDetector.trainable_variables:
    # [h_correction_scale, err_var_correction_scale_raw, llr_correction_scale, ...nn_weights...]
    h_correction_scale = float(rx_weights[0])
    err_var_correction_scale_raw = float(rx_weights[1])
    llr_correction_scale = float(rx_weights[2])

    # Apply softplus to get actual scale: softplus(x) = log(1 + exp(x))
    # This transformation ensures the error variance scale is always positive
    err_var_correction_scale = np.log(1 + np.exp(err_var_correction_scale_raw))

    print("Correction scales:")
    print(f"  h_correction_scale: {h_correction_scale:.6f}")
    print(f"  err_var_correction_scale (softplus): {err_var_correction_scale:.6f}")
    print(f"  llr_correction_scale: {llr_correction_scale:.6f}")

# =========================================================================
# Final Constellation Plot (vs Standard 16-QAM)
# =========================================================================
# Compare trained constellation against standard 16-QAM
# tx_weights layout: [base_points_r, base_points_i, labeling_logits]
# Use the pre-computed normalized constellation from the weights dict
if "normalized_constellation" in final_weights:
    final_const = final_weights["normalized_constellation"]
else:
    # Fallback: reconstruct from base points (would need reflection logic)
    print("Warning: normalized_constellation not in weights, using raw values")
    final_const = normalize_constellation(
        final_weights["tx_weights"][0], final_weights["tx_weights"][1]
    )

# Extract learned permutation for bit labeling
if "learned_permutation" in final_weights:
    learned_permutation = final_weights["learned_permutation"]
else:
    # Fallback to Gray coding if permutation not available
    learned_permutation = np.arange(16)

# Create inverse mapping: symbol_index -> bit_pattern
bit_labels = [format(i, "04b") for i in range(16)]
symbol_to_bits = {
    int(symbol_idx): bit_labels[bit_pattern]
    for bit_pattern, symbol_idx in enumerate(learned_permutation)
}

fig, ax = plt.subplots(figsize=(6, 6))
ax.scatter(
    standard_const.real, standard_const.imag, s=40, marker="o", label="Standard 16-QAM"
)
ax.scatter(final_const.real, final_const.imag, s=40, marker="x", label="Trained")

# Add bit pattern labels to each trained constellation point
for idx, (x, y) in enumerate(zip(final_const.real, final_const.imag)):
    bit_pattern = symbol_to_bits[idx]
    ax.annotate(
        bit_pattern,
        xy=(x, y),
        xytext=(5, 5),  # Offset text slightly from point
        textcoords="offset points",
        fontsize=8,
        color="darkblue",
        bbox=dict(
            boxstyle="round,pad=0.3",
            facecolor="white",
            edgecolor="lightgray",
            alpha=0.7,
        ),
    )

ax.axhline(0, color="gray", linewidth=0.5)
ax.axvline(0, color="gray", linewidth=0.5)
ax.set_xlim([-1.5, 1.5])
ax.set_ylim([-1.5, 1.5])
ax.set_aspect("equal", "box")
ax.grid(True, linestyle="--", linewidth=0.5)
ax.set_xlabel("In-phase")
ax.set_ylabel("Quadrature")
ax.set_title(f"Normalized Constellation with Bit Mapping ({num_bs_ant} BS Ant)")
ax.legend()

const_outfile = os.path.join(
    DEMO_DIR, "results", f"constellation_normalized{ant_suffix}.png"
)
fig.savefig(const_outfile, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"Saved constellation plot to {const_outfile}")

# =========================================================================
# Constellation Evolution at Checkpoints
# =========================================================================
# Visualize how constellation geometry evolves during training
# Useful for understanding optimization dynamics and detecting problems
iterations = [1000, 2000, 3000, 4000]

for iteration in iterations:
    weights_path = os.path.join(
        DEMO_DIR,
        "results",
        f"PUSCH_autoencoder_weights_iter_{iteration}{ant_suffix}",
    )

    if not os.path.exists(weights_path):
        # print(f"Warning: {weights_path} not found, skipping.")
        continue

    with open(weights_path, "rb") as f:
        weights = pickle.load(f)

    # Use pre-computed normalized constellation from weights
    if "normalized_constellation" in weights:
        trained_const = weights["normalized_constellation"]
    else:
        # Fallback: reconstruct from base points
        trained_const = normalize_constellation(
            weights["tx_weights"][0], weights["tx_weights"][1]
        )

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.scatter(
        standard_const.real,
        standard_const.imag,
        s=40,
        marker="o",
        label="Standard 16-QAM",
    )
    ax.scatter(
        trained_const.real,
        trained_const.imag,
        s=40,
        marker="x",
        label=f"Iter {iteration}",
    )
    ax.axhline(0, color="gray", linewidth=0.5)
    ax.axvline(0, color="gray", linewidth=0.5)
    ax.set_aspect("equal", "box")
    ax.grid(True, linestyle="--", linewidth=0.5)
    ax.set_xlabel("In-phase")
    ax.set_ylabel("Quadrature")
    ax.set_title(f"Constellation at Iteration {iteration} ({num_bs_ant} BS Ant)")
    ax.legend()

    iter_outfile = os.path.join(
        DEMO_DIR, "results", f"constellation_iter_{iteration}{ant_suffix}.png"
    )
    fig.savefig(iter_outfile, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved constellation plot to {iter_outfile}")

print("\n" + "=" * 60)
print("Plot generation complete for all antenna configurations.")
print("=" * 60)
