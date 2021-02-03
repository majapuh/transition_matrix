# -*- coding: utf-8 -*-


import collections
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd


class TransitionMatrix(object):
    
    def __init__(self,  value_pairs):
        self.new_value_pairs = value_pairs

            
    def generate_initial_transformation_matrix(self):
        self.labels = list(sorted(set(old_model_dict.values())))
        self.labels.append('None')
    
        #additional row/column for missing values
        self.size = len(set(old_model_dict.values())) + 1
        
        self.transition_matrix = np.zeros((self.size,self.size), dtype=int)
        
        
    def process_new_model(self):
       
        for key, new_value in self.new_value_pairs: 
                    
            #if any additional sample in new model, give it transition none
            old_value = old_model_dict.pop(int(key), 'None')
            
            try:
                self.transition_matrix[self.labels.index(new_value)][self.labels.index(old_value)] += 1
            
            except ValueError: 
                #if there is new label in new Model
                new_label = np.zeros((1,self.size),  dtype=int)
                new_label[0][self.labels.index(old_value)] += 1
                
                arr = np.append(self.transition_matrix[:-1,:], new_label, axis=0)
                self.transition_matrix = np.append(arr, [self.transition_matrix[-1,:]], axis=0)
                
                #add new label to list, and expand cf for oldModel
                self.labels.insert(-1, new_value)
                self.size += 1
                
                new_label = np.zeros((self.size), dtype=int)
                arr = np.c_[self.transition_matrix[:,:-1], new_label]
                
                self.transition_matrix = np.c_[arr, self.transition_matrix[:,-1]]
 
                
        #check if any additional sample in old model
        while old_model_dict:
            key, old_value = old_model_dict.popitem()
            self.transition_matrix[-1][self.labels.index(old_value)] += 1
            
      
  
    
    def calculate_match_perc (self):
        x = round((self.transition_matrix.trace()/ self.transition_matrix.sum()) * 100, 2)
        
        print('Percentage of labels that match: {0}%'.format(x))
        print()



    def find_most_common_transitions (self, N = 3):
        mask = (self.transition_matrix)*(-1)
        np.fill_diagonal(mask, 0)
        
        indices = np.array(np.unravel_index(np.argsort(mask, axis=None), mask.shape))
        
        print('Most common label transitions:')
        
        for x, y in np.dstack(indices[:,:N])[0]:       
            print('Old label: {0}, new label: {1}, count:{2}'.format (self.labels[y], self.labels[x], self.transition_matrix[x][y]))
            
        print()
     
    
    
    def plot_distribution (self):
        oldFreq = self.transition_matrix[:,:-1].sum(axis=0)
        newFreq = self.transition_matrix[:-1,:].sum(axis=1)
    
        x = np.arange(self.size-1)  
        width = 0.35  
        kwargs = dict(alpha=0.7, align='edge')
        
        fig, ax = plt.subplots()
        ax.bar(x, oldFreq, -width, **kwargs, label='Old Model')
        ax.bar(x, newFreq, width, **kwargs, label='New Model', color='g')
        
        ax.set_xlabel('Classes')
        ax.set_ylabel('Frequency')
        ax.set_title('Distribution over classes')
        ax.set_xticks(x)
        ax.set_xticklabels(self.labels)
        ax.set_axisbelow(True)
        ax.yaxis.grid(color='gray', linestyle='dashed')
        ax.legend()
        
 
    
    def format_confusion_matrix(self):    
        df = pd.DataFrame(self.transition_matrix, columns=self.labels, index=self.labels)
        print('New model / Old model\n')
        print(df)
        

        
    def create_transition_matrix(self):
        self.generate_initial_transformation_matrix() 
        self.process_new_model()
        self.calculate_match_perc()    
        self.find_most_common_transitions()
        self.plot_distribution()
        self.format_confusion_matrix()
  


def process_model(file):       
    try:
        
        with open (file, 'r') as f:
            for line in f: 
                try:
                    key, value  = line.strip().split(delimiter)
                    
                    yield key, value
                   
                except ValueError: 
                    print('Wrongly formatted value in the file.')
                                 
    except FileNotFoundError:
        print('Could not find the {0} file. '.format(file))

   
    
    
if __name__ == '__main__':
    
    #default values
    old_model_file = 'oldModel.txt'
    new_model_file = 'newModel.txt'
    delimiter = ','  
    old_model_dict = collections.defaultdict(str)
    
    
    value_pairs =  process_model(old_model_file)   
    
    for key, value in value_pairs: 
        old_model_dict[int(key)] = value

    value_pairs = process_model(new_model_file) 

    transition_matrix = TransitionMatrix(value_pairs)
    transition_matrix.create_transition_matrix()
        
        

        
    
    

    