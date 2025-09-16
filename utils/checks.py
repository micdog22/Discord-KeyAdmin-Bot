import os
from typing import Set
from discord import Interaction

ALLOWED_USER_IDS: Set[int] = set()
raw = os.getenv("ALLOWED_USER_IDS", "")
for token in raw.split(","):
    token = token.strip()
    if token.isdigit():
        ALLOWED_USER_IDS.add(int(token))

def has_admin_or_allowed(interaction: Interaction) -> bool:
    if interaction.user and interaction.user.id in ALLOWED_USER_IDS:
        return True
    perms = getattr(interaction.user, "guild_permissions", None)
    return bool(perms and perms.administrator)