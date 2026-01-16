###############################################################################
#
# (C) Copyright 2026 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
import random
import re
import string

from everysk.core.fields import IntField, TupleField

###############################################################################
# Globals
###############################################################################

CNPJ_LENGTH: IntField = IntField(default=14, readonly=True)
CNPJ_BASE_LENGTH: IntField = IntField(default=12, readonly=True)

WEIGHTS_DV1: TupleField = TupleField(default=(5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2), readonly=True)
WEIGHTS_DV2: TupleField = TupleField(default=(6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2), readonly=True)

BASE_VALUES = string.ascii_uppercase + string.digits
BASE_VALUES_REGEX = r'[A-Z0-9]'


class CNPJError(ValueError):
    """
    Exception raised for errors encountered during the parsing or validation of a CNPJ (Cadastro Nacional da Pessoa Jurídica).

    Attributes:
        message (str): Explanation of the error.
    """


class CNPJ:
    """
    Base class for handling Brazilian CNPJ (Cadastro Nacional da Pessoa Jurídica) documents.

    This class provides methods for sanitizing, normalizing, validating, formatting, and generating CNPJ numbers,
    including support for the new alphanumeric base format and the updated verification digit (DV) calculation rules.

    cnpj : str | int | float | None
        The CNPJ value to be processed. Can be a string, integer, float, or None.

    Attributes
    ----------
    firm : str
        The main firm identifier portion of the CNPJ (first 8 digits).
    subsidiary : str
        The branch/subsidiary identifier portion of the CNPJ (next 4 digits).
    dv : str
        The verification digits (last 2 digits) of the CNPJ.
    """

    def __init__(self, cnpj: str | int | float | None):
        """
        Initialize the instance with a CNPJ value.

        Args:
            cnpj (str | int | float | None): The CNPJ value, which can be a string, integer, float, or None.
        """
        self._input_cnpj = cnpj
        self.cnpj = cnpj

    def __str__(self) -> str:
        """
        Returns a string representation of the object by formatting it.
        If formatting fails or returns None, an empty string is returned.

        Returns:
            str: The formatted string representation of the object, or an empty string if formatting fails.
        """
        return self.cnpj

    def __repr__(self) -> str:
        """
        Return a string representation of the object, displaying the class name and the value of the 'cnpj' attribute.

        Returns:
            str: A string in the format "<ClassName>(cnpj='<cnpj_value>')".
        """
        return f"{self.__class__.__name__}('{self.cnpj}')"

    @property
    def firm(self) -> str:
        """
        Returns the base part of the firm's CNPJ (Cadastro Nacional da Pessoa Jurídica) as a string.
        The CNPJ is sanitized and zero-filled if necessary, then truncated to exclude the last 4 digits.

        Returns:
            str: The base CNPJ string, excluding the branch identifier.
        """
        if self.is_valid():
            return self.cnpj[: CNPJ_BASE_LENGTH.default - 4]
        return None

    @property
    def subsidiary(self) -> str:
        """
        Returns the subsidiary portion of the CNPJ number as a string.

        This property sanitizes the CNPJ value (optionally zero-filling it), then extracts and returns the last 4 digits, which represent the subsidiary code according to the CNPJ format.

        Returns:
            str: The 4-digit subsidiary code from the CNPJ.
        """
        if self.is_valid():
            return self.cnpj[CNPJ_BASE_LENGTH.default - 4 : CNPJ_BASE_LENGTH.default]
        return None

    @property
    def dv(self) -> str:
        """
        Returns the 'dv' (check digit) portion of the sanitized identifier string.

        The method first sanitizes the identifier (optionally zero-filling it), then slices
        the string from the position defined by `CNPJ_BASE_LENGTH.default` to extract the check digit(s).

        Returns:
            str: The check digit(s) of the sanitized identifier.
        """
        if self.is_valid():
            return self.cnpj[CNPJ_BASE_LENGTH.default :]
        return None

    def sanitize(self, zfill: bool = True) -> str | None:
        """
        Sanitize a CNPJ string.

        - Removes non-alphanumeric characters
        - Uppercases letters
        - If zfill=True, left-pads with zeros until length == 14

        Parameters
        ----------
        zfill : bool, default=True
            Whether to left-pad the sanitized value to length 14.

        Returns
        -------
        str | None
            Sanitized CNPJ or None if input is None.

        Raises
        ------
        TypeError
            If `cnpj` is not str|None.
        """
        sanitized = self._input_cnpj

        if sanitized in {None, True, False, ''}:
            self.cnpj = None

        else:
            if isinstance(sanitized, float):
                sanitized = int(sanitized)

            if isinstance(sanitized, int):
                sanitized = str(sanitized)

            if not isinstance(sanitized, str):
                raise TypeError('CNPJ must be a string, integer, float, or None')

            sanitized = ''.join(ch for ch in sanitized.strip() if ch.isalnum()).upper()

            if zfill:
                sanitized = sanitized.zfill(CNPJ_LENGTH.default)

            self.cnpj = sanitized

        return self.cnpj

    def normalize(self, zfill: bool = False, errors: str = 'raise') -> str | None:
        """
        Normalize a CNPJ with structural validation only (no DV check).

        Always:
        - sanitizes input
        - applies zfill to reach length 14

        Structural rules:
        - first 12 chars: alphanumeric
        - last 2 chars: digits

        Parameters
        ----------
        zfill : bool, default=False
            Whether to left-pad the sanitized value to length 14.
        errors : {'raise', 'coerce', 'ignore'}, default='raise'
            Behavior when parsing fails while normalizing ``self.cnpj``.

        Returns
        -------
        str | None
            Sanitized 14-character CNPJ, None, or original input.
        """
        if errors not in {'raise', 'coerce', 'ignore'}:
            raise ValueError("errors must be one of: 'raise', 'coerce', 'ignore'")

        try:
            self.sanitize(zfill=zfill)

            if self.cnpj is None:
                raise CNPJError('CNPJ is None.')

            if not self.is_valid(check_dv=False):
                raise CNPJError('CNPJ validation failed.')

        except CNPJError as err:
            if errors == 'coerce':
                self.cnpj = None
            if errors == 'raise':
                raise err

        return self.cnpj

    def _ascii48_value(self, ch: str) -> int:
        """
        Converts a single alphanumeric character to its ASCII code minus 48.

        This method is used internally for mapping characters according to the new DV rule.
        It validates that the input is a single alphanumeric character and raises a CNPJError
        if the input is invalid.

        Args:
            ch (str): A single character string to be converted.

        Returns:
            int: The ASCII value of the uppercase version of `ch`, minus 48.

        Raises:
            CNPJError: If `ch` is not a single character or is not alphanumeric.
        """
        if len(ch) != 1:
            raise CNPJError(f'Invalid character {ch!r}: must be a single character')
        if not ch.isalnum():
            raise CNPJError(f'Invalid character {ch!r}: must be alphanumeric')
        return ord(ch.upper()) - 48

    def _calc_dv(self, payload: str, weights: tuple[int, ...]) -> str:
        """
        Calculates a single check digit (DV) using the modulo 11 algorithm.

        Args:
            payload (str): The input string for which the check digit is to be calculated.
            weights (tuple[int, ...]): A tuple of integer weights to be applied to each character in the payload.

        Returns:
            str: The calculated check digit as a string. Returns '0' if the result is less than 2, otherwise returns (11 - result) as a string.

        Note:
            This is an internal method used for check digit calculation in Brazilian document validation.
        """
        total = sum(self._ascii48_value(ch) * w for ch, w in zip(payload, weights))
        result = total % 11
        return '0' if result < 2 else str(11 - result)

    def _calc_dvs_from_base(self, base: str) -> str:
        """
        Calculates and returns the two check digits (DVs) for a given 12-character CNPJ base string.

        Args:
            base (str): A 12-character alphanumeric string representing the CNPJ base.

        Returns:
            str: The two calculated check digits concatenated as a string.

        Raises:
            CNPJError: If the base is not exactly 12 alphanumeric characters.
        """
        if len(base) != CNPJ_BASE_LENGTH.default or not all(ch.isalnum() for ch in base):
            raise CNPJError('Base must be exactly 12 alphanumeric characters')
        dv1 = self._calc_dv(base, WEIGHTS_DV1.default)
        dv2 = self._calc_dv(f'{base}{dv1}', WEIGHTS_DV2.default)
        return f'{dv1}{dv2}'

    def is_valid(self, check_dv: bool = False) -> bool:
        """
        Validate a *sanitized* CNPJ (14 chars).
        If instantiated with an unsanitized CNPJ, call self.sanitize() first.

        Parameters
        ----------
        check_dv : bool, default=False
            If False, only structural checks are performed.
            If True, structural + DV check (módulo 11 with ASCII-48 mapping).

        Returns
        -------
        bool
            True if valid, else False.
        """
        if not isinstance(self.cnpj, str) or len(self.cnpj) != CNPJ_LENGTH.default:
            return False

        base, dvs = self.cnpj[: CNPJ_BASE_LENGTH.default], self.cnpj[CNPJ_BASE_LENGTH.default :]

        if not dvs.isdigit():
            return False

        if not re.fullmatch(rf'{BASE_VALUES_REGEX}{{{CNPJ_BASE_LENGTH.default}}}', base):
            return False

        if not check_dv:
            return True

        try:
            return dvs == self._calc_dvs_from_base(base)
        except CNPJError:
            return False

    def format(self, errors: str = 'raise') -> str | None:
        """
        Format a CNPJ as 'AA.AAA.AAA/AAAA-DD'.

        Delegates parsing to cls.normalize().

        Parameters
        ----------
        errors : {'raise', 'coerce', 'ignore'}, default='raise'
            Normalization error behavior.

        Returns
        -------
        str | None
            Formatted CNPJ, None, or original input.
        """
        self.normalize(zfill=True, errors=errors)
        if self.cnpj is None or not isinstance(self.cnpj, str):
            return self.cnpj
        return f'{self.cnpj[0:2]}.{self.cnpj[2:5]}.{self.cnpj[5:8]}/{self.cnpj[8:12]}-{self.cnpj[12:]}'

    @staticmethod
    def generate_random(valid_dv: bool = True) -> str:
        """
        Generate a random CNPJ using the new alphanumeric base format.

        Parameters
        ----------
        valid_dv : bool, default=True
            If True, generate a DV-valid CNPJ.
            If False, generate a structurally valid but DV-invalid CNPJ.

        Returns
        -------
        str
            Sanitized 14-character CNPJ.
        """
        base = ''.join(random.choice(BASE_VALUES) for _ in range(CNPJ_BASE_LENGTH.default))

        # To avoid calling cls from a staticmethod, compute using local helpers:
        # We'll re-use the module-level logic through a lightweight inline calc.
        def ascii48_value(ch: str) -> int:
            return ord(ch.upper()) - 48

        def calc_dv(payload: str, weights: tuple[int, ...]) -> str:
            total = sum(ascii48_value(ch) * w for ch, w in zip(payload, weights))
            rest = total % 11
            return '0' if rest < 2 else str(11 - rest)

        dv1 = calc_dv(base, WEIGHTS_DV1.default)
        dv2 = calc_dv(f'{base}{dv1}', WEIGHTS_DV2.default)
        dvs = f'{dv1}{dv2}'

        if valid_dv:
            return CNPJ(f'{base}{dvs}')

        invalid_second_dv = str((int(dvs[1]) + random.randint(1, 9)) % 10)
        return CNPJ(f'{base}{dvs[0]}{invalid_second_dv}')
