enum ItemType { schedule, deadline, todo }

enum ItemStatus { pending, inProgress, completed, cancelled }

class ScheduleItem {
  final int id;
  final int calendarId;
  final int? createdBy;
  final String title;
  final String? description;
  final ItemType type;
  final ItemStatus status;
  final DateTime? startDate;
  final DateTime? endDate;
  final DateTime? dueDate;
  final int priority;
  final bool isAllDay;
  final List<int> tagIds;
  final DateTime createdAt;
  final DateTime? completedAt;

  ScheduleItem({
    required this.id,
    required this.calendarId,
    this.createdBy,
    required this.title,
    this.description,
    required this.type,
    required this.status,
    this.startDate,
    this.endDate,
    this.dueDate,
    required this.priority,
    required this.isAllDay,
    this.tagIds = const [],
    required this.createdAt,
    this.completedAt,
  });

  factory ScheduleItem.fromJson(Map<String, dynamic> json) {
    return ScheduleItem(
      id: json['id'] as int,
      calendarId: json['calendar_id'] as int,
      createdBy: json['created_by'] as int?,
      title: json['title'] as String,
      description: json['description'] as String?,
      type: ItemType.values.firstWhere(
        (e) => e.name == (json['type'] as String?)?.toLowerCase(),
        orElse: () => ItemType.schedule,
      ),
      status: ItemStatus.values.firstWhere(
        (e) => e.name == (json['status'] as String?)?.replaceAll('_', '').toLowerCase(),
        orElse: () => ItemStatus.pending,
      ),
      startDate: json['start_date'] != null ? DateTime.parse(json['start_date'] as String) : null,
      endDate: json['end_date'] != null ? DateTime.parse(json['end_date'] as String) : null,
      dueDate: json['due_date'] != null ? DateTime.parse(json['due_date'] as String) : null,
      priority: json['priority'] as int? ?? 3,
      isAllDay: json['is_all_day'] as bool? ?? false,
      tagIds: List<int>.from(json['tag_ids'] as List? ?? []),
      createdAt: DateTime.parse(json['created_at'] as String),
      completedAt: json['completed_at'] != null ? DateTime.parse(json['completed_at'] as String) : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'calendar_id': calendarId,
      'created_by': createdBy,
      'title': title,
      'description': description,
      'type': type.name,
      'status': status.name,
      'start_date': startDate?.toIso8601String(),
      'end_date': endDate?.toIso8601String(),
      'due_date': dueDate?.toIso8601String(),
      'priority': priority,
      'is_all_day': isAllDay,
      'tag_ids': tagIds,
      'created_at': createdAt.toIso8601String(),
      'completed_at': completedAt?.toIso8601String(),
    };
  }

  bool get isOverdue {
    if (status == ItemStatus.completed) return false;
    if (dueDate == null) return false;
    return dueDate!.isBefore(DateTime.now());
  }

  bool get isDueToday {
    if (dueDate == null) return false;
    final now = DateTime.now();
    return dueDate!.year == now.year &&
        dueDate!.month == now.month &&
        dueDate!.day == now.day;
  }
}
