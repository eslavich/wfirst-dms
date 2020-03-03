#!/usr/bin/env python3
"""
Adjust a WFIRST example dark to make it suitable to open as a jwst datamodel.
In addition to these changes, we also need to add the WFI instrument enum value
and H4RG detector enum value to the datamodels core schema.
"""
import sys

from astropy.io import fits

infile = sys.argv[1]
outfile = sys.argv[2]

hdul = fits.open(infile)

# The cal code expects 4D data in a separate HDU
sci_shape = (1,) + hdul[0].data.shape
sci_data = hdul[0].data.reshape(sci_shape)
sci_hdu = fits.ImageHDU(sci_data, name="SCI")
hdul.append(sci_hdu)
hdul[0].data = None

hdul[0].header["DATAMODL"] = "RampModel"
hdul[0].header["GRATING"] = "UNKNOWN"
hdul[0].header["DATE-OBS"] = "2025-06-01"
hdul[0].header["FILTER"] = "CLEAR"
hdul[0].header["SUBARRAY"] = "FULL"
hdul[0].header["INSTRUME"] = "WFI"

# DATE-END is set to an invalid value (an integer) per the datamodels core
# schema.
del hdul[0].header["DATE-END"]

# At time of writing, there was a discrepancy of ~ 900 bytes between the expected
# and actual file sizes.  Rewriting the file sets the sizes correctly.
# These header values are invalid but can be fixed by the verifier:
# DETECTOR, DEWAR, DIODE_SN, DLL_VER, DSP_TIME, DSP_VRSN, DWRFILT, ELECBOX,
# EXPTYPE, E_GAIN, GRATING, OBSERVER, ORG, PROJECT, ROOTNAME, SOURCE, SUBARRAY,
# TESTNAME, TIMINGBD, TOOL_VER, VENDOR
hdul.writeto(outfile, overwrite=True, output_verify="fix")
