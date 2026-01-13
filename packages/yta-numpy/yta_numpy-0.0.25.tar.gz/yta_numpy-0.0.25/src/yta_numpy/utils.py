from yta_numpy.converter import NumpyConverter
from yta_programming.decorators.requires_dependency import requires_dependency
from yta_validation import PythonValidator
from typing import Union

import numpy as np
import random


def _force_numpy_as_uint8(
    frame: np.ndarray
) -> np.ndarray:
    """
    *For internal use only*
    
    Force the provided `frame` numpy array to be `uint8`
    to be able to store it using pillow.
    
    (!) Use this method before trying to operate with
    the pillow library.
    """
    return NumpyConverter.to_dtype(
        array = frame,
        dtype = np.uint8
    )

@requires_dependency('PIL', 'yta_numpy', 'pillow')
def numpy_to_pillow(
    frame: np.ndarray,
    do_read_as_rgba: bool = True
) -> 'Image.Image':
    """
    *Optional `pillow` (imported as `PIL`) library is required*

    Transform the provided `frame` numpy array into a
    pillow image. The array will be forced to be uint8
    and will be read as an RGBA if `do_read_as_rgba` is
    True or as an RGB if False.

    TODO: I think I have this method in other library and
    maybe it should not be here...
    """
    from PIL import Image

    # We need to transform to RGBA [0, 255]
    return Image.fromarray(
        obj = _force_numpy_as_uint8(frame)
    ).convert(
        mode = (
            'RGBA'
            if do_read_as_rgba else
            'RGB'
        )
    )

def numpy_to_file(
    frame: np.ndarray,
    output_filename: str
) -> str:
    """
    *Optional `pillow` (imported as `PIL`) library is required*

    Save the provided numpy frame array as a file.

    The image must be a RGB (uint8 as numpy) to be able
    to be stored by the pillow library, so we will force
    the array to be transformed to it.
    
    Pillow only accepts this:
    - `uint8` for RGB/RGBA `[0, 255]`
    - `float32` for 1 channel (grayscale)
    """
    # TODO: Force 'IMAGE' output (?)
    # Example: np.zeros((480, 640, 3), dtype=np.uint8)

    # We need to transform to RGBA [0, 255]
    numpy_to_pillow(
        frame = frame,
        do_read_as_rgba = True
    ).save(output_filename)
    
    # TODO: Remove this if above is working
    #Image.fromarray(_force_numpy_as_uint8(frame)).save(output_filename)

    return output_filename

@requires_dependency('PIL', 'yta_numpy', 'pillow')
def read_image_as_numpy(
    path: str,
    do_read_as_rgba: bool = True,
    size: Union[tuple[int, int], None] = None
) -> np.ndarray:
    """
    *Optional dependency `pillow` (imported as `PIL`) required*

    Read an image from a file and transform it into a
    numpy array. It will force the 'size' if provided,
    or leave the original one if it is None.
    """
    from PIL import Image

    mode = (
        'RGBA'
        if do_read_as_rgba else
        'RGB'
    )

    with Image.open(path) as img:
        img = img.convert(mode)
        np_img = np.array(img, dtype = np.uint8)

    return (
        scale_numpy_pillow(
            input = np_img,
            size = size
        ) if size is not None else
        np_img
    )

@requires_dependency('pydub', 'yta_numpy', 'pydub')
def read_audio_as_numpy(
    filename: str,
    do_normalize: bool = False
) -> Union[np.ndarray, float]:
    """
    Turn `.mp3` file into a `numpy` array. It only
    works for 16-bit files for now.

    The return:
    - (`audio_numpy_array`, `audio_sample_rate`)
    """
    import pydub

    audio = pydub.AudioSegment.from_mp3(filename)
    y = np.array(audio.get_array_of_samples())

    if audio.channels == 2:
        y = y.reshape((-1, 2))

    audio_array, audio_sample_rate = (
        (np.float32(y) / 2**15, audio.frame_rate)
        if do_normalize else
        (y, audio_sample_rate)
    )

    return  (audio_array, audio_sample_rate)

@requires_dependency('pydub', 'yta_numpy', 'pydub')
def audio_numpy_to_file(
    audio: np.ndarray,
    sample_rate: float,
    is_normalized: bool,
    output_filename: str
) -> str:
    """
    Write the `audio` provided (as a `numpy` array)
    to an `output_filename` file, using the
    `sample_rate` provided.

    This method will write only `.mp3` files with a
    `bitrate=320k`.
    """
    import pydub

    # TODO: We should check that 'output_filename' is '.mp3'

    number_of_channels = (
        2 if (
            audio.ndim == 2 and
            audio.shape[1] == 2
        )
        else
        1
    )

    audio_to_write = (
        # normalized array - each item should be a float in [-1, 1)
        np.int16(audio * 2 ** 15)
        if is_normalized else
        np.int16(audio)
    )

    pydub_audio = pydub.AudioSegment(
        audio_to_write.tobytes(),
        frame_rate = sample_rate,
        sample_width = 2,
        channels = number_of_channels
    )

    pydub_audio.export(
        output_filename,
        format = 'mp3',
        bitrate = '320k'
    )

    return output_filename

"""
TODO: Code migrated from other project, check if this
is set in the 'yta_numpy_resizer' library or not, and
remove if duplicated.
"""
@requires_dependency('cv2', 'yta_numpy', 'opencv-python')
def scale_numpy(
    input: np.ndarray,
    size: tuple[int, int]
) -> np.ndarray:
    """
    *Optional dependency `opencv-python` (imported as `cv2`) required*

    Resize the 'input' numpy array to the provided 'size'
    if needed, using a rescaling method with 'opencv-python'
    (cv2).

    The 'size' provided must be (width, height).
    """
    import cv2

    return cv2.resize(input, size, interpolation = cv2.INTER_LINEAR)

@requires_dependency('PIL', 'yta_numpy', 'pillow')
def scale_numpy_pillow(
    input: np.ndarray,
    size: tuple[int, int]
) -> np.ndarray:
    """
    *Optional dependency `pillow` (imported as `PIL`) required*

    Resize the 'input' numpy array to the provided 'size'
    if needed, using a rescaling method with 'pillow'
    (PIL).

    The 'size' provided must be (width, height).
    """
    from PIL import Image

    # TODO: We should do `_force_numpy_as_uint8(frame)` but
    # maybe we have `dtype` that we cannot manage yet...
    return np.array(Image.fromarray(input).resize(size, Image.BILINEAR))

# TODO: Maybe create a '_Dtype' to add the shortcut
# and use it as NumpyUtils.dtype.method_name
class _Dtype:
    """
    *For internal use only*

    Static class to be wrapped by the general NumpyUtils
    class, to act as a shortcut to the functionality 
    related to dtypes.
    """

    _DTYPES_AS_STR = [
        # Unsigned ints
        'uint8'
        'uint16'
        'uint32'
        'uint64'
        # Signed ints
        'int8'
        'int16'
        'int32'
        'int64'
        # Floats
        'float16'
        'float32'
        'float64'
        'float128'   # only in some platforms (x86/Linux)
        # Complex
        'complex64'   # (float32 + float32j)
        'complex128'  # (float64 + float64j)
        'complex256'  # (float128 + float128j, depending on the platform)
        # Bool
        'bool'
        # Others
        'object'
        'str'
        'bytes'
    ]
    """
    The dtypes that exist in the numpy library, but as
    strings to be able to validate them easier.
    """

    @staticmethod
    def is_dtype_class(
        dtype: np.dtype
    ) -> bool:
        """
        Check if the provided `dtype` is a dtype class, which
        is True if you pass `np.uint8` directly.
        """
        # Maybe 'if isinstance(dtype, type)' also (?)
        return PythonValidator.is_subclass_of(dtype, np.generic)
    
    @staticmethod
    def is_dtype_instance(
        dtype: np.dtype
    ) -> bool:
        """
        Check if the provided `dtype` is an instance of a dtype,
        which is True if you pass `np.dtype('uint8')` directly.
        """
        return PythonValidator.is_instance_of(dtype, np.dtype)
    
    @staticmethod
    def is_dtype_str(
        dtype: str
    ) -> bool:
        """
        Check if the provided `dtype` is a string of a valid dtype.
        """
        return dtype in _Dtype._DTYPES_AS_STR

    @staticmethod
    def is_a_dtype(
        dtype: np.dtype
    ) -> bool:
        """
        Check if the `dtype` provided is a valid dtype class
        (`np.uint8`) or instance (`np.dtype('uint8')`).

        Thanks to:
        - https://stackoverflow.com/a/26921882
        """
        return (
            _Dtype.is_dtype_class(dtype) or
            _Dtype.is_dtype_instance(dtype)
        )
    
    @staticmethod
    def is_this_dtype(
        dtype_one: Union[np.dtype, str],
        dtype_two: np.dtype = np.uint8
    ) -> bool:
        """
        Check if the provided `dtype_one` dtype is the also given
        `dtype` (provide it as 'np.uint8', 'np.float32', for example).

        This is one of the best ways to check if the `dtype_one` is of
        an specific dtype. It is the correct way to do the equivalent
        (but working) to a 'something is np.uint8'.
        """
        if not _Dtype.is_dtype_class(dtype_two):
            raise Exception('The `dtype_two` parameter provided is not a dtype class.')
        
        return np.dtype(dtype_one) == np.dtype(dtype_two)
    
    @staticmethod
    def is_integer_dtype(
        dtype: np.dtype
    ) -> bool:
        """
        Check if the provided `dtype` is integer or not.
        """
        return np.issubdtype(dtype, np.integer)
    
    @staticmethod
    def is_float_dtype(
        dtype: np.dtype
    ) -> bool:
        """
        Check if the provided `dtype` is float or not.
        """
        return np.issubdtype(dtype, np.floating)
    
    @staticmethod
    def get_dtype_as_class(
        dtype: Union[np.dtype, str]
    ) -> Union[np.dtype, None]:
        """
        Get the `dtype` provided but as a class, if a valid
        one (class, instance or str) is provided.
        """
        return (
            dtype
            if _Dtype.is_dtype_class(dtype) else
            dtype.type
            if _Dtype.is_dtype_instance(dtype) else
            np.dtype(dtype).type
            if _Dtype.is_dtype_str(dtype) else
            None
        )
    
    @staticmethod
    def limit_values_of_dtype(
        dtype: np.dtype
    ) -> Union[float, int, None]:
        """
        Get the limit values of the provided `dtype`. If the dtype
        is a float you will always get (0.0, 1.0) as the limits,
        because those are the useful limits for us.

        (!) We only accept integer or floating dtypes.
        """
        # The `dtype` here is accepted in any form (class, instance
        # or str)
        """
        The actual limit values are useless for us when creating numpy
        arrays, as we will use the real range, and thats why we are
        returning (0.0, 1.0) always for the float dtypes.
        """
        return (
            (
                np.iinfo(dtype).min,
                np.iinfo(dtype).max
            )
            if _Dtype.is_integer_dtype(dtype) else
            (
                0.0,
                1.0
                # This is the way to show the actual limit. For np.float32 is:
                # (np.float32(-3.4028235e+38), np.float32(3.4028235e+38))
                # np.finfo(dtype).min,
                # np.finfo(dtype).max
            )
            if _Dtype.is_float_dtype(dtype) else
            None
        )
    
class _Generator:
    """
    *For internal use only*

    Static class to be wrapped by the general NumpyUtils
    class, to act as a shortcut to the functionality 
    related to generating numpy arrays.
    """

    @staticmethod
    def min(
        shape: any,
        dtype: np.dtype
    ) -> np.ndarray:
        """
        Create a numpy array with the provided `shape` and
        `dtype` having the minimum value possible (0.0 adapted
        to the provided dtype) in the whole array.
        """
        return np.zeros(
            shape = shape,
            dtype = dtype
        )
    
    @staticmethod
    def half(
        shape: any,
        dtype: np.dtype
    ) -> np.ndarray:
        """
        Create a numpy array with the provided `shape` and
        `dtype` having the half of the maximum value possible
        (0.5 adapted to the provided dtype) in the whole array.
        """
        return _Generator.custom(
            shape = shape,
            dtype = dtype,
            value = 0.5
        )
    
    @staticmethod
    def max(
        shape: any,
        dtype: np.dtype
    ) -> np.ndarray:
        """
        Create a numpy array with the provided `shape` and
        `dtype` having the maximum value possible (1.0 adapted
        to the provided dtype) in the whole array.
        """
        return _Generator.custom(
            shape = shape,
            dtype = dtype,
            value = 1.0
        )
    
    @staticmethod
    def custom(
        shape: any,
        dtype: np.dtype,
        value: float
    ) -> np.ndarray:
        """
        Create a numpy array with the provided `shape` and
        `dtype` having the provided `value` (but adapted
        to the provided dtype) in the whole array.

        If `value=0.75` and `dtype=np.uint8`, the array
        will include `191` as the value for each position.
        """
        return np.full(
            shape = shape,
            fill_value = NumpyUtils.get_fill_value(
                value = value,
                dtype = dtype
            ),
            dtype = dtype
        )
    
    @staticmethod
    def random(
        shape: any,
        dtype: np.dtype
    ) -> np.ndarray:
        """
        Create a numpy array with the provided `shape` and
        `dtype` having a random value (between 0.0 and 1.0
        but adapted to the provided dtype) in the whole array.
        """
        return _Generator.custom(
            shape = shape,
            dtype = dtype,
            # Random in [0.0, 1.0] range
            value = random.uniform(0, 1)
        )
    
    # This will generate a random array, in which all the
    # values are different and random:
    # - `np.random.random((3,2))`

class NumpyUtils:
    """
    *Static class*

    Class to wrap some utils related to numpy.
    """
    
    dtype: _Dtype = _Dtype
    """
    Shortcut to the functionality related to dtypes.
    """
    generator: _Generator = _Generator
    """
    Shortcut to the functionality related to generating numpy
    arrays.
    """

    def get_fill_value(
        value: float,
        dtype: np.dtype
    ) -> Union[float, int]:
        """
        Get the `value` but converted to the provided `dtype` to
        be used to fill a numpy array. The `value` parameter must
        be in the [0.0, 1.0] range (values out of bounds will be
        automatically transformed into the limit).

        Integer values will be automatically converted (and 
        truncated if needed).

        Examples below:
        - `get_fill_value(0.5, np.float32) == 0.5`
        - `get_fill_value(0.75, np.uint8) == 191`
        """
        # Out of bounds to limits
        value = (
            0.0
            if value < 0 else
            1.0
            if value > 1.0 else
            value
        )

        value = (
            int(value * _Dtype.limit_values_of_dtype(dtype)[1])
            if _Dtype.is_integer_dtype(dtype) else
            value
            if _Dtype.is_float_dtype(dtype) else
            None
        )

        if value is None:
            raise Exception(f'The dtype "{str(dtype)}" provided is not an int nor a float dtype.')
        
        return value

    