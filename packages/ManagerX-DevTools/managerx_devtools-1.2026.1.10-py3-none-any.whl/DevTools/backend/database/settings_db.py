# src/database/settings_db.py

import sqlite3
import os
from datetime import datetime
from typing import Optional, Dict, Any

class SettingsDB:
    """
    Datenbank-Klasse zur Verwaltung von Benutzer- und Servereinstellungen.
    Unterstützt automatische Schema-Migration für bestehende Datenbanken.
    """
    
    # Aktuelle Schema-Version
    SCHEMA_VERSION = 2
    
    # Standard-Einstellungen
    DEFAULT_USER_SETTINGS = {
        'language': 'en',
        'timezone': 'UTC',
        'notifications_enabled': True,
        'dm_notifications': True,
        'ephemeral_responses': False,
        'auto_translate': False
    }
    
    DEFAULT_SERVER_SETTINGS = {
        'language': 'en',
        'timezone': 'UTC',
        'ephemeral_responses': False,
        'admin_role_id': None,
        'moderator_role_id': None
    }
    
    def __init__(self, db_path="data/settings.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Prüfen ob Datenbank existiert
        db_exists = os.path.exists(self.db_path)
        
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        
        if db_exists:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] [DATABASE] Existing database found, checking for migrations...")
            self.migrate_schema()
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] [DATABASE] Creating new database...")
            self.create_tables()
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [DATABASE] Settings Database initialized ✓")

    def create_tables(self):
        """Erstellt alle Tabellen mit dem aktuellen Schema."""
        
        # Schema-Versions-Tabelle
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS schema_version (
                version INTEGER PRIMARY KEY,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Benutzereinstellungen
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_settings (
                user_id INTEGER PRIMARY KEY,
                language TEXT NOT NULL DEFAULT 'en',
                timezone TEXT DEFAULT 'UTC',
                notifications_enabled BOOLEAN DEFAULT 1,
                dm_notifications BOOLEAN DEFAULT 1,
                ephemeral_responses BOOLEAN DEFAULT 0,
                auto_translate BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Servereinstellungen
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS server_settings (
                server_id INTEGER PRIMARY KEY,
                language TEXT NOT NULL DEFAULT 'en',
                timezone TEXT DEFAULT 'UTC',
                ephemeral_responses BOOLEAN DEFAULT 0,
                admin_role_id INTEGER,
                moderator_role_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Aktuelle Schema-Version speichern
        self.cursor.execute("""
            INSERT OR REPLACE INTO schema_version (version) VALUES (?)
        """, (self.SCHEMA_VERSION,))
        
        self.conn.commit()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [DATABASE] Tables created with schema version {self.SCHEMA_VERSION}")

    def get_schema_version(self) -> int:
        """Gibt die aktuelle Schema-Version der Datenbank zurück."""
        try:
            self.cursor.execute("SELECT version FROM schema_version ORDER BY version DESC LIMIT 1")
            result = self.cursor.fetchone()
            return result[0] if result else 0
        except sqlite3.OperationalError:
            return 0

    def migrate_schema(self):
        """Migriert das Schema von älteren Versionen zur aktuellen Version."""
        current_version = self.get_schema_version()
        
        if current_version == self.SCHEMA_VERSION:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] [DATABASE] Schema is up to date (v{current_version})")
            return
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [DATABASE] Migrating schema from v{current_version} to v{self.SCHEMA_VERSION}")
        
        # Migration von Version 0 (alte Struktur) zu Version 1
        if current_version < 1:
            self._migrate_v0_to_v1()
        
        # Migration von Version 1 zu Version 2
        if current_version < 2:
            self._migrate_v1_to_v2()
        
        # Schema-Version aktualisieren
        self.cursor.execute("""
            INSERT OR REPLACE INTO schema_version (version) VALUES (?)
        """, (self.SCHEMA_VERSION,))
        
        self.conn.commit()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [DATABASE] Migration completed ✓")

    def _migrate_v0_to_v1(self):
        """Migration von der ursprünglichen Version zur Version 1."""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [DATABASE] Applying migration v0 → v1")
        
        # Schema-Version Tabelle erstellen
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS schema_version (
                version INTEGER PRIMARY KEY,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Prüfen ob alte user_settings existiert
        self.cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='user_settings'
        """)
        
        if self.cursor.fetchone():
            # Alte Daten sichern
            self.cursor.execute("SELECT user_id, language FROM user_settings")
            old_data = self.cursor.fetchall()
            
            # Tabelle umbenennen
            self.cursor.execute("ALTER TABLE user_settings RENAME TO user_settings_old")
            
            # Neue Tabelle mit erweitertem Schema erstellen
            self.cursor.execute("""
                CREATE TABLE user_settings (
                    user_id INTEGER PRIMARY KEY,
                    language TEXT NOT NULL DEFAULT 'en',
                    timezone TEXT DEFAULT 'UTC',
                    notifications_enabled BOOLEAN DEFAULT 1,
                    dm_notifications BOOLEAN DEFAULT 1,
                    ephemeral_responses BOOLEAN DEFAULT 0,
                    auto_translate BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Alte Daten migrieren
            for row in old_data:
                self.cursor.execute("""
                    INSERT INTO user_settings (user_id, language) 
                    VALUES (?, ?)
                """, (row[0], row[1]))
            
            # Alte Tabelle löschen
            self.cursor.execute("DROP TABLE user_settings_old")
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] [DATABASE] Migrated {len(old_data)} user settings")
        
        self.conn.commit()

    def _migrate_v1_to_v2(self):
        """Migration von Version 1 zu Version 2 - Server Settings hinzufügen."""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [DATABASE] Applying migration v1 → v2")
        
        # Server-Settings Tabelle erstellen
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS server_settings (
                server_id INTEGER PRIMARY KEY,
                language TEXT NOT NULL DEFAULT 'en',
                timezone TEXT DEFAULT 'UTC',
                ephemeral_responses BOOLEAN DEFAULT 0,
                admin_role_id INTEGER,
                moderator_role_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.conn.commit()

    # ===== BENUTZER-EINSTELLUNGEN =====
    
    def set_user_language(self, user_id: int, lang_code: str):
        """Speichert den Sprachcode für einen Benutzer."""
        self.set_user_setting(user_id, 'language', lang_code)

    def get_user_language(self, user_id: int) -> str:
        """Ruft den Sprachcode für einen Benutzer ab."""
        return self.get_user_setting(user_id, 'language')

    def set_user_setting(self, user_id: int, setting: str, value: Any):
        """Setzt eine spezifische Benutzereinstellung."""
        valid_settings = self.DEFAULT_USER_SETTINGS.keys()
        
        if setting not in valid_settings:
            raise ValueError(f"Invalid setting: {setting}")
        
        # Benutzer erstellen falls nicht vorhanden
        self._ensure_user_exists(user_id)
        
        # Boolean zu Integer für SQLite
        if isinstance(value, bool):
            value = 1 if value else 0
        
        self.cursor.execute(f"""
            UPDATE user_settings 
            SET {setting} = ?, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        """, (value, user_id))
        
        self.conn.commit()

    def get_user_setting(self, user_id: int, setting: str) -> Any:
        """Ruft eine spezifische Benutzereinstellung ab."""
        self.cursor.execute(f"""
            SELECT {setting} FROM user_settings WHERE user_id = ?
        """, (user_id,))
        
        result = self.cursor.fetchone()
        
        if result:
            value = result[0]
            # Boolean-Werte konvertieren
            if setting in ['notifications_enabled', 'dm_notifications', 'ephemeral_responses', 'auto_translate']:
                return bool(value)
            return value
        
        return self.DEFAULT_USER_SETTINGS.get(setting)

    def get_all_user_settings(self, user_id: int) -> Dict[str, Any]:
        """Ruft alle Einstellungen eines Benutzers ab."""
        self.cursor.execute("SELECT * FROM user_settings WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()
        
        if result:
            settings = dict(result)
            # Boolean-Werte konvertieren
            for key in ['notifications_enabled', 'dm_notifications', 'ephemeral_responses', 'auto_translate']:
                if key in settings:
                    settings[key] = bool(settings[key])
            return settings
        
        return self.DEFAULT_USER_SETTINGS.copy()

    def _ensure_user_exists(self, user_id: int):
        """Stellt sicher, dass ein Benutzer-Eintrag existiert."""
        self.cursor.execute("SELECT user_id FROM user_settings WHERE user_id = ?", (user_id,))
        
        if not self.cursor.fetchone():
            self.cursor.execute("""
                INSERT INTO user_settings (user_id) VALUES (?)
            """, (user_id,))
            self.conn.commit()

    # ===== SERVER-EINSTELLUNGEN =====
    
    def set_server_setting(self, server_id: int, setting: str, value: Any):
        """Setzt eine spezifische Server-Einstellung."""
        valid_settings = self.DEFAULT_SERVER_SETTINGS.keys()
        
        if setting not in valid_settings:
            raise ValueError(f"Invalid setting: {setting}")
        
        self._ensure_server_exists(server_id)
        
        if isinstance(value, bool):
            value = 1 if value else 0
        
        self.cursor.execute(f"""
            UPDATE server_settings 
            SET {setting} = ?, updated_at = CURRENT_TIMESTAMP
            WHERE server_id = ?
        """, (value, server_id))
        
        self.conn.commit()

    def get_server_setting(self, server_id: int, setting: str) -> Any:
        """Ruft eine spezifische Server-Einstellung ab."""
        self.cursor.execute(f"""
            SELECT {setting} FROM server_settings WHERE server_id = ?
        """, (server_id,))
        
        result = self.cursor.fetchone()
        
        if result:
            value = result[0]
            # Boolean-Werte konvertieren
            if setting == 'ephemeral_responses':
                return bool(value)
            return value
        
        return self.DEFAULT_SERVER_SETTINGS.get(setting)

    def get_all_server_settings(self, server_id: int) -> Dict[str, Any]:
        """Ruft alle Einstellungen eines Servers ab."""
        self.cursor.execute("SELECT * FROM server_settings WHERE server_id = ?", (server_id,))
        result = self.cursor.fetchone()
        
        if result:
            settings = dict(result)
            # Boolean-Werte konvertieren
            if 'ephemeral_responses' in settings:
                settings['ephemeral_responses'] = bool(settings['ephemeral_responses'])
            return settings
        
        return self.DEFAULT_SERVER_SETTINGS.copy()

    def _ensure_server_exists(self, server_id: int):
        """Stellt sicher, dass ein Server-Eintrag existiert."""
        self.cursor.execute("SELECT server_id FROM server_settings WHERE server_id = ?", (server_id,))
        
        if not self.cursor.fetchone():
            self.cursor.execute("""
                INSERT INTO server_settings (server_id) VALUES (?)
            """, (server_id,))
            self.conn.commit()

    # ===== UTILITY-METHODEN =====
    
    def reset_user_settings(self, user_id: int):
        """Setzt alle Benutzereinstellungen auf Standard zurück."""
        self.cursor.execute("DELETE FROM user_settings WHERE user_id = ?", (user_id,))
        self.conn.commit()

    def reset_server_settings(self, server_id: int):
        """Setzt alle Server-Einstellungen auf Standard zurück."""
        self.cursor.execute("DELETE FROM server_settings WHERE server_id = ?", (server_id,))
        self.conn.commit()

    def get_stats(self) -> Dict[str, int]:
        """Gibt Statistiken über die Datenbank zurück."""
        stats = {}
        
        self.cursor.execute("SELECT COUNT(*) FROM user_settings")
        stats['total_users'] = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM server_settings")
        stats['total_servers'] = self.cursor.fetchone()[0]
        
        stats['schema_version'] = self.get_schema_version()
        
        return stats

    def close(self):
        """Schließt die Datenbankverbindung."""
        self.conn.close()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [DATABASE] Connection closed")