def WtStrToOz(wt):
    if wt == "":
        return 0.0
    parts = wt.split("#")
    lb_str = parts[0].strip()
    oz_str = parts[1].strip()
    oz_result = (float(lb_str) * 16.0) + float(oz_str)
    return oz_result


COUNTRY_LOOKUPS = {
    "AUSTRALIA": "AU",
    "BRAZIL": "BR",
    "CANADA": "CA",
    "COLOMBIA": "CO",
    "CZECHIA": "CZ",
    "DENMARK": "DK",
    "FRANCE": "FR",
    "GERMANY": "DE",
    "MALTA": "MT",
    "NEW ZEALAND": "NZ",
    "PUERTO RICO": "US",
    "SINGAPORE": "SG",
    "UNITED KINGDOM": "GB",
    "UNITED STATES": "US",
    "US": "US",
    "USA": "US",
}


def country_iso2(c):
    c = c.upper()
    if c in COUNTRY_LOOKUPS:
        return COUNTRY_LOOKUPS[c]
    raise ValueError("Country Code '{}'".format(c))
