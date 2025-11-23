import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'JIS Password Generator',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.indigo),
        useMaterial3: true,
      ),
      home: const PasswordGeneratorScreen(),
    );
  }
}

class PasswordGeneratorScreen extends StatefulWidget {
  const PasswordGeneratorScreen({super.key});

  @override
  State<PasswordGeneratorScreen> createState() => _PasswordGeneratorScreenState();
}

class _PasswordGeneratorScreenState extends State<PasswordGeneratorScreen> {
  final TextEditingController _keywordController = TextEditingController();
  final TextEditingController _keyController = TextEditingController();
  
  String _resultMessage = "Generate a password";
  bool _isLoading = false;

  Future<void> _generatePassword() async {
    final keyword = _keywordController.text;
    final keyString = _keyController.text;

    if (keyword.isEmpty || keyString.isEmpty) {
      setState(() => _resultMessage = "入力が空です");
      return;
    }

    List<int> keyList = [];
    try {
      keyList = keyString.replaceAll(RegExp(r'[^0-9,]'), '').split(',')
          .where((s) => s.isNotEmpty).map((s) => int.parse(s)).toList();
      if (keyList.isEmpty) throw Exception();
    } catch (e) {
      setState(() => _resultMessage = "秘密鍵の形式が正しくありません");
      return;
    }

    setState(() {
      _isLoading = true;
      _resultMessage = "Djangoに問い合わせ中...";
    });

    // ★Windowsアプリとして動かす場合は localhost (127.0.0.1) でOK
    final url = Uri.parse('http://10.84.147.119/api/generate/');

    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'keyword': keyword, 'key_list': keyList}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() => _resultMessage = data['password']);
      } else {
        setState(() => _resultMessage = "エラー: ${response.statusCode}");
      }
    } catch (e) {
      setState(() => _resultMessage = "通信失敗: Djangoは起動していますか？\n$e");
    } finally {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Password Generator'), backgroundColor: Theme.of(context).colorScheme.inversePrimary),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(32.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              TextField(controller: _keywordController, decoration: const InputDecoration(labelText: 'Keyword (e.g. apple)', border: OutlineInputBorder())),
              const SizedBox(height: 16),
              TextField(controller: _keyController, decoration: const InputDecoration(labelText: 'Private Key (e.g. 3,2,5)', border: OutlineInputBorder())),
              const SizedBox(height: 32),
              FilledButton.icon(
                onPressed: _isLoading ? null : _generatePassword,
                icon: _isLoading ? const SizedBox.shrink() : const Icon(Icons.vpn_key),
                label: _isLoading ? const CircularProgressIndicator(color: Colors.white) : const Text('生成する'),
                style: FilledButton.styleFrom(minimumSize: const Size(double.infinity, 50)),
              ),
              const SizedBox(height: 32),
              Container(
                padding: const EdgeInsets.all(16),
                width: double.infinity,
                decoration: BoxDecoration(color: Colors.grey.shade200, borderRadius: BorderRadius.circular(8)),
                child: SelectableText(_resultMessage, style: const TextStyle(fontSize: 20, fontFamily: 'monospace', fontWeight: FontWeight.bold), textAlign: TextAlign.center),
              ),
            ],
          ),
        ),
      ),
    );
  }
}