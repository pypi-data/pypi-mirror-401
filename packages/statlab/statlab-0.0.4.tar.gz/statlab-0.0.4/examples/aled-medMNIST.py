"""
DESCRIPTION:
This is an example of using Adaptive Label Error Detection (ALED, via 
statlab.aled) on a few medMNIST datasets. In this example, we introduce random
label error in each dataset, and we analyze ALED's ability to identify label
noise. We compare with two similar methods developed by work done by another 
group (CleanLab and CleanLab with features).
The entire ALED algorithm is described in detail here: (link will be inserted 
once available).
This example is based on code deposited in Zenodo (link will be inserted here
once available), which was used to generate the results for the above paper.
Also see the Zenodo for the intended Python environment.
"""

import statlab.aled

from cleanlab import Datalab
import torch
from torch.utils.data import DataLoader
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from torch import optim
from torch.autograd import Variable
from sklearn.utils.multiclass import unique_labels
import sklearn
from torch.utils.data import Dataset
import copy
from torch.utils.data import Subset
import torchvision.transforms as T
import torch.nn as nn
from torchvision.models import resnet50, ResNet50_Weights, densenet121, DenseNet121_Weights
from medmnist import PneumoniaMNIST
from medmnist import BreastMNIST
from medmnist import DermaMNIST
from medmnist import RetinaMNIST
from medmnist import BloodMNIST
import os
import contextlib
import warnings
from IPython.utils import io
from PIL import Image
os.environ['CUDA_LAUNCH_BLOCKING'] = '1'

RUN_PARAMS = {
    "model": resnet50, # could also use densenet121, etc
    "weights": "DEFAULT", # "DEFAULT" for pretrained model, or None for untrained model
    "num_epochs": 16, # 16 suggested for pretrained model; 32 suggested for untrained model
    "mislabeled_percentage": 0.05, # percentage of samples to be artificially mislabeled for demonstration purposes
    "num_trials": 1, # how many times to repeat the ALED detection experiment; set to >1 if you want multiple trials
    "device": torch.device('cuda' if torch.cuda.is_available() else 'cpu'),
    "ALED_hyperparams": {
        "num_ensembles": 10,
        "num_components": 2,
        "batch_size": 16
        }
    }

RUN_PARAMS["ALED_hyperparams"]["device"] = RUN_PARAMS["device"]

## Model-Related functions

def generate(model, dataset, BATCH_SIZE):

    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=False)
    model.eval()
    device = RUN_PARAMS["device"]

    # Generate outputs from random model
    with torch.no_grad():
        for i, (images, labels) in enumerate(dataloader):
            images_cuda = images.to(device)

            output = model(images_cuda)

            del images_cuda

            yield output

def create_dataset_labels(outputs_generator):
    outputs_list = []
    for output in outputs_generator:
        output_cpu = output.cpu()
        outputs_list.append(output_cpu)
        del output
    outputs_tensor = torch.cat(outputs_list).squeeze()
    return outputs_tensor

def softmaxed_outputs_array(model, dataset, BATCH_SIZE):
    model_outputs = create_dataset_labels(generate(model, dataset, BATCH_SIZE))
    m = nn.Softmax(dim=1)
    softmaxed_array = m(model_outputs).numpy()
    return softmaxed_array

def CL_num_estimate(model, dataset, BATCH_SIZE):
  # homemade estimate for CleanLab based on their paper; this is included in 
  # case it is useful (e.g., for manipulation), but you are most likely looking
  # for the real implementation of CleanLab below
  outs = softmaxed_outputs_array(model, dataset, BATCH_SIZE)
  thresholds_dict = {}
  for n in range(len(dataset.classes)):
      idx_n = np.where(np.array(dataset.labels) == n)[0]
      thresh_n = np.mean(outs[idx_n, n])
      thresholds_dict[n] = thresh_n

  predictions = np.argmax(outs, axis=1)
  df = pd.DataFrame(outs)
  df["label"] = np.array(dataset.labels)
  df["pred"] = predictions

  misclass_df = df[df["pred"] != df["label"]]
  misclass_df["CL_pred"] = misclass_df.apply(lambda row : row[row["pred"]] > thresholds_dict[row["pred"]], axis=1)

  num_estimate = sum(misclass_df["CL_pred"])

  return misclass_df, num_estimate

@contextlib.contextmanager
def suppress_all_output():
    with open(os.devnull, 'w') as devnull:
        with contextlib.redirect_stdout(devnull), \
             contextlib.redirect_stderr(devnull), \
             warnings.catch_warnings(), \
             io.capture_output() as captured:  # IPython-specific
            warnings.simplefilter("ignore")
            yield

## Dataset setup
class Mislabeling_Dataset(Dataset):
    """
    a Dataset class that contains a Dataset, providing the data of the internal Dataset
    but with labeling errors
    """
    def __init__(self, internal_dataset, internal_dataset_labels = None, fraction_mislabeled = 0.1, random_state = None):

        super().__init__()
        self.internal_dataset = copy.deepcopy(internal_dataset)
        self.true_labels = copy.deepcopy(internal_dataset_labels)
        if self.true_labels is None:
            self.set_true_labels()
        elif len(self.true_labels) != len(internal_dataset):
          raise Exception("Must have same number of labels as the length of the dataset [i.e. len(internal_dataset_labels) == len(internal_dataset)]")
        self.classes = unique_labels(self.true_labels)
        self.fraction_mislabeled = fraction_mislabeled
        self.rng = np.random.default_rng(random_state)
        # could potentially add a parameter to choose what method to mislabel (e.g., completely random, half mislabeled from each class)


        self.mislabel_sample_inds = self.rng.choice(np.arange(len(self.internal_dataset)), size=int(self.fraction_mislabeled*len(internal_dataset)), replace=False)
        mislabel_maps = [[class_j for class_j in self.classes if class_j != class_i] for class_i in self.classes]

        self.labels = copy.deepcopy(self.true_labels)
        self.mislabel_bool_array = np.zeros(len(self.labels), dtype=bool)
        for ind in self.mislabel_sample_inds:
            self.labels[ind] = mislabel_maps[self.true_labels[ind]][self.rng.integers(len(self.classes)-1)]
            self.mislabel_bool_array[ind] = True


    def set_true_labels(self):
        # helper function used by __init__()
        self.true_labels = np.zeros(len(self.internal_dataset), dtype=object)
        for i in range(len(self.internal_dataset)):
            self.true_labels[i] = self.internal_dataset[i][1]

    def __getitem__(self, idx):
        try:
            return self.internal_dataset[idx][0], self.labels[idx].item()
        except:
            return self.internal_dataset[idx][0], self.labels[idx]

    def __len__(self):
        return len(self.internal_dataset)

class custom_Subset(Subset):
  def __init__(self, dataset, indices):
    self.classes = dataset.classes
    self.indices = indices
    self.dataset = dataset
    self.labels = dataset.labels[indices]
    self.true_labels = dataset.true_labels[indices]

class GrayscaleToRGB(torch.nn.Module):
    def __init__(self):
        super(GrayscaleToRGB, self).__init__()

    def forward(self, img):
        # Convert the grayscale image to a 3-channel image by repeating the single channel
        return img.convert("RGB")

data_T = T.Compose([
                GrayscaleToRGB(),
                T.Resize(size = (224,224)),
                T.ToTensor(),
                T.Normalize(0,1)
        ])

## MedMNIST binary classes
class BinaryDermaMNIST(Dataset):
    def __init__(self, original_dataset, nevi_class=0):
        self.data = original_dataset
        self.images = original_dataset.imgs
        self.original_labels = original_dataset.labels.squeeze()

        # Binary: 0 = nevi (nevi_class), 1 = all others
        self.labels = torch.tensor(
            [0 if label == nevi_class else 1 for label in self.original_labels],
            dtype=torch.long
        )

        self.transform = original_dataset.transform

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        img = self.images[idx]
    
        # Always convert to PIL before transforms
        if isinstance(img, np.ndarray):
            img = Image.fromarray(img)
    
        if self.transform:
            img = self.transform(img)
    
        return img, self.labels[idx]

class BinaryRetinaMNIST(Dataset):
    def __init__(self, original_dataset):
        self.data = original_dataset
        self.images = original_dataset.imgs
        original_labels = original_dataset.labels.squeeze()

        # Binary: 0 = no disease, 1 = any condition
        self.labels = torch.tensor(
            [0 if label == 0 else 1 for label in original_labels],
            dtype=torch.long
        )

        self.transform = original_dataset.transform

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        img = self.images[idx]
    
        # Always convert to PIL before transforms
        if isinstance(img, np.ndarray):
            img = Image.fromarray(img)
    
        if self.transform:
            img = self.transform(img)
    
        return img, self.labels[idx]

class BinaryBloodMNIST(Dataset):
    def __init__(self, original_dataset, class_0=0, class_1=3):
        self.data = original_dataset
        self.images = original_dataset.imgs
        original_labels = original_dataset.labels.squeeze()

        # Filter to only class_0 and class_1
        mask = (original_labels == class_0) | (original_labels == class_1)
        self.images = self.images[mask]
        selected_labels = original_labels[mask]

        # Remap labels: class_0 → 0, class_1 → 1
        self.labels = torch.tensor(
            [0 if label == class_0 else 1 for label in selected_labels],
            dtype=torch.long
        )

        self.transform = original_dataset.transform

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        img = self.images[idx]
    
        # Always convert to PIL before transforms
        if isinstance(img, np.ndarray):
            img = Image.fromarray(img)
    
        if self.transform:
            img = self.transform(img)
    
        return img, self.labels[idx]

## Metrics
def AUC(model, dataset, BATCH_SIZE):
    model_outputs = create_dataset_labels(generate(model, dataset, BATCH_SIZE))
    print(model_outputs)
    labels = np.array(dataset.targets)
    print(labels)
    auc = sklearn.metrics.roc_auc_score(labels, model_outputs[:, 1])
    return auc

import sklearn.metrics
def print_classification_report(true, prediction, weights=None, confidence=None):
    true, prediction = np.array(true), np.array(prediction)
    stats = sklearn.metrics.classification_report(true, prediction, output_dict=True)
    print(f"""F1 score: {sklearn.metrics.f1_score(true, prediction)}
Sensitivity: {stats['True']['recall']}
Specificity: {stats['False']['recall']}
Positive predictive value: {stats['True']['precision']}
Negative predictive value: {stats['False']['precision']}""")
    print("Accuracy (unweighted):", np.mean(true==prediction))

    if not (weights is None): print(f"Accuracy (weighted): {np.average((true==prediction).astype(int), weights=weights)}")
    else: print(f"Accuracy (weighted by 0/1 class): {0.5*np.average(true[true==1]==prediction[true==1]) + 0.5*np.average(true[true==0]==prediction[true==0])}")

    if not (confidence is None):
        print("AUC:", sklearn.metrics.roc_auc_score(true, confidence))
        print("AUPRC:", sklearn.metrics.average_precision_score(true, confidence))
    print()

    data = [stats, sklearn.metrics.roc_auc_score(true, confidence), sklearn.metrics.average_precision_score(true, confidence)]
    
    return data

def train(num_epochs, cnn, loaders, optimizer, loss_func):
    device = RUN_PARAMS["device"]

    # Train the model
    total_step = len(loaders['train'])
    best_model = None
    min_val_loss = np.inf

    for epoch in range(num_epochs):
        cnn.train()
        running_loss_list = []
        for i, (images, labels) in enumerate(loaders['train']):

            # gives batch data, normalize x when iterate train_loader
            b_x = Variable(images).to(device)   # batch x
            
            b_y = Variable(labels).to(device)   # batch y

            print(labels)
            output = cnn(b_x)
            loss = loss_func(output, b_y)
            
            running_loss_list.append(loss.item())

            # clear gradients for this training step
            optimizer.zero_grad()

            # backpropagation, compute gradients
            loss.backward()
            # apply gradients
            optimizer.step()

            if epoch==0 and i==0:
                print("Initial loss: {:.4f}".format(loss.item()))

            if ((i+1) % 100 == 0) or (i+1 == total_step):
                print ('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'
                       .format(epoch + 1, num_epochs, i + 1, total_step, np.mean(running_loss_list)))
                running_loss_list = []
                
        # after training, print metrics:
        y_pred = np.array([])
        y_true = np.array([])
        losses = []
        cnn.eval()
        for i, (images, labels) in enumerate(loaders['val']):
        
            # gives batch data, normalize x when iterate train_loader
            b_x = Variable(images).to(device)
            b_y = Variable(labels)
            output = cnn(b_x)
            y_true = np.append(y_true, b_y)
            y_pred = np.append(y_pred, np.argmax(output.cpu().detach(), axis=1))
            loss = loss_func(output, b_y.to(device)).item()
            losses.append(loss)
        print("Val Accuracy:", np.mean(y_pred==y_true))
        print("Average Val Loss:", np.mean(losses))
        if np.mean(losses) < min_val_loss:
            best_model = copy.deepcopy(cnn.state_dict())
            min_val_loss = np.mean(losses)

        confusion_matrix = sklearn.metrics.confusion_matrix(y_true, y_pred)
        cm_display = sklearn.metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = [False, True])
    
        cm_display.plot()
        plt.show()

    # after training, print metrics:
    y_pred = np.array([])
    y_true = np.array([])
    for i, (images, labels) in enumerate(loaders['train']):

        # gives batch data, normalize x when iterate train_loader
        b_x = Variable(images).to(device)   # batch x
        y_true = np.append(y_true, Variable(labels))
        y_pred = np.append(y_pred, np.argmax(cnn(b_x).cpu().detach(), axis=1))
    print("accuracy:", np.mean(y_pred==y_true))
    try:
      print("weighted accuracy:", np.mean([np.mean(y_pred[y_true==i]==y_true[y_true==i] for i in np.unique(y_true))]))
    except:
      pass
    confusion_matrix = sklearn.metrics.confusion_matrix(y_true, y_pred)
    cm_display = sklearn.metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = [False, True])

    cm_display.plot()
    plt.show()
    return best_model

def full_looper(traindata, valdata, model, ALED_hyperparams):
  device = RUN_PARAMS["device"]
  batch_size = 8

  loaders = {
    'train' : torch.utils.data.DataLoader(traindata,
                                        batch_size=batch_size,
                                        shuffle=True,
                                        num_workers=0),

    'val' : torch.utils.data.DataLoader(valdata,
                                        batch_size=batch_size,
                                        shuffle=True,
                                        num_workers=0)
  }
  
  new_model = model(weights=RUN_PARAMS["weights"])
    
  if model == densenet121:
      new_model.classifier = nn.Linear(in_features=1024, out_features=2)
  else:
      new_model.fc = nn.Linear(in_features=2048, out_features=2)
  
  new_model = new_model.to(device)
  criterion = nn.CrossEntropyLoss()
  optimizer = torch.optim.Adam(new_model.parameters(), lr = 0.0001)
  epochs = RUN_PARAMS["num_epochs"]
  with suppress_all_output():
      new_model.load_state_dict(train(epochs, new_model, loaders, optimizer, criterion))
  print("Done Training")
  auc1, auc2 = CL_Looper(new_model, mislabeled_data=traindata, num_epochs=epochs, batch_size=batch_size, retrain=False, device=device)

  aled_detector = statlab.aled.ALEDDetector()
  print("Starting ALED")
  print("\n**classification report**")
  prob_df = aled_detector.fit_predict(model=new_model, dataset=traindata, **ALED_hyperparams)
  auc3 = print_classification_report(traindata.mislabel_bool_array, prob_df["Mislabel"].to_numpy(), weights=None, confidence=prob_df["mislabel_prob"].to_numpy())
  
  return auc1, auc2, auc3

## CleanLab and ALED workflows
def CL_Looper(cnn, mislabeled_data, num_epochs, batch_size, retrain, device):

    if retrain:
        loss_func = nn.CrossEntropyLoss()
        optimizer = optim.Adam(cnn.parameters(), lr = 0.01)

        loaders = {
            'train' : torch.utils.data.DataLoader(mislabeled_data,
                                                batch_size=batch_size,
                                                shuffle=True,
                                                num_workers=0)
        }

        train(num_epochs, cnn, loaders, optimizer, loss_func)

    print("Starting Cleanlab")

    try:
        y_labels = mislabeled_data.labels.tolist()
    except:
        y_labels = mislabeled_data.labels

    print("**LAB1**: CleanLab report without embeddings (only predict probas):")
    lab1 = Datalab(data={'y': y_labels}, label_name="y")  # include `image_key` to detect low-quality images
    lab1.find_issues(pred_probs=softmaxed_outputs_array(cnn, mislabeled_data, batch_size))#, features=features)

    #lab1.report()

    print("\n**classification report**")
    auc1 = print_classification_report(mislabeled_data.mislabel_bool_array, lab1.get_issues()['is_label_issue'], confidence= (-1) * lab1.get_issues()['label_score'])

    ####

    print("\n\n\n**LAB2**: CleanLab report with embeddings:")
    lab2 = Datalab(data={'y': y_labels}, label_name="y")  # include `image_key` to detect low-quality images
    with torch.no_grad():
        lab2.find_issues(features=compute_embeddings(cnn, mislabeled_data).numpy())
    print("\n**classification report**")
    auc2 = print_classification_report(mislabeled_data.mislabel_bool_array, lab2.get_issues()['is_label_issue'], confidence= (-1) * lab2.get_issues()['label_score'])


    ###

    return auc1, auc2


def compute_embeddings(model, loader):
    device = RUN_PARAMS["device"]
    embeddings_list = []
    feature_extractor = nn.Sequential(*list(copy.deepcopy(model).eval().children())[:-1])
    with torch.no_grad():
        for images, labels in loader:
            images = torch.unsqueeze(images, 0).to(device)

            embeddings = torch.flatten(feature_extractor(images))
            embeddings_list.append(embeddings.detach().cpu())
    print(torch.vstack(embeddings_list).shape)
    return torch.vstack(embeddings_list)


## Run and Compare:
if __name__ == "__main__":
    print("**Running with the following hyperparameters:**", RUN_PARAMS, sep='\n')
    SEED = 123
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    
    performance_dict = {}
    mislabeled_percentage = RUN_PARAMS["mislabeled_percentage"]
    num_trials = RUN_PARAMS["num_trials"]
    
    for dataset in [PneumoniaMNIST, BreastMNIST, DermaMNIST, RetinaMNIST, BloodMNIST]:
        trainset = dataset(split="train", download=True, size=224, transform = data_T)
        valset = dataset(split="val", download=True, size=224, transform = data_T)
        if dataset == DermaMNIST:
            trainset = BinaryDermaMNIST(trainset)
            valset = BinaryDermaMNIST(valset)
        if dataset == RetinaMNIST:
            trainset = BinaryRetinaMNIST(trainset)
            valset = BinaryRetinaMNIST(valset)
        if dataset == BloodMNIST:
            trainset = BinaryBloodMNIST(trainset)
            valset = BinaryBloodMNIST(valset)
    
        CL_perf_list = []
        CL_feat_perf_list = []
        ALED_perf_list = []
        for trial in range(num_trials):
            traindata = Mislabeling_Dataset(trainset, internal_dataset_labels=trainset.labels.squeeze(), fraction_mislabeled=mislabeled_percentage)
            valdata = Mislabeling_Dataset(valset, internal_dataset_labels=valset.labels.squeeze(), fraction_mislabeled=mislabeled_percentage)
            model = RUN_PARAMS["model"]
            CL_stats, CL_feat_stats, ALED_stats = full_looper(traindata, valdata, model, RUN_PARAMS["ALED_hyperparams"])
            CL_perf_list.append(CL_stats)
            CL_feat_perf_list.append(CL_feat_stats)
            ALED_perf_list.append(ALED_stats)
        performance_dict[dataset] = {"CL" : CL_perf_list, "CL_feat" : CL_feat_perf_list, "ALED" : ALED_perf_list}
