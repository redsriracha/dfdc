from config import *

if __name__ == '__main__':
    SPECTROGRAM_DIR = VIDEO_DIR_PATH + "_spectrogram"
    if not os.path.exists(SPECTROGRAM_DIR):
        os.mkdir(SPECTROGRAM_DIR)

    file_ds = tf.data.Dataset.list_files(os.path.join(VIDEO_DIR_PATH, "*"), shuffle=False).take(10)
    for file in tqdm(file_ds.as_numpy_iterator()):
        file = file.decode("utf-8")
        filename_ext = os.path.basename(file)
        filename = os.path.splitext(filename_ext)[0]
        dest = os.path.join(SPECTROGRAM_DIR, filename + ".png")
        cmd = "ffmpeg -i " + file + " -lavfi showspectrumpic=s=hd480:legend=0,format=yuv420p " + dest
        # os.system(cmd)
