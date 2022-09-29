//import 'dart:html';
//import 'dart:io';

import 'package:flutter/material.dart';
//import 'package:flutter/services.dart';

import 'package:shared_preferences/shared_preferences.dart';
import './VoteScreen.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import './sidemenu.dart';

class Elections extends StatefulWidget {
  var _logout;
  var voter_id;
  Elections(this._logout, this.voter_id);
  @override
  State<StatefulWidget> createState() {
    return EcState();
  }
}

class EcState extends State<Elections> {
  TextEditingController _eidController = TextEditingController();
  var btns = [];
  var btnlabels = [];
  @override
  void initState() {
    _ListElections();
    super.initState();
  }

  _ListElections() async {
    try {
      SharedPreferences _prefs = await SharedPreferences.getInstance();
      var _vid = _prefs.getString("vid") ?? "";
      print(_vid);

      final response = await http.post(
        Uri.parse('http://10.0.2.2:5000/active'),
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(<String, String>{
          'voter_id': _vid,
        }),
      );
      setState(() {
        btns = jsonDecode(response.body)["result"];
      });
    } catch (e) {
      print(e);
    }
  }

  @override
  Widget build(BuildContext context) {
    btnlabels = [];
    for (int i = 0; i < btns.length; i++) {
      btnlabels.add(Column(children: [
        Container(
          width: 400,
          child: Table(
            //border: TableBorder.all(color: Colors.black),
            columnWidths: const {
              0: FractionColumnWidth(.35),
              1: FractionColumnWidth(.65),
            },
            children: [
              TableRow(children: [
                const Text("Post: "),
                Text("${btns[i]["post"]}",
                    style: const TextStyle(color: Colors.blue))
              ]),
              TableRow(children: [
                const Text("Organisation: "),
                Text("${btns[i]["organisation"]}",
                    style: const TextStyle(color: Colors.blue))
              ]),
              TableRow(children: [
                const Text("Election Date: "),
                Text("${btns[i]["election_date"]}",
                    style: const TextStyle(color: Colors.blue))
              ]),
              TableRow(children: [
                const Text("Election ID: "),
                Text("${btns[i]["election_id"]}",
                    style: const TextStyle(color: Colors.blue))
              ]),
              TableRow(children: [
                const Text(""),
                ElevatedButton(
                  //padding: const EdgeInsets.all(3.0),
                    onPressed: () {
                      //send Cast Vote Request to api
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                            builder: (context) => CastVoteScreen(
                                btns[i]["election_id"],
                                widget.voter_id,
                                widget._logout)),
                      );
                      //Navigator.pop(context);
                    },
                    child: const Icon(
                      IconData(0xe79b,
                          fontFamily: 'MaterialIcons',
                          matchTextDirection: true),
                      color: Color(0xFFFFFFFF),
                    )),
              ])
            ],
          ),
          decoration: BoxDecoration(border: Border.all(color: Colors.black)),
          padding: const EdgeInsets.all(5.0),
        ),
      ]));
    }
    return Scaffold(
        drawer: SideDrawer(widget._logout),
        appBar: AppBar(
          backgroundColor: Colors.blueAccent,
          title: const Text("Vote in Election"),
        ),
        body: Center(
          child: Padding(
            padding: const EdgeInsets.all(20.0),
            child: ListView(children: [...btnlabels]),
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
}

/*

  int c = 0;
  var stateContestants = {'bjp': 0, 'cong': 0, 'sad': 0, 'aap': 0};
  var centerContestants = {'bjp': 0, 'cong': 0, 'sad': 0, 'aap': 0};
  var statebuttons = [
    const ElevatedButton(onPressed: null, child: Text('Select a candidate'))
  ];
  var centerbuttons = [
    const ElevatedButton(onPressed: null, child: Text('Select a candidate'))
  ];
  void StateElections() {
    setState(() {
      c = 1;
      stateContestants
          .forEach((String key, int value) => statebuttons.add(ElevatedButton(
              child: Text('$key'),
              onPressed: () {
                setState(() {
                  stateContestants.update(key, (dynamic val) => value + 1,
                      ifAbsent: () => 0);
					c=4;
                });
              })));
    });
  }

  void CenterElections() {
    setState(() {
      c = 2;
      centerContestants
          .forEach((String key, int value) => centerbuttons.add(ElevatedButton(
              child: Text('$key'),
              onPressed: () {
                setState(() {
                  centerContestants.update(key, (dynamic val) => value + 1,
                      ifAbsent: () => 0);
					c=4;
                });
              })));
    });
  }

  @override
  Widget build(BuildContext context) {
    switch (c) {
    case 0:
        return Center(
          child: Column(children: [
            ElevatedButton(
                onPressed: StateElections,
                child: const Text("State Elections")),
            ElevatedButton(
                onPressed: CenterElections,
                child: const Text("Centre Elections")),
          ],
        ));
    case 1:
        return Center(
            child: Column(
          children: statebuttons,
        ));
	case 2:
        return Center(
            child: Column(
          children: centerbuttons,
        ));
	case 4:
		return Column(children: [const Text("Thank you for casting your vote! Please close this window for security reasons."),
    TextButton(onPressed: widget._logout, child: const Text("Close")),
      ]
    );
      default:
        return const Text("An error occurred! Try again later");
    }
  }
*/
