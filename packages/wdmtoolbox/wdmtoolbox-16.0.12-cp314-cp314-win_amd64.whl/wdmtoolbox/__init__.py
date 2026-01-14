"""Package __init__.py."""


# start delvewheel patch
def _delvewheel_patch_1_11_2():
    import os
    if os.path.isdir(libs_dir := os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'wdmtoolbox.libs'))):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_11_2()
del _delvewheel_patch_1_11_2
# end delvewheel patch

__all__ = [
    "cleancopywdm",
    "copydsn",
    "copydsnlabel",
    "createnewdsn",
    "createnewwdm",
    "csvtowdm",
    "deletedsn",
    "describedsn",
    "extract",
    "hydhrseqtowdm",
    "listdsns",
    "renumberdsn",
    "setattrib",
    "stdtowdm",
    "wdmtoswmm5rdii",
]
from .wdmtoolbox import (
    cleancopywdm,
    copydsn,
    copydsnlabel,
    createnewdsn,
    createnewwdm,
    csvtowdm,
    deletedsn,
    describedsn,
    extract,
    hydhrseqtowdm,
    listdsns,
    renumberdsn,
    setattrib,
    stdtowdm,
    wdmtoswmm5rdii,
)
