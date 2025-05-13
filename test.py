import xmlrpc.client

url = "http://localhost:8200"  # Cambia esto por la URL de tu instancia de Odoo
db = "odoo"  # Cambia esto por el nombre de tu base de datos
username = "admin"  # Cambia esto por tu usuario de Odoo
password = "admin"  # Cambia esto por tu contraseña de Odoo

# Autenticación
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})

# Crear el contacto
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
partner_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{
    'name': 'Imanol Moreno',
}])

print(f"Nuevo contacto creado con ID: {partner_id}")