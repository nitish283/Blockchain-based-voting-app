import 'package:flutter/material.dart';
import './elections.dart';
import 'package:shared_preferences/shared_preferences.dart';
import './login.dart';


void main() => runApp(const VoteApp());



class VoteApp extends StatefulWidget {
  const VoteApp({Key? key}) : super(key: key);

  @override
  createState() => _VoteAppState();
}

class _VoteAppState extends State<VoteApp> {
  var _loggedIn = false;
  var _voter_id = "";

  @override
  void initState() {
    getVid();
    super.initState();
  }

  getVid() async{
    try {
      SharedPreferences _prefs = await SharedPreferences.getInstance();
      var _vid = _prefs.getString("vid") ?? "";
      var _password = _prefs.getString("password") ?? "";
      
      print(_vid);
      print(_password);
      if (_vid != "") {
        setState(() {
          _voter_id=_vid;
          _loggedIn = true;  
        });
      }
    }
    catch (e) {
      print(e);
    }
  }
  
  void _logout(){
    SharedPreferences.getInstance().then(
      (prefs) {
        prefs.setString('vid', "");
        prefs.setString('password', "");
      },
    );
    setState(() {
      _loggedIn = false;
    });
  }

  void _login(){
    setState(() {
      _loggedIn = true;
    });
  }

  @override
  Widget build(BuildContext context) {
    
    if(_loggedIn){
      return MaterialApp(home: Elections(_logout,_voter_id), debugShowCheckedModeBanner: false,);
    } 
    else{
      return MaterialApp(home: LoginPage(_login), debugShowCheckedModeBanner: false,);
    }
  }
}

/*
class MyStatefulWidget extends StatefulWidget {
  const MyStatefulWidget({Key? key}) : super(key: key);

  @override
  State<MyStatefulWidget> createState() => _MyStatefulWidgetState();
}

class _MyStatefulWidgetState extends State<MyStatefulWidget> {
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          TextFormField(
            decoration: const InputDecoration(
              hintText: 'Enter your email',
            ),
            validator: (String? value) {
              if (value == null || value.isEmpty) {
                return 'Please enter some text';
              }
              return null;
            },
          ),
          TextFormField(
            decoration: const InputDecoration(
              hintText: 'Enter Password',
            ),
            validator: (String? value) {
              if (value == null || value.isEmpty) {
                return 'Please enter some text';
              }
              return null;
            },
          ),
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 16.0),
            child: ElevatedButton(
              onPressed: () {
                // Validate will return true if the form is valid, or false if
                // the form is invalid.
                if (_formKey.currentState!.validate()) {
                  // Process data.
                  // Then call corresponding election screen
                  Navigator.push(context, MaterialPageRoute(builder: (ctxt) => const FirstScreen()));
                }
              },
              child: const Text('Submit'),
            ),
          ),
          const TextButton(
          child: Text("Click here to sign up"),
            onPressed : null,
            // Navigate to sign up
          ),
        ],
      ),
    );
  }
}


class FirstScreen extends StatefulWidget {
  const FirstScreen({Key? key}) : super(key: key);
  @override
  State<StatefulWidget> createState() {
    return FirstScreenState();
  }
}

class FirstScreenState extends State<FirstScreen> {
  int x = 0;
  void fun() {
    setState(() {
      x++;
    });
    //print(x);
  }


  @override
  Widget build(BuildContext context) {
    var arr = [
      ElevatedButton(
          onPressed: null,
          child: Text(
            "$x",
            style: const TextStyle(fontSize: 30, fontStyle: FontStyle.italic),
            textAlign: TextAlign.center,
          ))
    ];
    for (int i = 0; i < 5; i++) {
      arr.add(ElevatedButton(
        child: Text(
         'Button $i',
          style: const TextStyle(fontSize: 30, fontStyle: FontStyle.italic),
          textAlign: TextAlign.center,
        ),
        onPressed: fun,
      ));
    }
    return Scaffold(
        appBar: AppBar(
          title: const Text("Elections"),
        ),
        body: Elections(),
    );
  }
}


*/