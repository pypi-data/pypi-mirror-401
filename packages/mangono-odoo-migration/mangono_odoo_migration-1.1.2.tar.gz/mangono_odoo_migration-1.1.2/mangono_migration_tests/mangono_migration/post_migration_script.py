from odoo.addons.mangono_migration.mangono_migration import migrate_mangono

# on teste les différentes méthodes d'appel du décorateur


@migrate_mangono()
def post_fake_script(self, has_run):
    pass


@migrate_mangono(run_always=True)
def post_run_always(self, has_run):
    pass


@migrate_mangono(allowed_to_fail=True, priority=1)
def post_allowed_to_fail(self, has_run):
    _ = 1 / 0


@migrate_mangono()
def post_without_has_run(self):
    pass


@migrate_mangono
def post_with_no_run_no_parameter(self):
    self.env["res.country"].search([("code", "=", "FR")]).name = "Groland"
