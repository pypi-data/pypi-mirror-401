"""
Module to convert safely from one dtype to another,
transforming the values if needed.
"""
from yta_validation.parameter import ParameterValidator

import numpy as np


class NumpyConverter:
    """
    Class to wrap static methods that transform one
    numpy array into another one by changing the
    dtype and modifying the values if needed.

    The transform methods are stored in dicts and
    called dynamically based on the origin and the
    desired dtype.

    (!) This module is being developed so the amount
    of dtypes accepted could be not as big as you
    expected :)
    """

    ACCEPTED_DTYPES = ['uint8', 'float32']
    """
    The list of dtypes that we accept in our class to
    be handled.

    If we get `np.uint8`, we need to do `np.dtype(dtype)`
    and compare it as a string, thats why we have strings
    here and not `np.uint8`.
    """
    _TO_FLOAT32 = {
        # np.uint8 has values in [0, 255]
        'uint8': lambda array: (array.astype(np.float32) / 255.0),
        # np.float32 has values in [0.0, 1.0]
        'float32': lambda array: array
    }
    """
    *For internal use only*

    The dict to transform a numpy array from a specific
    dtype to the `np.float32`. Key is the original dtype.

    Call it like this:
    - `NumpyConverter._TO_FLOAT32.get(array.dtype)(array)`

    The formulas:
    - `np.uint8` => `(input.astype(np.float32) / 255.0)`
    """
    _TO_UINT8 = {
        # np.uint8 has values in [0, 255]
        'uint8': lambda array: array,
        # np.float32 has values in [0.0, 1.0]
        'float32': lambda array: np.clip(array * 255.0, 0, 255).astype(np.uint8)
    }
    """
    *For internal use only*

    The dict to transform a numpy array from a specific
    dtype to the `np.uint8`. Key is the original dtype.

    Call it like this:
    - `NumpyConverter._TO_UINT8.get(array.dtype)(array)`

    The formulas:
    - `np.float32` => `np.clip(array * 255.0, 0, 255).astype(np.uint8)`
    """
    _TO_DTYPE_INDEX_DICT = {
        'uint8': _TO_UINT8,
        'float32': _TO_FLOAT32
    }
    """
    *For internal use only*

    The dict that includes the different internal dicts
    we have to transform to one specific dtype. You will
    get the dict to apply to obtain the transform
    function according to the origin dtype.

    Call it like this:
    - `NumpyConverter._TO_DTYPE_INDEX_DICT.get(str(np.dtype(dtype))).get(str(array.dtype))(array)`
    """

    @staticmethod
    def is_accepted_dtype(
        dtype: np.dtype
    ) -> bool:
        """
        Check if the provided `dtype` is a valid one or not
        for our class. You can see the `ACCEPTED_DTYPES`
        variable to obtain the accepted values.
        """
        return str(np.dtype(dtype)) in NumpyConverter.ACCEPTED_DTYPES
    
    @staticmethod
    def _validate_numpy_array(
        array: np.ndarray
    ) -> None:
        """
        *For internal use only*

        Check if the `dtype` of the provided `array` is valid,
        raising an exception if not.
        """
        if not NumpyConverter.is_accepted_dtype(array.dtype):
            raise Exception(f'The dtype "{array.dtype}" of the array provided is not accepted by our system. We only accept: {", ".join(NumpyConverter.ACCEPTED_DTYPES)}')
        
    @staticmethod
    def _validate_dtype(
        dtype: np.dtype
    ) -> None:
        """
        *For internal use only*

        Check if the provided `dtype` is valid, raising an
        exception if not.
        """
        if not NumpyConverter.is_accepted_dtype(dtype):
            raise Exception(f'The provided dtype "{dtype}" is not accepted by our system. We only accept: {", ".join(NumpyConverter.ACCEPTED_DTYPES)}')

    @staticmethod
    def to_dtype(
        array: np.ndarray,
        dtype: np.dtype
    ) -> np.ndarray:
        """
        Transform the provided `input` numpy array to the
        `dtype` provided (if available in our system).

        This method will raise an exception if the dtype of
        the `input` numpy array provided is not accepted by
        our system.

        Check the formulas in the dicts of this class.

        Call this method like this:
        - `NumpyConverter.to_dtype(array, np.uint8)`
        """
        ParameterValidator.validate_mandatory_numpy_array('array', array)
        dtype = np.dtype(dtype)
        ParameterValidator.validate_mandatory_instance_of('dtype', dtype, np.dtype)

        NumpyConverter._validate_numpy_array(array)
        NumpyConverter._validate_dtype(dtype)

        # We obtain the dict and we call it inmediately
        return (
            NumpyConverter._TO_DTYPE_INDEX_DICT
            .get(str(dtype))
            .get(str(array.dtype))(array)
        )

"""
Notes for the developer:
- Numpy, when passing 'np.uint8' it is not easy to
compare, but doing `np.dtype(dtype)` you can obtain
a str to compare with 'uint8', 'float32', etc.
- Numpy, when having an array and accessing to the
`array.dtype`, it can be compared with str directly
(as I said with 'uint8', 'float32', etc.).
"""