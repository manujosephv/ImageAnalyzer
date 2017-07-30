# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 06:50:39 2017

@author: Manu Joseph
"""

import os
import time
from PIL import Image
import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.covariance import EllipticEnvelope

from PyQt4 import QtCore


class ImageAnamolyDetector:

    def __init__(self,start_path, outlier_method, thread):
        self.start_path = start_path
        self.outlier_method = outlier_method
        self.thread = thread

        
    def run(self):
        self.thread.emit(QtCore.SIGNAL("update(QString)"), "Scanning Folder")
        df = self.scan_folder_images(self.start_path)
        if not df.empty:
            df = self.classify_images(df)
            self.df = self.normalize_features(df)
            self.thread.emit(QtCore.SIGNAL("update(QString)"), "Running Outlier Detection")
            if self.outlier_method=="One Class SVM":
                df, ret_data = self.one_class_svm(self.df)
            elif self.outlier_method == "Robust Covariance":
                df, ret_data = self.robust_covariance(self.df)
            elif self.outlier_method == "Univariate MAD based":
                df, ret_data = self.mad_outliers(self.df)
            return df, ret_data
        else:
            self.thread.emit(QtCore.SIGNAL("error(QString)"), "Found no images. Check the folder path")
            return None, None

    def scan_folder_images(self,folder):
        dict_list = {}
        for root, dirs, files in os.walk(folder):
            for name in files:
                dict_file = {}
                if name.endswith((".png")):
                    fstat = os.stat(os.path.realpath(os.path.join(root,name)))
                    dict_file['size'] = fstat.st_size
                    dict_file['date_time'] = time.strftime("%X %x", time.gmtime(fstat.st_mtime))
                    dict_file['name'] = name
                    img = Image.open(os.path.realpath(os.path.join(root,name)))
                    width, height = img.size
                    colors = img.getcolors(width * height)    
                    if colors:
                        dict_file['colors'] = len(colors)
                    dict_list[os.path.realpath(os.path.join(root,name))] = dict_file
        df = pd.DataFrame.from_dict(dict_list, orient='index').reset_index()
        df.rename(columns= {'index':'full_path'}, inplace=True)
        return df

    def classify_images(self,df):
        ##Classify Images
        df['classification'] = ""
        mask1=df.name.str.contains('\w+_CY.png')
        mask2=~df.name.str.contains('Quota_CY.png')
        mask = mask1&mask2
        df.loc[mask,['classification']] = 'AOPR'
        mask1=df.name.str.contains('\w+_NY.png')
        mask2=~df.name.str.contains('Quota_NY.png')
        mask = mask1&mask2
        df.loc[mask,['classification']] = 'AOPR'
        mask=df.name.str.contains('^BIM')
        df.loc[mask,['classification']] = 'AOPR'
        mask=df.name.str.contains('^FA')
        df.loc[mask,['classification']] = 'FA'
        mask=df.name.str.contains('^FB')
        df.loc[mask,['classification']] = 'FB'
        mask=df.name.str.contains('^Quota')
        df.loc[mask,['classification']] = 'AOPE'
        mask=df.name.str.contains('^quota')
        df.loc[mask,['classification']] = 'AOPE'
        mask1=df.name.str.contains('cpgNY.png')
        mask2=df.name.str.contains('cpgCY.png')
        mask = mask1&mask2
        df.loc[mask,['classification']] = 'AOPR'
        mask=df.name.str.contains('^FBv')
        df.loc[mask,['classification']] = 'FBv'
        mask=df.name.str.contains('^category\d')
        df.loc[mask,['classification']] = 'AOPE_cat'
        mask = df['classification'] == ""
        df.loc[mask,['classification']] = 'Others'
        return df


    ###############################################################################
    # MAD based outliers
    ###############################################################################

    def doubleMADsfromMedian(self,y,thresh=3.5):
        # warning: this function does not check for NAs
        # nor does it address issues when 
        # more than 50% of your data have identical values
        m = np.median(y)
        abs_dev = np.abs(y - m)
        left_mad = np.median(abs_dev[y <= m])
        right_mad = np.median(abs_dev[y >= m])
        y_mad = left_mad * np.ones(len(y))
        y_mad[y > m] = right_mad
        modified_z_score = 0.6745 * abs_dev / y_mad
        modified_z_score[y == m] = 0
        return modified_z_score > thresh


    ###############################################################################
    # Get classifier robust covariance
    ###############################################################################

    def getClassifierRobustCovariance(self,data):

        #------------------------------------------------------------------------------
        # Checking prerequisites
        #------------------------------------------------------------------------------

        numberOfSamples = data.shape[0]
        numberOfFeatures = data.shape[1]
        
        if (numberOfSamples > numberOfFeatures ** 2):
            
            #------------------------------------------------------------------------------
            # Preparing and fitting model
            #------------------------------------------------------------------------------
            
            # Initializing classifier
            classifier = EllipticEnvelope(contamination=0.001)
            
            # Fitting classifier
            classifier.fit(data)
            
            return classifier
           
        return None
        
    ###############################################################################
    # Get classifier one class SVM
    ###############################################################################

    def getClassifierOneClassSVM(self,data):

        #------------------------------------------------------------------------------
        # Preparing and fitting model
        #------------------------------------------------------------------------------    
        
        # Initializing classifier
        classifier = svm.OneClassSVM(nu=0.003, gamma=2.0)
        
        # Fitting classifier
        classifier.fit(data)
        
        return classifier
        

    def normalize_features(self,df):
        ###############################################################################
        # Selection and normalization of Features
        ###############################################################################
        features = df.loc[:, ['size', 'colors']]
        # Normalizing features
        features = (features - features.mean()) / (features.max() - features.min())
        features.columns = ['size_normalized','colors_normalized']
        df = df.join(features)
        return df


    def mad_outliers(self,df):
        df_grp = df.groupby('classification')
        outlier_dict = {}
        combined_outlier_dict = {}
        for grp in df_grp.groups:
            df_class = df_grp.get_group(grp)
            if grp != 'Others':
                features = df_class.loc[:,['size_normalized','colors_normalized']]
                decision_array_size = self.doubleMADsfromMedian(features.size_normalized)
                outliers_df_size = df_class[decision_array_size]
                outlier_dict[grp+"_size"] = outliers_df_size
           
                decision_array_color = self.doubleMADsfromMedian(features.colors_normalized)
                outliers_df_color = df_class[decision_array_color]
                outlier_dict[grp+"_color"] = outliers_df_color
                # Displaying results
                combined_outliers = pd.concat([outliers_df_color,outliers_df_size]).drop_duplicates(['full_path'])
                combined_outlier_dict[grp] = combined_outliers
            elif grp == 'Others':
                others_grp = df_class.groupby('name')
                for name in others_grp.groups:
                    df_others_grp = others_grp.get_group(name)
                    features = df_others_grp.loc[:,['size_normalized','colors_normalized']]
                    # Classifying inliers/outliers
                    decision_array_size = self.doubleMADsfromMedian(features.size_normalized)
                    outliers_df_size = df_others_grp[decision_array_size]
                    outlier_dict[grp+"_size"] = outliers_df_size
                    # Displaying results
                    
                    decision_array_color = self.doubleMADsfromMedian(features.colors_normalized)
                    outliers_df_color = df_others_grp[decision_array_color]
                    outlier_dict[name+"_color"] = outliers_df_color
                    
        mad_outliers = pd.concat(outlier_dict.values(), ignore_index=True).drop_duplicates(['full_path'])
        mad_outliers.to_csv('outliers.csv')
        ret_data = {}
        ret_data['count'] = len(mad_outliers.index)
        ret_data['outlier_dict'] = combined_outlier_dict
        return df,ret_data


    ###############################################################################
    # Robust Covariance
    ###############################################################################

    def robust_covariance(self,df):

        df_grp = df.groupby('classification')
        outlier_dict = {}
        classifier_dict = {}
        inlier_dict = {}
        msg_flag = False
        for grp in df_grp.groups:
            df_class = df_grp.get_group(grp)
            if grp != 'Others':
                features = df_class.loc[:,['size_normalized','colors_normalized']]
                # Getting classifier
                classifierRobustCovariance = self.getClassifierRobustCovariance(features)
                if classifierRobustCovariance is not None:
                    classifier_dict[grp] = classifierRobustCovariance
                    # Classifying inliers/outliers
                    decisionsRobustCovariance = classifierRobustCovariance.decision_function(features)
                    outliers = features[decisionsRobustCovariance < 0]
                    outliers_index = outliers.index.values
                    outliers_df = df_class[df_class.index.isin(outliers_index)]
                    outlier_dict[grp] = outliers_df
                    inlier_dict[grp] = features[decisionsRobustCovariance >= 0]
                else:
                    msg_flag = True

            elif grp == 'Others':
                others_grp = df_class.groupby('name')
                for name in others_grp.groups:
                    df_others_grp = others_grp.get_group(name)
                    features = df_others_grp.loc[:,['size_normalized','colors_normalized']]
                    # Getting classifier
                    classifierRobustCovariance = self.getClassifierRobustCovariance(features)
                    if classifierRobustCovariance is not None:
                        # Classifying inliers/outliers
                        decisionsRobustCovariance = classifierRobustCovariance.decision_function(features)
                        outliers = features[decisionsRobustCovariance < 0]
                        outliers_index = outliers.index.values
                        outliers_df = df_class[df_class.index.isin(outliers_index)]
                        outlier_dict[grp] = outliers_df
                    else:
                        msg_flag = True
        if msg_flag:
            self.thread.emit(QtCore.SIGNAL("error(QString)"), "Robust Covariance needs atleast 4 images to work. Please try another method")
        robust_covariance_outliers=pd.concat(outlier_dict.values(), ignore_index=True)
        robust_covariance_outliers.to_csv('outliers.csv')
        ret_data = {}
        ret_data['count'] = len(robust_covariance_outliers.index)
        ret_data['outlier_dict'] = outlier_dict
        ret_data['inlier_dict'] = inlier_dict
        ret_data['classifier_dict'] = classifier_dict
        return df,ret_data

    ###############################################################################
    # One Class SVM
    ###############################################################################

    def one_class_svm(self,df):
        df_grp = df.groupby('classification')
        outlier_dict = {}
        classifier_dict = {}
        inlier_dict = {}
        for grp in df_grp.groups:
            df_class = df_grp.get_group(grp)
            if grp != 'Others':
                features = df_class.loc[:,['size_normalized','colors_normalized']]
                # Getting classifier
                classifierOneClassSVM = self.getClassifierOneClassSVM(features)
                classifier_dict[grp] = classifierOneClassSVM
                # Classifying inliers/outliers
                decisionsOneClassSVM = classifierOneClassSVM.decision_function(features)
                outliers = features[decisionsOneClassSVM < 0]
                outliers_index = outliers.index.values
                outliers_df = df_class[df_class.index.isin(outliers_index)]
                outlier_dict[grp] = outliers_df
                inlier_dict[grp] = features[decisionsOneClassSVM >= 0]
            elif grp == 'Others':
                others_grp = df_class.groupby('name')
                for name in others_grp.groups:
                    df_others_grp = others_grp.get_group(name)
                    features = df_others_grp.loc[:,['size_normalized','colors_normalized']]
                    # Getting classifier
                    classifierOneClassSVM = self.getClassifierOneClassSVM(features)
                    # Classifying inliers/outliers
                    decisionsOneClassSVM = classifierOneClassSVM.decision_function(features)
                    outliers = features[decisionsOneClassSVM < 0]
                    outliers_index = outliers.index.values
                    outliers_df = df_class[df_class.index.isin(outliers_index)]
                    outlier_dict[grp] = outliers_df

        one_class_svm_outliers=pd.concat(outlier_dict.values(), ignore_index=True)
        one_class_svm_outliers.to_csv('outliers.csv')
        ret_data = {}
        ret_data['count'] = len(one_class_svm_outliers.index)
        ret_data['outlier_dict'] = outlier_dict
        ret_data['inlier_dict'] = inlier_dict
        ret_data['classifier_dict'] = classifier_dict
        return df,ret_data