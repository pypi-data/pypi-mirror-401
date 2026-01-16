# SPDX-License-Identifier: MIT
# Copyright (c) 2025–present Srikanth Pagadarai

import pytest
import tensorflow as tf
from sionna.phy.nr import PUSCHConfig
from demos.pusch_autoencoder.src.config import Config
from demos.pusch_autoencoder.src.pusch_trainable_transmitter import (
    PUSCHTrainableTransmitter,
)


def get_pusch_config(cfg):
    """Helper to create PUSCHConfig."""
    pusch_config = PUSCHConfig()
    pusch_config.carrier.subcarrier_spacing = cfg.subcarrier_spacing / 1000.0
    pusch_config.carrier.n_size_grid = cfg.num_prb
    pusch_config.num_antenna_ports = cfg.num_ue_ant
    pusch_config.num_layers = cfg.num_layers
    pusch_config.precoding = "codebook"
    pusch_config.tpmi = 1
    pusch_config.dmrs.dmrs_port_set = list(range(cfg.num_layers))
    pusch_config.dmrs.config_type = 1
    pusch_config.dmrs.length = 1
    pusch_config.dmrs.additional_position = 1
    pusch_config.dmrs.num_cdm_groups_without_data = 2
    pusch_config.tb.mcs_index = cfg.mcs_index
    pusch_config.tb.mcs_table = cfg.mcs_table
    return pusch_config


@pytest.mark.parametrize("training", [True, False])
def test_trainable_transmitter_initialization(training):
    """Test PUSCHTrainableTransmitter initialization with symmetric constellation."""
    cfg = Config()
    pusch_config = get_pusch_config(cfg)

    tx = PUSCHTrainableTransmitter(
        [pusch_config], output_domain="freq", training=training
    )

    # Check that BASE constellation variables are created (not full constellation)
    assert hasattr(tx, "_base_points_r")
    assert hasattr(tx, "_base_points_i")
    assert isinstance(tx._base_points_r, tf.Variable)
    assert isinstance(tx._base_points_i, tf.Variable)

    # For 16-QAM, we should have 4 base points (num_points // 4)
    expected_base_points = 4
    assert tx._base_points_r.shape[0] == expected_base_points
    assert tx._base_points_i.shape[0] == expected_base_points

    # Check trainability
    assert tx._base_points_r.trainable == training
    assert tx._base_points_i.trainable == training

    print(f"\n[Symmetric Trainable TX Init] Training={training}:")
    print(f"  Base constellation real: {tx._base_points_r.shape}")
    print(f"  Base constellation imag: {tx._base_points_i.shape}")
    print(f"  Trainable: {tx._base_points_r.trainable}")
    print(f"  Full constellation size: {tx._num_constellation_points}")


@pytest.mark.parametrize("training", [True, False])
def test_trainable_transmitter_forward(training):
    """Test PUSCHTrainableTransmitter forward pass."""
    cfg = Config()
    pusch_config = get_pusch_config(cfg)
    batch_size = 4

    tx = PUSCHTrainableTransmitter(
        [pusch_config], output_domain="freq", training=training
    )

    # Forward pass
    output = tx(batch_size)

    # The trainable transmitter returns (x_map, x, b, c) when return_bits=True (default)
    x_map, x, b, c = output
    assert x_map.shape[0] == batch_size
    assert x.shape[0] == batch_size
    assert b.shape[0] == batch_size
    assert c.shape[0] == batch_size

    print(f"\n[Symmetric Trainable TX Forward] Training={training}:")
    print(f"  x_map shape: {x_map.shape}")
    print(f"  x shape: {x.shape}")
    print(f"  b shape: {b.shape}")
    print(f"  c shape: {c.shape}")


def test_normalized_constellation():
    """Test constellation normalization with symmetry."""
    cfg = Config()
    pusch_config = get_pusch_config(cfg)

    tx = PUSCHTrainableTransmitter([pusch_config], output_domain="freq", training=True)

    # Get normalized constellation (should have full 16 points from 4 base points)
    constellation = tx.get_normalized_constellation()

    # Check shape: should be 16 points for 16-QAM
    assert constellation.shape[0] == 16

    # Check unit power (average energy should be 1)
    energy = tf.reduce_mean(tf.square(tf.abs(constellation)))

    print("\n[Constellation Normalization]:")
    print(f"  Constellation shape: {constellation.shape}")
    print(f"  Average energy: {float(energy):.6f} (should be ~1.0)")
    print(f"  Mean: {tf.reduce_mean(constellation)}")

    # Energy should be close to 1.0
    assert tf.abs(energy - 1.0) < 0.1


def test_symmetric_constellation_properties():
    """Test that the constellation maintains 4-fold symmetry."""
    cfg = Config()
    pusch_config = get_pusch_config(cfg)

    tx = PUSCHTrainableTransmitter([pusch_config], output_domain="freq", training=True)

    # Get full constellation
    constellation = tx.get_normalized_constellation()

    # For 16-QAM with our reflection scheme:
    # Indices [0:3]:   Q1 (I>0, Q>0) - base points
    # Indices [4:7]:   Q2 (I<0, Q>0) - Q-axis reflection
    # Indices [8:11]:  Q4 (I>0, Q<0) - I-axis reflection
    # Indices [12:15]: Q3 (I<0, Q<0) - origin reflection

    q1 = constellation[0:4]
    q2 = constellation[4:8]
    q4 = constellation[8:12]
    q3 = constellation[12:16]

    # Test I-axis symmetry: Q1 should be conjugate of Q4
    # i.e., q1[i] = conj(q4[i])
    i_axis_error = tf.reduce_mean(tf.abs(q1 - tf.math.conj(q4)))

    # Test Q-axis symmetry: Q1 should be -conjugate of Q2
    # i.e., q1[i] = -conj(q2[i])
    q_axis_error = tf.reduce_mean(tf.abs(q1 + tf.math.conj(q2)))

    # Test origin symmetry: Q1 should be -Q3
    # i.e., q1[i] = -q3[i]
    origin_error = tf.reduce_mean(tf.abs(q1 + q3))

    print("\n[Symmetry Verification]:")
    print(f"  I-axis symmetry error: {float(i_axis_error):.6e} (should be ~0)")
    print(f"  Q-axis symmetry error: {float(q_axis_error):.6e} (should be ~0)")
    print(f"  Origin symmetry error: {float(origin_error):.6e} (should be ~0)")

    # All symmetry errors should be very small (numerical precision)
    tolerance = 1e-5
    assert i_axis_error < tolerance, f"I-axis symmetry violated: {i_axis_error}"
    assert q_axis_error < tolerance, f"Q-axis symmetry violated: {q_axis_error}"
    assert origin_error < tolerance, f"Origin symmetry violated: {origin_error}"


def test_trainable_variables():
    """Test that trainable variables are correctly exposed (base points only)."""
    cfg = Config()
    pusch_config = get_pusch_config(cfg)

    # Training mode
    tx_train = PUSCHTrainableTransmitter(
        [pusch_config], output_domain="freq", training=True
    )
    train_vars = tx_train.trainable_variables

    # Should have 3 variables: base_points_r, base_points_i, labeling_logits
    assert len(train_vars) == 3
    assert all(isinstance(v, tf.Variable) for v in train_vars)
    assert all(v.trainable for v in train_vars)

    # First two should be base points (shape [4] for 16-QAM)
    assert train_vars[0].shape[0] == 4  # base_points_r
    assert train_vars[1].shape[0] == 4  # base_points_i
    # Third should be labeling logits (shape [16, 16] for 16-QAM)
    assert train_vars[2].shape == [16, 16]  # labeling_logits

    # Inference mode
    tx_infer = PUSCHTrainableTransmitter(
        [pusch_config], output_domain="freq", training=False
    )
    infer_vars = tx_infer.trainable_variables
    assert len(infer_vars) == 3
    assert not any(v.trainable for v in infer_vars)

    print("\n[Trainable Variables]:")
    print(f"  Training mode vars: {len(train_vars)} trainable")
    print(f"    Base real: {train_vars[0].shape}")
    print(f"    Base imag: {train_vars[1].shape}")
    print(f"    Labeling:  {train_vars[2].shape}")
    print(f"  Inference mode vars: {len(infer_vars)} non-trainable")


def test_geometry_vs_labeling_variables():
    """Test that geometry and labeling variables are correctly separated."""
    cfg = Config()
    pusch_config = get_pusch_config(cfg)

    tx = PUSCHTrainableTransmitter([pusch_config], output_domain="freq", training=True)

    geom_vars = tx.geometry_variables
    label_vars = tx.labeling_variables

    # Geometry should be 2 variables (real and imag)
    assert len(geom_vars) == 2
    assert geom_vars[0].shape[0] == 4  # base points
    assert geom_vars[1].shape[0] == 4

    # Labeling should be 1 variable
    assert len(label_vars) == 1
    assert label_vars[0].shape == [16, 16]

    print("\n[Variable Separation]:")
    print(f"  Geometry vars: {len(geom_vars)}")
    print(f"    {geom_vars[0].name}: {geom_vars[0].shape}")
    print(f"    {geom_vars[1].name}: {geom_vars[1].shape}")
    print(f"  Labeling vars: {len(label_vars)}")
    print(f"    {label_vars[0].name}: {label_vars[0].shape}")


def test_constellation_update_during_call():
    """Test that constellation is updated with normalized values during call."""
    cfg = Config()
    pusch_config = get_pusch_config(cfg)
    batch_size = 2

    tx = PUSCHTrainableTransmitter([pusch_config], output_domain="freq", training=True)

    # Modify base constellation variables (this should propagate to full constellation)
    tx._base_points_r.assign(tx._base_points_r * 2.0)
    tx._base_points_i.assign(tx._base_points_i * 2.0)

    # Call should normalize internally
    _ = tx(batch_size)

    # Get the constellation from the mapper (which should be normalized)
    constellation = tx._constellation.points

    # Check that it's normalized (unit power)
    energy = tf.reduce_mean(tf.square(tf.abs(constellation)))

    print("\n[Constellation Update]:")
    print(f"  Energy after scaling: {float(energy):.6f}")

    assert tf.abs(energy - 1.0) < 0.1


def test_symmetry_preserved_during_training():
    """Test that symmetry is preserved when base points are modified."""
    cfg = Config()
    pusch_config = get_pusch_config(cfg)

    tx = PUSCHTrainableTransmitter([pusch_config], output_domain="freq", training=True)

    # Modify base points
    new_base_r = tf.constant([0.5, 0.7, 0.3, 0.9], dtype=tx._base_points_r.dtype)
    new_base_i = tf.constant([0.6, 0.4, 0.8, 0.2], dtype=tx._base_points_i.dtype)

    tx._base_points_r.assign(new_base_r)
    tx._base_points_i.assign(new_base_i)

    # Get normalized constellation
    constellation = tx.get_normalized_constellation()

    # Extract quadrants
    q1 = constellation[0:4]
    q2 = constellation[4:8]
    q4 = constellation[8:12]
    q3 = constellation[12:16]

    # Verify symmetry is still maintained
    i_axis_error = tf.reduce_mean(tf.abs(q1 - tf.math.conj(q4)))
    q_axis_error = tf.reduce_mean(tf.abs(q1 + tf.math.conj(q2)))
    origin_error = tf.reduce_mean(tf.abs(q1 + q3))

    print("\n[Symmetry After Modification]:")
    print(f"  I-axis error: {float(i_axis_error):.6e}")
    print(f"  Q-axis error: {float(q_axis_error):.6e}")
    print(f"  Origin error: {float(origin_error):.6e}")

    tolerance = 1e-5
    assert i_axis_error < tolerance
    assert q_axis_error < tolerance
    assert origin_error < tolerance


def test_random_symmetric_constellation_generation():
    """Test the static method for generating random symmetric constellations."""
    num_points = 16

    # Generate with seed for reproducibility
    constellation1 = PUSCHTrainableTransmitter.generate_random_symmetric_constellation(
        num_points, seed=42
    )
    constellation2 = PUSCHTrainableTransmitter.generate_random_symmetric_constellation(
        num_points, seed=42
    )

    # Should be identical with same seed
    diff = tf.reduce_max(tf.abs(constellation1 - constellation2))
    assert diff < 1e-6

    # Verify unit power
    energy = tf.reduce_mean(tf.abs(constellation1) ** 2)
    assert tf.abs(energy - 1.0) < 0.1

    # Verify symmetry
    q1 = constellation1[0:4]
    q2 = constellation1[4:8]
    q4 = constellation1[8:12]
    q3 = constellation1[12:16]

    i_axis_error = tf.reduce_mean(tf.abs(q1 - tf.math.conj(q4)))
    q_axis_error = tf.reduce_mean(tf.abs(q1 + tf.math.conj(q2)))
    origin_error = tf.reduce_mean(tf.abs(q1 + q3))

    print("\n[Random Symmetric Generation]:")
    print(f"  Reproducibility check: {float(diff):.6e}")
    print(f"  Unit power: {float(energy):.6f}")
    print(
        f"  Symmetry errors: I={float(i_axis_error):.6e}, Q={float(q_axis_error):.6e}, Origin={float(origin_error):.6e}"
    )

    tolerance = 1e-5
    assert i_axis_error < tolerance
    assert q_axis_error < tolerance
    assert origin_error < tolerance
