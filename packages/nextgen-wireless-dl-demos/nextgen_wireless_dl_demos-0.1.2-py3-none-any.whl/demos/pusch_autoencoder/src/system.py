# SPDX-License-Identifier: MIT
# Copyright (c) 2025–present Srikanth Pagadarai

"""
End-to-end PUSCH link simulation for autoencoder training and evaluation.

Provides the core class that connects trainable transmitter and receiver components
through a realistic ray-traced channel. Supports both baseline (classical LMMSE)
and autoencoder (neural detector with learnable geometry and labeling) configurations.

The system implements the full uplink signal processing chain:
TX bits -> Encoding -> Modulation -> OFDM -> Channel -> OFDM Rx -> Detection -> Decoding
"""

import numpy as np
import tensorflow as tf

from sionna.phy.channel import (
    OFDMChannel,
    subcarrier_frequencies,
    cir_to_ofdm_channel,
    ApplyOFDMChannel,
)
from sionna.phy.nr import PUSCHConfig, PUSCHTransmitter, PUSCHReceiver
from sionna.phy.utils import ebnodb2no
from sionna.phy.ofdm import LinearDetector
from sionna.phy.mimo import StreamManagement

from .config import Config
from .pusch_trainable_transmitter import PUSCHTrainableTransmitter
from .pusch_neural_detector import PUSCHNeuralDetector
from .pusch_trainable_receiver import PUSCHTrainableReceiver


class PUSCHLinkE2E(tf.keras.Model):
    r"""
    End-to-end differentiable PUSCH link model for MU-MIMO autoencoder training.

    This class simulates a complete 5G NR PUSCH uplink that can operate in two modes:

    1. **Baseline mode** (``use_autoencoder=False``): Uses standard QAM constellation
       with LS channel estimation + LMMSE equalization for BER/BLER benchmarking.

    2. **Autoencoder mode** (``use_autoencoder=True``): Uses trainable constellation
       geometry AND labeling, plus a neural detector, enabling end-to-end optimization.

    The model supports both perfect and imperfect CSI scenarios, where imperfect
    CSI uses LS channel estimation with optional neural refinement.

    Parameters
    ----------
    channel_model : tuple or CIRDataset
        For baseline mode: ``CIRDataset`` object for on-demand CIR generation.
        For autoencoder mode: tuple ``(a, tau)`` of pre-loaded CIR tensors.
    perfect_csi : bool
        If ``True``, provides ground-truth channel to the receiver.
        If ``False``, receiver performs LS channel estimation.
    use_autoencoder : bool
        If ``True``, uses trainable transmitter and neural detector.
        If ``False``, uses standard PUSCH TX/RX with LMMSE detection.
    training : bool
        If ``True``, ``call()`` returns the training loss (BCE + regularization).
        If ``False``, ``call()`` returns ``(bits, bits_hat)`` for BER evaluation.
    config : ~demos.pusch_autoencoder.src.config.Config, optional
        System configuration. Defaults to ``Config()`` if not provided.
        Use this to customize system parameters like ``num_bs_ant``.
    gumbel_temperature : float, optional
        Initial Gumbel-Softmax temperature for learnable labeling.
        Lower values produce sharper (more discrete) assignments.
        Default 0.5.

    Notes
    -----
    For autoencoder mode, ``channel_model`` must be a tuple ``(a, tau)`` where
    ``a`` contains complex CIR coefficients with shape
    ``[num_samples, num_bs, num_bs_ant, num_ue, num_ue_ant, num_paths, num_time_steps]``
    and ``tau`` contains path delays with shape ``[num_samples, num_bs, num_ue, num_paths]``.
    For baseline mode, ``channel_model`` must be a valid ``CIRDataset``.

    The trainable transmitter now includes:

    - **Learnable constellation geometry**: Point positions can be optimized
      starting from random initialization to escape QAM local minima.
    - **Learnable labeling**: Bit-to-symbol assignment learned via Gumbel-Softmax
      enables optimization beyond fixed Gray coding.

    This dual optimization enables full geometric shaping potential that is
    limited when using fixed Gray labeling.

    Additional notes:

    - ``self._cfg`` contains PUSCH resource grid information after construction.
    - ``self.trainable_variables`` returns all trainable weights (TX + RX).
    - In training mode, ``call()`` returns a scalar loss tensor.
    - In inference mode, ``call()`` returns ``(b, b_hat)`` bit tensors.
    - The PUSCH configuration (PRBs, MCS, layers) remains fixed after init.
    - Constellation normalization maintains unit average power.
    - Channel model type (tuple vs CIRDataset) determines internal processing path.

    Example
    -------
    >>> # Autoencoder training setup
    >>> cir_manager = CIRManager()
    >>> a, tau = cir_manager.load_from_tfrecord(group_for_mumimo=True)
    >>> model = PUSCHLinkE2E((a, tau), perfect_csi=False,
    ...                       use_autoencoder=True, training=True)
    >>> loss = model(batch_size=32, ebno_db=10.0)
    >>> # Train with separate optimizers for geometry, labeling, and receiver
    """

    def __init__(
        self,
        channel_model,
        perfect_csi,
        use_autoencoder=False,
        training=False,
        config=None,
        gumbel_temperature=0.5,
    ):
        super().__init__()

        # Store configuration flags for use in forward pass
        self._training = training
        self._channel_model = channel_model
        self._perfect_csi = perfect_csi
        self._use_autoencoder = use_autoencoder
        self._gumbel_temperature = gumbel_temperature

        # Centralized config object for system parameters
        self._cfg = config if config is not None else Config()

        # Cache frequently-used config values for performance
        self._num_prb = self._cfg.num_prb
        self._mcs_index = self._cfg.mcs_index
        self._num_layers = self._cfg.num_layers
        self._mcs_table = self._cfg.mcs_table
        self._domain = self._cfg.domain

        self._num_ue_ant = self._cfg.num_ue_ant
        self._num_ue = self._cfg.num_ue
        # Subcarrier spacing must match the value used during CIR generation
        # to ensure correct Doppler and delay spread scaling.
        self._subcarrier_spacing = self._cfg.subcarrier_spacing

        # =====================================================================
        # PUSCH Configuration for First UE
        # =====================================================================
        # The first UE's config serves as the template; others are cloned with
        # different DMRS port assignments to enable MU-MIMO multiplexing.
        pusch_config = PUSCHConfig()
        pusch_config.carrier.subcarrier_spacing = self._subcarrier_spacing / 1000.0
        pusch_config.carrier.n_size_grid = self._num_prb
        pusch_config.num_antenna_ports = self._num_ue_ant
        pusch_config.num_layers = self._num_layers
        # Codebook precoding with TPMI=1 selects a fixed precoding matrix,
        # simplifying the autoencoder by removing precoder optimization.
        pusch_config.precoding = "codebook"
        pusch_config.tpmi = 1
        # DMRS configuration: Type 1, single-symbol, with additional position
        # for improved channel tracking in time-varying scenarios.
        pusch_config.dmrs.dmrs_port_set = list(range(self._num_layers))
        pusch_config.dmrs.config_type = 1
        pusch_config.dmrs.length = 1
        pusch_config.dmrs.additional_position = 1
        # 2 CDM groups without data reserves sufficient DMRS density for
        # reliable channel estimation across 4 co-scheduled UEs.
        pusch_config.dmrs.num_cdm_groups_without_data = 2
        pusch_config.tb.mcs_index = self._mcs_index
        pusch_config.tb.mcs_table = self._mcs_table

        # Propagate PUSCH grid info to Config so neural detector can access it
        self._cfg.pusch_pilot_indices = pusch_config.dmrs_symbol_indices
        self._cfg.pusch_num_subcarriers = pusch_config.num_subcarriers
        self._cfg.pusch_num_symbols_per_slot = pusch_config.carrier.num_symbols_per_slot

        # =====================================================================
        # Create PUSCH Configs for All UEs
        # =====================================================================
        # Each UE gets a unique DMRS port set to enable orthogonal pilot
        # transmission and per-UE channel estimation at the BS.
        pusch_configs = [pusch_config]
        for i in range(1, self._num_ue):
            pc = pusch_config.clone()
            pc.dmrs.dmrs_port_set = list(
                range(i * self._num_layers, (i + 1) * self._num_layers)
            )
            pusch_configs.append(pc)

        # =====================================================================
        # Transmitter Setup
        # =====================================================================
        # Autoencoder uses trainable constellation with random initialization
        # and learnable labeling; baseline uses fixed QAM with Gray coding.
        if self._use_autoencoder:
            self._pusch_transmitter = PUSCHTrainableTransmitter(
                pusch_configs,
                output_domain=self._domain,
                training=self._training,
                gumbel_temperature=self._gumbel_temperature,
            )
        else:
            self._pusch_transmitter = PUSCHTransmitter(
                pusch_configs, output_domain=self._domain
            )
        self._cfg.resource_grid = self._pusch_transmitter.resource_grid

        # =====================================================================
        # Detector Setup
        # =====================================================================
        # Stream management defines the RX-TX association matrix for MU-MIMO.
        # All UEs are associated with the single BS (all-ones matrix).
        rx_tx_association = np.ones([1, self._num_ue], bool)
        stream_management = StreamManagement(rx_tx_association, self._num_layers)

        if self._use_autoencoder:
            self._detector = PUSCHNeuralDetector(self._cfg)
        else:
            # LMMSE with max-log demapping provides the classical baseline
            self._detector = LinearDetector(
                equalizer="lmmse",
                output="bit",
                demapping_method="maxlog",
                resource_grid=self._pusch_transmitter.resource_grid,
                stream_management=stream_management,
                constellation_type="qam",
                num_bits_per_symbol=pusch_config.tb.num_bits_per_symbol,
            )

        # =====================================================================
        # Receiver Setup
        # =====================================================================
        receiver = PUSCHTrainableReceiver if self._use_autoencoder else PUSCHReceiver
        receiver_kwargs = {
            "mimo_detector": self._detector,
            "input_domain": self._domain,
            "pusch_transmitter": self._pusch_transmitter,
        }

        # Perfect CSI bypasses channel estimation entirely
        if self._perfect_csi:
            receiver_kwargs["channel_estimator"] = "perfect"

        if self._use_autoencoder:
            receiver_kwargs["training"] = training

        self._pusch_receiver = receiver(**receiver_kwargs)

        # =====================================================================
        # Channel Setup
        # =====================================================================
        if self._use_autoencoder:
            # Pre-compute subcarrier frequencies for CIR-to-OFDM conversion
            self._frequencies = subcarrier_frequencies(
                self._pusch_transmitter.resource_grid.fft_size,
                self._pusch_transmitter.resource_grid.subcarrier_spacing,
            )
            # Apply channel together with AWGN addition for autoencoder training
            self._channel = ApplyOFDMChannel(add_awgn=True)

            if self._training:
                # Binary cross-entropy loss for soft LLR training
                self._bce = tf.keras.losses.BinaryCrossentropy(from_logits=True)
        else:
            # OFDMChannel wrapper for baseline simulation with CIRDataset
            self._channel = OFDMChannel(
                self._channel_model,
                self._pusch_transmitter.resource_grid,
                normalize_channel=True,
                return_channel=True,
            )

    @property
    def trainable_variables(self):
        """
        Collect all trainable variables from transmitter and receiver.

        Returns
        -------
        list of tf.Variable
            Combined list of transmitter and receiver trainable variables.
            For autoencoder mode, includes:
            - Constellation geometry (real/imag coordinates)
            - Labeling logits (permutation matrix)
            - Neural detector weights (ResBlocks, correction scales)
        """
        vars_ = []
        if hasattr(self, "_pusch_transmitter"):
            vars_ += list(self._pusch_transmitter.trainable_variables)
        if hasattr(self, "_pusch_receiver"):
            vars_ += list(self._pusch_receiver.trainable_variables)
        return vars_

    @property
    def tx_geometry_variables(self):
        """
        Get transmitter geometry (constellation point) variables.

        Returns
        -------
        list of tf.Variable
            Two-element list: ``[_points_r, _points_i]`` for separate
            optimization from labeling variables.
        """
        if hasattr(self._pusch_transmitter, "geometry_variables"):
            return self._pusch_transmitter.geometry_variables
        return []

    @property
    def tx_labeling_variables(self):
        """
        Get transmitter labeling (permutation) variables.

        Returns
        -------
        list of tf.Variable
            One-element list: ``[_labeling_logits]`` for separate
            optimization from geometry variables.
        """
        if hasattr(self._pusch_transmitter, "labeling_variables"):
            return self._pusch_transmitter.labeling_variables
        return []

    @property
    def rx_variables(self):
        """
        Get receiver trainable variables.

        Returns
        -------
        list of tf.Variable
            All trainable variables from the receiver (neural detector
            weights including correction scales and ResBlock parameters).
        """
        if hasattr(self, "_pusch_receiver"):
            return list(self._pusch_receiver.trainable_variables)
        return []

    @property
    def constellation(self):
        """
        Get the current normalized constellation points.

        Returns
        -------
        tf.Tensor
            Complex tensor of shape ``[num_points]`` with unit average power.
            For 16-QAM, this is 16 complex values.
        """
        return self._pusch_transmitter.get_normalized_constellation()

    @property
    def gumbel_temperature(self):
        """
        Get current Gumbel-Softmax temperature.

        Returns
        -------
        float or None
            Current temperature value, or ``None`` if transmitter does not
            support learnable labeling.
        """
        if hasattr(self._pusch_transmitter, "gumbel_temperature"):
            return self._pusch_transmitter.gumbel_temperature
        return None

    @gumbel_temperature.setter
    def gumbel_temperature(self, value):
        """
        Set Gumbel-Softmax temperature (for annealing during training).

        Parameters
        ----------
        value : float
            New temperature value. Lower values produce sharper
            (more discrete) assignments.
        """
        if hasattr(self._pusch_transmitter, "gumbel_temperature"):
            self._pusch_transmitter.gumbel_temperature = value

    def get_hard_labeling(self):
        """
        Get the hard (argmax) labeling permutation from the transmitter.

        Returns
        -------
        tf.Tensor or None
            Integer permutation indices if learnable labeling is enabled,
            otherwise ``None``.
        """
        if hasattr(self._pusch_transmitter, "get_hard_labeling_permutation"):
            return self._pusch_transmitter.get_hard_labeling_permutation()
        return None

    @tf.function(jit_compile=False)
    def call(self, batch_size, ebno_db):
        """
        Execute forward pass through the end-to-end PUSCH link.

        Parameters
        ----------
        batch_size : int
            Number of transport blocks to simulate in parallel.
        ebno_db : tf.Tensor
            Energy per bit to noise power spectral density ratio in dB.
            Can be scalar (same SNR for all samples) or vector ``[batch_size]``.

        Returns
        -------
        tf.Tensor or tuple
            - **Training mode**: Scalar loss tensor (BCE)
            - **Inference mode**: Tuple ``(b, b_hat)`` where:
              - ``b``: Original bits, shape ``[batch_size, num_ue, tb_size]``
              - ``b_hat``: Detected bits, same shape as ``b``

        Notes
        -----
        JIT compilation is disabled (``jit_compile=False``) because the neural
        detector uses dynamic shapes and control flow that are incompatible
        with XLA compilation.

        The processing flow follows standard PUSCH transmission:

        1. **Transmitter**: Bit generation, encoding, constellation mapping
           with learnable labeling, layer mapping, resource grid mapping,
           precoding (if enabled), OFDM modulation (if time domain)

        2. **Channel**: Random sampling from pre-loaded CIR tensors (autoencoder)
           or on-demand CIR generation (baseline), CIR-to-OFDM conversion,
           AWGN addition

        3. **Receiver**: OFDM demodulation (if time domain), channel estimation
           (perfect or LS), neural MIMO detection with constellation
           synchronization, layer demapping, transport block decoding (inference)

        4. **Loss computation** (training only): BCE loss on soft LLRs plus
           minimum distance regularization to prevent constellation collapse
        """
        # =====================================================================
        # Transmitter Processing
        # =====================================================================
        if self._use_autoencoder:
            # Returns: mapped symbols, OFDM signal, original bits, coded bits
            x_map, x, b, c = self._pusch_transmitter(batch_size)
        else:
            # Baseline returns only OFDM signal and original bits
            x, b = self._pusch_transmitter(batch_size)

        # Convert Eb/N0 to noise variance using coderate and bits/symbol
        no = ebnodb2no(
            ebno_db,
            self._pusch_transmitter._num_bits_per_symbol,
            self._pusch_transmitter._target_coderate,
            self._pusch_transmitter.resource_grid,
        )

        # =====================================================================
        # Channel Application
        # =====================================================================
        if self._use_autoencoder:
            # Unpack pre-loaded CIR tensors and sample a random batch
            a, tau = self._channel_model
            num_samples = tf.shape(a)[0]

            # Random sampling enables diverse channel realizations per batch
            # without requiring a tf.data.Dataset pipeline.
            idx = tf.random.shuffle(tf.range(num_samples))[:batch_size]

            a_batch = tf.gather(a, idx, axis=0)
            tau_batch = tf.gather(tau, idx, axis=0)

            # Convert time-domain CIR to frequency-domain channel matrix.
            # Normalization ensures consistent SNR interpretation across
            # different channel realizations and antenna configurations.
            h = cir_to_ofdm_channel(
                self._frequencies, a_batch, tau_batch, normalize=True
            )

            y = self._channel(x, h, no)
        else:
            # OFDMChannel handles CIR sampling internally via CIRDataset
            y, h = self._channel(x, no)

        # =====================================================================
        # Receiver Processing
        # =====================================================================
        if self._use_autoencoder and self._training:
            # Training: compute loss from LLRs without full TB decoding
            if self._perfect_csi:
                llr = self._pusch_receiver(y, no, h)
            else:
                llr = self._pusch_receiver(y, no)

            # Binary cross-entropy between coded bits and soft LLR estimates
            # This is the optimization objective driving end-to-end learning
            bce_loss = self._bce(c, llr)

            return bce_loss
        else:
            # Inference: decode bits and return for BER/BLER computation
            if self._perfect_csi:
                b_hat = self._pusch_receiver(y, no, h)
            else:
                b_hat = self._pusch_receiver(y, no)
            return b, b_hat
