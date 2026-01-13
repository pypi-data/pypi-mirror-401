import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter_speed_dial/flutter_speed_dial.dart';

List<SpeedDialChild> parseChildDial(
    List<Control> children, BuildContext context) {
  return children.map((children) => _childDial(children, context)).toList();
}

SpeedDialChild _childDial(Control child, BuildContext context) {
  final theme = Theme.of(context);
  var backend = FletBackend.of(context);

  var label = child.getString("label");
  var labelStyle = child.getTextStyle("label_style", theme);
  var labelBgcolor = child.getColor("label_bgcolor", context);
  var labelWidget = child.buildWidget("label_widget");
  var labelShadow = child.getBoxShadows("label_shadow", theme);
  var childs = child.buildIconOrWidget("child");
  var bgColor = child.getColor("bgcolor", context);
  var foregroundColor = child.getColor("foreground_color", context);
  var shape = child.getShape("shape", theme);
  var visible = child.getBool("visible", true)!;
  var elevation = child.getDouble("elevation");

  return SpeedDialChild(
    label: label,
    labelStyle: labelStyle,
    labelBackgroundColor: labelBgcolor,
    labelWidget: labelWidget,
    labelShadow: labelShadow,
    child: childs,
    backgroundColor: bgColor,
    foregroundColor: foregroundColor,
    shape: shape,
    visible: visible,
    elevation: elevation,
    onTap: () {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        backend.triggerControlEvent(child, "tap", "child fab on tap!");
      });
    },
    onLongPress: () {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        backend.triggerControlEvent(
            child, "long_press", "child fab on long press!");
      });
    },
  );
}
