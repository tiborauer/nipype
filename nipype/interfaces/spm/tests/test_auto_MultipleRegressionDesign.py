# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..model import MultipleRegressionDesign


def test_MultipleRegressionDesign_inputs():
    input_map = dict(covariates=dict(field='cov',
    ),
    explicit_mask_file=dict(field='masking.em',
    ),
    global_calc_mean=dict(field='globalc.g_mean',
    xor=['global_calc_omit', 'global_calc_values'],
    ),
    global_calc_omit=dict(field='globalc.g_omit',
    xor=['global_calc_mean', 'global_calc_values'],
    ),
    global_calc_values=dict(field='globalc.g_user.global_uval',
    xor=['global_calc_mean', 'global_calc_omit'],
    ),
    global_normalization=dict(field='globalm.glonorm',
    ),
    ignore_exception=dict(deprecated='1.0.0',
    nohash=True,
    usedefault=True,
    ),
    in_files=dict(field='des.mreg.scans',
    mandatory=True,
    ),
    include_intercept=dict(field='des.mreg.incint',
    usedefault=True,
    ),
    matlab_cmd=dict(),
    mfile=dict(usedefault=True,
    ),
    no_grand_mean_scaling=dict(field='globalm.gmsca.gmsca_no',
    ),
    paths=dict(),
    spm_mat_dir=dict(field='dir',
    ),
    threshold_mask_absolute=dict(field='masking.tm.tma.athresh',
    xor=['threshold_mask_none', 'threshold_mask_relative'],
    ),
    threshold_mask_none=dict(field='masking.tm.tm_none',
    xor=['threshold_mask_absolute', 'threshold_mask_relative'],
    ),
    threshold_mask_relative=dict(field='masking.tm.tmr.rthresh',
    xor=['threshold_mask_absolute', 'threshold_mask_none'],
    ),
    use_implicit_threshold=dict(field='masking.im',
    ),
    use_mcr=dict(),
    use_v8struct=dict(min_ver='8',
    usedefault=True,
    ),
    user_covariates=dict(field='des.mreg.mcov',
    ),
    )
    inputs = MultipleRegressionDesign.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value


def test_MultipleRegressionDesign_outputs():
    output_map = dict(spm_mat_file=dict(),
    )
    outputs = MultipleRegressionDesign.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
