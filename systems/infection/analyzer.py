'''Analysis of sample files

'''
import sys
import os
import pandas as pd

from core.helper_funcs import sigmoid_10

AGENT_PREFIX = 'agent_sample'
GRAPH_PREFIX = 'graph_sample'
ENV_PREFIX = 'env_sample'

def get_files(root_path, file_prefix):

    uu = os.listdir(root_path)
    return [root_path + '/' + f for f in uu if file_prefix in f]

def get_sample_data(file_paths):

    container = []
    for f in file_paths:
        container.append(pd.read_csv(f))

    df_tmp = pd.concat(container).reset_index()
    df_ret = df_tmp.drop(labels=['index'], axis=1)

    return df_ret

def classify_agent(df):

    def _pheno(x, p_type, shape, belief):
        max_val = x['value','essence:Exterior Disposition:max_' + p_type]
        mid_val = x['value','essence:Exterior Disposition:midpoint_' + p_type]
        return sigmoid_10(max_val, mid_val, shape, belief)

    df['value','pheno:share_friend'] = df.apply(_pheno, axis=1, 
                                   belief=1.0, shape=False, p_type='share')
    df['value','pheno:share_ufriend'] = df.apply(_pheno, axis=1, 
                                   belief=0.0, shape=False, p_type='share')
    df['value','pheno:gulp_friend'] = df.apply(_pheno, axis=1, 
                                   belief=1.0, shape=False, p_type='gulp')
    df['value','pheno:gulp_ufriend'] = df.apply(_pheno, axis=1, 
                                   belief=0.0, shape=False, p_type='gulp')
    df['value','pheno:tox_friend'] = df.apply(_pheno, axis=1, 
                                   belief=1.0, shape=True, p_type='tox')
    df['value','pheno:tox_ufriend'] = df.apply(_pheno, axis=1, 
                                   belief=0.0, shape=True, p_type='tox')

    return df

def main(args):

    files_agent_sample = get_files(args[0], AGENT_PREFIX)

    df = get_sample_data(files_agent_sample)
    df = df.set_index(['agent_index','generation','name','variable'])
    df = df.unstack()
    df = classify_agent(df)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
