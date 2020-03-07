from config import *

if __name__ == '__main__':
    spectrogram_dir = VIDEO_DIR_PATH + "_spectrogram"
    if not os.path.exists(spectrogram_dir):
        os.mkdir(spectrogram_dir)

    file_ds = tf.data.Dataset.list_files(os.path.join(VIDEO_DIR_PATH, "*.mp4"), shuffle=False)
    for file in tqdm(file_ds.as_numpy_iterator()):
        file = file.decode("utf-8")
        filename_ext = os.path.basename(file)
        filename = os.path.splitext(filename_ext)[0]
        dest = os.path.join(spectrogram_dir, filename + ".png")
        if os.path.exists(dest):
            continue
        cmd = "ffmpeg -i " + file + " -lavfi showspectrumpic=s=hd480:legend=0,format=yuv420p " + dest
        # print(cmd)
        os.system(cmd)
