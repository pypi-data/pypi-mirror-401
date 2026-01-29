"""
U(3) Complex Frame and Gauge Field Unification Framework
================================================================================

Complete implementation based on "Complex Frame and Gauge Field Unification Program"

Core Theory:
- Complex frame U(x) ∈ U(3) as unified structure of spacetime and gauge fields
- Symmetry breaking chain: SU(4) → SU(3) × SU(2) × U(1)
- Imaginary time embedding: ℝ³ × iℝ → internal rotational degrees of freedom
- Gauge field as complex frame connection: A_μ ∈ 𝔲(3)
- Three phase angles corresponding to color degrees of freedom (red, green, blue)

Author: Enhanced by AI following theoretical framework
Date: 2025-12-04
Version: 7.0.0-alpha
DOI: https://doi.org/10.5281/zenodo.18217542
"""

__version__ = '7.0.0-alpha'

import numpy as np
from typing import Tuple, Optional, List, Dict, Any
from dataclasses import dataclass
import warnings

# Attempt to import basic coordinate system
try:
    from .coordinate_system import coord3, vec3, quat
except ImportError:
    try:
        from coordinate_system import coord3, vec3, quat
    except ImportError:
        coord3 = None
        vec3 = None
        quat = None

# Physical constants
HBAR = 1.0  # Reduced Planck constant (natural units)
C_SPEED = 1.0  # Speed of light (natural units)


# ============================================================
# U(3) Complex Frame Class
# ============================================================

class U3Frame:
    """
    U(3) Complex Frame - Complete three-dimensional unitary matrix frame

    Mathematical form:
        U(x) = [e₁(x), e₂(x), e₃(x)] ∈ U(3)

    Each basis vector eₖ = aₖ + ibₖ ∈ ℂ³ satisfies:
        ⟨eⱼ, eₖ⟩ = δⱼₖ  (complex inner product)
        det(U) = e^{iφ}  (phase degree of freedom)

    Symmetry decomposition:
        U(3) ⊃ SU(3) × U(1)
        SU(3) ⊃ SU(2) × U(1)

    Physical interpretation:
        - Real part Re(eₖ): spatial direction vectors
        - Imaginary part Im(eₖ): imaginary time evolution direction
        - Three phase angles (θ₁, θ₂, θ₃): color degrees of freedom (red, green, blue)
    """

    def __init__(self,
                 e1: Optional[np.ndarray] = None,
                 e2: Optional[np.ndarray] = None,
                 e3: Optional[np.ndarray] = None,
                 ensure_unitary: bool = True):
        """
        Initialize U(3) complex frame

        Args:
            e1, e2, e3: Three complex basis vectors, each a complex array of shape (3,)
            ensure_unitary: Whether to ensure unitarity
        """
        if e1 is None:
            # Default: identity frame
            self.e1 = np.array([1.0+0j, 0.0+0j, 0.0+0j], dtype=complex)
            self.e2 = np.array([0.0+0j, 1.0+0j, 0.0+0j], dtype=complex)
            self.e3 = np.array([0.0+0j, 0.0+0j, 1.0+0j], dtype=complex)
        else:
            self.e1 = np.array(e1, dtype=complex)
            self.e2 = np.array(e2, dtype=complex)
            self.e3 = np.array(e3, dtype=complex)

        if ensure_unitary:
            self._gram_schmidt_orthonormalize()

    # -------------------- Basic Properties --------------------

    @property
    def matrix(self) -> np.ndarray:
        """
        U(3) matrix representation

        Returns:
            3×3 complex matrix [e₁ | e₂ | e₃]
        """
        return np.column_stack([self.e1, self.e2, self.e3])

    @property
    def determinant(self) -> complex:
        """
        Determinant det(U) = e^{iφ}

        For U(3): |det(U)| = 1
        """
        return np.linalg.det(self.matrix)

    @property
    def global_phase(self) -> float:
        """
        Global phase φ = arg(det(U))

        Corresponds to U(1) global gauge transformation
        """
        return np.angle(self.determinant)

    @property
    def real_part(self) -> np.ndarray:
        """Real part: spatial frame"""
        return np.column_stack([self.e1.real, self.e2.real, self.e3.real])

    @property
    def imag_part(self) -> np.ndarray:
        """Imaginary part: imaginary time direction"""
        return np.column_stack([self.e1.imag, self.e2.imag, self.e3.imag])

    @property
    def metric_tensor(self) -> np.ndarray:
        """
        Metric tensor from real part: g_μν = U^(R)ᵀ U^(R)

        Returns:
            3×3 metric tensor
        """
        real = self.real_part
        return real.T @ real

    @property
    def gauge_potential(self) -> np.ndarray:
        """
        Gauge potential from imaginary part: A_μ ∝ U^(I)

        Returns:
            3×3 anti-Hermitian matrix
        """
        return 1j * self.imag_part

    # -------------------- Symmetry Decomposition --------------------

    def to_su3_u1(self) -> Tuple['SU3Component', complex]:
        """
        Decompose into SU(3) × U(1)

        U(3) = SU(3) × U(1)
        U = (det U)^{1/3} · V

        where V ∈ SU(3), det(V) = 1

        Returns:
            (su3_component, u1_phase)
        """
        det_u = self.determinant
        u1_phase = det_u ** (1/3)  # ∛det(U)

        # Normalize to SU(3)
        V_matrix = self.matrix / u1_phase

        return SU3Component(V_matrix), u1_phase

    def color_phases(self) -> Tuple[float, float, float]:
        """
        Extract color phase angles (θ₁, θ₂, θ₃)

        For diagonalized complex frame:
            U = diag(e^{iθ₁}, e^{iθ₂}, e^{iθ₃})

        Constraint: θ₁ + θ₂ + θ₃ = φ (global phase)

        Returns:
            (θ_red, θ_green, θ_blue)
        """
        # Extract phases of diagonal elements
        diag = np.diag(self.matrix)
        phases = np.angle(diag)

        return tuple(phases)

    def to_quaternion_representation(self) -> Tuple[complex, complex, complex, complex]:
        """
        Convert to quaternion representation (SU(2) subgroup only)

        SU(2) ⊂ SU(3) corresponds to quaternion q = a + bi + cj + dk

        Returns:
            (q0, q1, q2, q3) quaternion components
        """
        # Extract upper-left 2×2 submatrix (corresponding to SU(2))
        su2_block = self.matrix[:2, :2]

        # SU(2) → quaternion
        # U = [[a+ib, -c+id], [c+id, a-ib]]
        a = su2_block[0, 0].real
        b = su2_block[0, 0].imag
        c = su2_block[1, 0].real
        d = su2_block[1, 0].imag

        # Normalize
        norm = np.sqrt(a**2 + b**2 + c**2 + d**2)
        if norm > 1e-10:
            return (a/norm, b/norm, c/norm, d/norm)
        else:
            return (1.0, 0.0, 0.0, 0.0)

    # -------------------- Gauge Transformations --------------------

    def gauge_transform_u1(self, phi: float) -> 'U3Frame':
        """
        U(1) global gauge transformation

        U → e^{iφ} U

        Args:
            phi: Gauge phase

        Returns:
            Transformed frame
        """
        factor = np.exp(1j * phi)
        return U3Frame(
            e1=self.e1 * factor,
            e2=self.e2 * factor,
            e3=self.e3 * factor,
            ensure_unitary=False
        )

    def gauge_transform_su2(self, pauli_vector: Tuple[float, float, float]) -> 'U3Frame':
        """
        SU(2) gauge transformation (acting on first two basis vectors)

        Corresponds to weak interaction gauge group

        Args:
            pauli_vector: (θ_x, θ_y, θ_z) Pauli vector parameters

        Returns:
            Transformed frame
        """
        θ_x, θ_y, θ_z = pauli_vector
        θ = np.sqrt(θ_x**2 + θ_y**2 + θ_z**2)

        if θ < 1e-10:
            return self

        # SU(2) matrix: exp(i θ·σ/2)
        n = np.array([θ_x, θ_y, θ_z]) / θ
        cos_half = np.cos(θ/2)
        sin_half = np.sin(θ/2)

        # Construct SU(2) matrix
        su2_matrix = np.array([
            [cos_half + 1j*n[2]*sin_half, (1j*n[0] + n[1])*sin_half],
            [(1j*n[0] - n[1])*sin_half, cos_half - 1j*n[2]*sin_half]
        ], dtype=complex)

        # Apply to first two basis vectors
        e12_block = np.column_stack([self.e1[:2], self.e2[:2]])
        e12_transformed = e12_block @ su2_matrix

        new_e1 = np.concatenate([e12_transformed[:, 0], [self.e1[2]]])
        new_e2 = np.concatenate([e12_transformed[:, 1], [self.e2[2]]])

        return U3Frame(e1=new_e1, e2=new_e2, e3=self.e3, ensure_unitary=False)

    def gauge_transform_su3(self, gell_mann_params: np.ndarray) -> 'U3Frame':
        """
        SU(3) gauge transformation (gluon transformation)

        Corresponds to strong interaction gauge group (QCD)

        Args:
            gell_mann_params: 8 Gell-Mann matrix parameters (θ₁, ..., θ₈)

        Returns:
            Transformed frame
        """
        if len(gell_mann_params) != 8:
            raise ValueError("SU(3) requires 8 parameters (Gell-Mann matrices)")

        # Construct SU(3) matrix: exp(i Σₐ θₐ λₐ/2)
        su3_matrix = self._build_su3_matrix(gell_mann_params)

        # Apply transformation
        new_matrix = self.matrix @ su3_matrix

        return U3Frame(
            e1=new_matrix[:, 0],
            e2=new_matrix[:, 1],
            e3=new_matrix[:, 2],
            ensure_unitary=False
        )

    # -------------------- Imaginary Time Evolution --------------------

    def imaginary_time_evolution(self, tau: float, hamiltonian: Optional[np.ndarray] = None) -> 'U3Frame':
        """
        Imaginary time evolution operator: exp(-τĤ)

        Corresponds to Wick rotation: t → -iτ

        Mathematical form:
            U(τ) = exp(-τĤ) U(0)

        Physical meaning:
            - τ > 0: Imaginary time parameter (thermodynamic β = 1/kT)
            - Ĥ: Hamiltonian operator (energy operator)
            - Connection to path integral: Z = Tr[exp(-βĤ)]

        Args:
            tau: Imaginary time parameter
            hamiltonian: 3×3 Hermitian matrix (default uses standard Laplacian)

        Returns:
            Evolved frame
        """
        if hamiltonian is None:
            # Default: use simple diagonal Hamiltonian
            hamiltonian = np.diag([1.0, 1.0, 1.0])

        # Evolution operator: exp(-τĤ)
        evolution_op = scipy_expm(-tau * hamiltonian)

        # Apply to frame
        new_matrix = evolution_op @ self.matrix

        return U3Frame(
            e1=new_matrix[:, 0],
            e2=new_matrix[:, 1],
            e3=new_matrix[:, 2],
            ensure_unitary=False
        )

    def wick_rotation(self, real_time: float) -> 'U3Frame':
        """
        Wick rotation: t → -iτ

        Convert real time evolution to imaginary time evolution

        Args:
            real_time: Real time t

        Returns:
            Frame after Wick rotation (imaginary time τ = it)
        """
        tau = -1j * real_time
        return self.imaginary_time_evolution(tau.imag)

    # -------------------- Internal Methods --------------------

    def _gram_schmidt_orthonormalize(self):
        """Gram-Schmidt orthonormalization"""
        # Normalize e1
        norm1 = np.sqrt(np.vdot(self.e1, self.e1).real)
        if norm1 > 1e-10:
            self.e1 = self.e1 / norm1

        # Orthogonalize and normalize e2
        self.e2 = self.e2 - np.vdot(self.e1, self.e2) * self.e1
        norm2 = np.sqrt(np.vdot(self.e2, self.e2).real)
        if norm2 > 1e-10:
            self.e2 = self.e2 / norm2

        # Orthogonalize and normalize e3
        self.e3 = self.e3 - np.vdot(self.e1, self.e3) * self.e1 - np.vdot(self.e2, self.e3) * self.e2
        norm3 = np.sqrt(np.vdot(self.e3, self.e3).real)
        if norm3 > 1e-10:
            self.e3 = self.e3 / norm3

    def _build_su3_matrix(self, params: np.ndarray) -> np.ndarray:
        """Construct SU(3) matrix"""
        # Gell-Mann matrices (λ₁ to λ₈)
        lambda_matrices = self._gell_mann_matrices()

        # Linear combination
        generator = sum(params[i] * lambda_matrices[i] for i in range(8))

        # Exponential map
        return scipy_expm(1j * generator)

    @staticmethod
    def _gell_mann_matrices() -> List[np.ndarray]:
        """Gell-Mann 矩阵（SU(3) 生成元）"""
        λ = [
            # λ₁
            np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex),
            # λ₂
            np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex),
            # λ₃
            np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex),
            # λ₄
            np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=complex),
            # λ₅
            np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex),
            # λ₆
            np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex),
            # λ₇
            np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex),
            # λ₈
            np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=complex) / np.sqrt(3),
        ]
        return λ

    # -------------------- Operator Overloading --------------------

    def __mul__(self, other):
        """Frame multiplication or scalar multiplication"""
        if isinstance(other, (int, float, complex)):
            # Scalar multiplication
            return U3Frame(
                e1=self.e1 * other,
                e2=self.e2 * other,
                e3=self.e3 * other,
                ensure_unitary=False
            )
        elif isinstance(other, U3Frame):
            # Matrix multiplication
            new_matrix = self.matrix @ other.matrix
            return U3Frame(
                e1=new_matrix[:, 0],
                e2=new_matrix[:, 1],
                e3=new_matrix[:, 2],
                ensure_unitary=False
            )
        return NotImplemented

    def __repr__(self):
        phases = self.color_phases()
        return f"U3Frame(phases=(R:{phases[0]:.3f}, G:{phases[1]:.3f}, B:{phases[2]:.3f}), φ={self.global_phase:.3f})"


# ============================================================
# SU(3) Component Class
# ============================================================

@dataclass
class SU3Component:
    """
    SU(3) component (strong interaction gauge group)

    Properties:
        - det(V) = 1
        - V† V = I
        - 8 generators (Gell-Mann matrices)

    Physical meaning:
        - Corresponds to Quantum Chromodynamics (QCD)
        - 8 gluon fields
        - Color charge conservation
    """
    matrix: np.ndarray  # 3×3 SU(3) matrix

    def __post_init__(self):
        """Verify SU(3) properties"""
        det = np.linalg.det(self.matrix)
        if not np.isclose(abs(det), 1.0, atol=1e-6):
            warnings.warn(f"SU(3) matrix determinant is not 1: |det|={abs(det):.6f}")

    def to_gell_mann_params(self) -> np.ndarray:
        """
        Decompose into Gell-Mann matrix parameters

        V = exp(i Σₐ θₐ λₐ)

        Returns:
            8 parameters (θ₁, ..., θ₈)
        """
        # Take logarithm
        log_v = scipy_logm(self.matrix)

        # Extract Hermitian part
        log_v_herm = (log_v - log_v.T.conj()) / (2j)

        # Project onto Gell-Mann matrices
        lambda_matrices = U3Frame._gell_mann_matrices()
        params = np.array([
            np.trace(log_v_herm @ lam).real / 2
            for lam in lambda_matrices
        ])

        return params

    def color_charge(self) -> Tuple[float, float]:
        """
        Color charge (corresponding to two Casimir operators of SU(3))

        Returns:
            (C₁, C₂) - First and second Casimir invariants
        """
        # First Casimir: C₁ = Tr(T) (always 0 for SU(3))
        C1 = np.trace(self.matrix).real

        # Second Casimir: C₂ = Tr(T²)
        C2 = np.trace(self.matrix @ self.matrix).real

        return (C1, C2)


# ============================================================
# Gauge Field Class
# ============================================================

class GaugeConnection:
    """
    Gauge field connection A_μ ∈ 𝔲(3)

    Mathematical form:
        A_μ = A_μ^{SU(3)} + A_μ^{SU(2)} + A_μ^{U(1)}

    Covariant derivative:
        D_μ U = ∂_μ U + A_μ U

    Field strength tensor (curvature):
        F_μν = ∂_μ A_ν - ∂_ν A_μ + [A_μ, A_ν]

    Physical interpretation:
        - A_μ^{SU(3)}: Gluon field (8 components)
        - A_μ^{SU(2)}: W/Z boson field (3 components)
        - A_μ^{U(1)}: Photon field (1 component)
    """

    def __init__(self,
                 su3_component: Optional[np.ndarray] = None,
                 su2_component: Optional[np.ndarray] = None,
                 u1_component: Optional[complex] = None):
        """
        Initialize gauge connection

        Args:
            su3_component: 8×1 real array (Gell-Mann components)
            su2_component: 3×1 real array (Pauli components)
            u1_component: Complex number (U(1) component)
        """
        self.su3 = su3_component if su3_component is not None else np.zeros(8)
        self.su2 = su2_component if su2_component is not None else np.zeros(3)
        self.u1 = u1_component if u1_component is not None else 0.0+0j

    def connection_matrix(self) -> np.ndarray:
        """
        Matrix representation of connection A_μ ∈ 𝔲(3)

        Returns:
            3×3 anti-Hermitian matrix
        """
        # SU(3) part
        lambda_matrices = U3Frame._gell_mann_matrices()
        A_su3 = sum(self.su3[i] * lambda_matrices[i] for i in range(8))

        # SU(2) part (embedded in upper-left 2×2 block)
        pauli_matrices = self._pauli_matrices()
        A_su2_block = sum(self.su2[i] * pauli_matrices[i] for i in range(3))
        A_su2 = np.zeros((3, 3), dtype=complex)
        A_su2[:2, :2] = A_su2_block

        # U(1) part
        A_u1 = self.u1 * np.eye(3)

        return 1j * (A_su3 + A_su2 + A_u1)

    def field_strength(self, other: 'GaugeConnection') -> 'FieldStrength':
        """
        Calculate field strength tensor F_μν = [D_μ, D_ν]

        Args:
            other: Connection in another direction A_ν

        Returns:
            FieldStrength object
        """
        A_mu = self.connection_matrix()
        A_nu = other.connection_matrix()

        # F_μν = [A_μ, A_ν] (simplified version, ignoring derivative terms)
        F_matrix = A_mu @ A_nu - A_nu @ A_mu

        return FieldStrength(F_matrix)

    @staticmethod
    def _pauli_matrices() -> List[np.ndarray]:
        """Pauli 矩阵（SU(2) 生成元）"""
        σ = [
            np.array([[0, 1], [1, 0]], dtype=complex),  # σ₁
            np.array([[0, -1j], [1j, 0]], dtype=complex),  # σ₂
            np.array([[1, 0], [0, -1]], dtype=complex),  # σ₃
        ]
        return σ

    def __repr__(self):
        return f"GaugeConnection(SU(3): {np.linalg.norm(self.su3):.3f}, SU(2): {np.linalg.norm(self.su2):.3f}, U(1): {abs(self.u1):.3f})"


@dataclass
class FieldStrength:
    """
    Field strength tensor F_μν (curvature of gauge field)

    Physical meaning:
        - Electromagnetic field: F_μν corresponds to electric and magnetic fields
        - Non-Abelian gauge field: Field strength of gluons/W bosons
    """
    matrix: np.ndarray  # 3×3 anti-Hermitian matrix

    def yang_mills_action(self) -> float:
        """
        Yang-Mills action: S = -1/(4g²) Tr(F_μν F^μν)

        Returns:
            Action (real number)
        """
        return -0.25 * np.trace(self.matrix @ self.matrix.T.conj()).real

    def topological_charge(self) -> float:
        """
        Topological charge: Q = (1/32π²) ∫ Tr(F ∧ F)

        Returns:
            Topological charge (instanton number)
        """
        # Simplified version: using matrix trace
        return (1.0 / (32 * np.pi**2)) * np.trace(self.matrix @ self.matrix).real


# ============================================================
# Symmetry Breaking Potential
# ============================================================

class SymmetryBreakingPotential:
    """
    Symmetry breaking potential function

    Mathematical form:
        V(U) = -μ² Tr(U†U) + λ [Tr(U†U)]² + γ Tr([U†,U]²)

    Minimum determines symmetry breaking pattern:
        - SU(4) → SU(3) × U(1)
        - SU(3) → SU(2) × U(1)

    Physical analogy:
        - Similar to Higgs potential
        - Vacuum expectation value breaks symmetry
    """

    def __init__(self, mu_squared: float = -1.0, lambda_coupling: float = 0.5, gamma_coupling: float = 0.1):
        """
        Initialize potential parameters

        Args:
            mu_squared: Mass squared term (negative value triggers symmetry breaking)
            lambda_coupling: Quartic coupling constant
            gamma_coupling: Non-Abelian coupling constant
        """
        self.mu2 = mu_squared
        self.lambda_ = lambda_coupling
        self.gamma = gamma_coupling

    def potential(self, frame: U3Frame) -> float:
        """
        Calculate potential V(U)

        Args:
            frame: U(3) frame

        Returns:
            Potential value
        """
        U = frame.matrix
        U_dag = U.T.conj()

        # First term: -μ² Tr(U†U)
        term1 = -self.mu2 * np.trace(U_dag @ U).real

        # Second term: λ [Tr(U†U)]²
        tr_UdagU = np.trace(U_dag @ U)
        term2 = self.lambda_ * (tr_UdagU * tr_UdagU.conj()).real

        # Third term: γ Tr([U†,U]²)
        commutator = U_dag @ U - U @ U_dag
        term3 = self.gamma * np.trace(commutator @ commutator).real

        return term1 + term2 + term3

    def gradient(self, frame: U3Frame) -> np.ndarray:
        """
        Calculate potential gradient ∇V(U)

        Used to minimize potential and find symmetry breaking vacuum

        Returns:
            3×3 complex matrix gradient
        """
        U = frame.matrix
        U_dag = U.T.conj()

        # Numerical gradient (simplified implementation)
        epsilon = 1e-6
        grad = np.zeros((3, 3), dtype=complex)

        V0 = self.potential(frame)

        for i in range(3):
            for j in range(3):
                # Real part direction
                U_perturb = U.copy()
                U_perturb[i, j] += epsilon
                frame_perturb = U3Frame(U_perturb[:, 0], U_perturb[:, 1], U_perturb[:, 2], ensure_unitary=False)
                grad[i, j] = (self.potential(frame_perturb) - V0) / epsilon

                # Imaginary part direction
                U_perturb = U.copy()
                U_perturb[i, j] += 1j * epsilon
                frame_perturb = U3Frame(U_perturb[:, 0], U_perturb[:, 1], U_perturb[:, 2], ensure_unitary=False)
                grad[i, j] += 1j * (self.potential(frame_perturb) - V0) / epsilon

        return grad

    def find_vacuum(self, initial_frame: Optional[U3Frame] = None,
                   max_iterations: int = 100, tolerance: float = 1e-6) -> U3Frame:
        """
        Find vacuum state (potential minimum)

        Using gradient descent method

        Args:
            initial_frame: Initial guess
            max_iterations: Maximum number of iterations
            tolerance: Convergence tolerance

        Returns:
            Vacuum state frame
        """
        if initial_frame is None:
            initial_frame = U3Frame()  # Start from identity frame

        current_frame = initial_frame
        learning_rate = 0.01

        for iteration in range(max_iterations):
            grad = self.gradient(current_frame)
            grad_norm = np.linalg.norm(grad)

            if grad_norm < tolerance:
                print(f"Converged at iteration {iteration}, |∇V| = {grad_norm:.2e}")
                break

            # Gradient descent step
            U_new = current_frame.matrix - learning_rate * grad
            current_frame = U3Frame(U_new[:, 0], U_new[:, 1], U_new[:, 2], ensure_unitary=True)

        return current_frame


# ============================================================
# Auxiliary Functions
# ============================================================

def scipy_expm(matrix: np.ndarray) -> np.ndarray:
    """Matrix exponential function (depends on scipy)"""
    try:
        from scipy.linalg import expm
        return expm(matrix)
    except ImportError:
        # Simplified implementation: Taylor expansion
        return _matrix_exp_taylor(matrix, order=10)

def scipy_logm(matrix: np.ndarray) -> np.ndarray:
    """Matrix logarithm function (depends on scipy)"""
    try:
        from scipy.linalg import logm
        return logm(matrix)
    except ImportError:
        raise NotImplementedError("Requires scipy.linalg.logm")

def _matrix_exp_taylor(A: np.ndarray, order: int = 10) -> np.ndarray:
    """Calculate matrix exponential using Taylor expansion"""
    result = np.eye(A.shape[0], dtype=A.dtype)
    term = np.eye(A.shape[0], dtype=A.dtype)

    for k in range(1, order + 1):
        term = term @ A / k
        result += term

    return result


# ============================================================
# Exports
# ============================================================

__all__ = [
    'U3Frame',
    'SU3Component',
    'GaugeConnection',
    'FieldStrength',
    'SymmetryBreakingPotential',
    'HBAR',
    'C_SPEED',
]


# ============================================================
# Demonstration
# ============================================================

def demonstrate():
    """Demonstrate U(3) complex frame and gauge field"""
    print("=" * 70)
    print("U(3) Complex Frame and Gauge Field Unification Framework Demo")
    print("=" * 70)

    # 1. Create U(3) frame
    print("\n1. Create U(3) complex frame")
    frame = U3Frame()
    print(f"   {frame}")
    print(f"   det(U) = {frame.determinant:.6f}")
    print(f"   Global phase φ = {frame.global_phase:.4f} rad")

    # 2. Color phases
    print("\n2. Color phases (RGB)")
    phases = frame.color_phases()
    print(f"   θ_R (red) = {phases[0]:.4f} rad")
    print(f"   θ_G (green) = {phases[1]:.4f} rad")
    print(f"   θ_B (blue) = {phases[2]:.4f} rad")
    print(f"   Constraint check: θ_R + θ_G + θ_B = {sum(phases):.4f} (should equal φ)")

    # 3. Symmetry decomposition
    print("\n3. U(3) → SU(3) × U(1) decomposition")
    su3_comp, u1_phase = frame.to_su3_u1()
    print(f"   SU(3) component det = {np.linalg.det(su3_comp.matrix):.6f} (should be 1)")
    print(f"   U(1) phase = {u1_phase:.6f}")

    # 4. Quaternion representation
    print("\n4. Quaternion representation (SU(2) subgroup)")
    q = frame.to_quaternion_representation()
    print(f"   q = ({q[0]:.4f}, {q[1]:.4f}, {q[2]:.4f}, {q[3]:.4f})")
    print(f"   |q| = {np.sqrt(sum(abs(x)**2 for x in q)):.6f}")

    # 5. Gauge transformations
    print("\n5. Gauge transformations")
    # U(1) transformation
    frame_u1 = frame.gauge_transform_u1(np.pi/4)
    print(f"   After U(1) transformation: {frame_u1}")

    # SU(2) transformation
    frame_su2 = frame.gauge_transform_su2((0.1, 0.2, 0.3))
    print(f"   After SU(2) transformation: {frame_su2}")

    # 6. Gauge field connection
    print("\n6. Gauge field connection")
    connection = GaugeConnection(
        su3_component=np.random.randn(8) * 0.1,
        su2_component=np.random.randn(3) * 0.1,
        u1_component=0.05+0.02j
    )
    print(f"   {connection}")
    A_matrix = connection.connection_matrix()
    print(f"   ||A_μ|| = {np.linalg.norm(A_matrix):.4f}")

    # 7. Field strength tensor
    print("\n7. Field strength tensor (curvature)")
    connection2 = GaugeConnection(
        su3_component=np.random.randn(8) * 0.1,
        su2_component=np.random.randn(3) * 0.1,
        u1_component=0.03+0.01j
    )
    F = connection.field_strength(connection2)
    print(f"   ||F_μν|| = {np.linalg.norm(F.matrix):.4f}")
    print(f"   Yang-Mills action S = {F.yang_mills_action():.6f}")
    print(f"   Topological charge Q = {F.topological_charge():.6f}")

    # 8. Symmetry breaking
    print("\n8. Symmetry breaking potential")
    potential = SymmetryBreakingPotential(mu_squared=-1.0, lambda_coupling=0.5)
    V = potential.potential(frame)
    print(f"   V(U) = {V:.6f}")
    print(f"   Finding vacuum state...")
    vacuum = potential.find_vacuum(max_iterations=50)
    V_vacuum = potential.potential(vacuum)
    print(f"   V(U_vacuum) = {V_vacuum:.6f}")
    print(f"   Vacuum state: {vacuum}")

    print("\n" + "=" * 70)
    print("Core Theory Summary:")
    print("  • U(3) = [e₁, e₂, e₃] ∈ U(3)  [Complete unitary frame]")
    print("  • U(3) = SU(3) × U(1)  [Symmetry decomposition]")
    print("  • (θ_R, θ_G, θ_B)  [Color phases]")
    print("  • A_μ = A_μ^{SU(3)} + A_μ^{SU(2)} + A_μ^{U(1)}  [Gauge connection]")
    print("  • F_μν = [D_μ, D_ν]  [Field strength tensor]")
    print("  • V(U) minimization → Symmetry breaking pattern")
    print("=" * 70)


if __name__ == "__main__":
    demonstrate()
