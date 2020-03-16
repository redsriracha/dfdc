from config import *

if __name__ == "__main__":
    files = tf.io.gfile.glob(os.path.join(DATASET_VIDEO_PATH, "*"))
    print("VIDEOS:", len(files))

    with open(LABEL_FILE, "r") as fp:
        labels = json.load(fp)
        print("LABELS:", len(labels))

    if not len(files) == len(labels):
        # VIDEOS
        missing_videos = [item for item in labels if not os.path.exists(os.path.join(DATASET_VIDEO_PATH, item))]

        # METADATA_FULL.JSON
        missing_originals = [print("MISSING ORIGINAL:", labels[item].get("original")) for item in labels if labels[item].get("original") is not None if not os.path.exists(os.path.join(DATASET_VIDEO_PATH, labels[item].get("original")))]

        # CHECK
        return_stat = [os.system("find " + DATASET_PATH + " -name *" + item) for item in missing_videos]

        # OUTPUT
        print(np.asarray(missing_videos))
        print(np.asarray(missing_originals))
        print(np.asarray(return_stat))
