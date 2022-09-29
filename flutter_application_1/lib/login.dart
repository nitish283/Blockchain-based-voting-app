
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class LoginPage extends StatefulWidget {
  var _login;
  LoginPage(this._login);

  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {

  TextEditingController _vidController = TextEditingController();
  TextEditingController _passwordController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          backgroundColor: Colors.blueAccent,
          title: const Text("Login Page"),
        ),
        body: Center(
          child: Padding(
            padding: const EdgeInsets.all(20.0),
            child: Column(children: [
              field(
                  _vidController, const Icon(Icons.email_outlined), "Enter Voter ID"),
              const SizedBox(
                height: 10,
              ),
              field(_passwordController,const Icon(Icons.lock), "Enter Password"),
              const SizedBox(
                height: 10,
              ),
              GestureDetector(
                  onTap: () {
                      _authUser();

                  },
                  child: const Text("Login", style: TextStyle(color: Colors.blue)
                  )
              ),
            ]),
          ),
        ));
  }

  field(TextEditingController controller, Icon icon, String label) {
    return Container(
      decoration: BoxDecoration(
          boxShadow: [
            const BoxShadow(
              color: Colors.white,
              blurRadius: 5.0,
            ),
          ],
          borderRadius: BorderRadius.circular(30),
          border: Border.all(color: const Color(0xffECEBEB))),
      child: TextField(
          controller: controller,
          //onChanged: onchange,

          decoration: InputDecoration(
            contentPadding: const EdgeInsets.only(top: 8, left: 20),
            focusedBorder: InputBorder.none,
            enabledBorder: InputBorder.none,
            errorBorder: InputBorder.none,
            disabledBorder: InputBorder.none,
            border: InputBorder.none,
            suffixIcon: icon,
            labelText: label,
            labelStyle:
                const TextStyle(fontSize: 14, decoration: TextDecoration.none),
          )),
    );
  }

  void _store_user() {
    SharedPreferences.getInstance().then(
      (prefs) {
        prefs.setString('vid', _vidController.text);
        prefs.setString('password', _passwordController.text);
      },
    );
  }
  
  Widget _popupDialog(BuildContext context, text) {
  return AlertDialog(
    title: const Text('Error'),
    content: Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.start,
      children: <Widget>[
        Text(text),
      ],
    ),
    actions: <Widget>[
      TextButton(
        onPressed: () {
          Navigator.of(context).pop();
        },
        child: const Text('Close'),
      ),
    ],
  );
}
  _authUser() async{
      final response = await http.post(
        Uri.parse('http://10.0.2.2:5000/signin'),
        headers: <String, String>{
            'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(<String, String>{
          'vid': _vidController.text,
          'password': _passwordController.text
        }),
      );
      if(jsonDecode(response.body)==1){
      _store_user();
      widget._login();
      }
      else if(jsonDecode(response.body)==-1){
        showDialog(
              context: context,
              builder: (BuildContext context) => _popupDialog(context,"Wrong Password"),
        );
      }
      else if(jsonDecode(response.body)==-2){
        showDialog(
              context: context,
              builder: (BuildContext context) => _popupDialog(context,"User not registered"),
        );
      }
      else {
        showDialog(
              context: context,
              builder: (BuildContext context) => _popupDialog(context,"An error occurred!"),
        );
      }
  }
}
