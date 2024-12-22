from datetime import datetime
from night_sky_pi.app.observation.data import (
    Period,
    ModuleDataConfig,
    HouseKeeping,
    DataConfig,
    ObservationData,
)


def test_within_observation_period():
    start = datetime(2022, 1, 1, 0, 0, 0)
    end = datetime(2022, 1, 1, 12, 0, 0)
    period = Period(start, end)

    assert period.within_observation_period(datetime(2022, 1, 1, 6, 0, 0)) == True
    assert period.within_observation_period(datetime(2022, 1, 1, 15, 0, 0)) == False


def test_calculate_wait_till_observation():
    start = datetime(2022, 1, 1, 10, 0, 0)
    end = datetime(2022, 1, 1, 12, 0, 0)
    period = Period(start, end)

    assert period.calculate_wait_till_observation(datetime(2022, 1, 1, 9, 0, 0)) == 3600
    assert period.calculate_wait_till_observation(datetime(2022, 1, 1, 11, 30, 0)) == 0


def test_observation_data_init():
    module = ModuleDataConfig(
        path="module/path", house_keeping=HouseKeeping(delete_after=1)
    )
    global_data_config = DataConfig(path="/data/path")
    period = Period(datetime(2022, 1, 1, 0, 0, 0), datetime(2022, 1, 1, 12, 0, 0))
    observation_data = ObservationData(module, global_data_config, period)

    assert observation_data.data_path == "/data/path/"
    assert observation_data.root_path == "/data/path/module/path/"
    assert observation_data.path == "/data/path/module/path/2022-01-01/"
    assert observation_data.house_keeping == HouseKeeping(delete_after=1)


def test_observation_data_init_with_different_values():
    module = ModuleDataConfig(
        path="another/module/path", house_keeping=HouseKeeping(delete_after=1)
    )
    global_data_config = DataConfig(path="/another/data/path")
    period = Period(datetime(2022, 2, 1, 0, 0, 0), datetime(2022, 2, 1, 12, 0, 0))
    observation_data = ObservationData(module, global_data_config, period)

    assert observation_data.data_path == "/another/data/path/"
    assert observation_data.root_path == "/another/data/path/another/module/path/"
    assert observation_data.path == "/another/data/path/another/module/path/2022-02-01/"
    assert observation_data.house_keeping == HouseKeeping(delete_after=1)
