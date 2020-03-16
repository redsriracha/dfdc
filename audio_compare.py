from config import *


def is_equal_image(src, compare):
    if tf.math.reduce_all(tf.equal(src, compare)):
        return True  # Same
    else:
        return False  # Different


if __name__ == "__main__":
    data_file = open(LABEL_FILE, "r")
    data = pd.read_json(data_file, orient="index")
    data = data.reset_index()
    data.rename(columns={"index": "file"}, inplace=True)
    data.pop("split")

    # data["label"] = pd.Categorical(data["label"])
    # data["label"] = data.label.cat.codes  # 0 - Fake, 1 - Real

    data.fillna(value={"original": ""}, inplace=True)

    label_ds = tf.data.Dataset.from_tensor_slices(data["label"])
    current_ds = tf.data.Dataset.from_tensor_slices(data["file"])
    original_ds = tf.data.Dataset.from_tensor_slices(data["original"])
    data_ds = tf.data.Dataset.zip((current_ds, original_ds)).skip(21050)

    # DECODE
    data_ds = data_ds.map(lambda x, y: (tf.strings.join((DATASET_SPECTROGRAM_PATH, x), separator=os.sep), y))
    data_ds = data_ds.map(lambda x, y: (x, tf.strings.join((DATASET_SPECTROGRAM_PATH, y), separator=os.sep)) if y != "" else (x, y))
    data_ds = data_ds.map(lambda x, y: (x, y) if y != "" else (x, x))
    data_ds = data_ds.map(lambda x, y: (tf.strings.regex_replace(x, ".mp4", ".png"), tf.strings.regex_replace(y, ".mp4", ".png")))
    data_ds = data_ds.map(lambda x, y: (tf.io.read_file(x), tf.io.read_file(y)) )
    data_ds = data_ds.map(lambda x, y: (tf.image.decode_png(x), tf.image.decode_png(y)))

    # COMPARISON
    audio_label_ds = data_ds.map(is_equal_image, num_parallel_calls=tf.data.experimental.AUTOTUNE)

    print(data.tail(10))
    data["alabel"] = list(tqdm(audio_label_ds.as_numpy_iterator(), total=len(data)))
    print(data.tail(10))

    audio_label_path = os.path.join(DATASET_PATH, "metadata_full_new.csv")
    data.to_csv(audio_label_path)

