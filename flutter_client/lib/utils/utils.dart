import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';

void showSnackBar(String content, BuildContext context){
  ScaffoldMessenger.of(context)
  ..hideCurrentSnackBar()
  ..showSnackBar(SnackBar(content: Text(content)));
}