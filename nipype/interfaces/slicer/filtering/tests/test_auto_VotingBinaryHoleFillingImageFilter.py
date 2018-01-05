# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..votingbinaryholefillingimagefilter import VotingBinaryHoleFillingImageFilter


def test_VotingBinaryHoleFillingImageFilter_inputs():
    input_map = dict(args=dict(argstr='%s',
    ),
    background=dict(argstr='--background %d',
    ),
    environ=dict(nohash=True,
    usedefault=True,
    ),
    foreground=dict(argstr='--foreground %d',
    ),
    ignore_exception=dict(deprecated='1.0.0',
    nohash=True,
    usedefault=True,
    ),
    inputVolume=dict(argstr='%s',
    position=-2,
    ),
    majorityThreshold=dict(argstr='--majorityThreshold %d',
    ),
    outputVolume=dict(argstr='%s',
    hash_files=False,
    position=-1,
    ),
    radius=dict(argstr='--radius %s',
    sep=',',
    ),
    terminal_output=dict(deprecated='1.0.0',
    nohash=True,
    ),
    )
    inputs = VotingBinaryHoleFillingImageFilter.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value


def test_VotingBinaryHoleFillingImageFilter_outputs():
    output_map = dict(outputVolume=dict(position=-1,
    ),
    )
    outputs = VotingBinaryHoleFillingImageFilter.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
