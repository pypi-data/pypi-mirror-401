from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Iterator

if TYPE_CHECKING:
    from pathlib import Path

import h5py
import matplotlib.pyplot as plt
import numpy as np
import pytest

from daxs.correctors import ConcentrationCorrectionError
from daxs.measurements import Measurement, Measurement1D, Rixs
from daxs.sources import Hdf5Source
from daxs.utils import resources


@pytest.fixture
def mock_hdf5_path(tmp_path_factory: pytest.TempPathFactory) -> Iterator[Path]:
    path = tmp_path_factory.mktemp("files") / "tmp.h5"
    with h5py.File(path, "w") as fh:
        for i in range(1, 4):
            fh.create_dataset(f"{i}.1/measurement/x", data=[i, i + 1, i + 2])
            fh.create_dataset(f"{i}.1/measurement/signal", data=[i, i * 2, i * 3])
    yield path
    os.remove(path)


def test_measurement_init(mock_hdf5_path: str):
    data_mappings = {"x": ".1/measurement/x", "signal": ".1/measurement/signal"}

    source = Hdf5Source(mock_hdf5_path, 1, data_mappings)
    measurement = Measurement(source)
    assert np.allclose(measurement.scans[0].signal, np.array([1, 2, 3]))

    source = Hdf5Source(mock_hdf5_path, [1, 2], data_mappings)
    measurement = Measurement(source)
    assert np.allclose(measurement.scans[1].x, np.array([2, 3, 4]))
    assert np.allclose(measurement.scans[1].signal, np.array([2, 4, 6]))


def test_measurement_remove_scans(mock_hdf5_path: str):
    data_mappings = {"x": ".1/measurement/x", "signal": ".1/measurement/signal"}
    source = Hdf5Source(mock_hdf5_path, [1, 2, 3], data_mappings)
    measurement = Measurement(source)

    indices = [1, 2, 3]
    measurement.remove_scans(indices)
    assert len(measurement.scans) == 0


@pytest.fixture()
def hdf5_path() -> str:
    return resources.getfile("Pd_foil_La_XANES.h5")


@pytest.fixture()
def data_mappings():
    return {
        "x": ".1/measurement/hdh_angle",
        "signal": [".1/measurement/g09", ".1/measurement/g14"],
    }


def test_measurement1d_properties(hdf5_path: str, data_mappings: dict[str, Any]):
    source = Hdf5Source(hdf5_path, [3, 4, 7], data_mappings=data_mappings)
    measurement = Measurement1D(source)
    assert measurement.x[-1] == pytest.approx(38.72936736)
    assert measurement.signal[-1] == pytest.approx(7.054761)

    data_mappings.update({"monitor": ".1/measurement/I0t"})
    source = Hdf5Source(hdf5_path, [3, 4, 7], data_mappings=data_mappings)
    measurement = Measurement1D(source)
    assert measurement.monitor[-1] == pytest.approx(55905.9619046667)

    measurement.process(normalization="area")
    assert measurement.signal[-1] == pytest.approx(0.0012821686)

    measurement.x = np.append(measurement.x, 39.0)
    assert np.isnan(measurement.signal[-1])


def test_measurement1d_aggregate(hdf5_path: str, data_mappings: dict[str, Any]):
    source = Hdf5Source(hdf5_path, [7], data_mappings=data_mappings)
    measurement = Measurement1D(source)
    assert np.all(measurement.x == measurement.scans[0].x)

    measurement.aggregate()
    assert np.all(measurement.signal == measurement.scans[0].signal)

    assert np.all(measurement.signal == measurement.scans[0].signal)

    data_mappings.update({"monitor": ".1/measurement/I0t"})
    source = Hdf5Source(hdf5_path, [7], data_mappings=data_mappings)
    measurement = Measurement1D(source)
    measurement.aggregate()
    assert measurement.signal[-1] == pytest.approx(0.0001546175)

    source = Hdf5Source(hdf5_path, [3, 7], data_mappings=data_mappings)
    measurement = Measurement1D(source)
    measurement.aggregate(mode="fraction of sums")
    assert measurement.signal[-1] == pytest.approx(0.0001306488)

    measurement.reset()
    measurement.aggregate(mode="mean of fractions")
    assert measurement.signal[-1] == pytest.approx(0.00013064935)

    with pytest.raises(ValueError):
        measurement.aggregate(mode="wrong")


def test_measurement1d_normalize(hdf5_path: str, data_mappings: dict[str, Any]):
    data_mappings.update({"monitor": ".1/measurement/I0t"})
    source = Hdf5Source(hdf5_path, [7], data_mappings=data_mappings)
    measurement = Measurement1D(source)

    with pytest.raises(ValueError):
        measurement.normalize(mode="wrong")

    measurement.normalize(mode="area")
    assert measurement.signal[-1] == pytest.approx(0.0015740913)

    measurement.normalize(mode="maximum")
    assert measurement.signal[-1] == pytest.approx(0.0004231201)

    measurement.reset()
    measurement.normalize(mode="maximum")
    assert measurement.signal[-1] == pytest.approx(0.0004231201)


def test_measurement1d_outliers(hdf5_path: str, data_mappings: dict[str, Any]):
    data_mappings.update({"monitor": ".1/measurement/I0t"})
    source = Hdf5Source(hdf5_path, [3, 5], data_mappings=data_mappings)
    measurement = Measurement1D(source)

    measurement.find_outliers(method="hampel", threshold=2.0)
    outliers = measurement.scans[0].outliers
    assert np.all(np.where(outliers)[1][:2] == [28, 60])

    measurement.reset()
    measurement.remove_outliers(method="hampel", threshold=3.5)
    outliers = measurement.scans[0].outliers
    assert np.all(np.where(outliers)[1][:2] == [123, 284])


def test_measurement1d_dead_time_correction(
    hdf5_path: str, data_mappings: dict[str, Any]
):
    data_mappings.update({"detection_time": ".1/measurement/sec"})
    source = Hdf5Source(hdf5_path, [3, 5], data_mappings=data_mappings)
    measurement = Measurement1D(source)
    with pytest.raises(TypeError):
        measurement.dead_time_correction()  # type: ignore
    measurement.dead_time_correction(tau=[0.1, 0.1])


def test_measurement1d_save(hdf5_path: str, data_mappings: dict[str, Any]):
    source = Hdf5Source(hdf5_path, [3, 5], data_mappings=data_mappings)
    measurement = Measurement1D(source)
    with pytest.raises(TypeError):
        measurement.save()  # type: ignore
    filename = "test.dat"
    measurement.save(filename)
    assert os.path.isfile(filename)
    os.remove(filename)


@pytest.mark.parametrize(
    "scan_ids, conc_corr_ids, expected",
    (
        ([4], [5], [0.0750053, 0.06380908]),
        ([4, 10], [5, 11], [0.07468005, 0.06404491]),
        ([4], [6], ConcentrationCorrectionError),
        ([4, 10], [5, 11, 12], ConcentrationCorrectionError),
    ),
)
def test_simple_concentration_correction_equal_number_of_scans(
    scan_ids: list[int], conc_corr_ids: list[int], expected: Any
):
    hdf5_path: str = resources.getfile("A1_Kb_XES.h5")
    data_mappings = {
        "x": ".1/measurement/xes_en",
        "signal": ".1/measurement/det_dtc_apd",
        "monitor": ".1/measurement/I02",
    }

    source = Hdf5Source(hdf5_path, scan_ids, data_mappings=data_mappings)
    measurement = Measurement1D(source)
    if isinstance(expected, list):
        measurement.concentration_correction(conc_corr_ids)
        assert measurement.signal[-2:] == pytest.approx(expected)
    else:
        with pytest.raises(expected):
            measurement.concentration_correction(conc_corr_ids)


def test_simple_concentration_correction_equal_number_of_scans_and_points():
    hdf5_path = resources.getfile("Fe2O3_Ka1Ka2_RIXS.h5")
    data_mappings = {
        "x": ".1/measurement/zaptime",
        "y": ".1/instrument/positioners/xes_en",
        "signal": [".1/measurement/det_dtc_apd"],
        "monitor": ".1/measurement/I02",
    }
    source = Hdf5Source(hdf5_path, list(range(4, 225)), data_mappings=data_mappings)
    measurement = Rixs(source)
    measurement.concentration_correction([225])
    assert measurement.scans[0].signal[-1] == pytest.approx(0.01887687)
    assert measurement.scans[-1].monitor[0] == pytest.approx(0.24412638)
    assert measurement.signal.mean() == pytest.approx(0.02197076489)


@pytest.fixture()
def rixs_hdf5_path() -> str:
    return resources.getfile("Fe2O3_Ka1Ka2_RIXS.h5")


@pytest.fixture()
def rixs_data_mappings() -> dict[str, Any]:
    return {
        "x": ".1/measurement/hdh_energy",
        "y": ".1/instrument/positioners/xes_en",
        "signal": ".1/measurement/det_dtc_apd",
        "monitor": ".1/measurement/I02",
    }


def test_rixs_basic_processing(rixs_hdf5_path: str, rixs_data_mappings: dict[str, Any]):
    RIXS_SCANS_SMALL = 7
    RIXS_SHAPE_POINTS = 145
    RIXS_SHAPE_SCANS = 7

    source = Hdf5Source(rixs_hdf5_path, "4-10", data_mappings=rixs_data_mappings)
    measurement = Rixs(source)

    assert len(measurement.scans) == RIXS_SCANS_SMALL
    assert measurement.acquisition_mode == "absorption"
    assert measurement.shape == (RIXS_SHAPE_POINTS, RIXS_SHAPE_SCANS)

    assert measurement.x[0] == pytest.approx(7.1080122790)
    assert measurement.x[-1] == pytest.approx(7.1218488914)

    assert measurement.y[0] == pytest.approx(6.3859981344)
    assert measurement.y[-1] == pytest.approx(6.3865992156)

    assert measurement.signal[0] == pytest.approx(0.0004252700)
    assert measurement.signal[-1] == pytest.approx(0.0084991166)


def test_rixs_concentration_correction(
    rixs_hdf5_path: str, rixs_data_mappings: dict[str, Any]
):
    source = Hdf5Source(rixs_hdf5_path, "4-224", data_mappings=rixs_data_mappings)
    measurement = Rixs(source)
    measurement.concentration_correction([225])

    assert measurement.signal[0] == pytest.approx(0.0025508853)
    assert measurement.signal[-1] == pytest.approx(0.0080452164)


def test_rixs_cuts(rixs_hdf5_path: str, rixs_data_mappings: dict[str, Any]):
    CIE_MASK_SUM = 2210

    source = Hdf5Source(rixs_hdf5_path, "4-224", data_mappings=rixs_data_mappings)
    measurement = Rixs(source)

    measurement.cut(mode="CIE", energies=[7.114], widths=0.001)
    assert "CIE@7.114" in measurement.cuts
    centers, signal, mask = measurement.cuts["CIE@7.114"]
    assert centers[0] == pytest.approx(6.3860536906)
    assert centers[-1] == pytest.approx(6.4079428386)
    assert signal[0] == pytest.approx(0.0016672864)
    assert signal[-1] == pytest.approx(0.0005284551)
    assert mask.sum() == CIE_MASK_SUM

    measurement.reset()
    measurement.cut(mode="CEE", energies=[6.4], widths=0.002)
    assert "CEE@6.4" in measurement.cuts
    centers, signal, _ = measurement.cuts["CEE@6.4"]
    assert centers[0] == pytest.approx(7.1080673353)
    assert centers[-1] == pytest.approx(7.1217950643)
    assert signal[0] == pytest.approx(0.0001061145)
    assert signal[-1] == pytest.approx(0.0155607257)

    measurement.reset()
    measurement.cut(mode="CET", energies=[0.7], widths=0.003)
    assert "CET@0.7" in measurement.cuts
    centers, signal, _ = measurement.cuts["CET@0.7"]
    assert centers[0] == pytest.approx(7.1080700092)
    assert centers[-1] == pytest.approx(7.1094111801)
    assert signal[0] == pytest.approx(0.0000033709, abs=1e-9)
    assert signal[-1] == pytest.approx(0.0000043391, abs=1e-9)

    with pytest.raises(ValueError, match="energies parameter must be defined"):
        measurement.cut(mode="CIE")

    with pytest.raises(ValueError, match="Unknown mode"):
        measurement.cut(mode="INVALID", energies=[7.114])


def test_rixs_interpolation(rixs_hdf5_path: str, rixs_data_mappings: dict[str, Any]):
    INTERPOLATED_SHAPE_X = 50
    INTERPOLATED_SHAPE_Y = 30
    INTERPOLATED_SIZE = 1500

    source = Hdf5Source(rixs_hdf5_path, "4-10", data_mappings=rixs_data_mappings)
    measurement = Rixs(source)

    xi = np.linspace(measurement.x.min(), measurement.x.max(), INTERPOLATED_SHAPE_X)
    yi = np.linspace(measurement.y.min(), measurement.y.max(), INTERPOLATED_SHAPE_Y)
    measurement.interpolate(xi, yi)

    assert measurement.shape == (INTERPOLATED_SHAPE_X, INTERPOLATED_SHAPE_Y)
    assert measurement.signal.size == INTERPOLATED_SIZE
    assert measurement.signal[0] == pytest.approx(0.0004252700)

    measurement.reset()
    assert measurement._y.size == 0


def test_rixs_save_and_plot(
    rixs_hdf5_path: str, rixs_data_mappings: dict[str, Any], tmp_path: Path
):
    DAT_COLUMNS = 4
    CUT_DAT_COLUMNS = 2
    PLOT_AXES = 2

    source = Hdf5Source(rixs_hdf5_path, "4-10", data_mappings=rixs_data_mappings)
    measurement = Rixs(source)
    measurement.cut(mode="CIE", energies=[7.114], widths=0.001)

    filename = tmp_path / "test_rixs.dat"
    measurement.save(str(filename))
    assert filename.exists()

    data = np.loadtxt(filename)
    assert data.shape[0] == measurement.signal.size
    assert data.shape[1] == DAT_COLUMNS

    assert data[0, 0] == pytest.approx(measurement.x[0])
    assert data[0, 1] == pytest.approx(measurement.y[0])
    assert data[0, 2] == pytest.approx(measurement.signal[0])
    assert data[-1, 0] == pytest.approx(measurement.x[-1])
    assert data[-1, 1] == pytest.approx(measurement.y[-1])
    assert data[-1, 2] == pytest.approx(measurement.signal[-1])

    cut_filename = tmp_path / "test_rixs_CIE_7.114.dat"
    assert cut_filename.exists()
    cut_data = np.loadtxt(cut_filename)
    assert cut_data.shape[1] == CUT_DAT_COLUMNS

    cut_centers, cut_signal, _ = measurement.cuts["CIE@7.114"]
    assert cut_data[0, 0] == pytest.approx(cut_centers[0])
    assert cut_data[0, 1] == pytest.approx(cut_signal[0])
    assert cut_data[-1, 0] == pytest.approx(cut_centers[-1])
    assert cut_data[-1, 1] == pytest.approx(cut_signal[-1])

    axes = measurement.plot()
    assert axes.size == PLOT_AXES
    plt.close("all")
