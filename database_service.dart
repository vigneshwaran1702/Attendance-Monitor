import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';
import '../models/attendance.dart';

class DatabaseService {
  static Database? _database;

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDB('attendance.db');
    return _database!;
  }

  Future<Database> _initDB(String filePath) async {
    final dbPath = await getDatabasesPath();
    final path = join(dbPath, filePath);

    return await openDatabase(
      path,
      version: 1,
      onCreate: _createDB,
    );
  }

  Future _createDB(Database db, int version) async {
    await db.execute('''
      CREATE TABLE attendances (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        check_in TEXT NOT NULL,
        check_out TEXT,
        status TEXT NOT NULL,
        is_synced INTEGER NOT NULL DEFAULT 0
      )
    ''');
  }

  Future<int> insertAttendance(Attendance attendance) async {
    final db = await database;
    return await db.insert('attendances', attendance.toJson());
  }

  Future<List<Attendance>> getUnsyncedAttendances() async {
    final db = await database;
    final result = await db.query('attendances', where: 'is_synced = ?', whereArgs: [0]);
    return result.map((e) => Attendance.fromJson(e)).toList();
  }

  Future<int> markAsSynced(int id) async {
    final db = await database;
    return await db.update(
      'attendances',
      {'is_synced': 1},
      where: 'id = ?',
      whereArgs: [id],
    );
  }
}
