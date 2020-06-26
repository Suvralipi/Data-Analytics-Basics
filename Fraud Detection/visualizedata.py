# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 11:21:11 2020

@author: 561527
"""
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from sklearn.externals.six import StringIO  
from IPython.display import Image  
from sklearn.tree import export_graphviz
import pydotplus
import io
import os
from FraudDependencyParser import FraudDependencyParser

import warnings
warnings.filterwarnings("ignore")

import gc
gc.enable()


obj = FraudDependencyParser()

def visualizeFraudData(input_df, df_fraud):
    # Counting frequency and percentage of fraud
    num_transaction_total, num_transaction_fraud = len(input_df), len(df_fraud)
    # Fraud Percentage and Non-Fraud Percentage
    percent_fraud = round(num_transaction_fraud / num_transaction_total * 100, 2)
    percent_safe = 100 - percent_fraud
    
    fig, ax = plt.subplots()
    color_palette_list = ['pink', '#C1F0F6'] 
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.size']=12
    labels = ['Non-Fraud', 'Fraud']
    percentages = [percent_fraud, percent_safe]
    explode=(0.1,0)
    ax.pie(percentages, explode=explode, labels=labels,  
           colors=color_palette_list[0:2], autopct='%1.0f%%', 
           shadow=False, startangle=0,   
           pctdistance=1.2,labeldistance=1.4)
    ax.axis('equal')
    ax.set_title("Percentage of Fraudulent vs Non-Fraudulent Transactions")
    ax.legend(frameon=False, bbox_to_anchor=(1.5,0.8))
    
    plt.savefig(os.path.join(obj.outpath, '/PieChartFraudNonFraud.jpg'))
    plt.close()
    return
    
    
    
def visualizeTransAmount(input_df, source, target):
    group_stats = input_df.groupby([target])[source].mean().reset_index()
    sns.set(style="whitegrid")
    sns.set(font_scale = 1.1)
    plt.figure(figsize=(6,5))
    ax=sns.barplot(x=target,y=source, data=group_stats, palette='Spectral')
    ax.set_title('Average Trans Amount per Class', size=14)
    ax.set_ylabel('Amount', fontsize = 14.0) # Y label
    ax.set_xlabel('Non-Fraud vs Fraud Trans Amount', fontsize = 14) # X label
    for i, v in enumerate(group_stats[source]):
        plt.text(i - 0.1, v + 0.01, str(int(v)))
    plt.savefig(obj.outpath+'/BarPlot_TransAmount.jpg')
    plt.close()
    return


def paired_plot(df_fraud, df_nonfraud, col_x, col_y):
    sns.set(style="whitegrid")
    sns.set(font_scale = 1.2)

    plt.figure(2, figsize=(20,12))
    the_grid = GridSpec(2, 2)

    plt.subplot(the_grid[0, 1])
    ax1=sns.barplot(x=col_x,y=col_y, data=df_fraud, palette='Spectral')
    title1='Fraudulent Trans ' + str(col_x) +' vs ' + str(col_y) + ' of Transaction '
    ax1.set_title(title1, size=18)
    ax1.set_ylabel(col_y, fontsize = 16.0) # Y label
    ax1.set_xlabel(col_x, fontsize = 16) # X label
    ax1.set_xticklabels(ax1.get_xticklabels(),rotation=45,ha="right",rotation_mode='anchor',fontweight="bold",fontsize=14)

    plt.subplot(the_grid[0, 0])
    ax2=sns.barplot(x=col_x,y=col_y, data=df_nonfraud, palette='Spectral')
    title2='Non-Fraudulent Trans ' + str(col_x) +' vs ' + str(col_y) + ' of Transaction '
    ax2.set_title(title2, size=18)
    ax2.set_ylabel(col_y, fontsize = 16.0) # Y label
    ax2.set_xlabel(col_x, fontsize = 16) # X label
    ax2.set_xticklabels(ax2.get_xticklabels(),rotation=45,ha="right",rotation_mode='anchor',fontweight="bold",fontsize=14)

    plt.tight_layout()
    fig_name = obj.outpath+'/Barplot_' + str(col_x) + 'vs' + str(col_y)+'.jpg'
    plt.savefig(fig_name)
    plt.close()
    return

def feature_distribution(v_features, df_fi):
    #Data Visualization for checking the distribution for Genuine cases & Fraud cases for each feature
    plt.figure(figsize=(20,15))
    plt.suptitle('Distribution of Features - Non-Fraud vs Fraud Class',fontsize=14)
    gs = GridSpec(3,3)

    for i, col in enumerate(v_features):
        j = i%3
        k = int(i/3)
        if i >= 9:
            break
        ax = plt.subplot(gs[k, j])
        sns.distplot(df_fi[col][df_fi['fraud']==0],hist=True, kde=True, 
                     bins=30,kde_kws={'linewidth': 2},color='green',label='Non-Fraud Class')
        sns.distplot(df_fi[col][df_fi['fraud']==1],hist=True, kde=True, 
                     bins=30,kde_kws={'linewidth': 2},color='red',label='Fraud Class')

    handles, labels = ax.get_legend_handles_labels()
    plt.figlegend(labels, loc='upper right')
    plt.tight_layout()
    plt.savefig(obj.outpath+'/featureDist.jpg')
    plt.close()
    return


def plot_feature_importance(ds_fi):
    # plotting feature imporance bar-graph
    plt.figure(figsize=(10,8))

    # Generating stacked bar-chart
    bars_ft = plt.bar(range(len(ds_fi)), ds_fi, width = .8, color = '#2d64bc')

    # Labeling
    plt.suptitle("Feature Importances", fontsize = 20)
    plt.xticks(range(len(ds_fi)), ds_fi.index, fontsize = 10, rotation=45)

    # plot-dejunking
    ax = plt.gca()
    ax.yaxis.set_visible(False) # hide entire y axis (both ticks and labels)
    ax.xaxis.set_ticks_position('none')  # hide only the ticks and keep the label
    # hide the frame
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    # value displaying
    rects = ax.patches  
    labels = ds_fi.values.round(2)
    for rect, label in zip(rects, labels):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2, height, label, ha='center', va='bottom', fontsize = 12)

    plt.savefig(obj.outpath+'/featureImportance.jpg')
    plt.close()
    return

def generate_DecisionTreeGraph(dt):
    dot_data = StringIO()
    export_graphviz(dt, out_file=dot_data,  
                filled=True, rounded=True,
                special_characters=True, feature_names = obj.col_names_data, class_names=['0','1'])
    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
    Image(graph.create_png())
    graph.write_pdf(obj.outpath+'/DT_Graph.pdf')
    
    return

    
    