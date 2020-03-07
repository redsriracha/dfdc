import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "1"  # or any {'0', '1', '2'}

import json
from tqdm import tqdm
import tensorflow as tf

tf.config.list_physical_devices("GPU")

DATASET_NAME = "dfdc_train_part_0"

ROOT_DATASET_DIR = "dataset"
if not os.path.exists(ROOT_DATASET_DIR):
    os.mkdir(ROOT_DATASET_DIR)

VIDEO_DIR_PATH = os.path.join(ROOT_DATASET_DIR, DATASET_NAME)

