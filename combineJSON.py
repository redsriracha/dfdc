from config import *

if __name__ == "__main__":
    # Find all the metadata.json files
    json_files = [os.path.join(root, item) for root, dirs, files in os.walk(DATASET_PATH) for item in files if not "dfdc_train_full" in root if ".json" in item]
    print(np.asarray(json_files))
    print(len(json_files))

    # Combine all json data
    file_read = open(json_files[0], "r")
    data_full = json.load(file_read)
    for item in json_files[1:]:
        file_read = open(item, "r")
        data_load = json.load(file_read)
        data_full.update(data_load)
        file_read.close()

    # Save combined json data
    dest_file = os.path.join(DATASET_PATH, "metadata_full.json")
    file_write = open(dest_file, "w")
    json.dump(data_full, file_write)
    file_write.close()

    # Check saved json file
    file_check = open(dest_file, "r")
    results = json.load(file_check)
    file_check.close()

    print("BEFORE")
    print(len(data_full))
    print("AFTER")
    print(len(results))
