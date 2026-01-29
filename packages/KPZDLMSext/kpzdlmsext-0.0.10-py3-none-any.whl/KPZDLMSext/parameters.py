from DLMS_SPODES.cosem_interface_classes import parameters as prs


CALIBRATE = prs.Register.parse("128.0.0.0.0.255")
FIRMWARE_DESCRIPTOR = prs.Register.parse("0.0.128.100.0.255")
AFE_OFFSETS = prs.Data.parse("0.128.96.2.2.255")
