import 'package:flutter/material.dart';
import 'package:flutter_client/pages/auth/login_page.dart';
import 'package:flutter_client/services/auth_service.dart';
import 'package:flutter_client/utils/utils.dart';

class ConfirmSignupPage extends StatefulWidget {
  final String email;
  static MaterialPageRoute<dynamic> route(String email) => MaterialPageRoute(builder: (context)=> ConfirmSignupPage(email: email,));
  const ConfirmSignupPage({super.key, required this.email});

  @override
  State<ConfirmSignupPage> createState() => _ConfirmSignupPageState();
}

class _ConfirmSignupPageState extends State<ConfirmSignupPage> {
  final otpController = TextEditingController();
  late TextEditingController emailController ;
  final formKey = GlobalKey<FormState>();
  final AuthService authService = AuthService();

@override
  void initState() {
    // TODO: implement initState
    super.initState();
    emailController = TextEditingController(text: widget.email);
  }

@override
  void dispose() {
    otpController.dispose();
    emailController.dispose();
    super.dispose();
  }

void signup() async {
  if(formKey.currentState!.validate()){
    try{
      final res = await authService.signUpUser(
      name: nameController.text.trim(), 
      email: emailController.text.trim(), 
      password: passwordController.text.trim()
      );
      showSnackBar(res, context);
    }catch(e){
      showSnackBar(e.toString(), context);
    }
    
  }
}

  @override
  Widget build(BuildContext context) {
    return Scaffold(
          body: Padding(
            padding: const EdgeInsets.all(15.0),
            child: Form(
              key: formKey,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                   Text('Confirm-Sign-up', style: TextStyle(
                    fontSize: 50,
                    fontWeight: FontWeight.bold,
                    ),
                    ),
                   const SizedBox(height:30),
                   
                   TextFormField(
                    controller: emailController,
                    decoration: InputDecoration(
                      hintText: 'Email',
                    ),
                    validator: (value) {
                      if(value!.trim().isEmpty){
                        return 'Field cannot be empty';
                      }
                      return null; 
                    },
                   ), 
                   const SizedBox(height:15),
                   TextFormField( 
                    controller: otpController,
                    obscureText: true,
                    enableSuggestions: false,
                    autocorrect: false,
                    decoration: InputDecoration(
                      hintText: 'OTP',
                    ),
                    validator: (value) {
                      if(value!.trim().isEmpty){
                        return 'Field cannot be empty';
                      }
                      return null; 
                    },
                   ), 
                    const SizedBox(height:20),
              
                    ElevatedButton(onPressed: signup,
                      child: Text('Sign-up', style: TextStyle(
                        color: Colors.white,
                        fontSize: 16,
                        ),
                      ),           
                    ),
                     
                ],
              ),
            ),
          ),
    );
  }
}

