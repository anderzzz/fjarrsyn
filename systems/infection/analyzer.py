'''Analysis of sample files

'''
import sys
import os
import pandas as pd

AGENT_PREFIX = 'agent_sample'
GRAPH_PREFIX = 'graph_sample'
ENV_PREFIX = 'env_sample'

def get_files(root_path, file_prefix):

    uu = os.listdir(root_path)
    return [f for f in uu if file_prefix in f]

def get_sample_data(file_paths):

    container = []
    for f in file_paths:
        container.append(pd.read_csv(f))

    df_tmp = pd.concat(container).reset_index()
    df_ret = df_tmp.drop(labels=['index'], axis=1)

    return df_ret

def classify_agent(df):

    g_agent = df.groupby(['generation','agent_index'])
    for key, tt in g_agent:
        print (tt)
        raise RuntimeError
        for row in tt.iterrows():
            if 'essence' in row[1].loc['variable']:
                print (row[1])

def main(args):

    files_agent_sample = get_files(args[0], AGENT_PREFIX)

    df = get_sample_data(files_agent_sample)
    df = classify_agent(df)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
