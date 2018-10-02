################
# Run ICA
################
from nilearn.decomposition import CanICA
import scipy.io as sio
import time

n_components = 50
#random_state = 12534646
subject_file = 'nifti_files.txt'

# Find file names
f = open(subject_file, 'r')
nifti_list = []
for line in f:
	nifti_list.append(line.rstrip())
f.close()

# movement regressors
## TBD!

# Initialize ICA object
canica = CanICA(n_components=n_components,
                memory="nilearn_cache", memory_level=2,
                threshold=None,
                n_init=10,
                verbose=1,
                mask_strategy='epi',
                smoothing_fwhm=6,
                detrend=True,
                high_pass=0.008,
                t_r=0.72)


## Run ICA
start = time.time()
print("RUNNING ICA")

canica.fit(nifti_list)

end = time.time()
print('Elapsed time %f' %(end - start))


# Save-stuff
canica.components_img_.to_filename('wm_ica_components_d%i.nii.gz'%(n_components))
canica.mask_img_.to_filename('wm_ica_mask.nii.gz') 

## Project all data into ICA space
print('Transforming data...')
start = time.time()
X = canica.transform(nifti_list)
end = time.time()
print('Elapsed time %f' %(end - start))

# Save 
result_dict = dict()
result_dict['X'] = X
result_dict['data_list'] = nifti_list
sio.savemat('wm_ica_ts_d%i'%(n_components), result_dict)
