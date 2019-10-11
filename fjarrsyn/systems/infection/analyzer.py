'''Analysis of sample files

'''
import sys
import os

import numpy as np
import pandas as pd

from fjarrsyn.core.helper_funcs import sigmoid_10

AGENT_PREFIX = 'agent_sample'
GRAPH_PREFIX = 'graph_sample'
ENV_PREFIX = 'env_sample'
PHENO_ARCHETYPES = {'ctp' : {'pheno:share' : 1.0, 
                             'pheno:gulp' : 1.0,
                             'pheno:tox' : 0.0},
                    'csp' : {'pheno:share' : 1.0,
                             'pheno:gulp' : 0.0,
                             'pheno:tox' : 0.0},
                    'ctw' : {'pheno:share' : 1.0,
                             'pheno:gulp' : 1.0,
                             'pheno:tox' : 1.0},
                    'csw' : {'pheno:share' : 1.0,
                             'pheno:gulp' : 0.0,
                             'pheno:tox' : 1.0},
                    'ntp' : {'pheno:share' : 0.0, 
                             'pheno:gulp' : 1.0,
                             'pheno:tox' : 0.0},
                    'nsp' : {'pheno:share' : 0.0,
                             'pheno:gulp' : 0.0,
                             'pheno:tox' : 0.0},
                    'ntw' : {'pheno:share' : 0.0,
                             'pheno:gulp' : 1.0,
                             'pheno:tox' : 1.0},
                    'nsw' : {'pheno:share' : 0.0,
                             'pheno:gulp' : 0.0,
                             'pheno:tox' : 1.0}}

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

def _clean_pheno(df):

    df_pheno = df.loc[:, df.columns.get_level_values(1).str.contains('pheno')]
    df_pheno_cols = df_pheno.columns.droplevel()
    df_pheno = pd.DataFrame(df_pheno.values, index=df_pheno.index, columns=df_pheno_cols)

    return df_pheno

def trender(df):

    df_pheno = _clean_pheno(df)
    gg = df_pheno.groupby('generation')
    d_qq = gg.quantile(q=[0.1,0.5,0.9])

    return d_qq

def grouper(df):

    df_pheno = _clean_pheno(df)
    index_tups = []
    data_cols = {}
    for row_id, data in df_pheno.iterrows():
        dd = data.to_dict()
        for env_type in ['friend', 'ufriend']:
            diff_2_min = None 
            for archetype, vals in PHENO_ARCHETYPES.items():
                diff_2 = 0.0
                for dim, clean_value in vals.items():
                    key = dim + '_' + env_type
                    diff_2 += (dd[key] - clean_value) * (dd[key] - clean_value)

                if diff_2_min is None or diff_2 < diff_2_min:
                    diff_2_min = diff_2
                    nearest_type = archetype

            x_type = data_cols.setdefault(env_type + '_type', [])
            x_dist = data_cols.setdefault(env_type + '_dist', [])
            x_type.append(nearest_type)
            x_dist.append(np.sqrt(diff_2_min))
            data_cols[env_type + '_type'] = x_type
            data_cols[env_type + '_dist'] = x_dist
        index_tups.append(row_id)

    return pd.DataFrame(data_cols, index=pd.MultiIndex.from_tuples(index_tups))

def main(args):

    files_agent_sample = get_files(args[0], AGENT_PREFIX)

    df = get_sample_data(files_agent_sample)
    df = df.set_index(['agent_index','generation','name','variable'])
    df = df.unstack()
    df = classify_agent(df)

    df_qq_trend = trender(df)
    df_agent_groups = grouper(df)
    df_agent_groups.to_csv('aaa.csv')

    idx = pd.IndexSlice
    for ii in args[1:]:
        df = df_agent_groups.loc[idx[:, int(ii), :], :]
        print (df.groupby(['friend_type', 'ufriend_type']).count())

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
