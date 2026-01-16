import numpy as np
import torch
from sklearn.covariance import MinCovDet
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils import check_X_y
from sklearn.utils.multiclass import unique_labels
import pandas as pd
from torch.utils.data import DataLoader
from collections import OrderedDict
import torch.nn as nn


class ALEDDetector(BaseEstimator, ClassifierMixin):
    """
    A method for Adaptive Label Error Detection, identifying mislabeling in 
    the reference labels used to train deep neural networks. Manuscript with
    further details will be available shortly. You may need to overwrite 
    ALEDDetector.extract_features() or manually assign ALEDDetector.feats if
    your model is in a different format.
    """

    def __init__(self, random_state=0):
        self.random_state = random_state
        self.feats = None


    def fit_predict(self, model, dataset, device=None, num_ensembles=10, num_components=2, likelihood_ratio_threshold=2, batch_size=100, support_fraction=None):
        """ # format is copied in part from sklearn, enabling interoperability
        
        Perform mislabeling detection, according to the Adaptive Label Error
        Detection (ALED) algorithm. Model input classes and predict which
        samples are mislabeled.

        Parameters
        ----------
        model : PyTorch model with multiple layers
            Neural network trained on the input dataset.
        
        dataset : PyTorch-style dataset
            Dataset that `model` was trained on. Currently, only 2 classes 
            are supported.
        
        device : PyTorch device, string, or None
            PyTorch device or string specifying a PyTorch-readable device for
            where to perform model inference. E.g., "cuda", None.
        
        num_ensembles : int
            Number of times to repeat random projection generation and
            likelihood estimation. Likelihoods are averaged across each
            ensemble.
        
        num_components : int
            Number of components to be used for class probability distribution 
            estimation. There is 1 predefined component, and the rest of the 
            components are random projections. Must be >= 1. Must be less than 
            the number of components in the high dimensional space (this is
            usually a large number, so conflicts are unlikely).
            
        likelihood_ratio_threshold : float
            Given the ratio of out-of-class likelihood to in-class likelihood 
            for each sample, change the label of the sample if the ratio is 
            greater than this threshold. Must be > 0.
        
        batch_size : int
            Batch size to use when extracting initial features (i.e., running 
            `dataset` through `model`). Used be ALEDDetector.extract_featurs().
            Must be > 0.
        
        support_fraction : float or None
            Input parameter to sklearn.covariance.MinCovDet. "The proportion 
            of points to be included in the support of the raw MCD estimate."
            If None, a formula is used to determine support_fraction. Must be 
            within (0, 1].


        Returns
        -------
        prediction_stats : Pandas Dataframe
            A dataframe with mislabeling analysis on `dataset`. Various 
            statistics are computed for each sample, including:
                - estimated posterior probability for each that the sample
                belongs to that class
                - mislabeling probability
                - ALED-predicted label
                - ALED-predicted mislabeling (boolean)
            Note that this function (ALEDDetector.fit_predict()) changes self
            and additional metadata is stored in the object.
        """
        
        self.check_params(num_ensembles, num_components,
                          likelihood_ratio_threshold, batch_size)
        
        self.likelihood_ratio_threshold = likelihood_ratio_threshold
        if self.feats == None:
            self.extract_features(model, dataset, device, batch_size)
        
        # Compute the mean vectors of each class in the feature space
        mean_vectors = {}
        for class_i in self.classes_:
            mean_vectors[class_i] = np.mean(self.X_[self.y_ == class_i], axis=0)

        # Define the first projection direction as the vector between the class means
        mean_0 = mean_vectors[self.classes_[0]]
        mean_1 = mean_vectors[self.classes_[1]]
        sep_vec = (mean_0 - mean_1) / np.linalg.norm(mean_0 - mean_1)

        # Perform classification for each random projection
        all_likelihoods = []
        for _ in range(num_ensembles):
            # Initialize the random projections matrix with the first component as `sep_vec`
            rp = np.random.randn(self.X_.shape[1], num_components - 1)  # Remaining random components
            rp_stacked = np.concatenate((np.resize(sep_vec, (sep_vec.shape[0], 1)), rp), axis=1)
            # Project the features using the custom random projection
            X_proj = self.X_.dot(rp_stacked)

            # Calculate covariance matrices for each class
            cov_dict = {}
            class_indices_dict = {}
            PC_dict = {}
            priors_dict = {}
        
            for class_i in self.classes_:
                class_indices = np.array(np.arange(len(X_proj))[self.y_ == class_i])
                class_indices_dict[f"class{class_i}_indices"] = class_indices
                class_PC_array = X_proj[class_indices, :]  # Transformed data for the current class
                PC_dict[f"class{class_i}_PC_array"] = class_PC_array
        
                # Robust covariance estimation
                cov_dict[f"robust_cov{class_i}"] = MinCovDet(random_state=self.random_state, support_fraction=support_fraction).fit(class_PC_array)

            mcd_list = []
            for class_i in self.classes_:
                mcd_list.append(cov_dict[f"robust_cov{class_i}"])
            
            # Compute priors for each class
            for class_i in self.classes_:
                prior = len(class_indices_dict[f"class{class_i}_indices"]) / len(self.y_)
                priors_dict[f"prior_prob{class_i}"] = prior
        
            # Calculate likelihoods based on Mahalanobis distances
            likelihoods_dict = {}
            for class_i in self.classes_:
                likelihoods_dict[class_i] = {}
                for class_j in self.classes_:
                    cov_matrix = cov_dict[f"robust_cov{class_j}"].covariance_
                    cov_mahalanobis = cov_dict[f"robust_cov{class_j}"].mahalanobis(PC_dict[f"class{class_i}_PC_array"])
                    likelihoods = np.array([self.gaussian_likelihood(cov_matrix, dist) for dist in cov_mahalanobis])
                    likelihoods_dict[class_i][class_j] = likelihoods
        
            # Create a DataFrame for this projection's likelihoods
            likelihoods_df = pd.DataFrame(index=np.arange(len(X_proj)))
            for class_j in self.classes_:
                all_class_likelihoods = np.zeros(len(X_proj))
                for class_i in self.classes_:
                    class_indices = class_indices_dict[f"class{class_i}_indices"]
                    all_class_likelihoods[class_indices] = likelihoods_dict[class_i][class_j]
                likelihoods_df[f"class{class_j}"] = all_class_likelihoods
        
            all_likelihoods.append(likelihoods_df)
        
        # Average likelihoods across ensembles
        avg_likelihoods_df = sum(all_likelihoods) / num_ensembles
        self.likelihoods_ = avg_likelihoods_df
        
        # Calculate posterior probabilities
        prediction_stats = pd.DataFrame(index=np.arange(len(avg_likelihoods_df)))
        epsilon = 1e-12
        
        for class_j in self.classes_:
            prediction_stats[f"p(k = {class_j} | x)"] = (
                avg_likelihoods_df[f"class{class_j}"]
                * priors_dict[f"prior_prob{class_j}"]
                / (sum(
                    [
                        avg_likelihoods_df[f"class{class_k}"] * priors_dict[f"prior_prob{class_k}"]
                        for class_k in self.classes_
                    ]
                ) + epsilon)
            )
        self.cov_dict = cov_dict
        prediction_stats["given label (name)"] = [self.classes_[int(label)] for label in self.y_]
        prediction_stats['mislabel_prob'] = prediction_stats.apply(lambda row: row[1] if row[2] == 0 else row[0], axis=1)
        prediction_stats["Aled label"] = prediction_stats.apply(self.extract_out_label, axis=1)
        prediction_stats["Mislabel"] = prediction_stats["given label (name)"].ne(prediction_stats["Aled label"])
        self.prediction_stats = prediction_stats
        return self.prediction_stats

    def check_params(self, num_ensembles, num_components, likelihood_ratio_threshold, batch_size):
        if (type(num_ensembles) != int) or (num_ensembles < 1):
            raise Exception("num_ensembles must be a positive integer (>=1).")
        
        if (type(num_components) != int) or (num_components < 1):
            raise Exception("num_components must be a positive integer (>=1).")
        
        if (not isinstance(likelihood_ratio_threshold, (int, float))) or \
            (likelihood_ratio_threshold < 1e-8):
                raise Exception("likelihood_ratio_threshold must be a positive float (>0).")
            
        if (type(batch_size) != int) or (batch_size < 1):
            raise Exception("batch_size must be a positive integer (>=1).")

    @staticmethod
    def gaussian_likelihood(cov_matrix, mahalanobis_squared_dist):
        n = cov_matrix.shape[0]
        sqrt_det = np.sqrt(np.linalg.det(cov_matrix))
        prob_x_f = (1 / ((2 * np.pi) ** (n / 2) * sqrt_det)) * np.exp(-0.5 * mahalanobis_squared_dist)
        return prob_x_f

    def extract_out_label(self, prediction_stats_row):
        given_label = prediction_stats_row['given label (name)']
        probabilities_row = np.array(
            [prediction_stats_row[f"p(k = {class_i} | x)"] for class_i in self.classes_]
        )
        if (self.classes_[probabilities_row.argmax()] != given_label) and (
            probabilities_row.max()
            / prediction_stats_row[f"p(k = {given_label} | x)"]
            > self.likelihood_ratio_threshold
        ):
            return self.classes_[probabilities_row.argmax()]
        else:
            return given_label

    def extract_features(self, model, dataset, device=None, batch_size=100):
        self.conv_net = nn.Sequential(OrderedDict(list(model.named_children())[:-1])) 
        self.conv_net.avgpool = torch.nn.AdaptiveAvgPool2d((1, 1))
        self.batch_size = batch_size
        
        BATCH_SIZE = self.batch_size
        dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=False)
        feat_array = None
        y = np.zeros(len(dataset))
        with torch.no_grad():
            for batch_num, (inputs, labels) in enumerate(dataloader):
                batch_cuda = inputs.to(device)
                batch_feat = self.conv_net(batch_cuda)
                batch_feat_cpu = batch_feat.to('cpu').squeeze()
                if feat_array is None:
                    feat_array = np.zeros((len(dataset), *batch_feat_cpu.shape[1:]))
                feat_array[batch_num * BATCH_SIZE:batch_num * BATCH_SIZE + len(batch_feat_cpu)] = batch_feat_cpu
                y[batch_num * BATCH_SIZE:batch_num * BATCH_SIZE + len(batch_feat_cpu)] = labels
        feat_array, y = check_X_y(feat_array, y)
        self.classes_ = unique_labels(y)
        self.X_ = feat_array
        self.y_ = y
        self.feats = "Done"