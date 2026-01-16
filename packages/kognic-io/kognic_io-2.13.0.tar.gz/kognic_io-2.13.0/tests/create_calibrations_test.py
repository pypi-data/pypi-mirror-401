from __future__ import absolute_import

from datetime import datetime

import pytest

import examples.calibration.create_calibrations as create_calibrations_example
import examples.calibration.get_calibrations as get_calibrations_example
import kognic.io.client as IOC
from kognic.io.model.calibration.calib import SensorCalibrationEntry


@pytest.mark.integration  # TODO: Remove this mark once the integration tests are ready
class TestCalibration:
    @pytest.fixture(scope="session")
    def calibration_identifier(self) -> str:
        return f"<calibration-{datetime.now().isoformat()}"

    @pytest.fixture(scope="session")
    def created_calibration(self, client: IOC.KognicIOClient, calibration_identifier: str) -> SensorCalibrationEntry:
        """Create calibration once for all tests in this class"""
        calibrations = create_calibrations_example.run(client, calibration_identifier)
        return calibrations

    @pytest.mark.no_assumptions
    def test_create_calibration(self, created_calibration: SensorCalibrationEntry, calibration_identifier: str):
        assert created_calibration.external_id == calibration_identifier

    @pytest.mark.no_assumptions
    def test_get_calibrations(self, client: IOC.KognicIOClient, created_calibration: SensorCalibrationEntry):
        calibrations = get_calibrations_example.run(client)
        assert isinstance(calibrations, list)
        assert all(
            [isinstance(calib, SensorCalibrationEntry) for calib in calibrations]
        ), "Calibrations are not of type SensorCalibrationEntry"

    @pytest.mark.no_assumptions
    def test_get_calibration(self, client: IOC.KognicIOClient, calibration_identifier: str, created_calibration: SensorCalibrationEntry):
        calibration = client.calibration.get_calibrations(external_id=calibration_identifier)
        assert len(calibration) == 1
        assert all(
            [isinstance(calib, SensorCalibrationEntry) for calib in calibration]
        ), "Calibrations are not of type SensorCalibrationEntry"
