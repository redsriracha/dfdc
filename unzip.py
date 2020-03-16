from config import *


@ray.remote
def zip_data_parser(zip_fname):
    return os.system("unzip -qu {0} -d {1}".format(zip_fname, DATASET_PATH))


if __name__ == "__main__":
    glob = tf.io.gfile.glob(os.path.join(DATASET_PATH, "*.zip"))

    ray.init()
    return_stat = [zip_data_parser.remote(item) for item in glob]
    results = [x for x in tqdm(to_iterator(return_stat), total=len(return_stat))]

    print(np.asarray(results))
