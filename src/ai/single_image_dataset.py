from torch.utils.data.dataset import Dataset
from PIL import Image
from torchvision.transforms import functional


class SingleImageDataset(Dataset):

    def __init__(self):

        # Initialize data lists
        self.images = []

    def load_image(self, filepath):

        self.images.clear()

        # Process image and append to list
        img = Image.open(filepath)
        img = img.convert('RGB')
        img = functional.resize(img, (64, 64))
        img = functional.to_tensor(img)

        self.images.append(img)

    def __getitem__(self, index):

        return self.images[index]

    def __len__(self):

        return len(self.images)
