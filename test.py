import xmlrpc.client

url = "http://localhost:8200"
db = "odoo"
username = "admin"
password = "admin"

# Autenticación
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})

# Crear el registro
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
partner_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{
    'name': 'Juan Pérez',
    'street': 'Calle Falsa 123',
    'email': 'juan.perez@example.com',
}])

print(f"Nuevo registro creado con ID: {partner_id}")