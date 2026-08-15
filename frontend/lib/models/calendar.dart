class Calendar {
  final int id;
  final int ownerId;
  final String name;
  final String? description;
  final String? color;
  final bool isDefault;
  final String? googleCalendarId;
  final bool isSyncedToGoogle;
  final DateTime createdAt;

  Calendar({
    required this.id,
    required this.ownerId,
    required this.name,
    this.description,
    this.color,
    required this.isDefault,
    this.googleCalendarId,
    required this.isSyncedToGoogle,
    required this.createdAt,
  });

  factory Calendar.fromJson(Map<String, dynamic> json) {
    return Calendar(
      id: json['id'] as int,
      ownerId: json['owner_id'] as int,
      name: json['name'] as String,
      description: json['description'] as String?,
      color: json['color'] as String?,
      isDefault: json['is_default'] as bool? ?? false,
      googleCalendarId: json['google_calendar_id'] as String?,
      isSyncedToGoogle: json['is_synced_to_google'] as bool? ?? false,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'owner_id': ownerId,
      'name': name,
      'description': description,
      'color': color,
      'is_default': isDefault,
      'google_calendar_id': googleCalendarId,
      'is_synced_to_google': isSyncedToGoogle,
      'created_at': createdAt.toIso8601String(),
    };
  }
}
