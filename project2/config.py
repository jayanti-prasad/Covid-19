import sys
import os

class Config:
    def __init__(self, cfg_parser):
        self.cfg_parser = cfg_parser

    def workspace_dir(self):
        tmp_dir = self.cfg_parser.get('input', 'workspace_dir')
        os.makedirs(tmp_dir, exist_ok=True)
        return tmp_dir 

    def output_dir(self):
        prefix=self.cfg_parser.get('models', 'prefix')
        sub_dir = prefix+"_" +self.epd_model() + "_" + self.beta_model() 
        tmp_dir = self.workspace_dir() + os.sep + sub_dir   
        os.makedirs(tmp_dir, exist_ok=True)
        return tmp_dir 


    def input_file(self):
        return self.cfg_parser.get('input', 'input_file')

    def plot_data(self):
        return self.cfg_parser.getboolean('input', 'plot_data')

    def lockdown_file(self):
        return self.cfg_parser.get('input', 'lockdown_file')

    def num_countries(self):
        return  self.cfg_parser.getint('input', 'num_countries')

    def num_days_predict(self):
        return  self.cfg_parser.getint('input', 'num_days_predict')

    def num_min_infect(self):
        return  self.cfg_parser.getint('input', 'num_min_infect')

    def population_file(self):
        return self.cfg_parser.get('input', 'population_file')
    
    def epd_model(self):
        return self.cfg_parser.get('models', 'epd_model')

    def beta_model(self):
        return self.cfg_parser.get('models', 'beta_model')

    def model(self):
        return self.epd_model()+"-"+self.beta_model() 

    def starting_point(self):
        return eval(self.cfg_parser.get(self.model(), 'starting_point'))

    def bounds(self):
        return eval(self.cfg_parser.get(self.model(), 'bounds'))

    def columns(self):
        return eval(self.cfg_parser.get(self.epd_model(), 'columns'))



