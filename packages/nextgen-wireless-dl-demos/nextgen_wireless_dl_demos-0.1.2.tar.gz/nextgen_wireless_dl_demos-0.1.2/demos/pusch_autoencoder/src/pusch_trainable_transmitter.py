# SPDX-License-Identifier: MIT
# Copyright (c) 2025–present Srikanth Pagadarai

"""
Trainable PUSCH transmitter with SYMMETRIC learnable constellation geometry AND labeling.

Extends Sionna's standard PUSCHTransmitter to support end-to-end
optimization of constellation points. The key is maintaining valid
constellation properties (unit average power, centered) while
allowing gradient flow through the constellation geometry.

Design Approach
---------------
**Symmetric Constellation Geometry**:

Instead of 16 independent complex points, we store only 4 base points in the first
quadrant (I>0, Q>0). The complete 16-point constellation is constructed by:

1. Original 4 base points -> 1st quadrant (I>0, Q>0)
2. Reflection across Q-axis -> 2nd quadrant (I<0, Q>0)
3. Reflection across I-axis -> 4th quadrant (I>0, Q<0)
4. Reflection across origin -> 3rd quadrant (I<0, Q<0)

This enforces mathematical symmetry that is preserved during gradient descent.

**Learnable Labeling** (unchanged):

Gumbel-Softmax labeling remains essential because:
- Random constellation initialization breaks Gray labeling assumptions
- The system needs to jointly optimize geometry AND bit-to-symbol assignment
- Even with symmetric geometry, labeling can and should adapt

Initialization Modes
--------------------
- **Training mode** (``training=True``): Random base points in Q1, then reflected
  to create full symmetric constellation. Labeling initialized to identity.

- **Inference mode** (``training=False``): Standard QAM initialization as placeholder
  until weights are loaded from trained model.
"""

from sionna.phy.nr import PUSCHTransmitter
from sionna.phy.mapping import Constellation
import tensorflow as tf
import numpy as np


class PUSCHTrainableTransmitter(PUSCHTransmitter):
    r"""
    PUSCH Transmitter with SYMMETRIC trainable constellation geometry AND labeling.

    This subclass enforces 4-fold symmetry (I-axis, Q-axis, origin) in the
    constellation while supporting learnable labeling for autoencoder-based
    communication system design.

    Parameters
    ----------
    *args : tuple
        Positional arguments passed to ``PUSCHTransmitter``.
    training : bool
        If ``True``, constellation and labeling are trainable with soft
        Gumbel-Softmax assignment. Default ``False``.
    gumbel_temperature : float
        Temperature for Gumbel-Softmax. Lower = sharper (more discrete).
        Default 0.5.
    **kwargs : dict
        Keyword arguments passed to ``PUSCHTransmitter``.

    Example
    -------
    >>> tx = PUSCHTrainableTransmitter(pusch_configs, output_domain="freq",
    ...                                 training=True, gumbel_temperature=0.5)
    >>> x_map, x, b, c = tx(batch_size=32)

    Notes
    -----
    The symmetric constellation is stored as ``[num_base_points]`` complex values
    (typically 4 for 16-QAM), and the full constellation is computed via reflections.
    This guarantees 4-fold symmetry is preserved during training.

    The learnable labeling uses a permutation logits matrix of shape
    ``[num_points, num_points]``. Row ``i`` contains logits for which
    constellation point should be assigned to bit pattern ``i``.
    """

    def __init__(self, *args, training=False, gumbel_temperature=0.5, **kwargs):
        self._training = training
        self._gumbel_temperature = gumbel_temperature

        # Parent constructor sets up standard PUSCH processing chain
        super().__init__(*args, **kwargs)

        # Replace standard constellation with symmetric trainable version
        self._setup_custom_constellation()

    @staticmethod
    def generate_random_symmetric_constellation(num_points, seed=None):
        """
        Generate random constellation with 4-fold symmetry and unit average energy.

        Creates a constellation by:
        1. Generating num_points/4 random base points in the first quadrant
        2. Reflecting them across I-axis, Q-axis, and origin
        3. Normalizing to unit average power

        Parameters
        ----------
        num_points : int
            Total constellation size (must be divisible by 4). For 16-QAM: 16.
        seed : int, optional
            Random seed for reproducibility.

        Returns
        -------
        tf.Tensor, complex64
            Symmetric constellation points with shape ``[num_points]``.
            Points are ordered: [Q1_points, Q2_points, Q4_points, Q3_points]

        Notes
        -----
        The generation process:

        1. Sample num_points/4 base points in Q1 (I>0, Q>0)
        2. Reflect across Q-axis: negate real part -> Q2 (I<0, Q>0)
        3. Reflect across I-axis: negate imag part -> Q4 (I>0, Q<0)
        4. Reflect across origin: negate both parts -> Q3 (I<0, Q<0)
        5. Normalize complete constellation to unit average power

        Example
        -------
        >>> points = PUSCHTrainableTransmitter.generate_random_symmetric_constellation(16, seed=42)
        >>> print(f"Power: {tf.reduce_mean(tf.abs(points)**2):.6f}")  # Should be ~1.0
        >>> # Verify I-axis symmetry (Q1 vs Q4)
        >>> print(f"I-sym check: {tf.reduce_mean(tf.abs(points[0] - tf.math.conj(points[8]))):.6f}")  # ~0
        """
        if num_points % 4 != 0:
            raise ValueError(f"num_points must be divisible by 4, got {num_points}")

        num_base_points = num_points // 4

        if seed is not None:
            np.random.seed(seed)
            tf.random.set_seed(seed)

        # Sample random base points in first quadrant (I>0, Q>0)
        real_base = tf.random.uniform([num_base_points], minval=0.1, maxval=1.0)
        imag_base = tf.random.uniform([num_base_points], minval=0.1, maxval=1.0)
        base_points = tf.complex(real_base, imag_base)

        # Generate all 4 quadrants via reflections
        points = PUSCHTrainableTransmitter._reflect_to_full_constellation(base_points)

        # Normalize to unit average power for consistent SNR interpretation
        energy = tf.reduce_mean(tf.square(tf.abs(points)))
        points = points / tf.cast(tf.sqrt(energy), points.dtype)

        return points

    @property
    def trainable_variables(self):
        """
        Return all trainable variables: base geometry + labeling.

        Returns
        -------
        list of tf.Variable
            Three-element list: ``[_base_points_r, _base_points_i, _labeling_logits]``
            where:
            - ``_base_points_r``: Real parts of Q1 base points
            - ``_base_points_i``: Imaginary parts of Q1 base points
            - ``_labeling_logits``: Permutation logits for bit-to-point mapping
        """
        return [self._base_points_r, self._base_points_i, self._labeling_logits]

    @property
    def geometry_variables(self):
        """Return only the base geometry (Q1 constellation points) variables."""
        return [self._base_points_r, self._base_points_i]

    @property
    def labeling_variables(self):
        """Return only the labeling (permutation) variable."""
        return [self._labeling_logits]

    @property
    def gumbel_temperature(self):
        """float: Current Gumbel-Softmax temperature."""
        return self._gumbel_temperature

    @gumbel_temperature.setter
    def gumbel_temperature(self, value):
        """Set Gumbel-Softmax temperature (e.g., for annealing)."""
        self._gumbel_temperature = value

    def get_base_points(self):
        """
        Get the base constellation points (Q1 only, not normalized).

        Returns
        -------
        tf.Tensor, complex64
            Base constellation points in first quadrant, shape ``[num_base_points]``.
            For 16-QAM, this is ``[4]`` complex values.
        """
        return tf.complex(
            tf.cast(self._base_points_r, self.rdtype),
            tf.cast(self._base_points_i, self.rdtype),
        )

    @staticmethod
    def _reflect_to_full_constellation(base_points):
        """
        Reflect base points to create full 4-fold symmetric constellation.

        Parameters
        ----------
        base_points : tf.Tensor, complex64
            Base points in Q1, shape ``[num_base_points]``.

        Returns
        -------
        tf.Tensor, complex64
            Full constellation with 4-fold symmetry, shape ``[4*num_base_points]``.

        Notes
        -----
        Reflection mapping:
        - Q1 (I>0, Q>0): base_points (original)
        - Q2 (I<0, Q>0): reflect across Q-axis (negate real part)
        - Q4 (I>0, Q<0): reflect across I-axis (negate imag part)
        - Q3 (I<0, Q<0): reflect across origin (negate both parts)
        """
        real_base = tf.math.real(base_points)
        imag_base = tf.math.imag(base_points)

        q1_points = base_points  # Original
        q2_points = tf.complex(-real_base, imag_base)  # Q-axis reflection
        q4_points = tf.complex(real_base, -imag_base)  # I-axis reflection
        q3_points = tf.complex(-real_base, -imag_base)  # Origin reflection

        return tf.concat([q1_points, q2_points, q4_points, q3_points], axis=0)

    def get_normalized_constellation(self):
        """
        Compute 4-fold symmetric and power-normalized constellation points.

        Returns
        -------
        tf.Tensor, complex64
            Normalized constellation points with 4-fold symmetry,
            shape ``[num_points]``. For 16-QAM, this is ``[16]`` complex values.

        Notes
        -----
        The normalization process:

        1. Retrieve base points from trainable variables (Q1 only)
        2. Reflect to create full 4-fold symmetric constellation
        3. Normalize to unit average power

        The normalization is differentiable and does NOT break symmetry since
        it's a uniform scaling operation applied to all points equally.

        Symmetry properties maintained:
        - I-axis: constellation[i] = conj(constellation[j]) for mirrored i,j
        - Q-axis: constellation[i] = -conj(constellation[k]) for mirrored i,k
        - Origin: constellation[i] = -constellation[m] for opposite i,m
        """
        # Get base points from trainable variables
        base_points = self.get_base_points()

        # Reflect to full constellation
        points = self._reflect_to_full_constellation(base_points)

        # Normalize to unit power (differentiable)
        energy = tf.reduce_mean(tf.square(tf.abs(points)))
        normalized_points = points / tf.cast(tf.sqrt(energy), points.dtype)

        return normalized_points

    def _gumbel_softmax(self, logits, temperature, hard=False):
        """
        Gumbel-Softmax sampling for differentiable discrete sampling.

        Parameters
        ----------
        logits : tf.Tensor, float
            Logits for categorical distribution, shape ``[..., num_classes]``.
        temperature : float
            Temperature for Gumbel-Softmax. Lower values make distribution
            more peaked (closer to hard one-hot).
        hard : bool
            If True, return one-hot samples (non-differentiable).
            If False, return soft samples (differentiable).

        Returns
        -------
        tf.Tensor, float
            Sampled distribution, same shape as ``logits``.

        Notes
        -----
        During training, use ``hard=False`` for gradient flow.
        During inference, use ``hard=True`` for discrete assignment.
        """
        if hard:
            # Hard one-hot assignment (inference mode)
            indices = tf.argmax(logits, axis=-1)
            return tf.one_hot(indices, depth=tf.shape(logits)[-1], dtype=logits.dtype)
        else:
            # Soft Gumbel-Softmax (training mode)
            gumbel_noise = -tf.math.log(
                -tf.math.log(tf.random.uniform(tf.shape(logits)))
            )
            y = logits + gumbel_noise
            return tf.nn.softmax(y / temperature)

    def get_soft_labeling_matrix(self, hard=False):
        """
        Get the current labeling matrix (permutation of constellation points).

        Parameters
        ----------
        hard : bool
            If True, return hard one-hot assignment.
            If False, return soft Gumbel-Softmax probabilities.

        Returns
        -------
        tf.Tensor, float
            Labeling matrix, shape ``[num_points, num_points]``.
            Row i indicates which constellation point(s) are assigned to
            bit pattern i.

        Example
        -------
        For hard assignment, row i will have a single 1 at column j,
        meaning bit pattern i maps to constellation point j.

        For soft assignment during training, row i contains probabilities
        summing to 1, enabling gradient flow through the labeling.
        """
        if hard:
            return self._gumbel_softmax(
                self._labeling_logits, self._gumbel_temperature, hard=True
            )
        else:
            return self._gumbel_softmax(
                self._labeling_logits, self._gumbel_temperature, hard=False
            )

    # [custom-constellation-start]
    def _setup_custom_constellation(self):
        """
        Initialize symmetric trainable constellation and learnable labeling.

        For 16-QAM (num_bits_per_symbol=4):
        - Stores 4 base points in Q1 as trainable variables
        - Other 12 points computed via reflections (enforces symmetry)
        - Labeling initialized to identity matrix (preserves structure initially)

        Notes
        -----
        Even with symmetric geometry, we preserve flexible labeling to allow
        the optimizer to discover optimal bit-to-symbol assignments that may
        differ from standard Gray coding.
        """
        num_points = 2**self._num_bits_per_symbol
        self._num_constellation_points = num_points
        self._num_base_points = num_points // 4

        if self._training:
            # Training mode: Use symmetric random initialization
            constellation_points = self.generate_random_symmetric_constellation(
                num_points, seed=None  # No seed = different init each run
            )
            # Extract just the base points (Q1 only)
            base_points = constellation_points[: self._num_base_points]
        else:
            # Inference mode: Use standard QAM as placeholder
            constellation_points = Constellation(
                "qam", num_bits_per_symbol=self._num_bits_per_symbol
            ).points
            # For QAM, assume first quarter are Q1 points (this is approximate)
            base_points = constellation_points[: self._num_base_points]

        # Store ONLY base points as trainable variables
        init_r = tf.math.real(base_points)
        init_i = tf.math.imag(base_points)

        self._base_points_r = tf.Variable(
            tf.cast(init_r, self.rdtype),
            trainable=self._training,
            name="constellation_base_real",
        )
        self._base_points_i = tf.Variable(
            tf.cast(init_i, self.rdtype),
            trainable=self._training,
            name="constellation_base_imag",
        )

        # Initialize labeling logits to identity-like matrix
        # This means bit pattern i initially maps to constellation point i
        identity_scale = 5.0  # Start sharply peaked at identity
        init_logits = tf.eye(num_points) * identity_scale

        self._labeling_logits = tf.Variable(
            tf.cast(init_logits, self.rdtype),
            trainable=self._training,
            name="labeling_logits",
        )

        # Create constellation object for compatibility with Sionna internals
        # (used by resource grid mapper, etc.)
        # Initialize with full reflected constellation
        full_constellation = self.get_normalized_constellation()
        self._constellation = Constellation(
            "custom",
            num_bits_per_symbol=self._num_bits_per_symbol,
            points=full_constellation,
            normalize=False,
            center=False,
        )

    # [custom-constellation-end]

    def _soft_symbol_mapping(self, c):
        """
        Map coded bits to symbols using soft learnable labeling.

        This replaces the standard hard lookup with a differentiable
        soft assignment that enables gradient flow through the labeling.

        Parameters
        ----------
        c : tf.Tensor, float32
            Coded bits, shape ``[batch, num_tx, num_coded_bits]``.

        Returns
        -------
        tf.Tensor, complex64
            Mapped symbols, shape ``[batch, num_tx, num_symbols]``.
        """
        # Get normalized constellation points (with 4-fold symmetry)
        constellation = self.get_normalized_constellation()  # [num_points]

        # Reshape bits for symbol grouping
        batch_size = tf.shape(c)[0]
        num_tx = tf.shape(c)[1]
        num_bits = tf.shape(c)[2]
        bits_per_sym = self._num_bits_per_symbol
        num_symbols = num_bits // bits_per_sym

        # Reshape to [batch, num_tx, num_symbols, bits_per_symbol]
        c_reshaped = tf.reshape(c, [batch_size, num_tx, num_symbols, bits_per_sym])

        # Convert bits to integer indices (binary to decimal)
        powers = tf.cast(2 ** tf.range(bits_per_sym - 1, -1, -1), c.dtype)
        indices = tf.reduce_sum(
            c_reshaped * powers, axis=-1
        )  # [batch, num_tx, num_symbols]
        indices = tf.cast(indices, tf.int32)

        # Get labeling assignment matrix
        if self._training:
            # Soft assignment during training for gradient flow
            assignment = self._gumbel_softmax(
                self._labeling_logits, self._gumbel_temperature, hard=False
            )  # [num_points, num_points]
        else:
            # Hard assignment during inference
            assignment = self.get_soft_labeling_matrix(hard=True)

        # Convert indices to one-hot: [batch, num_tx, num_symbols, num_points]
        one_hot = tf.one_hot(
            indices, depth=self._num_constellation_points, dtype=self.rdtype
        )

        # Apply labeling permutation: one_hot @ assignment
        soft_assignment = tf.einsum("btsp,pq->btsq", one_hot, assignment)

        # Weighted sum over constellation points
        constellation_r = tf.math.real(constellation)
        constellation_i = tf.math.imag(constellation)

        x_real = tf.einsum("btsq,q->bts", soft_assignment, constellation_r)
        x_imag = tf.einsum("btsq,q->bts", soft_assignment, constellation_i)

        x_map = tf.complex(x_real, x_imag)

        return x_map

    def call(self, inputs):
        """
        Execute transmitter processing chain with trainable constellation and labeling.

        The symmetric constellation is computed from base points before each forward pass.

        Parameters
        ----------
        inputs : int or tf.Tensor
            If ``return_bits=True``: ``int`` specifying batch size.
            If ``return_bits=False``: ``tf.Tensor`` of input bits.

        Returns
        -------
        tuple or tf.Tensor
            If ``return_bits=True``: tuple ``(x_map, x, b, c)``
            If ``return_bits=False``: just ``x`` (transmitted signal).

        Notes
        -----
        The processing chain:

        1. Compute full 16-point symmetric constellation from 4 base points
        2. Standard PUSCH transmission (bits -> symbols -> OFDM)
        3. Symbol mapping uses learnable labeling via Gumbel-Softmax
        """
        # Update constellation object with current normalized symmetric points
        self._constellation.points = self.get_normalized_constellation()

        if self._return_bits:
            batch_size = inputs
            b = self._binary_source([batch_size, self._num_tx, self._tb_size])
        else:
            b = inputs

        # TB encoding: CRC, segmentation, LDPC encoding, rate matching
        c = self._tb_encoder(b)

        # Custom soft symbol mapping with learnable labeling
        x_map = self._soft_symbol_mapping(c)

        # Distribute symbols across MIMO layers
        x_layer = self._layer_mapper(x_map)

        # Place symbols on OFDM resource grid with DMRS
        x_grid = self._resource_grid_mapper(x_layer)

        # Apply precoding if configured
        if self._precoding == "codebook":
            x_pre = self._precoder(x_grid)
        else:
            x_pre = x_grid

        # Convert to time domain if requested
        if self._output_domain == "time":
            x = self._ofdm_modulator(x_pre)
        else:
            x = x_pre

        if self._return_bits:
            return x_map, x, b, c
        else:
            return x
