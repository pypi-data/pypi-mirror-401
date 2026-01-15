def auto_load_mangono_migration(environ: dict) -> bool:
    print(
        "=== checking if mangono_migration should be loaded retuen ===",
        (environ.get("update", False) or environ.get("init", False))
        and not environ.get("DISABLE_MANGONO_MIGRATION", False),
        environ,
    )
    return (environ.get("UPDATE", False) or environ.get("INIT", False)) and not environ.get(
        "DISABLE_MANGONO_MIGRATION", False
    )
