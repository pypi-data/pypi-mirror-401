import "package:flutter/material.dart";
import 'package:flet/flet.dart';
import 'package:flutter_speed_dial/flutter_speed_dial.dart';

import './child_fab.dart';

class ExpandFabControl extends StatefulWidget {
  final Control control;
  ExpandFabControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));
  @override
  State<ExpandFabControl> createState() => _ExpandFabControlState();
}

class _ExpandFabControlState extends State<ExpandFabControl> {
  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    var backend = FletBackend.of(context);

    var children = widget.control.children("children");
    var visible = widget.control.getBool("visible", true)!;
    var bgColor = widget.control.getColor("bgcolor", context);
    var foregroundColor = widget.control.getColor("foreground_color", context);
    var activeBgColor = widget.control.getColor("active_bgcolor", context);
    var activeForegroundColor =
        widget.control.getColor("active_foreground_color", context);
    var gradient = widget.control.getGradient("gradient", theme);
    var gradientBoxShape =
        widget.control.getBoxShape("gradient_box_shape", BoxShape.rectangle)!;
    var elevation = widget.control.getDouble("elevation", 6.0)!;
    var buttonSize = widget.control.getSize("button_size", Size(56.0, 56.0))!;
    var childrenButtonSize =
        widget.control.getSize("children_button_size", Size(56.0, 56.0))!;
    var mini = widget.control.getBool("mini", false)!;
    var overlayOpacity = widget.control.getDouble("overlay_opacity", 0.8)!;
    var overlayColor = widget.control.getColor("overlay_color", context);
    var heroTag = widget.control.getString("hero_tag");
    var icon = widget.control.getIconData("icon");
    var activeIcon = widget.control.getIconData("active_icon");
    var child = widget.control.buildWidget("child");
    var activeChild = widget.control.buildWidget("active_child");
    var switchLabelPosition =
        widget.control.getBool("switch_label_position", false)!;
    var useRotationAnimation =
        widget.control.getBool("use_rotation_animation", true)!;
    var label = widget.control.buildWidget("label");
    var activeLabel = widget.control.buildWidget("active_label");
    var direction = widget.control.getString("direction");
    var closeManually = widget.control.getBool("close_manually", false)!;
    var renderOverlay = widget.control.getBool("render_overlay", true)!;
    var curve = widget.control.getCurve("curve", Curves.fastOutSlowIn)!;
    var animationDuration = widget.control
        .getDuration("animation_duration", Duration(milliseconds: 150))!;
    var isOpenOnStart = widget.control.getBool("is_open_on_start", false)!;
    var closeDialOnPop = widget.control.getBool("close_dial_on_pop", true)!;
    var childMargin = widget.control.getMargin(
        "child_margin", EdgeInsets.symmetric(horizontal: 16, vertical: 0))!;
    var childPadding = widget.control
        .getPadding("child_padding", EdgeInsets.symmetric(vertical: 5))!;
    var spaceBetweenChildren =
        widget.control.getDouble("space_between_children");
    var spacing = widget.control.getDouble("spacing");
    var animationCurve = widget.control.getCurve("animation_curve");

    // widget build
    Widget fabButton = SpeedDial(
      children: parseChildDial(children, context),
      visible: visible,
      backgroundColor: bgColor,
      foregroundColor: foregroundColor,
      activeBackgroundColor: activeBgColor,
      activeForegroundColor: activeForegroundColor,
      gradient: gradient,
      gradientBoxShape: gradientBoxShape,
      elevation: elevation,
      buttonSize: buttonSize,
      childrenButtonSize: childrenButtonSize,
      mini: mini,
      overlayOpacity: overlayOpacity,
      overlayColor: overlayColor,
      heroTag: heroTag,
      icon: icon,
      activeIcon: activeIcon,
      child: child,
      activeChild: activeChild,
      switchLabelPosition: switchLabelPosition,
      useRotationAnimation: useRotationAnimation,
      label: label,
      activeLabel: activeLabel,
      direction: _getDirection(direction),
      closeManually: closeManually,
      renderOverlay: renderOverlay,
      curve: curve,
      animationDuration: animationDuration,
      isOpenOnStart: isOpenOnStart,
      closeDialOnPop: closeDialOnPop,
      childMargin: childMargin,
      childPadding: childPadding,
      spaceBetweenChildren: spaceBetweenChildren,
      spacing: spacing,
      animationCurve: animationCurve,
      onOpen: () {
        WidgetsBinding.instance.addPostFrameCallback((_) {
          backend.triggerControlEvent(
              widget.control, "open", "floating button open!");
        });
      },
      onClose: () {
        WidgetsBinding.instance.addPostFrameCallback((_) {
          backend.triggerControlEvent(
              widget.control, "close", "floating button close!");
        });
      },
    );

    return LayoutControl(
      control: widget.control,
      child: fabButton,
    );
  }
}

SpeedDialDirection _getDirection(String? type) {
  switch (type) {
    case "up":
      return SpeedDialDirection.up;
    case "down":
      return SpeedDialDirection.down;
    case "left":
      return SpeedDialDirection.left;
    case "right":
      return SpeedDialDirection.right;
    default:
      return SpeedDialDirection.up;
  }
}
