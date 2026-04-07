import 'package:flutter/material.dart';
import 'package:flutter_client/pages/auth/signup_page.dart';

class LoginPage extends StatefulWidget {
  static route() => MaterialPageRoute(builder: (context)=> LoginPage());
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
          body: Padding(
            padding: const EdgeInsets.all(15.0),
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
                  decoration: InputDecoration(
                    hintText: 'Email',
                  ),
                 ), 
                 const SizedBox(height:15),
                 TextFormField( 
                  decoration: InputDecoration(
                    hintText: 'Password',
                  ),
                 ), 
                  const SizedBox(height:20),

                  ElevatedButton(onPressed: (){},
                    child: Text('Sign-up', style: TextStyle(
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
    );
  }
}

