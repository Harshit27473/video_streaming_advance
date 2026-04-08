import 'package:flutter/material.dart';
import 'package:flutter_client/pages/auth/signup_page.dart';

class LoginPage extends StatefulWidget {
  static MaterialPageRoute<dynamic> route() => MaterialPageRoute(builder: (context)=> LoginPage());
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
 
  final emailController = TextEditingController();
  final passwordController = TextEditingController();
  final formKey = GlobalKey<FormState>();

@override
  void dispose() {
   
    emailController.dispose();
    passwordController.dispose();
    super.dispose();
  }

  void login(){
  if(formKey.currentState!.validate()){
    print(emailController.text);
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
                   Text('Sign In.', style: TextStyle(
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
                    controller: passwordController,
                    obscureText: true,
                    enableSuggestions: false,
                    autocorrect: false,
                    decoration: InputDecoration(
                      hintText: 'Password',
                    ),
                    validator: (value) {
                        if(value!.trim().isEmpty){
                          return 'Field cannot be empty';
                        }
                        return null; 
                      },
                   ), 
                    const SizedBox(height:20),
              
                    ElevatedButton(onPressed: login,
                      child: Text('Sign-in.', style: TextStyle(
                        color: Colors.white,
                        fontSize: 16,
                        ),
                      ),           
                    ),
                    const SizedBox(height:20),
                      GestureDetector(
                      onTap: (){
                        Navigator.of(context).push(SignupPage.route());
                      },
                      child: RichText(text: TextSpan(
                        text: 'Don\'t have an account?',
                        style: Theme.of(context).textTheme.titleMedium,
                        children: [
                            TextSpan(
                              text: 'Sign Up',
                              style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold, color: Colors.green),
                              ),
                        ],
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

