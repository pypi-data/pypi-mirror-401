###############################################################################
#
# (C) Copyright 2026 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
################################################################################
import pandas as pd

from everysk.sdk.brutils.cnpj import CNPJ


@pd.api.extensions.register_series_accessor('cnpj')
class CNPJAccessor:
    """
    A pandas accessor class for handling CNPJ (Cadastro Nacional da Pessoa Jurídica) operations on pandas Series.

    Parameters
    ----------
    pandas_obj : pandas.Series
        The pandas Series object containing CNPJ values.
    """

    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def sanitize(self, zfill: bool = True):
        return self._obj.apply(lambda x: CNPJ(x).sanitize(zfill=zfill))

    def normalize(self, zfill: bool = False, errors: str = 'raise'):
        return self._obj.apply(lambda x: CNPJ(x).normalize(zfill=zfill, errors=errors))

    def is_valid(self, check_dv: bool = False):
        return self._obj.apply(lambda x: CNPJ(x).is_valid(check_dv=check_dv))

    def format(self, errors: str = 'raise'):
        return self._obj.apply(lambda x: CNPJ(x).format(errors=errors))

    def generate(self, valid_dv: bool = True):
        return self._obj.apply(lambda x: str(CNPJ.generate_random(valid_dv=valid_dv)))
