from ai.training_dataset import TrainingDataset
from matplotlib import pyplot as plt
from torch.utils.data import DataLoader
from ai.single_image_dataset import SingleImageDataset
from ai.simple_net import SimpleNet
import torch.optim as optim
import math
from torch.utils.data.sampler import SubsetRandomSampler
from torch.autograd import Variable
from torch.nn.functional import binary_cross_entropy
from torch import max as torch_max
from torch import eq as torch_eq
from torch import save as torch_save
from ai.label import Label
import os
from pathlib import Path


def show_image_tensor(dataset, index):
    plt.imshow(rotor_dataset[index][0].permute(1, 2, 0))
    plt.show()


def show_image(images, index, result_value, label_value=None):
    plt.imshow(images[index].permute(1, 2, 0))
    result_name = Label.label_index_to_name(result_value)
    if label_value is not None:
        label_name = Label.label_index_to_name(label_value)
    else:
        label_name = "UNK"
    plt.title("Prediction: {}\nCorrect Label: {}".format(result_name, label_name))
    plt.show()


def train(epoch, optimizer_):
    loss_list = []

    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = Variable(data), Variable(target)
        optimizer_.zero_grad()
        output = model(data)
        loss = binary_cross_entropy(output, target)

        loss_list.append(loss.item())

        loss.backward()
        optimizer_.step()

        if batch_idx % 10 == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                       100. * batch_idx / len(train_loader), loss.item()))

    model.eval()
    total_correct = 0
    total = 0
    for batch_idx, (data, target) in enumerate(validation_loader):
        data, target = Variable(data), Variable(target)
        _, target_inds = torch_max(target, dim=1)

        output = model(data)
        _, output_inds = torch_max(output, dim=1)

        num_correct = torch_eq(target_inds, output_inds).sum().item()
        total_correct += num_correct
        total += len(target_inds)

    accuracy = total_correct / total * 100
    print("Model Accuracy: {:.2f}%".format(accuracy))

    return loss_list, accuracy


if __name__ == '__main__':

    data_dir = "/Users/Robbie/rotor/rtrcmd/data"

    # Create the dataset and show a sample image
    rotor_dataset = TrainingDataset(data_dir)
    # show_image_tensor(rotor_dataset, 80)

    begin_training = input("Begin training (y/n)? ")
    if begin_training != 'y':
        exit()

    # Split the data into training and validation data
    data_size = len(rotor_dataset)
    validation_split = .1
    split_ind = math.floor((1 - validation_split) * data_size)
    data_indices = list(range(data_size))
    train_ind, validation_ind = data_indices[0:split_ind], data_indices[split_ind:]

    # Create random samplers for the training and validation data
    train_sampler = SubsetRandomSampler(train_ind)
    validation_sampler = SubsetRandomSampler(validation_ind)

    # Create data loaders for training and validation data
    batch_size = 10
    train_loader = DataLoader(rotor_dataset, batch_size=batch_size, sampler=train_sampler)
    validation_loader = DataLoader(rotor_dataset, batch_size=batch_size, sampler=validation_sampler)

    # Reinitialize model
    model = SimpleNet()
    learning_rate = 0.05
    optimizer = optim.SGD(model.parameters(), lr=learning_rate)

    # Train
    loss_list = []
    accuracy_list = []
    for epoch in range(0, 20):
        loss, accuracy = train(epoch, optimizer)
        loss_list.extend(loss)
        accuracy_list.append(accuracy)

    # Plot the loss and accuracy
    fig, axs = plt.subplots(2)
    legend = []
    axs[0].plot(list(range(len(loss_list))), loss_list)
    axs[0].set_title("Loss Convergence")
    axs[0].set(xlabel='Batch', ylabel='Loss')
    axs[1].plot(list(range(len(accuracy_list))), accuracy_list)
    axs[1].set_title("Accuracy")
    axs[1].set(xlabel='Epoch', ylabel='Accuracy')
    legend.append('Learning Rate: {}'.format(learning_rate))
    plt.legend(legend, loc='lower right')
    plt.show()

    # Show a test image
    single_image_dataset = SingleImageDataset()

    while True:
        command = input("Test model on random image (y/n)? ")
        if command != 'y':
            break

        single_image_dataset.load_image(rotor_dataset.random_image_filepath())
        data_loader = DataLoader(single_image_dataset, batch_size=1)
        data_iter = iter(data_loader)
        image = data_iter.next()

        # Generate the steering value prediction
        output = model(image)

        _, result_value = torch_max(output, dim=1)

        result_name = Label.label_index_to_name(result_value)

        show_image(image, 0, result_value, None)

    # Save off the model
    save_model = input("Save model (y/n)? ")
    if save_model == 'y':
        model_export_filepath = str(Path(os.getcwd()) / Path('nn_model.pt'))
        torch_save(model.state_dict(), model_export_filepath)
