import os
from pathlib import Path

EXPORT_FILES = {
    'INVBAL.csv': 'inventory_balances',
    'ITMAST.csv': 'item_master',
    'SLSHIST.csv': 'sales_history',
    'OPNORD.csv': 'open_orders',
    'AROPEN.csv': 'ar_open',
    'CHGBK.csv': 'chargebacks',
}


def _connect_sftp():
    import paramiko  # type: ignore

    host = os.getenv('S2K_EXPORT_SFTP_HOST')
    user = os.getenv('S2K_EXPORT_SFTP_USER')
    key_path = os.getenv('S2K_EXPORT_SFTP_KEY_PATH', './keys/s2k_sftp.pem')
    transport = paramiko.Transport((host, 22))
    pkey = paramiko.RSAKey.from_private_key_file(key_path)
    transport.connect(username=user, pkey=pkey)
    return paramiko.SFTPClient.from_transport(transport)


def sync_exports() -> dict:
    """Downloads configured S2K exports into local drop path and parses CSV."""
    drop = Path(os.getenv('S2K_EXPORT_DROP_PATH', './data/s2k_exports'))
    drop.mkdir(parents=True, exist_ok=True)
    synced = {}
    sftp = _connect_sftp()
    for filename, table in EXPORT_FILES.items():
        remote = f'/{filename}'
        local = drop / filename
        sftp.get(remote, str(local))
        # Keep this module runnable even if pandas is unavailable locally.
        try:
            import pandas as pd  # type: ignore

            df = pd.read_csv(local)
            synced[table] = int(len(df))
        except Exception:
            with local.open('r', encoding='utf-8') as fh:
                rows = fh.readlines()
            synced[table] = max(len(rows) - 1, 0)
    sftp.close()
    return synced
