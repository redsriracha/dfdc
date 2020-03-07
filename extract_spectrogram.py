from config import *


def mp4_to_spectrogram(video_filepath):
    video_filepath = video_filepath.decode("utf-8")
    filename_ext = os.path.basename(video_filepath)
    filename = os.path.splitext(filename_ext)[0]
    dest = os.path.join(spectrogram_dir, filename + ".png")
    if os.path.exists(dest):
        return
    cmd = "ffmpeg -i " + video_filepath + " -lavfi showspectrumpic=s=hd480:legend=0,format=yuv420p " + dest
    # print(cmd)
    os.system(cmd)


def is_equal_image(img_1, img_2):
    return tf.math.reduce_all(tf.equal(img_1, img_2))


if __name__ == "__main__":
    spectrogram_dir = VIDEO_DIR_PATH + "_spectrogram"
    if not os.path.exists(spectrogram_dir):
        os.mkdir(spectrogram_dir)

    video_filepath_ds = tf.data.Dataset.list_files(os.path.join(VIDEO_DIR_PATH, "*.mp4"), shuffle=False)
    for video_filepath in tqdm(video_filepath_ds.as_numpy_iterator()):
        mp4_to_spectrogram(video_filepath=video_filepath)

    data_file = open("dataset/dfdc_train_part_0/metadata.json")
    data = json.load(data_file)
    for item in data:
        if not data[item].get("original") == None:
            img_1_path = os.path.splitext(item)[0] + ".png"
            img_1 = tf.io.read_file(os.path.join(spectrogram_dir, img_1_path))
            img_1 = tf.image.decode_png(img_1)

            img_2_path = os.path.splitext(data[item].get("original"))[0] + ".png"
            img_2 = tf.io.read_file(os.path.join(spectrogram_dir, img_2_path))
            img_2 = tf.image.decode_png(img_2)

            result = is_equal_image(img_1, img_2)
            result = result.numpy()

        else:
            result = "NA"
        print("{0:6s}".format(str(result)), item, data[item].get("original"))

    # spectrogram_ds = tf.data.Dataset.list_files(os.path.join(spectrogram_dir, "*"), shuffle=False)
