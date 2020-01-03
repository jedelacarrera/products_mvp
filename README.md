# Facebook profile search

Buscar múltiples perfiles de facebook por nombre y apellido

## Funcionamiento General

### Flujo:
Se busca a una persona siguiendo el siguiente orden
  - 2 Nombres 2 Apellidos
  - 1 Nombre 2 Apellidos
  - 2 Nombres 1 Apellido

Luego de cada una de las opciones anteriores se aplica un filtro. Si se encuentran algún perfil que cumpla las condiciones se deja de buscar.

### Filtro:
- Se elimina cualquier signo !"#$%&/()=?¡*¨}{-.,|@ que esté dentro del nombre del perfil de facebook
- Si el nombre del perfil de facebook luego del paso anterior contiene palabras que no se encuentran en la busqueda, entonces se omite.
- Si hay muchos perfiles, tomar primeros 3, ordenados según como aparecen en facebook
  - Si perfil no tiene primer apellido, omitir
  - Si perfil no tiene ni primer nombre ni segundo nombre, omitir
  - Si tenemos segundo apellido y no calza con el encontrado, omitir
  - Si apellidos estan desordenados, omitir
  - Si hay muchos perfiles, tomar primeros 3

En resumen:
- Debe estar al menos un nombre y un apellido.
- Cualquier palabra válida que venga en el nombre de facebook debe estar en el nombre completo de la persona y en el orden correcto.
  
### Web Scrapper:
  - Encontrar div con id="BrowseResultsContainer"
  - Para cada elemento dentro de ese div se extrae el texto y la url de ese perfil

## Base de datos

Hay dos tablas en base de datos:
- search: contiene información de la búsqueda de muchos perfiles.
- profile: contiene la información de un perfil que ya ha sido buscado en facebook, junto con sus resultados.

![alt text](https://github.com/jedelacarrera/facebook_profile_search/raw/master/static/DB_models.jpeg "Modelo Base de Datos")


## Instalación

### Descargar código
```
git clone https://github.com/jedelacarrera/facebook_profile_search.git
```

### Crear variables de entorno

- Crear una base de datos Postgres.
- Crear un archivo llamado .env and y pegar toda la información de .env.template.
- Reemplazar con datos de la propia base de datos.

#### Variables

- **FLASK_ENV**: `development` para desarrollo, `production` para producción.
- **FLASK_APP**: `main.py`, nombre del archivo donde se define la `app`. No cambiar
- **PG_USER_FB**: postgres user, para la base de datos
- **PG_PW_FB**: postgres password
- **PG_URL_FB**: postgres url, en desarrollo usar `localhost`
- **PG_DB_FB**: nombre de la base de datos
- **search_limit_before_restart**: Cantidad de perfiles que se buscan hasta que se resetea el browser. Esto permite que se libere memoria RAM en caso de que se ocupe un servidor con RAM limitada. En desarrollo se puede usar un valor grande.
- **SECRET_KEY**: Es como una contraseña, se debe ingresar para poder buscar perfiles y debe calzar la ingresada con la que está como variable de entorno.
- **wait_between_searchs**: Tiempo por defecto que se espera entre cada búsqueda. Esto sirve para que se simule de mejor forma a un usuario "real" y así evitar que facebook bloquee la cuenta. Puede ser cambiado por el usuario en el form.
- **facebook_email**: Email de la cuenta de facebook que se usará por defecto. Puede ser cambiado por el usuario en el form.
- **facebook_password**: Contraseña de la cuenta de facebook que se usará por defecto. Puede ser cambiado por el usuario en el form.


### Instalar dependencias.

Se necesita python3 y pip instalados, luego correr el siguiente comando
```
pip3 install -r requirements.txt
```

### Crear tablas en base de datos
```
python3 seed.py
```

## Correr programa en localhost

Abrir un terminal y pegar información de .env.

Luego correr el siguiente comando

```
python3 -m flask run --host=0.0.0.0
```


## Archivos

- main.py: contiene las rutas disponibles del sistema
- api_controllers.py: contiene las funciones que se corren ante cada request
- dbconfig.py: configuración de base de datos
- seed.py: crea las tablas en la base de datos. Es posible agregar seeds a este archivo.
- models.py: contiene los modelos/tablas de base de datos.
- requirements.txt: Requerimientos de librerías de python. Heroku lee este archivo.
- Procfile: Heroku lee este archivo para saber como iniciar el sistema.
- templates/: Archivos html
- web_scraper/: Scraper de la página de facebook, ocupa selenium para simular acciones de usuario.
- excel_scraper/: Lee archivos de input

## Inputs

Para crear una nueva instancia de búsqueda se debe llenar el form que aparece en la vista /searchs/ con la siguiente información:

- **Nombre**: Para poder identificarlo después.
- **Api key**: Debe calzar con la que está en las variables de entorno (SECRET_KEY) del programa.
- **Email de facebook**: Email de una cuenta real de un usuario de facebook. Se puede ingresar más de una, deben ir separadas por comas. Sobreescribe la que viene por defecto.
- **Contraseña de facebook**: Contraseña de una cuenta real de un usuario de facebook. Ingresar la misma cantidad que emails. Sobreescribe la que viene por defecto.
- **Tiempo entre búsquedas**: Espera en segundos entre cada búsqueda, sobreescribe el valor que está como variable de entorno (wait_between_searchs) que es el por defecto.
- **Archivo**: Debe ser un archivo csv (Valores separados por comas) con las siguientes columnas:
  - Rut de la persona. Opcional, puede venir vacío
  - **Nombres**: Primer y segundo nombre
  - **Apellido paterno**
  - **Apellido materno**
  - Nombre completo. Opcional, nunca se ocupa

Primera fila debe contener los headers, no información de una persona.

### Ej:

- Nombre: Empleados de empresa X
- Api key: my_password
- Email de facebook: profile1@gmail.com
- Contraseña de facebook: 12345678
- Tiempo entre búsquedas: 3
- Archivo: perfiles.csv

Rut,Nombres,AP,AM,NC

25676979,YOSSELIN ROCIO,PEREZ,FERNANDEZ,YOSSELIN ROCIO PEREZ FERNANDEZ

25054634,JHONATAN KENNY,SANTOS,MERCEDES,JHONATAN KENNY SANTOS MERCEDES

24657244,ANA GABRIELA,ESPINOZA,FUENMAYOR

## Outputs

Archivo csv con las siguientes columnas:
- Rut
- first_name
- second_name
- first_lastname
- second_lastname
- url1: Url del perfil más probable
- url2: Url del segundo perfil más probable
- url3: Url del tercer perfil más probable
- count: Cantidad de perfiles probables encontrados

## Rutas

- GET /searchs/: vista principal, se muestra información sobre todas las búsquedas realizadas y un formulario para crear nuevas búsquedas. Única ruta que devuelve un HTML.
- POST /searchs/: Crea una nueva búsqueda, según la información que se envía en el formulario. Redirige a /searchs/.
- GET /searchs/:id/: Devuelve un json con la información de esa búsqueda
- GET /searchs/:id/profiles: Devuelve un archivo con la lista de los perfiles encontrados para una búsqueda.
- POST, PATCH /searchs/:id/cancel: Cancelar una búsqueda mientras se sigue ejecutando. Redirige a /searchs/.
- POST, DELETE /searchs/:id/delete: Eliminar una búsqueda, borra todos sus registros de base de datos. Redirige a /searchs/.
