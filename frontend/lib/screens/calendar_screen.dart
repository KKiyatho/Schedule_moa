import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../models/calendar.dart';
import '../models/schedule_item.dart';
import '../services/api_service.dart';

class CalendarScreen extends StatefulWidget {
  final VoidCallback onRefresh;

  const CalendarScreen({Key? key, required this.onRefresh}) : super(key: key);

  @override
  State<CalendarScreen> createState() => _CalendarScreenState();
}

class _CalendarScreenState extends State<CalendarScreen> {
  late DateTime _currentMonth;
  List<Calendar> _calendars = [];
  List<ScheduleItem> _items = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _currentMonth = DateTime.now();
    _loadCalendars();
  }

  Future<void> _loadCalendars() async {
    setState(() => _isLoading = true);

    try {
      final calendars = await apiService.getCalendars();
      final items = await apiService.getScheduleItems();

      if (mounted) {
        setState(() {
          _calendars = calendars ?? [];
          _items = items ?? [];
        });
      }
    } catch (e) {
      print('Load calendars error: $e');
    } finally {
      if (mounted) {
        setState(() => _isLoading = false);
      }
    }
  }

  List<ScheduleItem> _getItemsForDate(DateTime date) {
    return _items.where((item) {
      if (item.startDate == null && item.dueDate == null) return false;

      final checkDate = item.dueDate ?? item.startDate;
      if (checkDate == null) return false;

      return checkDate.year == date.year &&
          checkDate.month == date.month &&
          checkDate.day == date.day;
    }).toList();
  }

  Widget _buildCalendarGrid() {
    final firstDay = DateTime(_currentMonth.year, _currentMonth.month, 1);
    final lastDay = DateTime(_currentMonth.year, _currentMonth.month + 1, 0);
    final daysInMonth = lastDay.day;
    final firstWeekday = firstDay.weekday;

    final days = <Widget>[];

    // Empty cells for days before the month starts
    for (int i = 1; i < firstWeekday; i++) {
      days.add(const SizedBox());
    }

    // Days of the month
    for (int day = 1; day <= daysInMonth; day++) {
      final date = DateTime(_currentMonth.year, _currentMonth.month, day);
      final itemsForDay = _getItemsForDate(date);
      final isToday = date.year == DateTime.now().year &&
          date.month == DateTime.now().month &&
          date.day == DateTime.now().day;

      days.add(
        GestureDetector(
          onTap: () {
            // Show day details
          },
          child: Card(
            elevation: 0,
            color: isToday ? Colors.blue.shade50 : null,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(8),
              side: isToday
                  ? BorderSide(color: Colors.blue.shade300)
                  : BorderSide.none,
            ),
            child: Padding(
              padding: const EdgeInsets.all(8),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    day.toString(),
                    style: Theme.of(context).textTheme.bodySmall?.copyWith(
                          fontWeight: FontWeight.bold,
                        ),
                  ),
                  const SizedBox(height: 4),
                  Wrap(
                    spacing: 2,
                    children: itemsForDay.take(3).map((item) {
                      Color color = Colors.blue;
                      if (item.type == ItemType.deadline) {
                        color = Colors.orange;
                      } else if (item.type == ItemType.todo) {
                        color = Colors.green;
                      }

                      return Container(
                        width: 6,
                        height: 6,
                        decoration: BoxDecoration(
                          color: color,
                          borderRadius: BorderRadius.circular(3),
                        ),
                      );
                    }).toList(),
                  ),
                ],
              ),
            ),
          ),
        ),
      );
    }

    return GridView.count(
      crossAxisCount: 7,
      childAspectRatio: 1,
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      children: days,
    );
  }

  @override
  Widget build(BuildContext context) {
    return RefreshIndicator(
      onRefresh: _loadCalendars,
      child: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Month navigation
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      IconButton(
                        icon: const Icon(Icons.chevron_left),
                        onPressed: () {
                          setState(() {
                            _currentMonth = DateTime(
                              _currentMonth.year,
                              _currentMonth.month - 1,
                            );
                          });
                        },
                      ),
                      Text(
                        DateFormat('MMMM yyyy', 'ko_KR')
                            .format(_currentMonth),
                        style: Theme.of(context).textTheme.titleLarge,
                      ),
                      IconButton(
                        icon: const Icon(Icons.chevron_right),
                        onPressed: () {
                          setState(() {
                            _currentMonth = DateTime(
                              _currentMonth.year,
                              _currentMonth.month + 1,
                            );
                          });
                        },
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),

                  // Weekday headers
                  GridView.count(
                    crossAxisCount: 7,
                    childAspectRatio: 2,
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    children: ['일', '월', '화', '수', '목', '금', '토']
                        .map((day) => Center(
                              child: Text(
                                day,
                                style: Theme.of(context)
                                    .textTheme
                                    .bodySmall
                                    ?.copyWith(fontWeight: FontWeight.bold),
                              ),
                            ))
                        .toList(),
                  ),
                  const SizedBox(height: 8),

                  // Calendar grid
                  _buildCalendarGrid(),
                  const SizedBox(height: 24),

                  // Calendars list
                  Text(
                    '내 캘린더',
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                          fontWeight: FontWeight.bold,
                        ),
                  ),
                  const SizedBox(height: 12),
                  ..._calendars.map((cal) => ListTile(
                        leading: Container(
                          width: 12,
                          height: 12,
                          decoration: BoxDecoration(
                            color: Color(
                              int.parse('0xff${cal.color?.replaceFirst('#', '') ?? 'CCCCCC'}'),
                            ),
                            borderRadius: BorderRadius.circular(2),
                          ),
                        ),
                        title: Text(cal.name),
                        subtitle: cal.isDefault ? const Text('기본 캘린더') : null,
                      )),
                ],
              ),
            ),
    );
  }
}
