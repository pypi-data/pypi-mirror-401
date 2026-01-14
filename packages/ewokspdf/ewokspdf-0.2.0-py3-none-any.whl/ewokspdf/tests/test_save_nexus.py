import pytest
import h5py
import numpy as np
import os
from unittest.mock import MagicMock
from silx.io import utils as silx_io_utils

from ewokspdf.tasks.constants import SIGNAL_TYPES, PDF_CONFIG_PARSED
from types import SimpleNamespace
import json

from ewokspdf.tasks.save_nexus import PdfGetXSaveNexus, pdfgetx_config_as_nxdict


@pytest.fixture
def mock_result():
    """Creates a mock result object with signal attributes."""
    result = MagicMock()
    for signal_type in SIGNAL_TYPES:
        x_data = np.linspace(0, 10, 100)
        y_data = np.sin(x_data)  # Mock data for testing
        setattr(result, signal_type, (x_data, y_data))
    return result


@pytest.fixture
def setup_save_data(mock_result):
    """Sets up mock data for saving."""
    return [mock_result for _ in range(1)]  # Simulate multiple results


@pytest.fixture
def tmpdir(tmp_path):
    """Temporary directory for output files."""
    return tmp_path


@pytest.fixture
def pdfgetx_options_PDFGetter(requires_diffpy):
    """Mock pdfgetx options as PDFGetter object."""
    from diffpy import pdfgetx

    options = pdfgetx.PDFConfig()
    pdfgetx_options = dict(PDF_CONFIG_PARSED)
    for key, value in pdfgetx_options.items():
        setattr(options, key, value)
    return options


def test_save_nexus(
    setup_save_data,
    tmpdir,
    pdfgetx_options_PDFGetter,
):
    output_filename = os.path.join(tmpdir, "CeO2.h5")
    save_inputs = {
        "nxdata_url": f"{output_filename}::1.1/frelon6_integrate/integrated",
        "results": setup_save_data,
        "pdfgetx_options": pdfgetx_options_PDFGetter,
        "info": {"nb_avg": 2},
    }
    save = PdfGetXSaveNexus(inputs=save_inputs)
    save.execute()
    output_url = save.get_output_value("output_url")

    assert output_url == f"silx://{output_filename}::1.1/frelon6_PDF"

    with silx_io_utils.open(output_url) as nxprocess:
        assert isinstance(nxprocess, h5py.Group)
        assert nxprocess.attrs["NX_class"] == "NXprocess"

        configuration = nxprocess["configuration"]
        assert configuration.attrs["NX_class"] == "NXnote"

        averaging_group = nxprocess["averaging_options"]
        assert "nb_avg" in averaging_group
        np.testing.assert_allclose(averaging_group["nb_avg"][()], 2)

        assert nxprocess.attrs["default"] == list(SIGNAL_TYPES.keys())[-1]
        assert nxprocess.parent.attrs["default"] == os.path.basename(nxprocess.name)

        # Iterate over each signal type
        for signal_type in SIGNAL_TYPES:
            # Load the data for the current signal type
            nxdata = nxprocess[signal_type]
            assert isinstance(nxdata, h5py.Group)
            assert nxdata.attrs["NX_class"] == "NXdata"

            # Extract the data from the HDF5 file
            axes_data = np.squeeze(nxdata[nxdata.attrs["axes"]][()])
            signal_data = np.squeeze(nxdata[nxdata.attrs["signal"]][()])

            # Extract the expected data from setup_save_data
            for idx, result_obj in enumerate(setup_save_data):
                expected_data = getattr(result_obj, signal_type)
                expected_axes = np.squeeze(expected_data[0])
                expected_signal = np.squeeze(expected_data[1])

                np.testing.assert_allclose(
                    expected_axes,
                    axes_data,
                    rtol=1e-6,
                    err_msg=f"Failed for {signal_type} axes comparison at index {idx}",
                )
                np.testing.assert_allclose(
                    expected_signal,
                    signal_data,
                    atol=1e-6,
                    err_msg=f"Failed for {signal_type} signal comparison at index {idx}",
                )


def test_pdfgetx_config_as_nxdict_none():
    with pytest.raises(ValueError):
        pdfgetx_config_as_nxdict(None)


def test_pdfgetx_config_as_nxdict_without_dict():
    with pytest.raises(TypeError):
        pdfgetx_config_as_nxdict(object())


def test_pdfgetx_config_as_nxdict_serializes_simple_namespace():
    config = SimpleNamespace(qmax=25, mode="xray")
    nxtree = pdfgetx_config_as_nxdict(config)

    assert nxtree["@NX_class"] == "NXprocess"
    assert nxtree["program"] == "pdfgetx"
    configuration = nxtree["configuration"]
    assert configuration["@NX_class"] == "NXnote"
    assert configuration["type"] == "application/json"

    stored = json.loads(configuration["data"])
    assert stored["qmax"] == 25
    assert stored["mode"] == "xray"
