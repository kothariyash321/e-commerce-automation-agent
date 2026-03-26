def upload_to_sharepoint(local_path: str, folder: str) -> str:
    """Uploads report file to SharePoint (stub returns deterministic URL)."""
    file_name = local_path.split('/')[-1]
    return f'https://sharepoint.arettsales.local/{folder}/{file_name}'


def send_email(to: list[str], subject: str, body_html: str, attachments: list[str] | None = None) -> dict:
    """Sends outbound email through M365 (stub)."""
    return {'sent': True, 'to': to, 'subject': subject, 'attachments': attachments or []}
