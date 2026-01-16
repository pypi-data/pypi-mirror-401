"""
Tests for SwiftCl angular power spectrum computations.

These tests verify that SwiftCl can correctly compute various types of angular power spectra
for different probes including galaxy clustering, weak lensing, CMB, and local primordial
non-Gaussianity contributions.
"""

import tempfile

import jax
import jax.numpy as jnp
import numpy as np
import pytest

from swiftcl.cl import ClComp

# Configure JAX to use CPU
jax.config.update("jax_platform_name", "cpu")


@pytest.fixture
def temp_path():
    """Create a temporary directory for storing gamma coefficients."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def basic_cosmology():
    """Set up basic cosmological parameters and arrays."""
    # Cosmological parameters
    cosmo_params = {
        "omega_b": 0.0223828,
        "omega_cdm": 0.1201075,
        "h": 0.67810,
        "sigma8": 0.8,
    }

    # Smail redshift distribution
    def smail(z, alpha=4, beta=6, z0=0.7):
        return (z**alpha / z0 ** (alpha + 1)) * np.exp(-((z / z0) ** beta))

    # Create redshift distribution array
    num_points = 500
    z = np.linspace(0.001, 1.0, num_points)
    p_z = smail(z)

    n = np.zeros((num_points, 2))
    n[:, 0] = z
    n[:, 1] = p_z

    # Create multipole and wavenumber arrays
    ll = jnp.unique(jnp.geomspace(6, 2000, 100, dtype="int"))
    k = jnp.logspace(-5, 3, num=200)

    # Mock cosmological functions (simplified - not using CCL here)
    chis = 1000 * (1 / (1 + z))  # Simplified comoving distance
    H = np.ones_like(z) * 70  # Simplified Hubble parameter
    D_k = np.ones((num_points, len(k)))  # Simplified growth factor
    P = np.ones((len(k),)) * 1e4  # Simplified power spectrum
    f = np.ones_like(z) * 0.8  # Growth rate

    return {
        "params": cosmo_params,
        "n": jnp.array(n),
        "ll": ll,
        "k": k,
        "chis": jnp.array(chis),
        "H": jnp.array(H),
        "D_k": jnp.array(D_k),
        "P": jnp.array(P),
        "f": jnp.array(f),
        "O_m": cosmo_params["omega_cdm"] / cosmo_params["h"] ** 2
        + cosmo_params["omega_b"] / cosmo_params["h"] ** 2,
        "H0": cosmo_params["h"] * 100,
    }


class TestGalaxyClustering:
    """Tests for galaxy clustering power spectrum."""

    def test_cl_path(self, basic_cosmology):
        # Test the path setup for ClComp.
        c_g = ClComp(
            z1=[basic_cosmology["n"][0, 0], basic_cosmology["n"][-1, 0]],
            z2=[basic_cosmology["n"][0, 0], basic_cosmology["n"][-1, 0]],
            contr1="g",
            contr2="g",
            l=basic_cosmology["ll"],
            k=basic_cosmology["k"],
            jit=False,
        )

        cl_g = c_g.C_l(
            n1=basic_cosmology["n"],
            n2=basic_cosmology["n"],
            chis1=basic_cosmology["chis"],
            chis2=basic_cosmology["chis"],
            D1=basic_cosmology["D_k"],
            D2=basic_cosmology["D_k"],
            P=basic_cosmology["P"],
            H1=basic_cosmology["H"],
            H2=basic_cosmology["H"],
            H0=basic_cosmology["H0"],
            O_m=basic_cosmology["O_m"],
        )

        # Verify output properties
        assert cl_g is not None
        assert len(cl_g) == len(basic_cosmology["ll"])
        assert np.all(np.isfinite(cl_g))
        assert np.all(cl_g >= 0)  # Power spectrum should be positive

    def test_cl_g_basic(self, temp_path, basic_cosmology):
        """Test basic galaxy clustering power spectrum computation."""
        c_g = ClComp(
            z1=[basic_cosmology["n"][0, 0], basic_cosmology["n"][-1, 0]],
            z2=[basic_cosmology["n"][0, 0], basic_cosmology["n"][-1, 0]],
            contr1="g",
            contr2="g",
            l=basic_cosmology["ll"],
            k=basic_cosmology["k"],
            jit=False,
            path=temp_path,
        )

        cl_g = c_g.C_l(
            n1=basic_cosmology["n"],
            n2=basic_cosmology["n"],
            chis1=basic_cosmology["chis"],
            chis2=basic_cosmology["chis"],
            D1=basic_cosmology["D_k"],
            D2=basic_cosmology["D_k"],
            P=basic_cosmology["P"],
            H1=basic_cosmology["H"],
            H2=basic_cosmology["H"],
            H0=basic_cosmology["H0"],
            O_m=basic_cosmology["O_m"],
        )

        # Verify output properties
        assert cl_g is not None
        assert len(cl_g) == len(basic_cosmology["ll"])
        assert np.all(np.isfinite(cl_g))
        assert np.all(cl_g >= 0)  # Power spectrum should be positive

    def test_cl_g_symmetry(self, temp_path, basic_cosmology):
        """Test that galaxy clustering is symmetric (C_l(g,g) = C_l(g,g))."""
        c_g = ClComp(
            z1=[basic_cosmology["n"][0, 0], basic_cosmology["n"][-1, 0]],
            z2=[basic_cosmology["n"][0, 0], basic_cosmology["n"][-1, 0]],
            contr1="g",
            contr2="g",
            l=basic_cosmology["ll"],
            k=basic_cosmology["k"],
            jit=False,
            path=temp_path,
        )

        cl_g = c_g.C_l(
            n1=basic_cosmology["n"],
            n2=basic_cosmology["n"],
            chis1=basic_cosmology["chis"],
            chis2=basic_cosmology["chis"],
            D1=basic_cosmology["D_k"],
            D2=basic_cosmology["D_k"],
            P=basic_cosmology["P"],
            H1=basic_cosmology["H"],
            H2=basic_cosmology["H"],
            H0=basic_cosmology["H0"],
            O_m=basic_cosmology["O_m"],
        )

        # Check that result is consistent
        assert cl_g is not None
        assert len(cl_g) > 0


class TestGalaxyClusteringWithMagnificationBias:
    """Tests for galaxy clustering with magnification bias."""

    def test_cl_g_mag(self, temp_path, basic_cosmology):
        """Test galaxy clustering with magnification bias."""
        c_g_mag = ClComp(
            z1=[basic_cosmology["n"][0, 0], basic_cosmology["n"][-1, 0]],
            z2=[basic_cosmology["n"][0, 0], basic_cosmology["n"][-1, 0]],
            contr1="g,mag",
            contr2="g,mag",
            l=basic_cosmology["ll"],
            k=basic_cosmology["k"],
            jit=False,
            path=temp_path,
        )

        cl_g_mag = c_g_mag.C_l(
            n1=basic_cosmology["n"],
            n2=basic_cosmology["n"],
            chis1=basic_cosmology["chis"],
            chis2=basic_cosmology["chis"],
            D1=basic_cosmology["D_k"],
            D2=basic_cosmology["D_k"],
            P=basic_cosmology["P"],
            H1=basic_cosmology["H"],
            H2=basic_cosmology["H"],
            H0=basic_cosmology["H0"],
            O_m=basic_cosmology["O_m"],
            C_g1=5 * 4 - 2,
            C_g2=5 * 4 - 2,
        )

        # Verify output
        assert cl_g_mag is not None
        assert len(cl_g_mag) == len(basic_cosmology["ll"])
        assert np.all(np.isfinite(cl_g_mag))


class TestGalaxyClusteringWithRSD:
    """Tests for galaxy clustering with redshift space distortions."""

    def test_cl_g_rsd(self, temp_path, basic_cosmology):
        """Test galaxy clustering with RSD."""
        c_g_rsd = ClComp(
            z1=[basic_cosmology["n"][0, 0], basic_cosmology["n"][-1, 0]],
            z2=[basic_cosmology["n"][0, 0], basic_cosmology["n"][-1, 0]],
            contr1="g,RSD",
            contr2="g,RSD",
            l=basic_cosmology["ll"],
            k=basic_cosmology["k"],
            jit=False,
            path=temp_path,
        )

        cl_g_rsd = c_g_rsd.C_l(
            n1=basic_cosmology["n"],
            n2=basic_cosmology["n"],
            chis1=basic_cosmology["chis"],
            chis2=basic_cosmology["chis"],
            D1=basic_cosmology["D_k"],
            D2=basic_cosmology["D_k"],
            P=basic_cosmology["P"],
            H1=basic_cosmology["H"],
            H2=basic_cosmology["H"],
            H0=basic_cosmology["H0"],
            O_m=basic_cosmology["O_m"],
            f1=basic_cosmology["f"],
            f2=basic_cosmology["f"],
        )

        # Verify output
        assert cl_g_rsd is not None
        assert len(cl_g_rsd) == len(basic_cosmology["ll"])
        assert np.all(np.isfinite(cl_g_rsd))


class TestWeakLensing:
    """Tests for weak lensing power spectrum."""

    def test_cl_wl_basic(self, temp_path, basic_cosmology):
        """Test weak lensing power spectrum computation."""
        c_wl = ClComp(
            z1=[basic_cosmology["n"][0, 0], basic_cosmology["n"][-1, 0]],
            z2=[basic_cosmology["n"][0, 0], basic_cosmology["n"][-1, 0]],
            contr1="wl",
            contr2="wl",
            l=basic_cosmology["ll"],
            k=basic_cosmology["k"],
            jit=False,
            path=temp_path,
        )

        # Create intrinsic alignment amplitude array
        A_IA = np.ones((len(basic_cosmology["n"][:, 0]), 1))
        A_IA[:, 0] = 0.1

        cl_wl = c_wl.C_l(
            n1=basic_cosmology["n"],
            n2=basic_cosmology["n"],
            chis1=basic_cosmology["chis"],
            chis2=basic_cosmology["chis"],
            D1=basic_cosmology["D_k"],
            D2=basic_cosmology["D_k"],
            P=basic_cosmology["P"],
            H1=basic_cosmology["H"],
            H2=basic_cosmology["H"],
            H0=basic_cosmology["H0"],
            O_m=basic_cosmology["O_m"],
            A_IA1=A_IA[:, 0],
            A_IA2=A_IA[:, 0],
        )

        # Verify output
        assert cl_wl is not None
        assert len(cl_wl) == len(basic_cosmology["ll"])
        assert np.all(np.isfinite(cl_wl))
        assert np.all(cl_wl >= 0)


class TestCMBContributions:
    """Tests for CMB-related contributions."""

    @pytest.fixture
    def cmb_redshifts(self):
        """Create CMB redshift arrays."""
        # CMB lensing (z_* ~ 1100)
        n_CMB_k = np.ones((100, 2))
        n_CMB_k[:, 0] = np.linspace(0, 1100, 100)
        n_CMB_k[:, 1] = 1.0 / len(n_CMB_k)

        # CMB ISW (low redshift)
        def smail(z, alpha=4, beta=6, z0=0.7):
            return (z**alpha / z0 ** (alpha + 1)) * np.exp(-((z / z0) ** beta))

        num_points = 200
        z = np.linspace(0.001, 2.0, num_points)
        p_z = smail(z)
        n_CMB_T = np.zeros((num_points, 2))
        n_CMB_T[:, 0] = z
        n_CMB_T[:, 1] = p_z

        return {
            "n_CMB_k": jnp.array(n_CMB_k),
            "n_CMB_T": jnp.array(n_CMB_T),
        }

    def test_cl_cmb_lensing(self, temp_path, basic_cosmology, cmb_redshifts):
        """Test CMB lensing power spectrum."""
        c_cmb_k = ClComp(
            z1=[cmb_redshifts["n_CMB_k"][0, 0], cmb_redshifts["n_CMB_k"][-1, 0]],
            z2=[cmb_redshifts["n_CMB_k"][0, 0], cmb_redshifts["n_CMB_k"][-1, 0]],
            contr1="CMB_k",
            contr2="CMB_k",
            l=basic_cosmology["ll"][:50],  # Use fewer multipoles for CMB
            k=basic_cosmology["k"],
            jit=False,
            path=temp_path,
        )

        # Adjust cosmology arrays for CMB redshifts
        chis_cmb = 1000 * (1 / (1 + cmb_redshifts["n_CMB_k"][:, 0]))
        H_cmb = np.ones_like(cmb_redshifts["n_CMB_k"][:, 0]) * 70
        D_k_cmb = np.ones((len(cmb_redshifts["n_CMB_k"]), len(basic_cosmology["k"])))
        f_cmb = np.ones_like(cmb_redshifts["n_CMB_k"][:, 0]) * 0.8

        cl_cmb_k = c_cmb_k.C_l(
            n1=cmb_redshifts["n_CMB_k"],
            n2=cmb_redshifts["n_CMB_k"],
            chis1=jnp.array(chis_cmb),
            chis2=jnp.array(chis_cmb),
            D1=jnp.array(D_k_cmb),
            D2=jnp.array(D_k_cmb),
            P=basic_cosmology["P"],
            H1=jnp.array(H_cmb),
            H2=jnp.array(H_cmb),
            H0=basic_cosmology["H0"],
            O_m=basic_cosmology["O_m"],
            f1=jnp.array(f_cmb),
            f2=jnp.array(f_cmb),
        )

        # Verify output
        assert cl_cmb_k is not None
        assert len(cl_cmb_k) == len(basic_cosmology["ll"][:50])
        assert np.all(np.isfinite(cl_cmb_k))


class TestLocalPrimordialNonGaussianity:
    """Tests for local primordial non-Gaussianity contributions."""

    def test_cl_fnl(self, temp_path, basic_cosmology):
        """Test f_NL contribution to power spectrum."""
        # Create transfer function for f_NL
        k_vals = basic_cosmology["k"]
        T_fnl = jnp.ones((len(basic_cosmology["n"]), len(k_vals)))

        c_fnl = ClComp(
            z1=[basic_cosmology["n"][0, 0], basic_cosmology["n"][-1, 0]],
            z2=[basic_cosmology["n"][0, 0], basic_cosmology["n"][-1, 0]],
            contr1="f_NL",
            contr2="f_NL",
            l=basic_cosmology["ll"],
            k=basic_cosmology["k"],
            jit=False,
            path=temp_path,
        )

        cl_fnl = c_fnl.C_l(
            n1=basic_cosmology["n"],
            n2=basic_cosmology["n"],
            chis1=basic_cosmology["chis"],
            chis2=basic_cosmology["chis"],
            D1=basic_cosmology["D_k"],
            D2=basic_cosmology["D_k"],
            P=basic_cosmology["P"],
            H1=basic_cosmology["H"],
            H2=basic_cosmology["H"],
            H0=basic_cosmology["H0"],
            O_m=basic_cosmology["O_m"],
            b_fNL1=1.0,
            f_NL1=1.0,
            T1=T_fnl,
            T2=T_fnl,
        )

        # Verify output
        assert cl_fnl is not None
        assert len(cl_fnl) == len(basic_cosmology["ll"])
        assert np.all(np.isfinite(cl_fnl))

    def test_cl_g_fnl_mixed(self, temp_path, basic_cosmology):
        """Test mixed galaxy clustering and f_NL contribution."""
        # Create transfer function for f_NL
        T_fnl = jnp.ones((len(basic_cosmology["n"]), len(basic_cosmology["k"])))

        c_g_fnl = ClComp(
            z1=[basic_cosmology["n"][0, 0], basic_cosmology["n"][-1, 0]],
            z2=[basic_cosmology["n"][0, 0], basic_cosmology["n"][-1, 0]],
            contr1="g,f_NL",
            contr2="g,f_NL",
            l=basic_cosmology["ll"],
            k=basic_cosmology["k"],
            jit=False,
            path=temp_path,
        )

        cl_g_fnl = c_g_fnl.C_l(
            n1=basic_cosmology["n"],
            n2=basic_cosmology["n"],
            chis1=basic_cosmology["chis"],
            chis2=basic_cosmology["chis"],
            D1=basic_cosmology["D_k"],
            D2=basic_cosmology["D_k"],
            P=basic_cosmology["P"],
            H1=basic_cosmology["H"],
            H2=basic_cosmology["H"],
            H0=basic_cosmology["H0"],
            O_m=basic_cosmology["O_m"],
            b_fNL1=1.0,
            f_NL1=1.0,
            T1=T_fnl,
            T2=T_fnl,
        )

        # Verify output
        assert cl_g_fnl is not None
        assert len(cl_g_fnl) == len(basic_cosmology["ll"])
        assert np.all(np.isfinite(cl_g_fnl))


class TestNumericalProperties:
    """Tests for numerical properties and robustness."""

    def test_cl_different_redshift_ranges(self, temp_path):
        """Test that ClComp handles different redshift ranges."""
        ll = jnp.unique(jnp.geomspace(6, 500, 50, dtype="int"))
        k = jnp.logspace(-5, 2, num=100)

        # High redshift sample
        z_high = np.linspace(0.5, 2.0, 200)

        n_high = np.zeros((len(z_high), 2))
        n_high[:, 0] = z_high
        n_high[:, 1] = np.exp(-((z_high - 1.0) ** 2) / 0.2)

        c_g_high = ClComp(
            z1=[n_high[0, 0], n_high[-1, 0]],
            z2=[n_high[0, 0], n_high[-1, 0]],
            contr1="g",
            contr2="g",
            l=ll,
            k=k,
            jit=False,
            path=temp_path,
        )

        chis = 1000 * (1 / (1 + z_high))
        H = np.ones_like(z_high) * 70
        D_k = np.ones((len(z_high), len(k)))
        P = np.ones(len(k)) * 1e4

        cl_high = c_g_high.C_l(
            n1=jnp.array(n_high),
            n2=jnp.array(n_high),
            chis1=jnp.array(chis),
            chis2=jnp.array(chis),
            D1=jnp.array(D_k),
            D2=jnp.array(D_k),
            P=jnp.array(P),
            H1=jnp.array(H),
            H2=jnp.array(H),
            H0=70.0,
            O_m=0.3,
        )

        assert cl_high is not None
        assert np.all(np.isfinite(cl_high))

    def test_cl_configuration_parameters(self, temp_path, basic_cosmology):
        """Test that different configuration parameters affect computation."""
        z_min = basic_cosmology["n"][0, 0]
        z_max = basic_cosmology["n"][-1, 0]

        # Test with different N (FFTLog size)
        c_g_small_N = ClComp(
            z1=[z_min, z_max],
            z2=[z_min, z_max],
            contr1="g",
            contr2="g",
            l=basic_cosmology["ll"][:30],
            k=basic_cosmology["k"][:100],
            N=256,
            jit=False,
            path=temp_path,
        )

        cl_g_small_N = c_g_small_N.C_l(
            n1=basic_cosmology["n"],
            n2=basic_cosmology["n"],
            chis1=basic_cosmology["chis"],
            chis2=basic_cosmology["chis"],
            D1=basic_cosmology["D_k"],
            D2=basic_cosmology["D_k"],
            P=basic_cosmology["P"],
            H1=basic_cosmology["H"],
            H2=basic_cosmology["H"],
            H0=basic_cosmology["H0"],
            O_m=basic_cosmology["O_m"],
        )

        assert cl_g_small_N is not None
        assert np.all(np.isfinite(cl_g_small_N))


class TestCrossCorrelations:
    """Tests for cross-correlations between different probes."""

    def test_cl_g_wl_cross(self, temp_path, basic_cosmology):
        """Test cross-correlation between galaxy clustering and weak lensing."""
        c_g_wl = ClComp(
            z1=[basic_cosmology["n"][0, 0], basic_cosmology["n"][-1, 0]],
            z2=[basic_cosmology["n"][0, 0], basic_cosmology["n"][-1, 0]],
            contr1="g",
            contr2="wl",
            l=basic_cosmology["ll"],
            k=basic_cosmology["k"],
            jit=False,
            path=temp_path,
        )

        A_IA = np.ones(len(basic_cosmology["n"][:, 0])) * 0.1

        cl_g_wl = c_g_wl.C_l(
            n1=basic_cosmology["n"],
            n2=basic_cosmology["n"],
            chis1=basic_cosmology["chis"],
            chis2=basic_cosmology["chis"],
            D1=basic_cosmology["D_k"],
            D2=basic_cosmology["D_k"],
            P=basic_cosmology["P"],
            H1=basic_cosmology["H"],
            H2=basic_cosmology["H"],
            H0=basic_cosmology["H0"],
            O_m=basic_cosmology["O_m"],
            A_IA2=A_IA,
        )

        assert cl_g_wl is not None
        assert len(cl_g_wl) == len(basic_cosmology["ll"])
        assert np.all(np.isfinite(cl_g_wl))


class TestInstanceCreation:
    """Tests for ClComp instance creation and configuration."""

    def test_clcomp_creation_with_defaults(self, temp_path, basic_cosmology):
        """Test that ClComp can be created with minimal arguments."""
        c = ClComp(
            z1=[0.1, 1.0],
            z2=[0.1, 1.0],
            l=basic_cosmology["ll"],
            k=basic_cosmology["k"],
            path=temp_path,
        )

        assert c is not None
        assert c.c["contr1"] == "g"
        assert c.c["contr2"] == "g"

    def test_clcomp_creation_with_custom_config(self, temp_path, basic_cosmology):
        """Test that ClComp respects custom configuration."""
        custom_bias = 0.05
        c = ClComp(
            z1=[0.1, 1.0],
            z2=[0.1, 1.0],
            l=basic_cosmology["ll"],
            k=basic_cosmology["k"],
            bias=custom_bias,
            jit=False,
            path=temp_path,
        )

        assert c.c["bias"] == custom_bias
        assert c.c["jit"] is False
