from torch.utils.data.dataset import Dataset
from sklearn.preprocessing import LabelBinarizer
from pathlib import Path
import json
from PIL import Image
from torchvision.transforms.functional import resize, to_tensor
import os
from ai.label import Label
from torch import from_numpy
import numpy as np
import random


class TrainingDataset(Dataset):

    def __init__(self, data_dir):

        # Construct one-hot label binarizer
        lb = LabelBinarizer()
        lb.fit([0, 1, 2, 3, 4])

        # Initialize data lists
        self.label_list = []
        self.images = []
        self.image_filepaths = []

        # Construct data lists
        data_root = Path(data_dir)
        all_json_paths = list(data_root.glob('data_*.json'))
        all_json_paths = [str(path) for path in all_json_paths]

        for json_path in all_json_paths:
            with open(json_path) as json_file:
                print(json_path)

                # The dataset includes multiple records
                json_data_set = json.load(json_file)

                for json_data_record in json_data_set["data"]:

                    # Process image and append to list
                    image_filepath = os.path.join(data_dir, json_data_record["camera"]["filename"])

                    try:
                        img = Image.open(image_filepath)
                    except Exception as e:
                        print(f"Could not load image: {str(e)}")
                        continue

                    img = img.convert('RGB')
                    img = resize(img, (64, 64))
                    img = to_tensor(img)
                    self.images.append(img)
                    self.image_filepaths.append(image_filepath)

                    steering_value = json_data_record["vehicle_ctl"]["steering"]
                    label_val = Label.steering_value_to_label_index(steering_value)
                    self.label_list.append(label_val)

        self.labels = lb.transform(self.label_list).astype(np.float32)

    def __getitem__(self, index):

        img = self.images[index]
        label = from_numpy(self.labels[index])

        return img, label

    def __len__(self):

        return len(self.images)

    def random_image_filepath(self):
        ind = random.randint(0, len(self.image_filepaths))
        return self.image_filepaths[ind]
