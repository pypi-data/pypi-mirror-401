import numpy
from tomwer.core.volume import EDFVolume, HDF5Volume, RawVolume
from tomwer.core.volume.rawvolume import RawVolumeIdentifier


def test_volume_data_parent_folder():
    edf_volume = EDFVolume(folder="/my/folder/path")
    assert edf_volume.volume_data_parent_folder() == "/my/folder"

    hdf5_volume = HDF5Volume(file_path="/path/to/hdf5/file.hdf5", data_path="entry")
    assert hdf5_volume.volume_data_parent_folder() == "/path/to/hdf5"

    raw_volume = RawVolume(file_path="/path/to/raw.vol")
    assert raw_volume.volume_data_parent_folder() == "/path/to"


def test_raw_identifier():
    raw_volume = RawVolume(file_path="/path/to/raw.vol")
    assert (
        RawVolumeIdentifier.from_str(raw_volume.get_identifier().to_str())
        == raw_volume.get_identifier()
    )


def test_volume_shape_cache():

    hdf5_volume = HDF5Volume(
        file_path="/path/to/hdf5/file.hdf5",
        data_path="entry",
        data=numpy.random.random((1, 2, 3)),
    )
    assert hdf5_volume.get_volume_shape() == (1, 2, 3)
    hdf5_volume.data = numpy.random.random((3, 2, 1))
    assert hdf5_volume.get_volume_shape() == (3, 2, 1)
