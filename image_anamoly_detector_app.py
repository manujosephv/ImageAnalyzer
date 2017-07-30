# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 20:18:57 2017

@author: 310228580
"""

from PyQt4 import QtGui
from PyQt4.QtCore import QThread, QCoreApplication, SIGNAL
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
import json
import logging
import sys, os # We need sys so that we can pass argv to QApplication and os to make paths
from ImageAnamolyDetector import ImageAnamolyDetector
import Image_Analyzer_UI # This file holds our MainWindow and all design related things
              # it also keeps events etc that we defined in Qt Designer
class AnalyzeThread(QThread):
    def __init__(self,dict_config):
        self.dict_config = dict_config
        logging.basicConfig(filename='error.log', level=logging.DEBUG, 
        format='%(asctime)s %(levelname)s %(name)s %(message)s')
        self.logger=logging.getLogger(__name__)
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        image_detector = ImageAnamolyDetector(self.dict_config['start_path'], self.dict_config['outlier_method'], self)        
        try:
            df, ret_data = image_detector.run()
            if df is not None:
                signal_dict = {}
                signal_dict['df'] = df
                signal_dict['ret_data'] = ret_data
                signal_dict['outlier_method'] = self.dict_config['outlier_method']
                self.emit(SIGNAL('end_analyze(PyQt_PyObject)'), signal_dict)
        except Exception as err:
            self.emit(SIGNAL("error(QString)"), "Something wet wrong. Please check the error log")
            self.logger.exception(err)
        

class ImageAnamolyDetectorApp(QtGui.QDialog,Image_Analyzer_UI.Ui_ImageAnalyzer):
    def __init__(self, parent=None):
       # Explaining super is out of the scope of this article
        # So please google it if you're not familar with it
        # Simple reason why we use it here is that it allows us to
        # access variables, methods etc in the design.py file
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
        # It sets up layout and widgets that are defined
        self.pushButton.clicked.connect(self.selectFolder)
        self.quit.clicked.connect(self.quit_app)
        self.analyze.clicked.connect(self.start_analyze)
        self.configfile_name = "config.json"
        dict_config = self.read_config()
        if dict_config:
            self.lineEdit.setText(dict_config['start_path'])
            
            for radio in self.anamolyBox.findChildren(QtGui.QRadioButton):
                if radio.text() == dict_config['outlier_method']:
                    radio.setChecked(True)
                else:
                    radio.setChecked(False)
            
        
        
    ###############################################################################
    # Display results
    ###############################################################################
    def displayResults(self,inliers, outliers, classifier, outputTitle, outputName, x_column_name, y_column_name, xlabel, ylabel, row, count, column):
        
        fig = self.figure
        ax = fig.add_subplot(row,column,count)
        # Defining grid
        gridX, gridY = np.meshgrid(np.linspace(-0.5, 1.5, 1000), np.linspace(-0.5, 1.5, 1000))
        # Computing decision for each point of the grid
        gridDecisions = classifier.decision_function(np.c_[gridX.ravel(), gridY.ravel()])
        # Plotting decision boundary (each point of the grid whose decision value is 0)
        gridDecisions = gridDecisions.reshape(gridX.shape)
        plotBoundary = ax.contour(gridX, gridY, gridDecisions, levels=[0], linewidths=2, colors='blue')
        ax.clabel(plotBoundary, inline=1, fontsize=12)
        # Plotting inliers and outliers
        ax.scatter(inliers.loc[:, x_column_name], inliers.loc[:, y_column_name], label="Inliers", color='green', alpha=0.2)
        ax.scatter(outliers.loc[:, x_column_name], outliers.loc[:, y_column_name], label="Outliers", color='red', alpha=1.0)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_ylabel("")
        ax.set_xlabel("")
        ax.set_title(outputTitle)
        plt.setp(ax.get_xticklabels(),visible=False)
        plt.setp(ax.get_yticklabels(),visible=False)
#        ax.legend()    
        plt.savefig(outputName + ".png")
        
    def displayResultsUnivariate(self,features, outliers, outputTitle, outputName,y_column_name1,y_column_name2 , ylabel, row, count, column):
        
        fig = self.figure
        ax = fig.add_subplot(row,column,count)
        # Defining grid
        gridX, gridY = np.meshgrid(np.linspace(-0.5, 1.5, 1000), np.linspace(-0.5, 1.5, 1000))
        sns.distplot(features[y_column_name1], ax=ax, rug=True, hist=False)
        sns.distplot(features[y_column_name2], ax=ax, rug=True, hist=False)    
        # Plotting inliers and outliers
        ax.plot(outliers[y_column_name1], np.zeros_like(outliers[y_column_name1]), 'ro', clip_on=False)
        ax.plot(outliers[y_column_name2], np.zeros_like(outliers[y_column_name2]), 'ro', clip_on=False)
        ax.set_ylabel("")
        ax.set_xlabel("")
        ax.set_title(outputTitle)
        plt.setp(ax.get_xticklabels(),visible=False)
        plt.setp(ax.get_yticklabels(),visible=False)
#        ax.legend()    
        plt.savefig(outputName + ".png")

    def plot_results(self,df,ret_dict,outlier_method):
        df_grp = df.groupby('classification')
        self.figure.clear()
        self.figure.subplots_adjust(left=0.03,right=0.97,bottom=0.06,top=0.77,hspace=.4, wspace=.06)
        self.figure.suptitle('Detecting potential outliers using \n {}'.format(outlier_method), fontsize=14)
        count = 1
        column = 3
        row = math.ceil(float(len(df_grp))/float(column))
        outlier_dict = ret_dict['outlier_dict']        
        if outlier_method != "Univariate MAD based":
            inlier_dict = ret_dict['inlier_dict']            
            classifier_dict = ret_dict['classifier_dict']
        
        for grp in df_grp.groups:
            if grp != 'Others':
                # Displaying results
                    if outlier_method != "Univariate MAD based":
                        self.displayResults(inliers=inlier_dict[grp],
                                        outliers=outlier_dict[grp],
                                        classifier=classifier_dict[grp],
                                        outputTitle = grp,
                                        outputName="plot",
                                        x_column_name = "size_normalized",
                                        y_column_name="colors_normalized",
                                        xlabel="Size of Image",
                                        ylabel = "No. Of Colors",
                                        row=row,
                                        count=count,
                                        column=column
                                      )
                    elif outlier_method == "Univariate MAD based":
                        df_class = df_grp.get_group(grp)                        
                        features = df_class.loc[:,['size_normalized','colors_normalized']]
                        self.displayResultsUnivariate(features=features,
                                outliers=outlier_dict[grp],
                                outputTitle = grp,
                                outputName="plot",
                                y_column_name1="size_normalized",
                                y_column_name2="colors_normalized",
                                ylabel = "Size and Color",
                                row=row,
                                count=count,
                                column=column
                              )   
                    count = count + 1
            self.figure.canvas.mpl_connect('button_press_event', self.on_click)
            self.canvas.setToolTip('Left Click on a Graph to zoom in. Right Click to go back')            
            self.canvas.draw()
   
    def on_click(self,event):
        """Enlarge or restore the selected axis."""
        ax = event.inaxes
        if ax is None:
            # Occurs when a region not in an axis is clicked...
            return
        if event.button is 1:
            # On left click, zoom the selected axes
            ax._orig_position = ax.get_position()
            ax.set_position([0.1, 0.1, 0.85, 0.7])
            for axis in event.canvas.figure.axes:
                # Hide all the other axes...
                if axis is not ax:
                    axis.set_visible(False)
        elif event.button is 3:
            # On right click, restore the axes
            try:
                ax.set_position(ax._orig_position)
                for axis in event.canvas.figure.axes:
                    axis.set_visible(True)
            except AttributeError:
                # If we haven't zoomed, ignore...
                pass
        else:
            # No need to re-draw the canvas if it's not a left or right click
            return
        event.canvas.draw()
                
    def selectFolder(self):
        self.lineEdit.setText(str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory")))
        

    def start_analyze(self):
        for radio in self.anamolyBox.findChildren(QtGui.QRadioButton):
            if radio.isChecked():
                outlier_method = radio.text()
        start_path = os.path.abspath(self.lineEdit.text())
        dict_config = {}
        dict_config['start_path'] = str(start_path)
        dict_config['outlier_method'] = str(outlier_method)
        # Next we need to connect the events from that thread to functions we want
        # to be run when those signals get fired
        self.update_config(dict_config)              
        self.analyze_thread = AnalyzeThread(dict_config)
        self.connect(self.analyze_thread, SIGNAL("end_analyze(PyQt_PyObject)"), self.end_analyze)  
        self.connect(self.analyze_thread, SIGNAL("update(QString)"), self.update_progress)
        self.connect(self.analyze_thread, SIGNAL("error(QString)"), self.error_end)
        self.analyze_thread.start()
        self.progressBar.setVisible(True)
        self.pushButton.setEnabled(False)
        self.analyze.setEnabled(False)
    
    def update_progress(self,status):
        self.resultLabel.setText("{}...".format(status))
    
    def update_config(self, dict_config):
        # Check if there is already a configurtion file
        # Create the configuration file as it doesn't exist yet or open the file and rewrite
        cfgfile = open(self.configfile_name, 'w')
        
        json.dump(dict_config,cfgfile)
        cfgfile.close()
        
    def read_config(self):
        # Check if there is already a configurtion file
        if os.path.isfile(self.configfile_name):
            cfgfile = open(self.configfile_name, 'r')
            dict_config = json.load(cfgfile)
            cfgfile.close()
            return dict_config
        else:
            return None
    
    
    def end_analyze(self, signal_dict):
        df = signal_dict['df']
        ret_data = signal_dict['ret_data']
        no_outliers = ret_data['count']
        outlier_method = signal_dict['outlier_method']
        self.plot_results(df,ret_data, outlier_method)
        self.progressBar.setVisible(False)
        self.resultLabel.setText("{} outliers found. Please check the excel file for details".format(no_outliers))
        self.pushButton.setEnabled(True)
        self.analyze.setEnabled(True)
            
    def error_end(self, error_msg):
        self.progressBar.setVisible(False)
        self.resultLabel.setText(error_msg)
        self.pushButton.setEnabled(True)
        self.analyze.setEnabled(True)
        
    def quit_app(self):
        QCoreApplication.instance().quit()                           
        


def main():
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    form = ImageAnamolyDetectorApp()                 # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function