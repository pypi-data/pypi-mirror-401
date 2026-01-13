"""video parsing module."""

import typing as t
import zipfile
from fractions import Fraction

from fw_file.video import Video
from fw_meta import MetaData

from ..util import AnyPath


def process(file_path: AnyPath) -> t.Tuple[t.Dict, MetaData, t.Dict]:
    """Process `file_path` and returns a `FileEntry` and its corresponding meta.

    Args:
        file_path (Path-like): Path to video input-file.

    Returns:
        dict: Dictionary of file attributes to update.
        dict: Dictionary containing the file meta.
        dict: Dictionary containing the qc metrics.

    """
    if zipfile.is_zipfile(file_path):
        video = Video.from_zip(file_path)
    else:
        video = Video(file_path)

    return _process(video.get_meta(), video.fields)


def _process(meta: MetaData, fields: dict) -> t.Tuple[t.Dict, MetaData, t.Dict]:
    """Helper function to process video metadata.

    Args:
        meta (MetaData): The metadata of the video.
        fields (dict): The fields extracted from the video.

    Returns:
        tuple: A tuple containing the updated fields, metadata, and quality control metrics.

    """
    # Reorganize the fields directly
    fields["streams"] = organize_ffprobe_metadata(fields.get("streams", []))
    fields["format"] = fields.get("format", {})

    # Convert any Fraction objects to strings
    fields = _convert_fractions(fields)

    # Build the final structure
    fe = {
        "modality": "",
        "info": {
            "header": {
                "video": fields  # Use the reorganized fields directly
            }
        },
    }

    qc = {}

    return fe, meta, qc


def _convert_fractions(data):
    """Recursively convert Fraction objects to strings in a dictionary.

    Args:
        data (dict | list): The input data to process.

    Returns:
        dict | list: The processed data with Fraction objects converted to strings.

    """
    if isinstance(data, dict):
        return {key: _convert_fractions(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [_convert_fractions(item) for item in data]
    elif isinstance(data, Fraction):
        return str(data)  # Convert Fraction to string (e.g., "30000/1001")
    else:
        return data


def organize_ffprobe_metadata(streams: list) -> dict:
    """
    Organizes ffprobe streams metadata by grouping streams into sub-levels.

    Args:
        streams (list): The list of streams from ffprobe metadata.

    Returns:
        dict: The reorganized streams grouped under 'video', 'audio', and 'other'.
    """
    # Initialize sub-levels for video and audio streams
    organized_streams = {
        "video": [],
        "audio": [],
        "other": [],  # For streams that are neither video nor audio
    }

    # Iterate through the streams and group them
    for stream in streams:
        codec_type = stream.get("codec_type")
        if codec_type == "video":
            organized_streams["video"].append(stream)
        elif codec_type == "audio":
            organized_streams["audio"].append(stream)
        else:
            organized_streams["other"].append(stream)

    return organized_streams
