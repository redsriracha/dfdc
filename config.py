import json
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "1"  # or any {'0', '1', '2'}

import numpy as np
import pandas as pd
import ray
import tensorflow as tf
from tqdm import tqdm


tf.config.list_physical_devices("GPU")

DATASET_PATH = os.path.join(os.sep, "media", "tran", "Data", "dfdc_train_all")
DATASET_VIDEO_PATH = os.path.join(DATASET_PATH, "dfdc_train_videos")
DATASET_AUDIO_PATH = os.path.join(DATASET_PATH, "dfdc_train_videos_audio")
DATASET_SPECTROGRAM_PATH = os.path.join(DATASET_PATH, "dfdc_train_videos_spectrogram")
LABEL_FILE = os.path.join(DATASET_PATH, "metadata_full.json")

# DATASET_PATH = os.path.join(os.sep, "media", "tran", "Data", "dfdc_train_all")
# DATASET_VIDEO_PATH = os.path.join(DATASET_PATH, "dfdc_train_part_0")
# DATASET_AUDIO_PATH = os.path.join(DATASET_PATH, "dfdc_train_part_0_audio")
# DATASET_SPECTROGRAM_PATH = os.path.join(DATASET_PATH, "dfdc_train_part_0_spectrogram")
# LABEL_FILE = os.path.join(DATASET_VIDEO_PATH, "metadata.json")

NEW_LABEL_FILE = os.path.join(DATASET_PATH, "metadata_full_new.csv")

# PROGRESS BAR FOR RAY
def to_iterator(obj_ids):
    while obj_ids:
        done, obj_ids = ray.wait(obj_ids)
        yield ray.get(done[0])