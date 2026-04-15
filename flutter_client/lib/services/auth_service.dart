import 'dart:convert';

import 'package:http/http.dart' as http;

class AuthService{
  final backendUrl = "http://localhost:8000/auth";
    Future<String> signUpUser({
      required String name,
      required String email,
      required String password,
    })async{
        final res = await http.post(
          Uri.parse("$backendUrl/signup"), 
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({
            "name": name,
            "email": email,
            "password": password,
          }),
        );

        if(res.statusCode!= 200){
          print(res.body);
          throw jsonDecode(res.body)['detail'] ?? 'an error occured';
        }
        return jsonDecode(res.body)['message'] ?? 'sign up successful, please verify your email ';
    }

     Future<String> confirmSignUpUser({
      required String email,
      required String otp,
      
    })async{
        final res = await http.post(
          Uri.parse("$backendUrl/confirm-signup"), 
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({
            "name": name,
            "email": email,
            "password": password,
          }),
        );

        if(res.statusCode!= 200){
          print(res.body);
          throw jsonDecode(res.body)['detail'] ?? 'an error occured';
        }
        return jsonDecode(res.body)['message'] ?? 'sign up successful, please verify your email ';
    }
}