WORKING MEMORY FROM HCP
-----------------------------
Preprocessing done by sfvn
(sfvn at dtu dot dk)
-----------------------------

Analysis and preprocessing of the working memory task from 100 subjects
taken from the human connectome project (HCP) [1]
(located at ssh-user@connectome-data). Subjects in the task are presented with images 
and are asked to press a button if it matches the image presented two instances back 
(2-back condition). Furthermore, they are asked in another experiment block 
to press when a target image is presented (0-back). Finally, there are periods of 
rest with no explicit task (fixation).

An independent compoenent analysis (ICA) has been run to extract 50 
spatially independent components using the nilearn python library (CanICA, [2]) . 
Preprocessing included spatial smoothing (FWHM 6 mm) and high-pass filtering 
at 0.008 Hz. ICA algorithm (fastICA) was restarted 10 times. Components were ranked
using the average temporal correlation. 

Furthermore, an atlas based on the Harvard-Oxford parcellation was extracted, 
also using spatial smoothing (FWHM 6 mm) and high-pass filtering at 0.008 Hz.

Data for further analysis is located in:
wm_ica_ts_d50_sorted.mat  		(time-courses, numpy-array 'X' with shape (n_subjects, n_timepoints, n_ica_comps))
wm_ica_components_d50.nii.gz	(spatial images) (visualized in the folder 'comps_imgs/*.png')
wm_ho_atlas_tc.mat				(time-courses, numpy-array 'X' with shape (n_subjects, n_timepoints, n_atlas_parcels)) 
wm_eventinfo.mat				(event information about the task)

--------------------
!!!! ICA INFO
NB! Component 2  (0-indexed) looks like a CSF-component  (respiatory effect)
SHOULD BE REMOVED
!!!!
---------------------

Python environment used is located at:
/dtu-compute/brainconnectivity/Data/miniconda3/envs/py36

can be activated by calling:
source /dtu-compute/brainconnectivity/Data/miniconda3/envs/py36/bin/activate

Scripts in this folder have been run in the following order:
./copySubjects.sh
python runICA.py
python plotEVs.py
python rankICAcomps.py
python extractAtlas.py


[1] Barch, D. M., Burgess, G. C., Harms, M. P., Petersen, S. E., Schlaggar, 
	B. L., Corbetta, M., ... WU-Minn HCP Consortium. (2013). 
	Function in the human connectome: task-fMRI and individual differences in behavior. 
	NeuroImage, 80, 169--189.

[2] Varoquaux, G., Sadaghiani, S., Pinel, P., Kleinschmidt, A., 
	Poline, J. B., & Thirion, B. (2010). 
	A group model for stable multi-subject ICA on fMRI datasets. 
	NeuroImage, 51(1), 288?299.
