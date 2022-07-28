
'''
calculate regression analysis column by column for every column against 
every other column in a csv file and save in a data frame.
Write dataframe data to html, tex etc. 
'''

from fileinput import filename
from scipy import stats
import pandas as pd
import numpy as np

def regress_from_csv(filename):
    '''All by all regression of the columns in a csv file.'''
    data_frame = pd.read_csv(filename)
    #print(data_frame.head(15))
    slope_list = []
    key_list = []
    data_names = []
    for (column_name,column_data) in data_frame.iteritems():
        dependent_data = column_data
        dependent_name = column_name
        data_names.append(dependent_name)
        slope_row_data = []
        key_row_data = []
        for (comparison_column_name,comparison_column_data) in data_frame.iteritems():
            independent_data = comparison_column_data
            independent_name = comparison_column_name
            # scipy regression
            slope, intercept, r_value, p_value, std_err = \
                stats.linregress(independent_data, dependent_data)
            
            # if stdout_flag == true:
            # print to stdout stuff.
            calculation_key =  independent_name + dependent_name
            print(calculation_key, slope, intercept, r_value, p_value, std_err)
            
            slope_row_data.append(slope)
            key_row_data.append(calculation_key)
        slope_list.append(slope_row_data)
        key_list.append(key_row_data)
    slope_array = np.array(slope_list)
    slope_dataframe = pd.DataFrame(slope_list)

    # Label columns/rows as Inpendent/Dependent variables.
    slope_dataframe.columns = pd.MultiIndex.from_product([["Independent"], data_names])
    slope_dataframe.index = pd.MultiIndex.from_product([["Dependent"], data_names])
    return slope_dataframe

def dataframe_to_html(dataframe, filename_stem):
    '''write dataframe to html file called filename_stem".html"'''
    html_filepointer = open(filename_stem+".html", "w")
    html_filepointer.write(dataframe.to_html())
    html_filepointer.close()

def dataframe_to_tex(dataframe, filename_stem):
    '''write dataframe to tex file called filename_stem".tex"''' 
    #write as .tex to file
    html_filepointer = open(filename_stem+".tex", "w")
    html_filepointer.write(dataframe.to_latex())
    html_filepointer.close()
        
slope_dataframe = regress_from_csv("Example1_3_node_chain_NetworkValues.csv")
dataframe_to_html(slope_dataframe, "test")
dataframe_to_tex(slope_dataframe, "test")