from phantasy_apps.settings_manager.app import get_snapshotdata
from phantasy_apps.settings_manager.utils import take_snapshot

ts = '2023-05-08T14:54:59'
uri = "/user/zhangt/development/tests/test-sm.db"
snp_template_data = get_snapshotdata(ts, uri)
df = take_snapshot('snapshot got from CLI', ['TEST', 'CLI'],
                   snp_template_data, 'Artemis', initial_mp=True,
                   cli=True)
print(df)
