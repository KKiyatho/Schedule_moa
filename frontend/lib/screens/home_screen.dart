import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../models/schedule_item.dart';
import '../models/user.dart';
import '../services/api_service.dart';
import 'calendar_screen.dart';
import 'item_detail_screen.dart';

class HomeScreen extends StatefulWidget {
  final User user;
  final VoidCallback onLogout;

  const HomeScreen({
    Key? key,
    required this.user,
    required this.onLogout,
  }) : super(key: key);

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _selectedIndex = 0;
  List<ScheduleItem> _todayItems = [];
  List<ScheduleItem> _overdueItems = [];
  List<ScheduleItem> _upcomingItems = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadDashboard();
  }

  Future<void> _loadDashboard() async {
    setState(() => _isLoading = true);

    try {
      final items = await apiService.getScheduleItems();
      if (items != null) {
        final today = DateTime.now();
        final tomorrow = today.add(const Duration(days: 1));

        setState(() {
          _todayItems = items
              .where((item) =>
                  item.isDueToday && item.status != ItemStatus.completed)
              .toList();

          _overdueItems = items
              .where((item) =>
                  item.isOverdue && item.status != ItemStatus.completed)
              .toList();

          _upcomingItems = items
              .where((item) =>
                  item.dueDate != null &&
                  item.dueDate!.isAfter(tomorrow) &&
                  item.status != ItemStatus.completed)
              .take(5)
              .toList();
        });
      }
    } catch (e) {
      print('Load dashboard error: $e');
    } finally {
      if (mounted) {
        setState(() => _isLoading = false);
      }
    }
  }

  Widget _buildDashboard() {
    return RefreshIndicator(
      onRefresh: _loadDashboard,
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // Header
          Padding(
            padding: const EdgeInsets.only(bottom: 24),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  '환영합니다, ${widget.user.username}!',
                  style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                ),
                Text(
                  DateFormat('EEEE, MMMM d, yyyy', 'ko_KR')
                      .format(DateTime.now()),
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        color: Colors.grey[600],
                      ),
                ),
              ],
            ),
          ),

          // Summary cards
          Row(
            children: [
              Expanded(
                child: _buildSummaryCard(
                  icon: Icons.today,
                  title: '오늘',
                  count: _todayItems.length,
                  color: Colors.blue,
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: _buildSummaryCard(
                  icon: Icons.warning,
                  title: '지연됨',
                  count: _overdueItems.length,
                  color: Colors.red,
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),

          // Overdue section
          if (_overdueItems.isNotEmpty) ...[
            _buildSectionTitle('🔴 지연된 일정'),
            ..._overdueItems.take(3).map(_buildItemCard),
            const SizedBox(height: 16),
          ],

          // Today section
          if (_todayItems.isNotEmpty) ...[
            _buildSectionTitle('📅 오늘의 일정'),
            ..._todayItems.map(_buildItemCard),
            const SizedBox(height: 16),
          ],

          // Upcoming section
          if (_upcomingItems.isNotEmpty) ...[
            _buildSectionTitle('🗓️ 예정된 일정'),
            ..._upcomingItems.map(_buildItemCard),
          ],

          if (_todayItems.isEmpty &&
              _overdueItems.isEmpty &&
              _upcomingItems.isEmpty)
            Center(
              child: Padding(
                padding: const EdgeInsets.symmetric(vertical: 48),
                child: Column(
                  children: [
                    Icon(Icons.check_circle,
                        size: 64, color: Colors.grey[300]),
                    const SizedBox(height: 16),
                    Text(
                      '할 일이 없습니다!',
                      style: Theme.of(context).textTheme.titleLarge,
                    ),
                  ],
                ),
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildSummaryCard({
    required IconData icon,
    required String title,
    required int count,
    required Color color,
  }) {
    return Card(
      elevation: 0,
      color: color.withOpacity(0.1),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(icon, color: color, size: 32),
            const SizedBox(height: 12),
            Text(
              title,
              style: Theme.of(context).textTheme.bodyMedium,
            ),
            const SizedBox(height: 8),
            Text(
              count.toString(),
              style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                    color: color,
                    fontWeight: FontWeight.bold,
                  ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSectionTitle(String title) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 12),
      child: Text(
        title,
        style: Theme.of(context).textTheme.titleMedium?.copyWith(
              fontWeight: FontWeight.bold,
            ),
      ),
    );
  }

  Widget _buildItemCard(ScheduleItem item) {
    Color statusColor = Colors.grey;
    IconData statusIcon = Icons.circle_outlined;

    switch (item.type) {
      case ItemType.schedule:
        statusColor = Colors.blue;
        statusIcon = Icons.event;
        break;
      case ItemType.deadline:
        statusColor = Colors.orange;
        statusIcon = Icons.hourglass_bottom;
        break;
      case ItemType.todo:
        statusColor = Colors.green;
        statusIcon = Icons.task_alt;
        break;
    }

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      child: ListTile(
        leading: Icon(statusIcon, color: statusColor),
        title: Text(item.title),
        subtitle: item.dueDate != null
            ? Text(DateFormat('MMM d, yyyy').format(item.dueDate!))
            : null,
        trailing: item.status == ItemStatus.completed
            ? const Icon(Icons.check_circle, color: Colors.green)
            : null,
        onTap: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => ItemDetailScreen(item: item),
            ),
          ).then((_) => _loadDashboard());
        },
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Schedule Moa'),
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () {
              apiService.clearAuthToken();
              widget.onLogout();
            },
          ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : (_selectedIndex == 0
              ? _buildDashboard()
              : CalendarScreen(onRefresh: _loadDashboard)),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: (index) => setState(() => _selectedIndex = index),
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: '홈',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.calendar_month),
            label: '캘린더',
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // Add new item
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => const ItemDetailScreen(item: null),
            ),
          ).then((_) => _loadDashboard());
        },
        child: const Icon(Icons.add),
      ),
    );
  }
}
