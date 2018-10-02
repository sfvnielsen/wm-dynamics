###################
# Plot EV's for each subject
# ... and save info
###################

import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import scipy.io as sio

subject_file = 'nifti_files.txt'
tasks = ['tfMRI_WM_LR', 'tfMRI_WM_RL']
TR = 0.72 # in secs

ev_txtfiles = ['EVs/0bk_body.txt',  #BLOCKED onset of 0Back body block condition
		  'EVs/0bk_faces.txt',  #BLOCKED onset of 0Back faces block condition
		'EVs/0bk_places.txt', #BLOCKED onset of 0Back places block condition
		'EVs/0bk_tools.txt', #BLOCKED onset of 0Back tools block condition
		'EVs/2bk_body.txt', #BLOCKED onset of 2Back body block condition
		'EVs/2bk_faces.txt', #BLOCKED onset of 2Back faces block condition
		'EVs/2bk_places.txt', #BLOCKED onset of 2Back places block condition
		'EVs/2bk_tools.txt'] #BLOCKED onset of 2Back tools block condition

ev_labels = [1,1,1,1, 2,2,2,2]
labels = ['Fixation', '0-back', '2-back']
event_vectors_all = []

# Extract list of directories containing data for analyis
f = open(subject_file, 'r')
dir_list = []
nifti_list = []
for line in f:
	fl = line.rstrip().split('/')
	nifti_list.append(fl[-1])
	dir_list.append('/'.join(fl[0:-1]) )
f.close()

# loop over dir list
for d,di in enumerate(dir_list):	
	# Touch nifti to see number of volumes
	nif = nib.load('%s/%s'%(di,nifti_list[d]))
	nvols=nif.header.get_data_shape()[-1]
	
	event_vector = np.zeros( (nvols,1))
	
	# loop over eventfiles
	for e, ef in enumerate(ev_txtfiles):
		# open event file
		x = np.loadtxt('%s/%s'%(di, ef))
		
		# extract onset and duration (first two entries)
		# fill event label into event_vector
		onset = int(np.round(x[0]/TR))
		stim_length = int(np.round(x[1]/TR))
		event_vector[ (onset-1):(onset+stim_length) ] = ev_labels[e]
	
	## Append to events
	event_vectors_all.append(event_vector)

E = np.array(event_vectors_all).squeeze()

fig, (ax1,ax2) = plt.subplots(1,2)
im1=ax1.imshow(E[0:-1:2], cmap='Paired')
im2=ax2.imshow(E[1:-1:2], cmap='Paired')
ax1.set_title(tasks[0])
ax2.set_title(tasks[1])
#plt.colorbar(im1, cax=ax3)
fig.show()

plt.savefig('wm_eventlog.png', dpi=300)

result_dict = dict()
result_dict['dir_list'] = dir_list
result_dict['event_info'] = event_vectors_all
result_dict['event_labels'] = labels
sio.savemat('wm_eventinfo',result_dict)
