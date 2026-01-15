from odoo.addons.mangono_migration.mangono_migration import migrate_mangono


@migrate_mangono()
def pre_fake_script(self, has_run):
    pass


@migrate_mangono(run_always=True, allowed_to_fail=True, priority=100)
def pre_fake_script_run_always(self, has_run):
    pass


@migrate_mangono(priority=500)
def pre_drop_table(self, has_run):
    self.cr.execute("""DROP TABLE fake_test_table;""")


@migrate_mangono(priority=400)
def pre_create_table(self):
    """This script create a table, the previous one destroy it, should be OK because of priority"""
    self.cr.execute("""CREATE TABLE fake_test_table ();""")
