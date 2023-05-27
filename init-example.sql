CREATE USER '<custom-user>'@'%' IDENTIFIED BY '<custom-password>';
GRANT ALL PRIVILEGES ON <custom-db-name>.* TO '<custom-user>'@'%';
FLUSH PRIVILEGES;