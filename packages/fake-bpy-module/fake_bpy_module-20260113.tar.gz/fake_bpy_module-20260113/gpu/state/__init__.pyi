"""
This module provides access to the gpu state.

"""

import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import gpu.types

def active_framebuffer_get() -> gpu.types.GPUFrameBuffer:
    """Return the active frame-buffer in context.

    :return: The active framebuffer.
    :rtype: gpu.types.GPUFrameBuffer
    """

def blend_get() -> str:
    """Current blending equation.

    :return: The current blend mode.
    :rtype: str
    """

def blend_set(mode: str) -> None:
    """Defines the fixed pipeline blending equation.

        :param mode: The type of blend mode.

    NONE No blending.

    ALPHA The original color channels are interpolated according to the alpha value.

    ALPHA_PREMULT The original color channels are interpolated according to the alpha value with the new colors pre-multiplied by this value.

    ADDITIVE The original color channels are added by the corresponding ones.

    ADDITIVE_PREMULT The original color channels are added by the corresponding ones that are pre-multiplied by the alpha value.

    MULTIPLY The original color channels are multiplied by the corresponding ones.

    SUBTRACT The original color channels are subtracted by the corresponding ones.

    INVERT The original color channels are replaced by its complementary color.
        :type mode: str
    """

def clip_distances_set(distances_enabled: int) -> None:
    """Sets the number of gl_ClipDistance planes used for clip geometry.

    :param distances_enabled: Number of clip distances enabled.
    :type distances_enabled: int
    """

def color_mask_set(r: bool, g: bool, b: bool, a: bool) -> None:
    """Enable or disable writing of frame buffer color components.

    :param r: Red component.
    :type r: bool
    :param g: Green component.
    :type g: bool
    :param b: Blue component.
    :type b: bool
    :param a: Alpha component.
    :type a: bool
    """

def depth_mask_get() -> bool:
    """Writing status in the depth component.

    :return: True if writing to the depth component is enabled.
    :rtype: bool
    """

def depth_mask_set(value: bool) -> None:
    """Write to depth component.

    :param value: True for writing to the depth component.
    :type value: bool
    """

def depth_test_get() -> str:
    """Current depth_test equation.

    :return: The current depth test mode.
    :rtype: str
    """

def depth_test_set(mode: str) -> None:
    """Defines the depth_test equation.

        :param mode: The depth test equation name.
    Possible values are NONE, ALWAYS, LESS, LESS_EQUAL, EQUAL, GREATER and GREATER_EQUAL.
        :type mode: str
    """

def face_culling_set(culling: str) -> None:
    """Specify whether none, front-facing or back-facing facets can be culled.

    :param culling: NONE, FRONT or BACK.
    :type culling: str
    """

def front_facing_set(invert: bool) -> None:
    """Specifies the orientation of front-facing polygons.

    :param invert: True for clockwise polygons as front-facing.
    :type invert: bool
    """

def line_width_get() -> float:
    """Current width of rasterized lines.

    :return: The current line width.
    :rtype: float
    """

def line_width_set(width: float) -> None:
    """Specify the width of rasterized lines.

    :param width: New width.
    :type width: float
    """

def point_size_set(size: float) -> None:
    """Specify the diameter of rasterized points.

    :param size: New diameter.
    :type size: float
    """

def program_point_size_set(enable: bool) -> None:
    """If enabled, the derived point size is taken from the (potentially clipped) shader builtin gl_PointSize.

    :param enable: True for shader builtin gl_PointSize.
    :type enable: bool
    """

def scissor_get() -> tuple[int, int, int, int]:
    """Retrieve the scissors of the active framebuffer.
    Note: Only valid between scissor_set and a framebuffer rebind.

        :return: The scissor of the active framebuffer as a tuple
    (x, y, xsize, ysize).
    x, y: lower left corner of the scissor rectangle, in pixels.
    xsize, ysize: width and height of the scissor rectangle.
        :rtype: tuple[int, int, int, int]
    """

def scissor_set(x: int, y: int, xsize: int, ysize: int) -> None:
    """Specifies the scissor area of the active framebuffer.
    Note: The scissor state is not saved upon framebuffer rebind.

        :param x: Lower left corner x coordinate, in pixels.
        :type x: int
        :param y: Lower left corner y coordinate, in pixels.
        :type y: int
        :param xsize: Width of the scissor rectangle.
        :type xsize: int
        :param ysize: Height of the scissor rectangle.
        :type ysize: int
    """

def scissor_test_set(enable: bool) -> None:
    """Enable/disable scissor testing on the active framebuffer.

        :param enable: True - enable scissor testing.
    False - disable scissor testing.
        :type enable: bool
    """

def viewport_get() -> tuple[int, int, int, int]:
    """Viewport of the active framebuffer.

    :return: The viewport as a tuple (x, y, xsize, ysize).
    :rtype: tuple[int, int, int, int]
    """

def viewport_set(x: int, y: int, xsize: int, ysize: int) -> None:
    """Specifies the viewport of the active framebuffer.
    Note: The viewport state is not saved upon framebuffer rebind.

        :param x: Lower left corner x coordinate, in pixels.
        :type x: int
        :param y: Lower left corner y coordinate, in pixels.
        :type y: int
        :param xsize: Width of the viewport.
        :type xsize: int
        :param ysize: Height of the viewport.
        :type ysize: int
    """
