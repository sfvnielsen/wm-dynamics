

from nilearn import datasets
from nilearn.input_data import NiftiLabelsMasker
import scipy.io as sio
import nilearn.plotting as niplot
from nilearn.image import index_img, new_img_like
import nibabel as nib
import matplotlib.pyplot as plt

# init
out = 'wm'
subject_file = 'nifti_files.txt'

# Find file names
f = open(subject_file, 'r')
nifti_list = []
for line in f:
	nifti_list.append(line.rstrip())
f.close()


# Fetch atlas
dataset = datasets.fetch_atlas_harvard_oxford('cort-maxprob-thr25-1mm') # resolution 1 mm, and grey-matter probability set at 25%
atlas_filename = dataset.maps
labels = dataset.labels

print('Number of regions: %i'%(len(labels)))

# Create masker
masker = NiftiLabelsMasker(labels_img=atlas_filename, standardize=True,
                           memory='nilearn_cache', verbose=5, 
                           smoothing_fwhm=6, t_r=0.72, high_pass=0.008,
                           detrend=True)


# Extract time-series
X = []
for nif in nifti_list:
	X.append(masker.fit_transform(nif))

X = np.array(X)

# Plot components
atlas = nib.load(atlas_filename)
for i in range(len(labels):
	niplot.plot_roi( newatlas.get_data()==i, 
	title = 'parcel %i - %s'%(i,labels[i]),
	cut_coords=1, display_mode='z')
	plt.savefig('atlas_imgs/ho_parcel%i.png'%(i), dpi=600)
	plt.close()

# Save stuff
del labels[masker.background_label]
result_dict = dict()
result_dict['X'] = X
result_dict['labels'] = labels
result_dict['data_list'] = nifti_list
sio.savemat('%s_ho_atlas_tc'%(out), result_dict)

