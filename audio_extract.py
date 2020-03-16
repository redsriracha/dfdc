from config import *


@ray.remote
def mp4_to_spectrogram(video_filepath, dest):
    cmd = "ffmpeg -y -i " + video_filepath + " -loglevel panic -lavfi showspectrumpic=legend=0 " + dest
    # print(cmd)
    return os.system(cmd)


@ray.remote
def mp4_to_wav(video_filepath, dest):
    cmd = "ffmpeg -y -i " + video_filepath + " -loglevel panic " + dest
    # print(cmd)
    return os.system(cmd)


if __name__ == "__main__":
    spectrogram_dir = DATASET_VIDEO_PATH + "_spectrogram"
    if not os.path.exists(spectrogram_dir):
        os.mkdir(spectrogram_dir)

    audio_dir = DATASET_VIDEO_PATH + "_audio"
    if not os.path.exists(audio_dir):
        os.mkdir(audio_dir)

    ray.init()
    spectrogram_return_stat = []
    wav_return_stat = []
    video_filepaths = tf.io.gfile.glob(os.path.join(DATASET_VIDEO_PATH, "*.mp4"))
    for video_filepath in video_filepaths:
        filename_ext = os.path.basename(video_filepath)
        filename = os.path.splitext(filename_ext)[0]

        # SPECTROGRAM
        spectro_path = os.path.join(spectrogram_dir, filename + ".png")
        if not os.path.exists(spectro_path):
            spectrogram_return_stat.append(mp4_to_spectrogram.remote(video_filepath=video_filepath, dest=spectro_path))
            # print(spectro_path)

        # WAV
        wav_path = os.path.join(audio_dir, filename + ".wav")
        if not os.path.exists(wav_path):
            wav_return_stat.append(mp4_to_wav.remote(video_filepath=video_filepath, dest=wav_path))
            # print(wav_path)

    # PROGRESS BAR
    spectrogram_results = [x for x in tqdm(to_iterator(spectrogram_return_stat), total=len(spectrogram_return_stat))]
    wav_results = [x for x in tqdm(to_iterator(wav_return_stat), total=len(wav_return_stat))]

    # print(spectrogram_results, "\n", wav_results)
