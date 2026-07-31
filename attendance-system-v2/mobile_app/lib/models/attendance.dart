class Attendance {
  final int? id;
  final int userId;
  final DateTime checkIn;
  final DateTime? checkOut;
  final String status;
  final bool isSynced;

  Attendance({
    this.id,
    required this.userId,
    required this.checkIn,
    this.checkOut,
    required this.status,
    this.isSynced = true,
  });

  factory Attendance.fromJson(Map<String, dynamic> json) {
    return Attendance(
      id: json['id'],
      userId: json['user_id'],
      checkIn: DateTime.parse(json['check_in']),
      checkOut: json['check_out'] != null ? DateTime.parse(json['check_out']) : null,
      status: json['status'],
      isSynced: json['is_synced'] ?? true,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'user_id': userId,
      'check_in': checkIn.toIso8601String(),
      'check_out': checkOut?.toIso8601String(),
      'status': status,
      'is_synced': isSynced,
    };
  }
}
