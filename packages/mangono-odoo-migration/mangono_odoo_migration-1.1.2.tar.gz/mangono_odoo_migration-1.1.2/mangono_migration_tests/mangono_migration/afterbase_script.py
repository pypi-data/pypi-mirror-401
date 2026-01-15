from odoo.addons.mangono_migration.mangono_migration import migrate_mangono


@migrate_mangono()
def afterbase_script(self, has_run):
    pass
