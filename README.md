# ImageAnalyzer
Checks a set of images and finds the outliers based on the size and colors in the image. Three algorithms used are: a) Double MAD based, b) Robust Covariance based, c) One-Class SVM

The tool has a UI which takes in the folder with images to analyze, and the method to use for Outlier Detection and a button to kick start the process.

In the background, it extracts the number of colors in the image, and the size of the image and then classifies the image based on filenames, and then runs the outlier detection methods to find out images with anamolies.

This helped automate a manual process of checking each image which was generated from a reporting tool for problems before creating decks out of it.
