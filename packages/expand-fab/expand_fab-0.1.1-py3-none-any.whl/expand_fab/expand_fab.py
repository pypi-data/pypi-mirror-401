from dataclasses import field
from enum import Enum
from typing import List, Optional, Union

import flet as ft


class FabDirection(Enum):
    """you can set where the child will appear"""

    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


@ft.control("FabChild")
class FabChild(ft.LayoutControl):
    """you can determine which buttons will appear"""

    child: Optional[ft.IconDataOrControl] = None
    """
    You can use `Icons` directly, or if you want to customize the icons, you can use `Icon`.
    """

    label: Optional[str] = None
    label_style: Optional[ft.TextStyle] = None
    label_bgcolor: Optional[ft.ColorValue] = None
    label_widget: Optional[ft.Control] = None
    label_shadow: Optional[List[ft.BoxShadowValue]] = None
    bgcolor: Optional[ft.ColorValue] = None
    foreground_color: Optional[ft.ColorValue] = None
    shape: Optional[ft.ShapeBorder] = None
    visible: bool = True

    on_tap: Optional[ft.ControlEventHandler["FabChild"]] = None
    on_long_press: Optional[ft.ControlEventHandler["FabChild"]] = None


@ft.control("ExpandFab")
class FloatingActionButton(ft.LayoutControl):
    """
    With this class, you can create cool FABs.

    Example:
        ```python
        page.floating_action_button = ef.FloatingActionButton(
            icon=ft.Icons.ADD,
            active_icon=ft.Icons.CLOSE,
            foreground_color=ft.Colors.BLUE,
            children=[
                ef.FabChild(
                    child=ft.Icons.BOOK,
                    label="Book",
                    on_tap=fab_child_tap,
                ),
                ef.FabChild(
                    child=ft.Icons.MEDIATION,
                    label="Mediation",
                    on_tap=fab_child_tap,
                ),
            ],
            on_open=fab_open,
        )  # type: ignore
        ```
    """

    children: List[FabChild] = field(default_factory=list)
    """
    You can add children that can display a popup Fab.
    """

    bgcolor: Optional[ft.ColorValue] = None
    foreground_color: Optional[ft.ColorValue] = None
    active_bgcolor: Optional[ft.ColorValue] = None
    active_foreground_color: Optional[ft.ColorValue] = None
    gradient: Optional[
        Union[ft.Gradient, ft.LinearGradient, ft.RadialGradient, ft.SweepGradient]
    ] = None
    """
    You can create color gradients on buttons.

    Example:
        ```python
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment(0.8, 1),
            tile_mode=ft.GradientTileMode.MIRROR,
            rotation=math.pi / 3,
            colors=[
                "0xff1f005c",
                "0xff5b0060",
                "0xff870160",
                "0xffac255e",
                "0xffca485c",
                "0xffe16b5c",
                "0xfff39060",
                "0xffffb56b",
            ],
        ),
        ```
    """
    gradient_box_shape: ft.BoxShape = ft.BoxShape.RECTANGLE
    """
    If you create a normal color gradient, the fab button will be square.
    You can change it to a circle to match the button.

    Example:
        ```python
        gradient_box_shape = ft.BoxShape.CIRCLE
        ```
    """

    elevation: ft.Number = 6.0
    button_size: ft.Size = field(default_factory=lambda: ft.Size(56.0, 56.0))
    children_button_size: ft.Size = field(default_factory=lambda: ft.Size(56.0, 56.0))
    mini: bool = False
    visible: bool = True
    overlay_opacity: ft.Number = 0.8
    overlay_color: Optional[ft.ColorValue] = None
    hero_tag: Optional[str] = None
    icon: Optional[ft.IconData] = None
    active_icon: Optional[ft.IconData] = None
    child: Optional[ft.Control] = None
    active_child: Optional[ft.Control] = None
    switch_label_position: bool = False
    use_rotation_animation: bool = True
    """
    You can set the animation when you interact with the button. The default is `True`.
    """

    label: Optional[ft.Control] = None
    active_label: Optional[ft.Control] = None
    direction: FabDirection = FabDirection.UP
    """
    You can set where the popup children will appear, the default is `FabDirection.UP`.
    """

    close_manually: bool = False
    render_overlay: bool = True
    curve: ft.AnimationCurve = ft.AnimationCurve.FAST_OUT_SLOWIN
    animation_duration: ft.DurationValue = field(
        default_factory=lambda: ft.Duration(milliseconds=150)
    )
    is_open_on_start: bool = False
    close_dial_on_pop: bool = True
    child_margin: ft.MarginValue = field(
        default_factory=lambda: ft.Margin.symmetric(horizontal=16, vertical=0)
    )
    child_padding: ft.PaddingValue = field(
        default_factory=lambda: ft.Padding.symmetric(vertical=5)
    )
    space_between_children: Optional[ft.Number] = None
    spacing: Optional[ft.Number] = None
    animation_curve: Optional[ft.AnimationCurve] = None

    on_open: Optional[ft.ControlEventHandler["FloatingActionButton"]] = None
    on_close: Optional[ft.ControlEventHandler["FloatingActionButton"]] = None
