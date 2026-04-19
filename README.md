# 1. Clonar el proyecto
git clone git@github.com:shekkosghub/mini-erp.git

# 2. Crear entorno virtual (Muy importante)
python -m venv venv

# 3. Activar entorno virtual
# En Windows (CMD/PowerShell):
venv\Scripts\activate
# En Mac/Linux (Bash/Zsh):
source venv/bin/activate

# 4. Instalar dependencias base
pip install django "psycopg2-binary" whitenoise dj-database-url

Ver AGENTS.md para mas información
