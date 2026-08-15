class Tag {
  final int id;
  final int ownerId;
  final String name;
  final String? color;
  final DateTime createdAt;

  Tag({
    required this.id,
    required this.ownerId,
    required this.name,
    this.color,
    required this.createdAt,
  });

  factory Tag.fromJson(Map<String, dynamic> json) {
    return Tag(
      id: json['id'] as int,
      ownerId: json['owner_id'] as int,
      name: json['name'] as String,
      color: json['color'] as String?,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'owner_id': ownerId,
      'name': name,
      'color': color,
      'created_at': createdAt.toIso8601String(),
    };
  }
}
