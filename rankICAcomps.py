###############
# Rank ICA components for importance
# ... average temporal-correlation over subjects
###############

import scipy.io as sio
import numpy as np
from nilearn import plotting as niplot
import nibabel as nib
from nilearn.image import iter_img, index_img
import matplotlib.pyplot as plt
from scipy.stats import zscore

ic_tc_file = 'wm_ica_ts_d50.mat' 
ic_comp_file = 'wm_ica_components_d50.nii.gz'
ic_tc_output = 'wm_ica_ts_d50_sorted.mat' 
ic_comp_plot_sorted_pat = 'comp_imgs/wm_ica_components_d50_sorted_c%02i.png'
pct_threshold=95

# IC time courses
load_dict = sio.loadmat(ic_tc_file)

# Load data tensor
(n_subs, n_tpts, n_ics) = load_dict['X'].shape

# Calc temporal corrleation for each ic and pair of subjects
corr_t = np.empty( ( int(n_subs*(n_subs-1)/2), n_ics))
for i in range(n_ics):
	print('Running on IC %i'%i)
	n=0
	for n1 in range(n_subs):
		for n2 in range(n1+1,n_subs):
			corr_t[n, i] = np.corrcoef(load_dict['X'][n1,:,i], load_dict['X'][n2,:,i] )[0,1]
			n+=1

# Calc mean correlation over subject pairs and sort
mean_corr = np.mean(corr_t,axis=0)
sorting = np.argsort(mean_corr)[::-1]
mean_corr = mean_corr[sorting]


# Load ica components, sort and plot, together with score
ica_nif = nib.load(ic_comp_file)
for i,i_sort in enumerate(sorting):
	absvalues = np.abs(index_img(ica_nif,i_sort).get_data().ravel())
	absvals_nonan = [val for val in absvalues if not np.isnan(val)]
	thresh = np.percentile(absvals_nonan, pct_threshold)
	
	niplot.plot_stat_map( index_img(ica_nif,i_sort), 
	title = 'IC %i, avg_corr %.3f'%(i,mean_corr[i]),
	cut_coords=1, display_mode='z', threshold=thresh)
	plt.savefig(ic_comp_plot_sorted_pat%(i), dpi=600)
	print('IC%i, SortedIC%i, AvgCorr%.3f'%(i,i_sort,mean_corr[i]))
	plt.close()

# Sort tc data and save to new file (zscore each time-series)
result_dict = load_dict
result_dict['X'] = zscore(load_dict['X'][:,:,sorting], axis=1)
result_dict['ic_mean_tcorr'] = mean_corr
sio.savemat(ic_tc_output, result_dict)
