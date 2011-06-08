import nipype.interfaces.io as nio           # Data i/o
import nipype.interfaces.spm as spm          # spm
import nipype.interfaces.freesurfer as fs    # freesurfer
import nipype.interfaces.nipy as nipy
import nipype.interfaces.utility as util
import nipype.pipeline.engine as pe          # pypeline engine
import nipype.algorithms.modelgen as model   # model specification
import nipype.workflows.fsl as fsl_wf
from nipype.interfaces.base import Bunch
import os                                    # system functions


"""In the following section, to showcase NiPyPe, we will describe how to create 
and extend a typical fMRI processing pipeline. We will begin with a basic 
processing layout and follow with extending it by adding/exchanging different 
components.

Most fMRI pipeline can be divided into two sections - preprocessing and 
modelling. First one deals with cleaning data from confounds and noise and the 
second one fits a model based on the experimental design. Preprocessing stage 
in our first iteration of a pipeline will consist of only two steps: 
realignment and smoothing. In NiPyPe Every processing step consist of an 
Interface (which defines how to execute corresponding software) encapsulated 
in a Node (which defines for example a unique name). For realignment (motion 
correction achieved by coregistering all volumes to the mean) and smoothing 
(convolution with 3D Gaussian kernel) we will use SPM implementation. 
Definition of appropriate nodes can be found in Listing 1 (TODO). Inputs 
(such as register_to_mean from listing 1) of nodes are accessible through the 
inputs property. Upon setting any input its type is verified to avoid errors 
during the execution."""

preprocessing = pe.Workflow(name="preprocessing")

iter_fwhm = pe.Node(interface=util.IdentityInterface(fields=["fwhm"]), 
                    name="iter_fwhm")
iter_fwhm.iterables = [('fwhm', [4, 8])]

iter_smoothing_method = pe.Node(interface=util.IdentityInterface(fields=["smoothing_method"]), 
                    name="iter_smoothing_method")
iter_smoothing_method.iterables = [('smoothing_method',['isotropic_voxel', 
                                           'anisotropic_voxel', 
                                           'isotropic_surface'])]

realign = pe.Node(interface=spm.Realign(), name="realign")
realign.inputs.register_to_mean = True

isotropic_voxel_smooth = pe.Node(interface=spm.Smooth(), name="isotropic_voxel_smooth")
preprocessing.connect(realign, "realigned_files", isotropic_voxel_smooth, "in_files")
preprocessing.connect(iter_fwhm, "fwhm", isotropic_voxel_smooth, "fwhm")

compute_mask = pe.Node(interface=nipy.ComputeMask(), name="compute_mask")
preprocessing.connect(realign, "mean_image", compute_mask, "mean_volume")

anisotropic_voxel_smooth = fsl_wf.create_susan_smooth(name="anisotropic_voxel_smooth", 
                                                      separate_masks=False)
preprocessing.connect(realign, "realigned_files", anisotropic_voxel_smooth, "inputnode.in_files")
preprocessing.connect(iter_fwhm, "fwhm", anisotropic_voxel_smooth, "inputnode.fwhm")
preprocessing.connect(compute_mask, "brain_mask", anisotropic_voxel_smooth, 'inputnode.mask_file')


recon_all = pe.Node(interface=fs.ReconAll(), name = "recon_all")

surfregister = pe.Node(interface=fs.BBRegister(),name='surfregister')
surfregister.inputs.init = 'fsl'
surfregister.inputs.contrast_type = 't2'
preprocessing.connect(realign, 'mean_image', surfregister, 'source_file')
preprocessing.connect(recon_all, 'subject_id', surfregister, 'subject_id')
preprocessing.connect(recon_all, 'subjects_dir', surfregister, 'subjects_dir')

isotropic_surface_smooth = pe.MapNode(interface=fs.Smooth(proj_frac_avg=(0,1,0.1)),
                                      iterfield=['in_file'],
                                      name="isotropic_surface_smooth")
preprocessing.connect(surfregister, 'out_reg_file', isotropic_surface_smooth, 'reg_file')
preprocessing.connect(realign, "realigned_files", isotropic_surface_smooth, "in_file")
preprocessing.connect(iter_fwhm, "fwhm", isotropic_surface_smooth, "surface_fwhm")
preprocessing.connect(iter_fwhm, "fwhm", isotropic_surface_smooth, "vol_fwhm")
preprocessing.connect(recon_all, 'subjects_dir', isotropic_surface_smooth, 'subjects_dir')

merge_smoothed_files = pe.Node(interface=util.Merge(3),
                               name='merge_smoothed_files')
preprocessing.connect(isotropic_voxel_smooth, 'smoothed_files', merge_smoothed_files, 'in1')
preprocessing.connect(anisotropic_voxel_smooth, 'outputnode.smoothed_files', merge_smoothed_files, 'in2')
preprocessing.connect(isotropic_surface_smooth, 'smoothed_file', merge_smoothed_files, 'in3')
        
select_smoothed_files = pe.Node(interface=util.Select(), name="select_smoothed_files")
preprocessing.connect(merge_smoothed_files, 'out', select_smoothed_files, 'inlist')
        
def chooseindex(roi):
    return {'isotropic_voxel':0, 'anisotropic_voxel':1, 'isotropic_surface':2}[roi]
        
preprocessing.connect(iter_smoothing_method, ("smoothing_method", chooseindex), select_smoothed_files, 'index')

"""Creating a modelling workflow which will define the design, estimate model and 
contrasts follows the same suite. We will again use SPM implementations. 
NiPyPe, however, adds extra abstraction layer to model definition which allows 
using the same definition for many model estimation implemantations (for 
example one from FSL or nippy). Therefore we will need four nodes: 
SpecifyModel (NiPyPe specific abstraction layer), Level1Design (SPM design 
definition), ModelEstimate, and ContrastEstimate. The connected modelling 
Workflow can be seen on Figure TODO. Model specification supports block, event 
and sparse designs. Contrasts provided to ContrastEstimate are defined using 
the same names of regressors as defined in the SpecifyModel."""

specify_model = pe.Node(interface=model.SpecifyModel(), name="specify_model")
specify_model.inputs.input_units             = 'secs'
specify_model.inputs.time_repetition         = 3.
specify_model.inputs.high_pass_filter_cutoff = 120
specify_model.inputs.subject_info = [Bunch(conditions=['Task-Odd','Task-Even'],
                                           onsets=[range(15,240,60),range(45,240,60)],
                                           durations=[[15], [15]])]*4

level1design = pe.Node(interface=spm.Level1Design(), name= "level1design")
level1design.inputs.bases = {'hrf':{'derivs': [0,0]}}
level1design.inputs.timing_units = 'secs'
level1design.inputs.interscan_interval = specify_model.inputs.time_repetition

level1estimate = pe.Node(interface=spm.EstimateModel(), name="level1estimate")
level1estimate.inputs.estimation_method = {'Classical' : 1}

contrastestimate = pe.Node(interface = spm.EstimateContrast(), name="contrastestimate")
contrastestimate.inputs.contrasts = [('Task>Baseline','T', ['Task-Odd','Task-Even'],[0.5,0.5])]

modelling = pe.Workflow(name="modelling")
modelling.connect(specify_model, 'session_info', level1design, 'session_info')
modelling.connect(level1design, 'spm_mat_file', level1estimate, 'spm_mat_file')
modelling.connect(level1estimate,'spm_mat_file', contrastestimate,'spm_mat_file')
modelling.connect(level1estimate,'beta_images', contrastestimate,'beta_images')
modelling.connect(level1estimate,'residual_image', contrastestimate,'residual_image')

"""Having preprocessing and modelling workflows we need to connect them together, 
add data grabbing facility and save the results. For this we will create a 
master Workflow which will host preprocessing and model Workflows as well as 
DataGrabber and DataSink Nodes. NiPyPe allows connecting Nodes between 
Workflows. We will use this feature to connect realignment_parameters and 
smoothed_files to modelling workflow."""

main_workflow = pe.Workflow(name="main_workflow")
main_workflow.base_dir = "smoothing_comparison_workflow"
main_workflow.connect(preprocessing, "realign.realignment_parameters", 
                      modelling, "specify_model.realignment_parameters")
main_workflow.connect(preprocessing, "select_smoothed_files.out", 
                      modelling, "specify_model.functional_runs")


"""DataGrabber allows to define flexible search patterns which can be 
parameterized by user defined inputs (such as subject ID, session etc.). 
This allows to adapt to a wide range of file layouts. In our case we will 
parameterize it with subject ID. In this way we will be able to run it for 
different subjects. We can automate this by iterating over a list of subject 
Ids, by setting an iterables property on the subject_id input of DataGrabber. 
Its output will be connected to realignment node from preprocessing workflow."""

datasource = pe.Node(interface=nio.DataGrabber(infields=['subject_id'],
                                               outfields=['func', 'struct']),
                     name = 'datasource')
datasource.inputs.base_directory = os.path.abspath('data')
datasource.inputs.template = '%s/%s.nii'
datasource.inputs.template_args = info = dict(func=[['subject_id', ['f3','f5','f7','f10']]],
                                              struct=[['subject_id','struct']])
datasource.inputs.subject_id = 's1'

main_workflow.connect(datasource, 'func', preprocessing, 'realign.in_files')
main_workflow.connect(datasource, 'struct', preprocessing, 'recon_all.T1_files')

"""DataSink on the other side provides means to storing selected results to a 
specified location. It supports automatic creation of folder stricter and 
regular expression based substitutions. In this example we will store T maps."""

datasink = pe.Node(interface=nio.DataSink(), name="datasink")
datasink.inputs.base_directory = os.path.abspath('workflow_from_scratch/output')

main_workflow.connect(modelling, 'contrastestimate.spmT_images', datasink, 'contrasts.@T')

main_workflow.run()
main_workflow.write_graph()
