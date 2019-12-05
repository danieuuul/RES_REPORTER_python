import numpy as np
from functools import lru_cache

@lru_cache(maxsize=512)     
def get_dimensionality(general, prop):
    """Get dimensionality of property from General/NameRecordTable on loaded SR3 file 

    Arguments:
        prop {str} -- Property 

    Returns:
        [(int, int)] -- Dimensionalities of Numerator and Denominator of property unit
    """

    if prop not in general.nameRecordTable.Keyword.values:
        return None, None

    dims = general.nameRecordTable[general.nameRecordTable.Keyword == prop].Dimensionality.values[0]
    dims = [int(i) for i in dims.replace('-', '').split('|') if i.isdigit()]

    if len(dims) == 2:
        num_dim, den_dim = dims
    elif len(dims) == 1:
        num_dim = dims[0]
        den_dim = None
    else:
        num_dim = None
        den_dim = None

    return num_dim, den_dim

@lru_cache(maxsize=512)
def conversion_params(general, dimensionality, inunit, outunit):
    """Get unit conversion gain and offset parameters given a dimensionallity, input and output units

    Arguments:
        dimensionality {int} -- Property Dimensionality
        inunit {str} -- input unit with which data is stored for the desired property
        outunit {str} -- output unit for the desired property selected on the basefile

    Returns:
        (gain, offset) {float, float} -- gain and offset unit conversion parameters
    """

    unit_filter_in = (general.unitsConversionTable['Unit Name'] == inunit) & (general.unitsConversionTable.Dimensionality == dimensionality)
    gain_in, offset_in = general.unitsConversionTable.loc[unit_filter_in, ['Gain', 'Offset']].values[0]

    unit_filter_out = (general.unitsConversionTable['Unit Name'] == outunit) & (general.unitsConversionTable.Dimensionality == dimensionality)
    gain_out, offset_out = general.unitsConversionTable.loc[unit_filter_out, ['Gain', 'Offset']].values[0]

    return gain_out / gain_in, offset_out / gain_out - offset_in / gain_in

@lru_cache(maxsize=512)
def conversion_gain_offset(general, prop):
    """Get unit conversion gain and offset parameters given a desired property

    Arguments:
        prop {str} -- property

    Returns:
        (gain, offset) {float, float} -- gain and offset unit conversion parameters
    """

    # Numerator and Denominator Dimensionalities
    num_dim, den_dim = get_dimensionality(general, prop)
    if num_dim is None:
        return 1., 0.

    # Numerator and Denominator Units
    num_inunit, num_outunit = general.unitsTable.loc[general.unitsTable.Index == num_dim, ['Internal Unit', 'Output Unit']].values[0]

    if den_dim is not None:
        den_inunit, den_outunit = general.unitsTable.loc[general.unitsTable.Index == den_dim, ['Internal Unit', 'Output Unit']].values[0]
    else:
        den_inunit, den_outunit = None, None

    # Numerator and Denominator Gains and Offsets
    num_gain, num_offset = conversion_params(general, num_dim, num_inunit, num_outunit)

    if den_dim is not None:
        den_gain, den_offset = conversion_params(general, den_dim, den_inunit, den_outunit)
    else:
        den_gain, den_offset = 1., 0.

    return den_gain / num_gain, den_offset / den_gain - num_offset / num_gain

@lru_cache(maxsize=512)
def get_output_unit(general, prop):
    """Get output unit for a desired property

    Arguments:
        prop {str} -- property

    Returns:
        outunit {str} -- output unit
    """

    # Numerator and Denominator Dimensionalities
    num_dim, den_dim = get_dimensionality(general, prop)
    if num_dim is None:
        return None

    # Numerator and Denominator Units
    num_inunit, num_outunit = general.unitsTable.loc[general.unitsTable.Index == num_dim, [
        'Internal Unit', 'Output Unit']].values[0]

    if den_dim is not None:
        den_inunit, den_outunit = general.unitsTable.loc[general.unitsTable.Index == den_dim, [
            'Internal Unit', 'Output Unit']].values[0]
    else:
        den_inunit, den_outunit = None, None

    if den_outunit:
        return num_outunit + '/' + den_outunit
    else:
        return num_outunit

def parse_all_string(all_string, dtype=np.float, shape=None):
    """Convert string in *ALL format to a numpy array.
    
    Arguments:
        all_string {str} -- String object containing *ALL lines.
    
    Keyword Arguments:
        dtype {numpy.{datatype}} -- numpy datatype selected for output (default: {np.float})
        shape {tuple} -- shape of the output array (default: {None})
    """

    all_string = all_string.strip().replace('\n', '').split(' ')
    
    all_array = np.concatenate([np.array(np.float(i)).reshape(1,) if '*' not in i
                                else np.repeat(np.float(i.split('*')[1]), i.split('*')[0]) 
                                for i in  all_string]).astype(dtype)
    if shape is not None:
        return all_array.reshape(shape)
    else:
        return all_array