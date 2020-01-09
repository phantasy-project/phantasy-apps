# -*- coding: utf-8 -*-

import csv
from collections import OrderedDict
from phantasy import Settings


def make_physics_settings(flat_settings, lat):
    """Generate Settings of *lat* from FlatSettings instance defined by
    *flat_settings*. For lattice settings, all settings are physics field
    settings.

    Parameters
    ----------
    flat_settings :
        FlatSettings instance from CSV settings file.
    lat : Lattice
        High-level lattice object.

    Returns
    -------
    r : Settings
        Physics settings.
    """
    s = Settings() # physics settings
    for name, field, sp, rd, last_sp in flat_settings:
        elem = lat[name]
        eng_fields = elem.get_eng_fields()
        phy_fields = elem.get_phy_fields()
        fld = elem.get_field(field)
        if name not in s:
            s[name] = OrderedDict()
        # generate PHY field from ENG field
        if fld.is_engineering_field():
            phy_field = phy_fields[eng_fields.index(field)]
            phy_sp = elem.convert(sp, field)
            phy_rd = elem.convert(rd, field)
            phy_last_sp = elem.convert(last_sp, field)
        else:
            phy_field = field
            phy_sp = sp
            phy_rd = rd
            phy_last_sp = last_sp
        s[name].update([(phy_field, phy_sp)])
    return s


class FlatSettings(list):
    """List of device settings, each list element is a tuple of device name,
    field name, field set value ,field value value and last field set value.
    """
    def __init__(self, settings_path=None, **kws):
        # settings_path is csv file path.
        super(FlatSettings, self).__init__()
        self.header = None
        if isinstance(settings_path, str):
            delimiter = kws.get('delimiter', ',')
            skipheader = kws.get('skipheader', True)
            self.read(settings_path, delimiter, skipheader)

    def read(self, path, delimiter=',', skipheader=True):
        """Read CSV file with the first line as header.
        """
        with open(path, 'r') as f:
            ss = csv.reader(f, delimiter=delimiter, skipinitialspace=True)
            if skipheader: self.header = next(ss)
            for name, field, sp, rd, last_sp in ss:
                self.append((name, field, float(sp), float(rd), float(last_sp)))

    def write(self, filepath, header=None, delimiter=','):
        """Write settings into *filepath*.
        """
        with open(filepath, 'w') as fp:
            ss = csv.writer(fp, delimiter=delimiter)
            if header is not None:
                ss.writerow(header)
            elif self.header is not None:
                ss.writerow(self.header)
            for name, field, sp, rd, old_sp in self:
                ss.writerow((name, field, sp, rd, old_sp))
