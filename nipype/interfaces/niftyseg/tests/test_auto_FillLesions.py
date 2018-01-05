# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..lesions import FillLesions


def test_FillLesions_inputs():
    input_map = dict(args=dict(argstr='%s',
    ),
    bin_mask=dict(argstr='-mask %s',
    ),
    cwf=dict(argstr='-cwf %f',
    ),
    debug=dict(argstr='-debug',
    ),
    environ=dict(nohash=True,
    usedefault=True,
    ),
    ignore_exception=dict(deprecated='1.0.0',
    nohash=True,
    usedefault=True,
    ),
    in_dilation=dict(argstr='-dil %d',
    ),
    in_file=dict(argstr='-i %s',
    mandatory=True,
    position=1,
    ),
    lesion_mask=dict(argstr='-l %s',
    mandatory=True,
    position=2,
    ),
    match=dict(argstr='-match %f',
    ),
    other=dict(argstr='-other',
    ),
    out_datatype=dict(argstr='-odt %s',
    ),
    out_file=dict(argstr='-o %s',
    name_source=['in_file'],
    name_template='%s_lesions_filled.nii.gz',
    position=3,
    ),
    search=dict(argstr='-search %f',
    ),
    size=dict(argstr='-size %d',
    ),
    smooth=dict(argstr='-smo %f',
    ),
    terminal_output=dict(deprecated='1.0.0',
    nohash=True,
    ),
    use_2d=dict(argstr='-2D',
    ),
    verbose=dict(argstr='-v',
    ),
    )
    inputs = FillLesions.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value


def test_FillLesions_outputs():
    output_map = dict(out_file=dict(),
    )
    outputs = FillLesions.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
