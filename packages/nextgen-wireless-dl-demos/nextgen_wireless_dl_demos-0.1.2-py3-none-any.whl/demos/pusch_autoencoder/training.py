# SPDX-License-Identifier: MIT
# Copyright (c) 2025–present Srikanth Pagadarai

"""
End-to-end training script for PUSCH autoencoder with neural detection.

This script trains the joint transmitter-receiver autoencoder system,
optimizing both the constellation geometry and the neural MIMO detector
to minimize Binary Cross-Entropy (BCE) loss on coded bits.

Architecture
------------
The autoencoder consists of:

- **Transmitter**: Trainable 16-QAM constellation (16 complex points)
- **Receiver**: Neural MIMO detector with:
  - Shared backbone (4 ResBlocks)
  - Channel estimation refinement head
  - Detection continuation network (6 ResBlocks)
  - Three trainable correction scales (h, err_var, LLR)

Training Strategy
-----------------
- **Gradient accumulation**: 16 micro-batches averaged before update
  to reduce gradient variance and enable larger effective batch sizes.
- **Separate optimizers**: TX, RX scales, and RX NN weights use different
  learning rates (1e-2, 1e-2, 1e-4 respectively with cosine decay).
- **SNR curriculum**: Random Eb/N0 in [-2, 10] dB per batch for robustness
  across operating conditions.

Output
------
Results are saved to ``results/`` directory with antenna suffix:

- ``PUSCH_autoencoder_weights_ant{num_bs_ant}``: Final TX/RX weights (pickle)
- ``training_data_ant{num_bs_ant}.npz``: All training data for visualization
- Checkpoints every 1000 iterations

Usage
-----
Run from the repository root::

    python -m demos.pusch_autoencoder.training
    python -m demos.pusch_autoencoder.training --num_bs_ant 32
"""

import os
import pickle
import argparse
import tensorflow as tf
from demos.pusch_autoencoder.src.cir_manager import CIRManager
from demos.pusch_autoencoder.src.system import PUSCHLinkE2E
from demos.pusch_autoencoder.src.config import Config
import numpy as np

import time

start = time.time()

# get directory name of file
DEMO_DIR = os.path.dirname(os.path.abspath(__file__))


# =============================================================================
# Command-Line Argument Parsing
# =============================================================================
parser = argparse.ArgumentParser(
    description="Train PUSCH autoencoder with neural detection."
)
parser.add_argument(
    "--num_bs_ant",
    type=int,
    default=32,
    help="Number of BS antennas (default: 32)",
)

args = parser.parse_args()
num_bs_ant = args.num_bs_ant

print(f"Number of BS antennas: {num_bs_ant}")


# =============================================================================
# System Configuration and Channel Model
# =============================================================================
_cfg = Config(num_bs_ant=num_bs_ant)
batch_size = _cfg.batch_size

# Load MU-MIMO grouped CIR data (4 UEs per sample)
# This is different from baseline.py which uses CIRDataset for on-demand sampling
cir_manager = CIRManager(config=_cfg)
channel_model = cir_manager.load_from_tfrecord(group_for_mumimo=True)


# =============================================================================
# Model Instantiation and Initial Verification
# =============================================================================
# Create E2E model in training mode (returns BCE loss, not decoded bits)
ebno_db_test = tf.fill([batch_size], 10.0)
model = PUSCHLinkE2E(
    channel_model, perfect_csi=False, use_autoencoder=True, training=True, config=_cfg
)

# Verify forward pass works and inspect model structure
loss = model(batch_size, ebno_db_test)
print("  Initial forward-pass loss:", loss.numpy())
print("  Trainable variable count:", len(model.trainable_variables))
for v in model.trainable_variables[:5]:
    print("   ", v.name, v.shape)

# Snapshot initial constellation for before/after comparison
# Get the full normalized constellation (computed from 4 symmetric base points)
init_constellation = tf.identity(
    model._pusch_transmitter.get_normalized_constellation()
)

# Snapshot initial labeling matrix (for visualization)
if hasattr(model._pusch_transmitter, "get_soft_labeling_matrix"):
    init_labeling_matrix = tf.identity(
        model._pusch_transmitter.get_soft_labeling_matrix(hard=True)
    )
else:
    # Fallback: identity matrix (standard Gray coding)
    init_labeling_matrix = tf.eye(16, dtype=tf.float32)

# Save raw base points (Q1 quadrant only for symmetric constellation)
init_base_real = tf.identity(model._pusch_transmitter._base_points_r)
init_base_imag = tf.identity(model._pusch_transmitter._base_points_i)


# =============================================================================
# Variable Grouping for Separate Learning Rates
# =============================================================================
# Different components benefit from different learning rates:
# - TX constellation: slow updates to allow RX to adapt
# - RX correction scales: fast updates to find good operating points
# - RX NN weights: moderate updates for stable convergence

tx_vars = model._pusch_transmitter.trainable_variables
rx_vars_all = model._pusch_receiver.trainable_variables

# Neural detector returns variables in specific order (see PUSCHNeuralDetector):
# [h_correction_scale, err_var_correction_scale_raw, llr_correction_scale, ...conv weights...]
rx_scale_vars = rx_vars_all[:3]
nn_rx_vars = rx_vars_all[3:]

print("\n=== Variable groups ===")
print(f"TX vars: {len(tx_vars)}")
for v in tx_vars:
    print(f"  {v.name}: {v.shape}")

print(f"\nRX Scale vars: {len(rx_scale_vars)}")
for v in rx_scale_vars:
    print(f"  {v.name}: {v.shape}")

print(f"\nNN RX vars: {len(nn_rx_vars)} (showing first 5)")
for v in nn_rx_vars[:5]:
    print(f"  {v.name}: {v.shape}")
print("=== End variable groups ===\n")

# Combined list for gradient computation (order matters for slicing)
all_vars = tx_vars + rx_scale_vars + nn_rx_vars


# =============================================================================
# Gradient Sanity Check
# =============================================================================
# Verify gradients flow to all variable groups before starting long training.
# This catches issues like disconnected computation graphs or None gradients.
print("\n=== Single-step gradient sanity check ===")

dbg_batch_size = 4
dbg_ebno = tf.fill([dbg_batch_size], 10.0)

with tf.GradientTape() as tape:
    loss_dbg = model(dbg_batch_size, dbg_ebno)

all_grads = tape.gradient(loss_dbg, all_vars)

# Slice gradients to match variable groups
n_tx = len(tx_vars)
n_scales = len(rx_scale_vars)

grads_tx = all_grads[:n_tx]
grads_scales = all_grads[n_tx : n_tx + n_scales]
grads_rx_nn = all_grads[n_tx + n_scales :]

# Print gradient norms to verify flow (None = disconnected, 0 = vanishing)
print("\nTransmitter gradients:")
for v, g in zip(tx_vars, grads_tx):
    g_norm = 0.0 if g is None else float(tf.norm(g).numpy())
    print(f"  {v.name:40s} grad_norm = {g_norm:.3e}")

print("\nReceiver correction scale gradients:")
for v, g in zip(rx_scale_vars, grads_scales):
    g_norm = 0.0 if g is None else float(tf.norm(g).numpy())
    print(f"  {v.name:40s} grad_norm = {g_norm:.3e}")

print("\nReceiver NN gradients (first 5):")
for v, g in zip(nn_rx_vars[:5], grads_rx_nn[:5]):
    g_norm = 0.0 if g is None else float(tf.norm(g).numpy())
    print(f"  {v.name:40s} grad_norm = {g_norm:.3e}")

print("=== End gradient sanity check ===\n")


# =============================================================================
# Training Hyperparameters
# =============================================================================
ebno_db_min = -1.0
ebno_db_max = 2.0
training_batch_size = batch_size
num_training_iterations = 5000

# Cosine decay schedules: start high, decay to 1% of initial LR
# TX and scales get higher LR (1e-2) for faster initial adaptation
# NN weights get lower LR (1e-4) to avoid disrupting pretrained-like behavior
lr_schedule_tx = tf.keras.optimizers.schedules.CosineDecay(
    initial_learning_rate=1e-2,
    decay_steps=num_training_iterations,
    alpha=0.01,
)
lr_schedule_rx_scales = tf.keras.optimizers.schedules.CosineDecay(
    initial_learning_rate=1e-2,
    decay_steps=num_training_iterations,
    alpha=0.01,
)
lr_schedule_rx_nn = tf.keras.optimizers.schedules.CosineDecay(
    initial_learning_rate=1e-4,
    decay_steps=num_training_iterations,
    alpha=0.01,
)

optimizer_tx = tf.keras.optimizers.Adam(learning_rate=lr_schedule_tx)
optimizer_scales = tf.keras.optimizers.Adam(learning_rate=lr_schedule_rx_scales)
optimizer_rx = tf.keras.optimizers.Adam(learning_rate=lr_schedule_rx_nn)

# [training-core-start]
# =============================================================================
# Gradient Computation Functions
# =============================================================================
# Gradient accumulation: 16 micro-batches averaged to reduce variance
# This simulates larger batch training without memory overhead
accumulation_steps = 16


@tf.function
def compute_grads_single():
    """
    Compute gradients for a single random SNR micro-batch.

    Returns
    -------
    loss : tf.Tensor
        BCE loss for this micro-batch.
    grads : list of tf.Tensor
        Gradients for all trainable variables.
    """
    ebno_db = tf.random.uniform(
        [training_batch_size], minval=ebno_db_min, maxval=ebno_db_max
    )
    with tf.GradientTape() as tape:
        loss = model(training_batch_size, ebno_db)
    grads = tape.gradient(loss, all_vars)
    return loss, grads


def compute_accumulated_grads():
    """
    Compute gradients accumulated over multiple micro-batches.

    Averages gradients from accumulation_steps forward passes to reduce
    variance. This simulates larger batch training without memory overhead.

    Returns
    -------
    avg_loss : tf.Tensor
        Mean BCE loss over all micro-batches.
    grads_tx : list of tf.Tensor
        Averaged gradients for transmitter variables.
    grads_scales : list of tf.Tensor
        Averaged gradients for correction scale variables.
    grads_rx_nn : list of tf.Tensor
        Averaged gradients for neural network weight variables.
    """
    accumulated_grads = [tf.zeros_like(v) for v in all_vars]
    total_loss = 0.0

    for _ in range(accumulation_steps):
        loss, grads = compute_grads_single()
        accumulated_grads = [ag + g for ag, g in zip(accumulated_grads, grads)]
        total_loss += loss

    # Average over accumulation steps
    accumulated_grads = [g / accumulation_steps for g in accumulated_grads]
    avg_loss = total_loss / accumulation_steps

    # Split into variable groups for separate optimizer application
    grads_tx = accumulated_grads[:n_tx]
    grads_scales = accumulated_grads[n_tx : n_tx + n_scales]
    grads_rx_nn = accumulated_grads[n_tx + n_scales :]

    return avg_loss, grads_tx, grads_scales, grads_rx_nn


# =============================================================================
# Main Training Loop
# =============================================================================
loss_history = []

# Suffix for all output files
ant_suffix = f"_ant{num_bs_ant}"

print(f"Starting training for {num_training_iterations} iterations...")
print("  TX LR: 1e-2, RX Scales LR: 1e-2, RX NN LR: 1e-4")
print(f"  Output files will have suffix: {ant_suffix}")

for i in range(num_training_iterations):
    avg_loss, grads_tx, grads_scales, grads_rx_nn = compute_accumulated_grads()
    loss_value = float(avg_loss.numpy())
    loss_history.append(loss_value)

    # Simultaneous update: all variable groups updated together
    optimizer_tx.apply_gradients(zip(grads_tx, tx_vars))
    optimizer_scales.apply_gradients(zip(grads_scales, rx_scale_vars))
    optimizer_rx.apply_gradients(zip(grads_rx_nn, nn_rx_vars))

    # Progress display (overwrite same line)
    print(
        "Iteration {}/{}  BCE: {:.4f}".format(
            i + 1, num_training_iterations, loss_value
        ),
        end="\r",
        flush=True,
    )

    # Periodic checkpointing to resume from crashes
    if (i + 1) % 1000 == 0:
        os.makedirs(os.path.join(DEMO_DIR, "results"), exist_ok=True)
        save_path = os.path.join(
            DEMO_DIR, "results", f"PUSCH_autoencoder_weights_iter_{i + 1}{ant_suffix}"
        )

        # Store both raw variables and normalized constellation
        normalized_const = (
            model._pusch_transmitter.get_normalized_constellation().numpy()
        )
        weights_dict = {
            "tx_weights": [
                v.numpy() for v in model._pusch_transmitter.trainable_variables
            ],
            "rx_weights": [
                v.numpy() for v in model._pusch_receiver.trainable_variables
            ],
            "tx_names": [v.name for v in model._pusch_transmitter.trainable_variables],
            "rx_names": [v.name for v in model._pusch_receiver.trainable_variables],
            "normalized_constellation": normalized_const,
        }
        with open(save_path, "wb") as f:
            pickle.dump(weights_dict, f)
        print(f"\n[Checkpoint] Saved weights at iteration {i + 1} -> {save_path}")
# [training-core-end]

print()  # Newline after progress display


# =============================================================================
# Save Final Results
# =============================================================================
os.makedirs(os.path.join(DEMO_DIR, "results"), exist_ok=True)

# Get final constellation (normalized)
final_constellation = model._pusch_transmitter.get_normalized_constellation().numpy()

# Get learned labeling permutation if available
if hasattr(model._pusch_transmitter, "get_soft_labeling_matrix"):
    # Get hard assignment (argmax of permutation matrix)
    final_labeling_matrix = model._pusch_transmitter.get_soft_labeling_matrix(
        hard=True
    ).numpy()
    # Extract permutation: which constellation point is assigned to each bit pattern
    learned_permutation = np.argmax(final_labeling_matrix, axis=1)
    has_learnable_labeling = True
else:
    # Fallback: identity permutation (standard Gray coding)
    final_labeling_matrix = np.eye(16)
    learned_permutation = np.arange(16)
    has_learnable_labeling = False

# Save all training data to a single .npz file for plots.py
training_data_path = os.path.join(DEMO_DIR, "results", f"training_data{ant_suffix}.npz")
np.savez(
    training_data_path,
    loss_history=np.array(loss_history),
    init_constellation=init_constellation.numpy(),
    final_constellation=final_constellation,
    learned_permutation=learned_permutation,
    has_learnable_labeling=has_learnable_labeling,
    num_training_iterations=num_training_iterations,
    init_labeling_matrix=init_labeling_matrix.numpy(),
    final_labeling_matrix=final_labeling_matrix,
)
print(f"Saved training data to: {training_data_path}")

# Also save loss history separately for backward compatibility
loss_path = os.path.join(DEMO_DIR, "results", f"training_loss{ant_suffix}.npy")
np.save(loss_path, np.array(loss_history))
print(f"Saved loss history to: {loss_path}")

# Save final weights
weights_path = os.path.join(
    DEMO_DIR, "results", f"PUSCH_autoencoder_weights{ant_suffix}"
)

weights_dict = {
    "tx_weights": [v.numpy() for v in model._pusch_transmitter.trainable_variables],
    "rx_weights": [v.numpy() for v in model._pusch_receiver.trainable_variables],
    "tx_names": [v.name for v in model._pusch_transmitter.trainable_variables],
    "rx_names": [v.name for v in model._pusch_receiver.trainable_variables],
    "normalized_constellation": final_constellation,
}
with open(weights_path, "wb") as f:
    pickle.dump(weights_dict, f)

print(
    f"Saved {len(weights_dict['tx_weights'])} TX and "
    f"{len(weights_dict['rx_weights'])} RX weight arrays to: {weights_path}"
)

# Print final correction scale values for analysis
# These indicate how much the neural network deviates from classical LMMSE
print("\nFinal correction scales:")
h_scale = float(rx_scale_vars[0].numpy())
err_var_scale_raw = float(rx_scale_vars[1].numpy())
err_var_scale = float(np.log(1 + np.exp(err_var_scale_raw)))  # softplus
llr_scale = float(rx_scale_vars[2].numpy())
print(f"  h_correction_scale: {h_scale:.6f}")
print(f"  err_var_correction_scale (softplus): {err_var_scale:.6f}")
print(f"  llr_correction_scale: {llr_scale:.6f}")

# Print labeling information for analysis
if has_learnable_labeling:
    print("\nLearned bit-to-symbol mapping:")
    # Check if labeling changed from identity (Gray code)
    is_identity = np.array_equal(learned_permutation, np.arange(16))
    if is_identity:
        print("  Labeling remained at identity (Gray code)")
    else:
        print("  Labeling adapted from Gray code:")
        # Show a few examples of the mapping
        for i in [0, 5, 10, 15]:
            bit_str = format(i, "04b")
            print(
                f"    Bit pattern {bit_str} (#{i}) -> constellation point #{learned_permutation[i]}"
            )

print(f"\nTotal training time: {time.time() - start:.1f} seconds")
print("\n" + "=" * 60)
print("Training complete!")
print("Run 'python -m demos.pusch_autoencoder.plots' to generate visualizations.")
print("=" * 60)
