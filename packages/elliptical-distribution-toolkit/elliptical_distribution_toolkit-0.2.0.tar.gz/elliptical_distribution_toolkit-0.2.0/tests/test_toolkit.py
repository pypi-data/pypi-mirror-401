"""
-------------------------------------------------------------------------------

Unit tests for the `elliptical-distribution-toolkit` package

-------------------------------------------------------------------------------
"""

import unittest
import numpy as np
import scipy.stats
import itertools

import elliptical_distribution_toolkit as ell_tools


class TestEllipticalTools(unittest.TestCase):
    """Unit tests for the `elliptical_tools` module"""

    # noinspection PyPep8Naming
    @staticmethod
    def make_scatter_matrix(C: np.ndarray, svs: np.ndarray) -> np.ndarray:
        """builds a scatter matrix from components"""

        return np.diag(svs).dot(C).dot(np.diag(svs))

    def make_comparable_list(self, array: np.ndarray) -> list:
        """Encapsulate rounded-list generation"""

        return list((self.rebase * np.round(array, self.precision)).astype(int))

    def setUp(self) -> None:
        """Recurring setup"""

        # defs
        np.random.seed(0)
        self.n_samples = 100000
        self.precision = 4
        self.rebase = np.power(10.0, self.precision).astype(int)

        # 1d case
        self.loc_1d = -3.1
        self.disp_1d = 7

        # 2d case
        self.loc_2d = np.array([1, -2], dtype=float)
        self.rho_2d = -3.0 / 5
        self.C_2d = np.array([[1, self.rho_2d], [self.rho_2d, 1]], dtype=float)
        self.svs_2d = np.array([1, 2], dtype=float)
        self.scatter_2d = self.make_scatter_matrix(self.C_2d, self.svs_2d)

    def test_t_distribution_samplecount_loss_factor(self):
        """Regression test for tabulated factors and unit test for interpolation"""

        # regression setup
        select_tabulated_loss_factors_theo = np.array(
            [
                [3, 66],
                [4, 8.7],
                [5, 3.5],
                [6, 2.4],
                [7, 2],
                [8, 1.8],
                [9, 1.6],
                [10, 1.5],
                [20, 1.2],
                [50, 1.1],
                [100, 1],
            ]
        )

        # regression test
        precision = 4
        with self.subTest(msg="test tabulated points (as regression)"):

            for df, factor_theo in select_tabulated_loss_factors_theo:

                factor_test = ell_tools.t_distribution_samplecount_loss_factor(
                    df
                )

                self.assertAlmostEqual(factor_test, factor_theo, precision)

        # interp setup
        tabulated_df_values = np.array(
            [
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                20,
                50,
                100,
            ]
        )
        pairwise_df_values = np.hstack(
            (
                tabulated_df_values[:-1, np.newaxis],
                tabulated_df_values[1:, np.newaxis],
            )
        )

        # test
        with self.subTest(msg="spot-check interpolation"):

            for df_low, df_high in pairwise_df_values:

                loss_df_low = ell_tools.t_distribution_samplecount_loss_factor(
                    df_low
                )
                loss_df_high = ell_tools.t_distribution_samplecount_loss_factor(
                    df_high
                )
                df_mean: float = np.mean([df_low, df_high])
                loss_mean: float = np.mean([loss_df_low, loss_df_high])

                loss_interp = ell_tools.t_distribution_samplecount_loss_factor(
                    df_mean
                )

                # invoking Jensen's inequality
                self.assertGreaterEqual(loss_mean, loss_interp, precision)

    def test_minimum_sample_count_for_statistical_variance_bounds_at_select_pts(
        self,
    ):
        """Spot checks solver results"""

        var_dev_bounds = np.array([1.05, 1.025])
        var_qtl_bounds = np.array([0.9, 0.95, 0.975])
        var_bound_pairs = np.array(
            list(itertools.product(var_dev_bounds, var_qtl_bounds))
        )
        n_samples_theos = np.array([1431, 2339, 3309, 5487, 9003, 12760])

        # iterate over Gaussian case (df = inf)
        with self.subTest(msg="Gaussian case"):

            for i, (var_dev, var_qtl) in enumerate(var_bound_pairs):

                n_samples_test = ell_tools.minimum_sample_count_for_statistical_variance_bounds(
                    var_dev, var_qtl
                )
                self.assertEqual(n_samples_test, n_samples_theos[i])

        # iterate again now with St-t case
        df = 4
        loss_factor = ell_tools.t_distribution_samplecount_loss_factor(df)
        with self.subTest(msg="St-t case"):

            for i, (var_dev, var_qtl) in enumerate(var_bound_pairs):

                n_samples_theo = np.round(
                    loss_factor * n_samples_theos[i]
                ).astype(int)
                n_samples_test = ell_tools.minimum_sample_count_for_statistical_variance_bounds(
                    var_dev, var_qtl, df
                )
                self.assertEqual(n_samples_test, n_samples_theo)

    def test_infer_data_dimension_correctly_infers_for_1d_thru_4d_data(self):
        """Infer dimension as # of data columns increases"""

        # 1d vector
        with self.subTest(msg="1d vector"):
            data = np.linspace(0, 1, 100)
            dim_theo = 1
            dim_test = ell_tools.infer_data_dimension(data)

            self.assertEqual(dim_test, dim_theo)

        # n-d panels
        dims = 1 + np.arange(4, dtype="int")
        n_init = 1200

        for i, dim_theo in enumerate(dims):

            data = np.arange(n_init).reshape(
                (n_init / dim_theo).astype(int), dim_theo
            )
            dim_test = ell_tools.infer_data_dimension(data)

            with self.subTest(msg="dimension: {0}".format(dim_theo)):

                self.assertEqual(dim_test, dim_theo)

    # noinspection PyPep8Naming
    def test_covariance_to_correlation_correctly_computes_correlation(self):
        """Test corr_mtx from cov_mtx and the reconstruction of cov_mtx"""

        # defs
        dims = np.array([2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=int)
        np.random.seed(0)

        # iter on dimension
        for dim in dims:

            # build positive-def cov matrix
            A = np.random.rand(dim, dim)
            cov_mtx_orig = 0.5 * (A + A.T) + dim * np.eye(dim)

            # decompose
            corr_mtx, std_devs = ell_tools.covariance_to_correlation(
                cov_mtx_orig
            )

            # rebuild
            cov_mtx_test = np.diag(std_devs) @ corr_mtx @ np.diag(std_devs)

            # test
            with self.subTest(msg="dim = {0}".format(dim)):

                # test trace
                self.assertEqual(np.round(np.trace(corr_mtx)).astype(int), dim)

                # test pos def
                e, v = np.linalg.eig(corr_mtx)
                self.assertTrue(np.all(e > 0))

                # test the reconstruction of the cov matrix
                self.assertSequenceEqual(
                    self.make_comparable_list(cov_mtx_test.flatten()),
                    self.make_comparable_list(cov_mtx_orig.flatten()),
                )

    def test_z_scores_are_correct_given_random_samples(self):
        """z-scores refer to 1D distributions"""

        # defs
        loc = self.loc_1d
        disp = self.disp_1d
        rvs = np.random.normal(loc, disp, self.n_samples)

        # test
        z_score_theo = (rvs - loc) / disp
        z_score_test = ell_tools.z_score(rvs, loc, disp)

        self.assertSequenceEqual(
            self.make_comparable_list(z_score_test),
            self.make_comparable_list(z_score_theo),
        )

    def test_point_weights_tdist_parametric_for_mv_gaussian_data(self):
        """Confirm that weights are unity for the Gaussian case"""

        # setup
        data = scipy.stats.multivariate_normal.rvs(
            self.loc_2d, self.scatter_2d, self.n_samples
        )
        df = np.inf

        # weights, test and theo
        weights_test = ell_tools.point_weights_tdist_parametric(
            data, df, self.loc_2d, self.scatter_2d
        )
        weights_theo = np.ones(self.n_samples)

        # test
        self.assertEqual(weights_test.shape[0], self.n_samples)
        self.assertSequenceEqual(list(weights_test), list(weights_theo))

    def test_point_weights_tdist_parametric_for_1d_linear_samples(self):
        """Confirm correct sample weights for 1D samples"""

        # defs
        df_value = 4
        loc = self.loc_1d
        disp = self.disp_1d
        scatter = disp**2
        samples = np.linspace(-5, 5, self.n_samples)

        # theo values
        z_scores = ell_tools.z_score(samples, loc, disp)
        weights_theo = (df_value + 1) / (df_value + z_scores**2)

        # test values
        weights_test = ell_tools.point_weights_tdist_parametric(
            samples, df_value, loc, scatter
        )

        # test
        self.assertSequenceEqual(
            self.make_comparable_list(weights_test),
            self.make_comparable_list(weights_theo),
        )

    # noinspection PyPep8Naming
    def test_mahal_explicit_is_correct_along_1d_line(self):
        """Confirms that parametric Ma2 is correct value for 1d line"""

        # params
        loc = self.loc_1d
        disp = self.disp_1d
        scatter = disp**2

        # set up line
        linear_pts = np.linspace(-5, 5, 100) + loc

        # compute test and theo
        Ma2_test = ell_tools.mahal_explicit(linear_pts, loc, scatter)
        Ma2_theo = (linear_pts - loc) ** 2 / scatter

        # test parametric reduced
        self.assertSequenceEqual(
            self.make_comparable_list(Ma2_test),
            self.make_comparable_list(Ma2_theo),
        )

    # noinspection PyPep8Naming
    def test_mahal_explicit_is_correct_around_2d_iso_contour(self):
        """Confirms that parametric Ma2 is correct value for iso-contour"""

        # params
        loc_vec = self.loc_2d
        scatter_mtx = self.scatter_2d
        l_scatter = np.linalg.cholesky(scatter_mtx)

        # set up fixed-Ma2 distance data vector
        thetas = np.linspace(-np.pi, np.pi, self.n_samples)
        radius = np.pi
        circular_pts = (
            radius * np.array([np.cos(thetas), np.sin(thetas)]).T + loc_vec
        )

        # switch to a collection of anisotropic pts
        anisotropic_pts = (circular_pts - loc_vec).dot(l_scatter.T) + loc_vec

        # compute parametric mahal distance, test and theo
        Ma2_theo = radius**2 * np.ones(self.n_samples)
        Ma2_test = ell_tools.mahal_explicit(
            anisotropic_pts, loc_vec, scatter_mtx
        )

        # test parametric reduced
        self.assertSequenceEqual(
            self.make_comparable_list(Ma2_test),
            self.make_comparable_list(Ma2_theo),
        )

    def test_point_weights_tdist_parametric_around_2d_iso_contour(self):
        """Confirms that point weights are correct for a 2d iso contour"""

        # params
        loc_vec = self.loc_2d
        scatter_mtx = self.scatter_2d
        l_scatter = np.linalg.cholesky(scatter_mtx)

        # set up fixed-Ma2 distance data vector
        thetas = np.linspace(-np.pi, np.pi, self.n_samples)
        radius = np.pi
        circular_pts = (
            radius * np.array([np.cos(thetas), np.sin(thetas)]).T + loc_vec
        )
        n_dim = ell_tools.infer_data_dimension(circular_pts)

        # switch to a collection of anisotropic pts
        anisotropic_pts = (circular_pts - loc_vec).dot(l_scatter.T) + loc_vec

        # compute point weights
        df = 13
        weights_test = ell_tools.point_weights_tdist_parametric(
            anisotropic_pts, df, loc_vec, scatter_mtx
        )
        weights_theo = (df + n_dim) / (df + radius**2) * np.ones_like(thetas)

        # test parametric reduced
        self.assertSequenceEqual(
            self.make_comparable_list(weights_test),
            self.make_comparable_list(weights_theo),
        )

    def test_mahal_estimated_is_correct_around_2d_iso_contour(self):
        """Confirms that mahal_estimated returns correct isocontour distances"""

        # params
        loc_vec = self.loc_2d
        scatter_mtx = self.scatter_2d
        l_scatter = np.linalg.cholesky(scatter_mtx)

        # set up fixed-Ma2 distance data vector
        thetas = np.linspace(-np.pi, np.pi, self.n_samples)
        radius = np.pi
        circular_pts = (
            radius * np.array([np.cos(thetas), np.sin(thetas)]).T + loc_vec
        )

        # switch to a collection of anisotropic pts
        anisotropic_pts = (circular_pts - loc_vec).dot(l_scatter.T) + loc_vec

        # set the weights vector
        weight_scale = 1.0 / 3.0
        weights = weight_scale * np.ones(self.n_samples)

        """
        Covariance of a 2D circle:

                    ( <c^2>_2pi     <cs>_2pi  )
            cov C = (                         )   =  1/2 I(2)
                    ( <cs>_2pi      <s^2>_2pi )

        We must correct for the (1/2) factor that's introduced when numerically
        computing the data covariance. 
        """
        circle_correction_factor = 0.5

        # compute parametric mahal distance, test and theo
        Ma2_theo = (1 / weight_scale) * np.ones(self.n_samples)
        Ma2_test = circle_correction_factor * ell_tools.mahal_estimated(
            anisotropic_pts, weights
        )

        # test
        avg_err = np.linalg.norm(Ma2_test - Ma2_theo) / self.n_samples
        self.assertAlmostEqual(avg_err, 0.0, self.precision)

    def test_mahal_estimated_correctly_scales_with_data_and_weights(self):
        """Confirms Ma2 scaling for data -> scale data and w -> scale w"""

        # params
        loc_vec = self.loc_2d
        scatter_mtx = self.scatter_2d
        l_scatter = np.linalg.cholesky(scatter_mtx)
        scale_factor = 1.0 / 3.0

        # set up fixed-Ma2 distance data vector
        thetas = np.linspace(-np.pi, np.pi, self.n_samples)
        circular_pts = np.array([np.cos(thetas), np.sin(thetas)]).T + loc_vec
        anisotropic_pts = (circular_pts - loc_vec).dot(l_scatter.T) + loc_vec
        circle_correction_factor = 0.5

        # set the weights vector
        weights = np.ones(self.n_samples)

        Ma2_test_unscaled = (
            circle_correction_factor
            * ell_tools.mahal_estimated(anisotropic_pts, weights)
        )
        Ma2_test_data_scaled = (
            circle_correction_factor
            * ell_tools.mahal_estimated(scale_factor * anisotropic_pts, weights)
        )
        Ma2_test_weight_scaled = (
            circle_correction_factor
            * ell_tools.mahal_estimated(anisotropic_pts, scale_factor * weights)
        )

        # tests
        with self.subTest(msg="data scaling"):
            avg_err = (
                np.linalg.norm(Ma2_test_data_scaled - Ma2_test_unscaled)
                / self.n_samples
            )
            self.assertAlmostEqual(avg_err, 0.0, self.precision)

        with self.subTest(msg="weight scaling"):
            avg_err = (
                np.linalg.norm(
                    Ma2_test_weight_scaled - Ma2_test_unscaled / scale_factor
                )
                / self.n_samples
            )
            self.assertAlmostEqual(avg_err, 0.0, self.precision)

    # noinspection SpellCheckingInspection,PyPep8Naming
    def test_mv_studentt_elliptical_fit_produces_approx_2d_params_from_mv_rvs(
        self,
    ):
        """Confirms mv_studentt_elliptical_fit can estimate loc, scatter from known 2d rvs"""

        # prepare to sweep df values
        n_samples = np.power(10, 6)
        loc_vec = self.loc_2d
        scatter_mtx = self.scatter_2d
        df_v = np.array([3, 5, 7, 10, 20, 30, 40, 50])
        sample_scalings = np.array([5, 2, 2, 2, 1, 1, 1, 1])

        # sweep df
        for i, df_fix in enumerate(df_v):

            # fetch mv_rvs
            mv_rvs = scipy.stats.multivariate_t.rvs(
                loc=loc_vec,
                shape=scatter_mtx,
                df=df_fix,
                size=(sample_scalings[i] * n_samples),
            )

            # compute actual weights
            weights_vec = ell_tools.point_weights_tdist_parametric(
                mv_rvs, df_fix, loc_vec, scatter_mtx
            )

            # estimate St-t params from mv_studentt_elliptical_fit
            (
                loc_hat,
                scatter_hat,
                weights_hat,
                n_iter,
            ) = ell_tools.mv_studentt_elliptical_fit(mv_rvs, df_fix, tol=1e-6)

            # tests
            with self.subTest(msg="df: {0} -- loc".format(df_fix)):
                for i, loc_value in enumerate(loc_vec):
                    self.assertAlmostEqual(loc_value, loc_hat[i], places=2)

            with self.subTest(msg="df: {0} -- scatter".format(df_fix)):
                scatter_hat_flat = scatter_hat.flatten()
                scatter_mtx_flat = scatter_mtx.flatten()
                for i, scat_value in enumerate(scatter_mtx_flat):
                    self.assertAlmostEqual(
                        scatter_hat_flat[i] / scat_value, 1.0, places=2
                    )

            with self.subTest(msg="df: {0} -- weights".format(df_fix)):
                self.assertAlmostEqual(
                    np.linalg.norm(weights_vec - weights_hat) / n_samples,
                    0.0,
                    places=4,
                )

    # noinspection PyPep8Naming
    def test_robust_mv_studentt_elliptical_fit_approx_3d_params_from_mv_rvs(
        self,
    ):
        """Confirms mv_studentt_elliptical_fit can estimate loc, scatter from known 3d rvs"""

        # prepare to sweep df values
        n_samples = np.power(10, 6)
        df_v = np.array([3, 5, 7, 10, 20, 30, 40, 50])
        weight_places = np.array([3, 3, 4, 4, 4, 4, 4, 4])

        # loc_vec = np.zeros(3)
        loc_vec = np.array([1, -2, 3])
        rho_xy = 3.0 / 5
        rho_xz = 2.0 / 5
        rho_yz = 2.5 / 5
        C = np.array(
            [[1, rho_xy, rho_xz], [rho_xy, 1, rho_yz], [rho_xz, rho_yz, 1]]
        )
        svs = np.sqrt(np.array([1, 2, 3]))  # singular values
        scatter_mtx = np.diag(svs).dot(C).dot(np.diag(svs))

        # sweep df
        for i, df_fix in enumerate(df_v):

            # fetch mv_rvs
            mv_rvs = scipy.stats.multivariate_t.rvs(
                loc=loc_vec, shape=scatter_mtx, df=df_fix, size=n_samples
            )

            # compute actual weights
            weights_vec = ell_tools.point_weights_tdist_parametric(
                mv_rvs, df_fix, loc_vec, scatter_mtx
            )

            # estimate St-t params from mv_studentt_elliptical_fit
            (
                loc_hat,
                scatter_hat,
                weights_hat,
                n_iter,
            ) = ell_tools.mv_studentt_elliptical_fit(mv_rvs, df_fix, tol=1e-6)

            # tests
            with self.subTest(msg="df: {0} -- loc".format(df_fix)):
                for j, loc_value in enumerate(loc_vec):
                    self.assertAlmostEqual(loc_value, loc_hat[j], places=2)

            with self.subTest(msg="df: {0} -- scatter".format(df_fix)):

                scatter_hat_flat = scatter_hat.flatten()
                scatter_mtx_flat = scatter_mtx.flatten()

                for j, scat_value in enumerate(scatter_mtx_flat):
                    self.assertAlmostEqual(
                        scatter_hat_flat[j] / scat_value,
                        1.0,
                        places=1,
                    )

            with self.subTest(msg="df: {0} -- weights".format(df_fix)):
                self.assertAlmostEqual(
                    np.linalg.norm(weights_vec - weights_hat) / n_samples,
                    0.0,
                    places=weight_places[i],
                )

    def test_robust_mv_studentt_elliptical_fit_approx_4d_params_from_mv_rvs(
        self,
    ):
        """Confirms mv_studentt_elliptical_fit can estimate loc, scatter from known 4d rvs"""

        # prepare to sweep df values
        n_samples = np.power(10, 6)
        df_v = np.array([3, 5, 7, 10, 20, 30, 40, 50])
        weight_places = np.array([3, 3, 3, 3, 4, 4, 4, 4])
        df_cutover = 20

        loc_vec = np.zeros(4)
        rho_wx = 1.0 / 5
        rho_wy = 0.5 / 5
        rho_wz = 0.25 / 5
        rho_xy = 3.0 / 5
        rho_xz = 2.0 / 5
        rho_yz = 2.5 / 5
        C = np.array(
            [
                [1, rho_wx, rho_wy, rho_wz],
                [rho_wx, 1, rho_xy, rho_xz],
                [rho_wy, rho_xy, 1, rho_yz],
                [rho_wz, rho_xz, rho_yz, 1],
            ]
        )
        svs = np.sqrt(np.array([1, 2, 3, 4]))  # singular values
        scatter_mtx = np.diag(svs).dot(C).dot(np.diag(svs))

        # sweep df
        for i, df_fix in enumerate(df_v):

            # fetch mv_rvs
            mv_rvs = scipy.stats.multivariate_t.rvs(
                loc=loc_vec, shape=scatter_mtx, df=df_fix, size=n_samples
            )

            # compute actual weights
            weights_vec = ell_tools.point_weights_tdist_parametric(
                mv_rvs, df_fix, loc_vec, scatter_mtx
            )

            # estimate St-t params from mv_studentt_elliptical_fit
            (
                loc_hat,
                scatter_hat,
                weights_hat,
                n_iter,
            ) = ell_tools.mv_studentt_elliptical_fit(mv_rvs, df_fix, tol=1e-6)

            # tests
            with self.subTest(msg="df: {0} -- loc".format(df_fix)):
                for j, loc_value in enumerate(loc_vec):
                    self.assertAlmostEqual(loc_value, loc_hat[j], places=2)

            with self.subTest(msg="df: {0} -- scatter".format(df_fix)):

                scatter_hat_flat = scatter_hat.flatten()
                scatter_mtx_flat = scatter_mtx.flatten()

                if df_fix < df_cutover:
                    for j, scat_value in enumerate(scatter_mtx_flat):
                        test_val = scatter_hat_flat[j] / scat_value
                        self.assertTrue(0.7 <= test_val <= 1.1)
                else:
                    for j, scat_value in enumerate(scatter_mtx_flat):
                        self.assertAlmostEqual(
                            scatter_hat_flat[j] / scat_value,
                            1.0,
                            places=1,
                        )

            with self.subTest(msg="df: {0} -- weights".format(df_fix)):
                self.assertAlmostEqual(
                    np.linalg.norm(weights_vec - weights_hat) / n_samples,
                    0.0,
                    places=weight_places[i],
                )
