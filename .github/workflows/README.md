# GitHub Actions Workflows

Este directorio contiene el workflow de GitHub Actions para automatizar el proceso de publicación del SDK de AI Spine en PyPI.

## Workflow: `publish-to-pypi.yml`

Este workflow se ejecuta automáticamente cuando:
- ✅ Haces push a `main` y cambia el archivo `__version__.py` (auto-deploy)
- ✅ Creas un release en GitHub
- ✅ Pusheas un tag que empiece con `v` (ej: `v2.2.0`)
- ✅ Lo ejecutas manualmente desde GitHub Actions

### ¿Qué hace el workflow?
1. Ejecuta los tests en múltiples versiones de Python (3.7-3.11)
2. Verifica la calidad del código (black, flake8, mypy)
3. Construye el paquete
4. Publica en Test PyPI (opcional)
5. Publica en PyPI
6. Crea un release en GitHub

## Configuración requerida

### 1. Obtener tokens de PyPI

#### Token de PyPI:
1. Ve a https://pypi.org/manage/account/token/
2. Crea un nuevo token con el nombre "GitHub Actions"
3. Selecciona el scope (puedes elegir "Entire account" o limitarlo al proyecto "ai-spine-sdk")
4. Copia el token (empieza con `pypi-`)

#### Token de Test PyPI (opcional):
1. Ve a https://test.pypi.org/manage/account/token/
2. Crea un nuevo token siguiendo los mismos pasos

### 2. Configurar secrets en GitHub

1. Ve a tu repositorio en GitHub
2. Settings → Secrets and variables → Actions
3. Click en "New repository secret"
4. Añade los siguientes secrets:

   - **PYPI_API_TOKEN**: El token de PyPI (pypi-...)
   - **TEST_PYPI_API_TOKEN**: El token de Test PyPI (opcional)

## Uso

### Publicación automática
Cuando hagas cambios y actualices la versión:

```bash
# 1. Actualiza la versión en ai_spine/__version__.py
# 2. Commit y push
git add ai_spine/__version__.py
git commit -m "chore: bump version to 2.2.0"
git push origin main

# El workflow se ejecutará automáticamente
```

### Publicación manual con release
```bash
# 1. Crea un tag
git tag v2.2.0
git push origin v2.2.0

# 2. O crea un release desde GitHub UI
```

### Ejecutar workflow manualmente
Puedes ejecutar el workflow manualmente desde GitHub:
1. Actions → Publish to PyPI
2. Click en "Run workflow"
3. Selecciona la rama y ejecuta

## Verificación

Después de la publicación:
1. Verifica en https://pypi.org/project/ai-spine-sdk/
2. Prueba la instalación: `pip install ai-spine-sdk==2.2.0`
3. Revisa el release en GitHub

## Troubleshooting

### Error: "Invalid or non-existent authentication"
- Verifica que los tokens estén configurados correctamente en los secrets
- Asegúrate de que el token no haya expirado

### Error: "Package already exists"
- La versión ya existe en PyPI
- Incrementa la versión en `__version__.py`

### Tests fallan en GitHub pero pasan localmente
- Verifica las dependencias en `requirements-dev.txt`
- Asegúrate de que los tests no dependan de archivos locales