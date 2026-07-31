class User {
  final int id;
  final String fullName;
  final String email;
  final bool isActive;

  User({
    required this.id,
    required this.fullName,
    required this.email,
    required this.isActive,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      fullName: json['full_name'],
      email: json['email'],
      isActive: json['is_active'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'full_name': fullName,
      'email': email,
      'is_active': isActive,
    };
  }
}
