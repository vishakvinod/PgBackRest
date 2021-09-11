import os

PGBACKREST_FULL_BACKUP = "pgbackrest --stanza=appbackups --log-level-console=info --type=full backup"
PGBACKREST_DIFF_BACKUP = "pgbackrest --stanza=appbackups --log-level-console=info --type=diff backup"
PGBACKREST_INCR_BACKUP = "pgbackrest --stanza=appbackups --log-level-console=info --type=incr backup"

PGBACKREST_RESTORE = "pgbackrest --stanza=appbackups --log-level-console=info restore --delta"
PGBACKREST_RESTORE_DB = "pgbackrest --stanza=appbackups --log-level-console=info restore --delta --db-include={} --type=immediate --target-action=promote"
PGBACKREST_RESTORE_TIME = "pgbackrest --stanza=appbackups --log-level-console=info restore --delta --type=time \"--target={}\" --target-action=promote"

PGBACKREST_INFO_BACKUP = "pgbackrest --stanza=appbackups --log-level-console=info info"
PGBACKREST_CHECK_BACKUP = "pgbackrest --stanza=appbackups --log-level-console=info check"

PGBACKREST_CREATE = "pgbackrest --stanza=appbackups stanza-create"

BACKUP_TIME = os.getenv('PG_BACKUP_TIME', "00:30")
BACKUP_TIME_SUN = os.getenv('PG_BACKUP_TIME_SUN', BACKUP_TIME)
BACKUP_TIME_MON = os.getenv('PG_BACKUP_TIME_MON', BACKUP_TIME)
BACKUP_TIME_TUE = os.getenv('PG_BACKUP_TIME_TUE', BACKUP_TIME)
BACKUP_TIME_WED = os.getenv('PG_BACKUP_TIME_WED', BACKUP_TIME)
BACKUP_TIME_THUR = os.getenv('PG_BACKUP_TIME_THUR', BACKUP_TIME)
BACKUP_TIME_FRI = os.getenv('PG_BACKUP_TIME_FRI', BACKUP_TIME)
BACKUP_TIME_SAT = os.getenv('PG_BACKUP_TIME_SAT', BACKUP_TIME)
