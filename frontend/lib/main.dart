import 'package:flutter/material.dart';
import 'package:dio/dio.dart';
import 'package:intl/intl.dart';

void main() {
  runApp(const ScheduleMoaApp());
}

class ScheduleMoaApp extends StatelessWidget {
  const ScheduleMoaApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Schedule Moa',
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF4648D4),
          brightness: Brightness.light,
        ),
        fontFamily: 'Inter',
      ),
      home: const HomePage(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final Dio dio = Dio();
  final String apiBase = 'http://localhost:8000/api/v1';
  String? authToken;
  bool isLoggedIn = false;
  String userName = 'User';
  int scheduleCount = 0;
  int deadlineCount = 0;
  int todoCount = 0;
  List<Map<String, dynamic>> deadlines = [];
  List<Map<String, dynamic>> todos = [];

  @override
  void initState() {
    super.initState();
    _loadAuthToken();
  }

  Future<void> _loadAuthToken() async {
    setState(() => isLoggedIn = false);
  }

  Future<void> _login(String email, String fullName) async {
    try {
      final response = await dio.post(
        '$apiBase/auth/register',
        data: {'email': email, 'full_name': fullName},
        options: Options(
          contentType: 'application/json',
          responseType: ResponseType.json,
        ),
      );

      if (response.statusCode == 200) {
        setState(() {
          authToken = response.data['access_token'];
          isLoggedIn = true;
          userName = fullName.split(' ').first;
        });
        _loadDashboard();
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('로그인 성공!')),
          );
        }
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('로그인 실패: $e')),
        );
      }
    }
  }

  Future<void> _loadDashboard() async {
    if (authToken == null) return;

    try {
      final response = await dio.get(
        '$apiBase/items/',
        options: Options(headers: {'Authorization': 'Bearer $authToken'}),
      );

      if (response.statusCode == 200) {
        final items = List<Map<String, dynamic>>.from(response.data ?? []);
        final deadlineList =
            items.where((i) => i['item_type'] == 'deadline').toList();
        final todoList = items.where((i) => i['item_type'] == 'todo').toList();

        setState(() {
          deadlines = deadlineList;
          todos = todoList;
          scheduleCount = items.where((i) => i['item_type'] == 'schedule').length;
          deadlineCount = deadlineList.length;
          todoCount = todoList.where((t) => t['is_completed'] != true).length;
        });
      }
    } catch (e) {
      print('Dashboard error: $e');
    }
  }

  Future<void> _toggleTodo(String itemId, bool isCompleted) async {
    if (authToken == null) return;
    try {
      if (isCompleted) {
        await dio.post(
          '$apiBase/items/$itemId/complete',
          options: Options(headers: {'Authorization': 'Bearer $authToken'}),
        );
      }
      _loadDashboard();
    } catch (e) {
      print('Toggle error: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    if (!isLoggedIn) {
      return Scaffold(
        body: LoginForm(onLogin: _login),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('Schedule Moa'),
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.notifications),
            onPressed: () {},
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: CircleAvatar(
              child: Text(userName[0].toUpperCase()),
            ),
          ),
        ],
      ),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            DrawerHeader(
              decoration: BoxDecoration(
                color: Theme.of(context).colorScheme.primary,
              ),
              child: Text(
                'Schedule Moa',
                style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                      color: Colors.white,
                    ),
              ),
            ),
            ListTile(
              leading: const Icon(Icons.dashboard),
              title: const Text('Dashboard'),
              selected: true,
              onTap: () => Navigator.pop(context),
            ),
            ListTile(
              leading: const Icon(Icons.description),
              title: const Text('Documents'),
              onTap: () => Navigator.pop(context),
            ),
            ListTile(
              leading: const Icon(Icons.calendar_month),
              title: const Text('Calendar'),
              onTap: () => Navigator.pop(context),
            ),
            ListTile(
              leading: const Icon(Icons.checklist),
              title: const Text('To-do List'),
              onTap: () => Navigator.pop(context),
            ),
            const Divider(),
            ListTile(
              leading: const Icon(Icons.settings),
              title: const Text('Settings'),
              onTap: () => Navigator.pop(context),
            ),
          ],
        ),
      ),
      body: RefreshIndicator(
        onRefresh: _loadDashboard,
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Hello, $userName!',
                style: Theme.of(context).textTheme.headlineLarge,
              ),
              const SizedBox(height: 8),
              Text(
                'You have $deadlineCount deadlines approaching today.',
                style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                      color: Colors.grey[600],
                    ),
              ),
              const SizedBox(height: 24),
              GridView.count(
                crossAxisCount:
                    MediaQuery.of(context).size.width > 600 ? 3 : 1,
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                childAspectRatio: 1.2,
                children: [
                  _buildSummaryCard(
                    "Today's Schedule",
                    scheduleCount.toString(),
                    Icons.calendar_today,
                    Colors.blue,
                  ),
                  _buildSummaryCard(
                    'Pending Deadlines',
                    deadlineCount.toString(),
                    Icons.timer,
                    Colors.red,
                  ),
                  _buildSummaryCard(
                    'Remaining To-dos',
                    todoCount.toString(),
                    Icons.fact_check,
                    Colors.green,
                  ),
                ],
              ),
              const SizedBox(height: 24),
              Text(
                'Urgent Deadlines',
                style: Theme.of(context).textTheme.titleLarge,
              ),
              const SizedBox(height: 12),
              if (deadlines.isEmpty)
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Text('No urgent deadlines yet.',
                        style: Theme.of(context).textTheme.bodyMedium),
                  ),
                )
              else
                ListView.builder(
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  itemCount: deadlines.length,
                  itemBuilder: (context, index) {
                    final deadline = deadlines[index];
                    return Card(
                      margin: const EdgeInsets.only(bottom: 8),
                      child: ListTile(
                        title: Text(deadline['title'] ?? 'Untitled'),
                        subtitle: Text(
                          DateFormat('MMM dd, yyyy').format(
                            DateTime.parse(deadline['due_date']),
                          ),
                        ),
                        trailing: const Chip(
                          label: Text('High Priority'),
                        ),
                      ),
                    );
                  },
                ),
              const SizedBox(height: 24),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'In-progress To-dos',
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                  FloatingActionButton.small(
                    onPressed: () => _showAddTodoDialog(),
                    child: const Icon(Icons.add),
                  ),
                ],
              ),
              const SizedBox(height: 12),
              if (todos.isEmpty)
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Text('No to-dos yet.',
                        style: Theme.of(context).textTheme.bodyMedium),
                  ),
                )
              else
                ListView.builder(
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  itemCount: todos.length,
                  itemBuilder: (context, index) {
                    final todo = todos[index];
                    return Card(
                      margin: const EdgeInsets.only(bottom: 8),
                      child: CheckboxListTile(
                        value: todo['is_completed'] ?? false,
                        onChanged: (bool? value) {
                          _toggleTodo(todo['id'], value ?? false);
                        },
                        title: Text(
                          todo['title'] ?? 'Untitled',
                          style: TextStyle(
                            decoration: (todo['is_completed'] ?? false)
                                ? TextDecoration.lineThrough
                                : null,
                          ),
                        ),
                      ),
                    );
                  },
                ),
            ],
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => _showUploadDialog(),
        icon: const Icon(Icons.cloud_upload),
        label: const Text('Upload'),
      ),
    );
  }

  Widget _buildSummaryCard(String title, String count, IconData icon,
      Color color) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              title,
              style: Theme.of(context).textTheme.labelSmall,
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  count,
                  style: Theme.of(context)
                      .textTheme
                      .headlineSmall
                      ?.copyWith(color: color),
                ),
                Icon(icon, color: color, size: 32),
              ],
            ),
          ],
        ),
      ),
    );
  }

  void _showUploadDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Upload Document'),
        content: const Text('Select a PDF, image, or document file.'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.pop(context);
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Upload feature coming soon!')),
              );
            },
            child: const Text('Select File'),
          ),
        ],
      ),
    );
  }

  void _showAddTodoDialog() {
    final controller = TextEditingController();
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Add To-do'),
        content: TextField(
          controller: controller,
          decoration: const InputDecoration(hintText: 'Enter to-do...'),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.pop(context);
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('To-do added!')),
              );
            },
            child: const Text('Add'),
          ),
        ],
      ),
    );
  }
}

class LoginForm extends StatefulWidget {
  final Function(String, String) onLogin;

  const LoginForm({Key? key, required this.onLogin}) : super(key: key);

  @override
  State<LoginForm> createState() => _LoginFormState();
}

class _LoginFormState extends State<LoginForm> {
  final emailController = TextEditingController();
  final nameController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            width: 64,
            height: 64,
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.primary,
              borderRadius: BorderRadius.circular(16),
            ),
            child: const Center(
              child: Text('SM',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 32,
                    fontWeight: FontWeight.bold,
                  )),
            ),
          ),
          const SizedBox(height: 24),
          Text('Schedule Moa',
              style: Theme.of(context).textTheme.headlineLarge),
          const SizedBox(height: 8),
          Text('AI-Powered Schedule Management',
              style: Theme.of(context).textTheme.bodyMedium),
          const SizedBox(height: 32),
          TextField(
            controller: emailController,
            decoration: InputDecoration(
              labelText: 'Email',
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
            ),
          ),
          const SizedBox(height: 16),
          TextField(
            controller: nameController,
            decoration: InputDecoration(
              labelText: 'Full Name',
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
            ),
          ),
          const SizedBox(height: 24),
          ElevatedButton(
            onPressed: () {
              widget.onLogin(emailController.text, nameController.text);
            },
            style: ElevatedButton.styleFrom(
              minimumSize: const Size.fromHeight(48),
            ),
            child: const Text('Sign In / Register'),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    emailController.dispose();
    nameController.dispose();
    super.dispose();
  }
}
