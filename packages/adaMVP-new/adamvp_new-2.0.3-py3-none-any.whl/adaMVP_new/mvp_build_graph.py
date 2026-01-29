import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
### MVP functions
from adaMVP_new import adj_mat_interactome as ami
from adaMVP_new import sig_first_neighbors as sfn
from adaMVP_new import graphical_models as gms
from adaMVP_new import markov_model_dataframe as mmd # degree of genes in the graph

def compute_TM(gm_core,p_p1,Wm = 0.5, alpha = 0.1):
    tm = gm_core.copy()
    p_p = np.array(p_p1)
    
    # min-max scale
    den = (p_p.max() - p_p.min())
    p_p = Wm * ((p_p - p_p.min()) / den) if den > 0 else np.zeros_like(p_p)
    
    ### set transition matrix
    for i in range(len(tm)):
        ind = np.where(tm.iloc[i,]==1)[0].tolist()
        N = len(ind)
    
        # If no neighbors, make it a self-loop (or uniform row)
        if N == 0:
            tm.iloc[i, :] = 0.0
            tm.iloc[i, i] = 1.0
            continue
    
        self_loop = p_p[ind]
        
        b = (1-p_p[i]-np.sum(self_loop)*alpha)/N
        weight = b+np.array(self_loop)*alpha
    
        tm.iloc[i, :] = 0.0  # clear row before setting weights
        tm.iloc[i, i] = p_p[i]
        tm.iloc[i,ind] = weight
    # if (tm<0).sum().sum()>0: # if there is any negative elements
    #     print('there is negative elements in the transition matrix!')
    
     # clip any remaining negatives
    tm = tm.clip(lower=0.0)
    
    TM = tm.to_numpy()
    row_sums = TM.sum(axis=1, keepdims=True)
    tm = tm / row_sums
    
    return tm

def find_fn_and_calculate_score(altered_freq_file,
            save_directory = '.',
            to_remove = [],
            thre = 0.05,n_perm = 10000):
    """
    Find first neighbors for each cancer type by permutation test
    Calculate the score for each first neighbor based on the average initial score of its neighbors in the seed
    """
    df = pd.read_csv(altered_freq_file)
    gm = ami.adj_mat()
    g_score = df.copy()
    g_score = g_score.loc[~g_score.Gene.isin(to_remove),]
    g_seed = g_score.Gene.values.tolist()
    fn = sfn.find_fn(g_seed,gm,n_perm)
    g_score.index = g_score['Gene']

    fn1 = fn.loc[fn.fdr_bh<thre,].copy()
    fn1.reset_index(drop = True, inplace = True)
    sum_initial_seed = []
    average_initial_seed = []
    for i in range(fn1.shape[0]):
        gene = fn1.loc[i,'candidate_gene']
        tmp1 = gm.index[gm.loc[gene,:]>0].tolist() # neighbors of a candidate first neighbor
        overlap = set(tmp1).intersection(g_seed)
        tmp2 = g_score.loc[list(overlap),'Freq'].sum()
        sum_initial_seed.append(tmp2)
        average_initial_seed.append(tmp2/len(overlap))
    fn1['sum_initial_score_of_neighbor_in_seed'] = sum_initial_seed
    fn1['avg_initial_score_of_neighbor_in_seed'] = average_initial_seed
    fnm1 = os.path.join(save_directory,f"first_neighbors_detected.csv")
    fn1.to_csv(fnm1,index = False)

def build_pgm(altered_freq_file,
            first_neighbor_file,
            save_directory = '.',
            to_remove = [],
            save_transition_mat = True,
            fn_num = 550,thre = 0.05,Wm = 0.5,alpha = 0.1):
    """
    Load the seed genes and altered freq, together with the first neighbors detected by the 'find_fn_and_calculate_score' function
    Run the Markov Chain model
    """
    df = pd.read_csv(altered_freq_file)
    g_score = df.copy()
    g_score = g_score.loc[~g_score.Gene.isin(to_remove),]
    g_seed = g_score.Gene.values.tolist()
    g_score.index = g_score['Gene']
    genex = g_seed[0]
    gm = ami.adj_mat()

   # first neighbors
    fn1 = pd.read_csv(first_neighbor_file)
    fn1 = fn1.sort_values(by = ['fdr_bh','neighbors_in_seed_divide_by_seed_size'],ascending = [True, False])
    fn1 = fn1.sort_values(by = ['avg_initial_score_of_neighbor_in_seed'],ascending = [False])
    fn1 = fn1.loc[fn1.fdr_bh<thre,]
    fn1 = fn1.iloc[:fn_num,]
    
    cb = set(g_seed).union(fn1.candidate_gene.values) # combine seed with first neighbors
    ### save the gene list, specify seed or not
    in_seed = []
    cb = list(cb)
    for j in cb:
        if j in g_seed:
            in_seed.append(1)
        else:
            in_seed.append(0)
    g_df = pd.DataFrame({'gene':cb,'in_seed':in_seed})
    ### load the genelist
    g_all = g_df['gene'].values
    g_filter = set(g_all).intersection(gm.index)

    # get the number of altered patients of the seed list (patient count that altered)
    score_ini = {}
    for j in g_filter:
        if j in g_score.Gene.values:
            score_ini[j] = g_score.loc[j,'Freq']
    s_list = g_filter

    ### run the pgm model
    print('---------------------------------------------')
    print(f'fn:{fn_num},Wm:{Wm},alpha:{alpha}')
    final_prob_markov0 = gms.run_pipeline_unequal(gm,genex,s_list,score_ini,alpha,Wm,modelx='Markov')
    final_prob_markov = mmd.info_markov(final_prob_markov0,s_list,gm)
    source = []
    for i in final_prob_markov.genes.values:
        if i not in g_score.index:
            source.append('first neighbor')
        else:
            source.append('seed')
    final_prob_markov['source'] = source        
    ## save final rank and probability
    filenm = os.path.join(save_directory,f"markov_output_Wm_{str(Wm)}_alpha_{str(alpha)}.csv")
    final_prob_markov.to_csv(filenm, index = False)
    if save_transition_mat:
        genes = final_prob_markov['genes'].values.tolist()
        p_p1 = final_prob_markov['initial_score'].values.tolist()
        gm_core = gm.loc[genes,genes]
        tm = compute_TM(gm_core,p_p1, Wm = Wm, alpha = alpha)
        # save transition matrix
        filenm = os.path.join(save_directory,f"transition_matrix.csv")
        tm.to_csv(filenm)


def find_fn_and_pgm(altered_freq_file,
            save_directory = '.',
            to_remove = [],
            save_transition_mat = True,
            fn_num = 550,thre = 0.05,Wm = 0.5,alpha = 0.1,n_perm = 10000):
    """
    Find first neighbors for each cancer type by permutation test
    Calculate the score for each first neighbor based on the average initial score of its neighbors in the seed
    Run the Markov Chain model
    """
    df = pd.read_csv(altered_freq_file)
    df = df.loc[~df.Gene.isin(to_remove),]
    genelist = df.Gene.values.tolist()
    gm = ami.adj_mat()
    fn = sfn.find_fn(genelist,gm,n_perm)
    g_score = df.copy()
    g_score = g_score.loc[~g_score.Gene.isin(to_remove),]
    g_seed = g_score.Gene.values.tolist()
    g_score.index = g_score['Gene']
    genex = g_seed[0]

    fn1 = fn.loc[fn.fdr_bh<thre,].copy()
    fn1.reset_index(drop = True, inplace = True)
    sum_initial_seed = []
    average_initial_seed = []
    for i in range(fn1.shape[0]):
        gene = fn1.loc[i,'candidate_gene']
        tmp1 = gm.index[gm.loc[gene,:]>0].tolist() # neighbors of a candidate first neighbor
        overlap = set(tmp1).intersection(g_seed)
        tmp2 = g_score.loc[list(overlap),'Freq'].sum()
        sum_initial_seed.append(tmp2)
        average_initial_seed.append(tmp2/len(overlap))
    fn1['sum_initial_score_of_neighbor_in_seed'] = sum_initial_seed
    fn1['avg_initial_score_of_neighbor_in_seed'] = average_initial_seed
    fnm1 = os.path.join(save_directory,f"first_neighbors_detected.csv")
    fn1.to_csv(fnm1,index = False)

    # first neighbors
    fn1 = fn1.sort_values(by = ['fdr_bh','neighbors_in_seed_divide_by_seed_size'],ascending = [True, False])
    fn1 = fn1.sort_values(by = ['avg_initial_score_of_neighbor_in_seed'],ascending = [False])
    fn1 = fn1.iloc[:fn_num,]
    
    cb = set(g_seed).union(fn1.candidate_gene.values) # combine seed with first neighbors
    ### save the gene list, specify seed or not
    in_seed = []
    cb = list(cb)
    for j in cb:
        if j in g_seed:
            in_seed.append(1)
        else:
            in_seed.append(0)
    g_df = pd.DataFrame({'gene':cb,'in_seed':in_seed})
    ### load the genelist
    tmp = g_df.loc[g_df.in_seed==0,'gene'].values
    g_all = g_df['gene'].values
    g_filter = set(g_all).intersection(gm.index)

    # get the number of altered patients of the seed list (patient count that altered)
    score_ini = {}
    for j in g_filter:
        if j in g_score.Gene.values:
            score_ini[j] = g_score.loc[j,'Freq']
    s_list = g_filter

    ### run the pgm model
    print('---------------------------------------------')
    print(f'fn:{fn_num},Wm:{Wm},alpha:{alpha}')
    final_prob_markov0 = gms.run_pipeline_unequal(gm,genex,s_list,score_ini,alpha,Wm,modelx='Markov')
    final_prob_markov = mmd.info_markov(final_prob_markov0,s_list,gm)
    source = []
    for i in final_prob_markov.genes.values:
        if i not in g_score.index:
            source.append('first neighbor')
        else:
            source.append('seed')
    final_prob_markov['source'] = source        
    ## save final rank and probability
    filenm = os.path.join(save_directory,f"markov_output_Wm_{str(Wm)}_alpha_{str(alpha)}.csv")
    final_prob_markov.to_csv(filenm, index = False)
    if save_transition_mat:
        genes = final_prob_markov['genes'].values.tolist()
        p_p1 = final_prob_markov['initial_score'].values.tolist()
        gm_core = gm.loc[genes,genes]
        tm = compute_TM(gm_core,p_p1, Wm = Wm, alpha = alpha)
        # save transition matrix
        filenm = os.path.join(save_directory,f"transition_matrix.csv")
        tm.to_csv(filenm)
