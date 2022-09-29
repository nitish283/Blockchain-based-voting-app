
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import './sidemenu.dart';

class CastVoteScreen extends StatefulWidget {
  var _eid;
  var _vid, _logout;
  CastVoteScreen(this._eid, this._vid, this._logout);
  
  @override
  State<StatefulWidget> createState() {
    return CastVoteScreenState();
  }
}

class CastVoteScreenState extends State<CastVoteScreen> {
  var candidates =[];
  var candidateLabels = [];
  @override
  void initState() {
    _getCandidates();
    super.initState();
  }
  
  @override
  Widget build(BuildContext context) {
    candidateLabels = [];
    for(var i = 0; i < candidates.length; i++)
    {
      candidateLabels.add(
        GestureDetector(
                  onTap: () {
                      //send Cast Vote Request to api
                      _castVote(widget._eid, widget._vid, candidates[i]["candidate_id"]);
                      
                      Navigator.pop(context);
                  },
                  child: Container(child: Column(children: [
                    const SizedBox(height: 30,),
                    Text("Candidate ID: ${candidates[i]["candidate_id"]}", style: TextStyle(color: Colors.blue)),
                    Text("Name: ${candidates[i]["name"]}", style: TextStyle(color: Colors.blue)),
                    Text("Dept: ${candidates[i]["dept"]}", style: TextStyle(color: Colors.blue)),
                    Text("Year: ${candidates[i]["year"]}", style: TextStyle(color: Colors.blue)),
                    ]
                    )
                  )
              )
      );
    }
    return Scaffold(
        drawer: SideDrawer(widget._logout),
        appBar: AppBar(
          backgroundColor: Colors.blueAccent,
          title: Text("Vote in Election: ${widget._eid}"),
        ),
        body: Center(
          child: Padding(
            padding: const EdgeInsets.all(20.0),
            child: ListView(children: [
              const SizedBox(
                height: 10,
              ),
              ...candidateLabels,
            ]),
          ),
        ));
  }

  _castVote(_eid, _vid, _cid) async{
    SharedPreferences _prefs = await SharedPreferences.getInstance();
    var _vid = _prefs.getString("vid") ?? "";
    var _password = _prefs.getString("password") ?? "";
    
    final resp = await http.post(
        Uri.parse('http://10.0.2.2:5000/castvote'),
        headers: <String, String>{
            'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(<String, String>{
          'election_id': _eid,
          'vid': _vid,
          'candidate_id': _cid,
          'credentials': _password
          }),
      );
      if(jsonDecode(resp.body) == 1){
        print("Vote Casted Succesfully...");
      } 
      else{
        print("Nahi Hua");
      }
  }

  _getCandidates() async{
      final resp = await http.post(
        Uri.parse('http://10.0.2.2:5000/getcandidates'),
        headers: <String, String>{
            'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(<String, String>{
          'election_id': widget._eid,
          }),
      );
      setState(() {
        candidates = jsonDecode(resp.body)['result']; 
      });
      
      
  }
}

