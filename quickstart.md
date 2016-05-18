
El objetivo de este tutorial es implementar [Sync API](https://www.paybook.com/syncdocs#api-Overview-Overview). Entender como funciona el sistema y las interacciones que se establecen entre tu aplicación y el API.

## Requerimientos

- Manejo básico de linea de comandos

- Tener el comando [cURL](https://curl.haxx.se/docs/manpage.html) instalado en linea de comandos

- Un API KEY de [Sync API](https://www.paybook.com/syncdocs#api-Overview-Overview)


## Gestión de Usuarios


Lo primero que tienes que hacer para sincronizar una institución por medio de Sync API es la gestión de usuarios. La estructura en Sync es la siguiente:

->![alt tag](pb_python_lite/lc_api.png?raw=true =500x300)<-

Es decir tu podrás registrar muchos usuarios por medio de tu **API_KEY** y, a su vez, cada uno de estos usuarios registrará cuentas de las instituciones que desea sincronizar. Al final todas las cuentas sincronizadas de cada una de las instituciones que un usuario dio de alta estarán ligadas a tu **API_KEY**.


## Conexión con Sync API

<br>
En este tutorial implementaremos [Sync API](https://www.paybook.com/syncdocs#api-Overview-Overview) por medio de la interfaz [cURL](https://curl.haxx.se/docs/manpage.html) desde la línea de comandos. La interacción entre tu terminal y el API se muestra a continuación:

->![alt tag](pb_python_lite/lc_api.png =500x250)<-

En resumen, estaremos consumiendo los enpoints GET/POST/PUT/DELETE de [Sync API](https://www.paybook.com/syncdocs#api-Overview-Overview) a través de nuestra línea de comandos.

## Flujo del Tutorial

<br>
En este tutorial haremos lo siguiente:

1. Crearemos un usuario nuevo que ligaremos a nuestra **API_KEY**
2. Consultaremos los usuarios que están ligados a nuestra **API_KEY**
3. Iniciaremos sesión con el usuario creado en el paso 1
4. Verificaremos la sesión creada en el paso 3. 

A partir de aquí ya tendremos una sesión iniciada (sesión del usuario creada en el paso 1) por lo que las siguientes acciones estarán ligadas a dicho usuario:

5. Consultaremos los catálogos de las instituciones que el usuario puede sincronzar con  [Sync API](https://www.paybook.com/syncdocs#api-Overview-Overview).
6. Registraremos las credenciales del usuario en una institución (SAT).
7. Revisaremos el estatus de sincronización para las credenciales registradas.
8. Consultaremos las transacciones sincronizadas.

Esperemos lo disfrutes ¡Aquí vamos!

###1. Creación de Usuario

Crear un usuario por medio de [Sync API](https://www.paybook.com/syncdocs#api-Overview-Overview) es muy sencillo, para esto únicamente requieres tu **API_KEY** y un nombre de usuaario para el usuario que deseas crear. 

**INPUT:** api_key y name
<br>
**OUTPUT:** id_user

```
curl -X POST -H "Content-type:application/json" -d '{"api_key":"your_api_key"","name":"some_name"}' https://sync.paybook.com/v1/users
```

Con esto se habrá creado un nuevo usuario "name" ligado a tu **API_KEY**, la respuesta de [Sync API](https://www.paybook.com/syncdocs#api-Overview-Overview) debe ser la siguiente:

```
{"code":200,"status":true,"message":null,"response":{"id_user":"573a91a90b212a0e3e8b4596","id_external":null,"name":"curlhugo1","dt_create":1463456169,"dt_modify":null}}
```

**Importante:** no olvides remplazar el valor de los parámetros en todos los comandos.


###2. Consulta de Usuarios

Para verificar los usuarios que están ligados a tu **API_KEY**, es decir, a tu cuenta de [Sync API](https://www.paybook.com/syncdocs#api-Overview-Overview), ejecuta el siguiente comando:

**INPUT:** api_key
<br>
**OUTPUT:** id_user

```
curl -X GET -H "Content-type:application/json" -d '{"api_key":"your_api_key"}' http://sync.paybook.com/v1/users
```

Para efectos de este tutorial la ejecución de este comando te debe regresar el usuario registrado anteriormente:

```
{"code":200,"status":true,"message":null,"response":[{"id_user":"573a91a90b212a0e3e8b4596","id_external":null,"name":"curlhugo1","dt_create":1463518052,"dt_modify":null}]}
```

###3. Inicio de Sesión

Para poder sincronizar una cuenta de alguna institución lo primero que tenemos que hacer es iniciar sesión con el usuario que deseamos sincronizar. Para esto es necesario tener el id del usuario i.e. id_user y ejecutar:

**INPUT:** api_key y id_user
<br>
**OUTPUT:** token

```
curl -X POST -H "Content-type:application/json" -d '{"api_key":"your_api_key","id_user":"id_user_value"}' https://sync.paybook.com/v1/sessions
```

Este comando nos regresará un token e.g. 701c899236ea141d25f63c88d9f09230 como se muestra a continuación:

```
{"code":200,"status":true,"message":null,"response":{"token":"701c899236ea141d25f63c88d9f09230"}}
```

**Importante:** El token tiene un periodo de expiración de 5 minutos después de su creación.

###4. Verificación de la Sesión

No está demás verificar la validez de la sesión i.e. del token, para esto ejecutar el siguiente comando:

**INPUT:** token
<br>
**OUTPUT:** code 200 o code 401

```
curl 'https://sync.paybook.com/v1/sessions/701c899236ea141d25f63c88d9f09230/verify'
```

Si la sesión es valida nos regresará lo siguiente:

```
{"code":200,"status":true,"message":null,"response":null}
```
Si la sesión ya no es valida tendremos un código 401 **Unauthoraized**

```
{"code":401,"status":false,"message":"Unauthorized","response":null}
```

###5. Consulta de Catálogos de Instituciones

Una vez que hemos iniciado sesión tenemos que consultar el catálogo de instituciones que [Sync API](https://www.paybook.com/syncdocs#api-Overview-Overview) tiene para nosotros de tal manera que podamos elegir la institución que queremos sincronizar para este usuario.

**INPUT:** token
<br>
**OUTPUT:** catalogues

```
curl 'https://sync.paybook.com/v1/catalogues/sites?token=your_token'
```

###6. Sincronizar una Institución

El siguiente paso consiste en seleccionar una institución del catálogo para sincronizarla, para efectos de este tutorial seleccionaremos el SAT, para esto obtenemos el id del sitio del SAT analizando el catálogo, se debe obtener el siguiente valor:

```
id_site = '56cf5728784806f72b8b456f'
```

Una vez que hemos seleccionado la institución hay que dar de alta las credenciales de nuestro usuario en esa institución, en el caso particular del SAT las credenciales deben ser el **RFC** así como su Clave de Identificación Electrónica Confidencial, o mejor conocida como **CIEC**:

**INPUT:** token, id_site, some_rfc y some_ciec
<br>
**OUTPUT:** url_status

```
curl -X POST -H "Content-type:application/json" -d '{"token":"your_token","id_site":"id_site","credentials":{"rfc" : "some_rfc","password" : "some_ciec"}}' https://sync.paybook.com/v1/credentials
```

Si las credenciales fueron registradas corréctamente obtendremos un resultado como el siguiente:

```
{"code":200,"status":true,"message":null,"response":{"id_credential":"573b88f90b212a033e8b4582","username":"O***********9","ws":"wss:\/\/sync.paybook.com\/v1\/status\/573b88f90b212af83d8b457f","status":"https:\/\/sync.paybook.com\/v1\/jobs\/573b88f90b212af83d8b457f\/status","twofa":"https:\/\/sync.paybook.com\/v1\/jobs\/573b88f90b212af83d8b457f\/twofa"}}
```

**Importante:** guardar el valor del campo de **status** -- es una url -- ya que se utilizará más adelante.

##7. Verificar creación de Credenciales

Como un paso de verificación podemos revisar las credenciales registradas para un usuario:

**INPUT:** api_key y id_user
<br>
**OUTPUT:** credentials_retrieved

```
curl 'https://sync.paybook.com/v1/credentials?api_key=b7e57daf2b782bee22f05e38a1823c3a&id_user=573a91a90b212a0e3e8b4596'
```

Y obtendremos un resultado parecido:

```
{"code":200,"status":true,"message":null,"response":[{"id_credential":"573b88f90b212a033e8b4582","id_site":"56cf5728784806f72b8b456f","id_site_organization":"56cf4ff5784806152c8b4568","id_site_organization_type":"56cf4f5b784806cf028b4569","username":"O***********9","dt_refresh":1463465010}]}
```

###8. Revisar el Estatus de Sincronización

Una vez que hemos registrado una credencial y hemos verificado que ésta se haya guardado corréctamente, el siguiente paso consiste en checar el estatus de sincronización para este contribuyente. Para esto haremos uso del valor que guardamos de **url_status** que obtuvimos anteriormente al crear credenciales, únicamente hay que agregar el valor de nuestro token de sesión:

```
curl <valor_status> + ? + token=<some_token>
```

Un ejemplo sería el siguiente:

**INPUT:** token
<br>
**OUTPUT:** status

```
curl 'https://sync.paybook.com/v1/jobs/573b88f90b212af83d8b457f/status?token=68f00287cde168ddbb851d90f5be3341'
```

Al ejecutar el comando anterior obtendremos el siguiente resultado:

```
{"code":200,"status":true,"message":null,"response":[{"code":100},{"code":101},{"code":102},{"code":200}]}
```

Estos son una serie de códigos que indican el estatus de sincronización de la cuenta del SAT que el usuario registró. La descripción de los códigos se muestra a continuación:

| Código     | Descripción     |
| ------------- | ------------- |
| 100 | Se registró un nuevo Job en el API |
| 101 | Se obtuvo el Job registrado y emepzará a trabajar |
| 102 | El login fue exitóso y la información está siendo sincronizada |
| 200 | Los datos han sido procesados exitósamente|
| 201 | Los fatos han sido procesados exitósamente, se continuará con la descarga |
| 202 | No se encontraron transacciones |


###9. Consultar Transacciones


Una vez que se registraron las credenciales
En caso de tener en el estatus un código 200, 201 o 202 podemos consultar las transacciones sincronizadas. Para esto ejecutamos el siguiente comando:

**INPUT:** token y id_site
<br>
**OUTPUT:** transactions_count

```
curl 'https://sync.paybook.com/v1/transactions/count?token=your_token&id_site=some_id_site'
```
 
Y esto nos regresará una respuesta con el número de transacciones sincronizadas:

```
{"code":200,"status":true,"message":null,"response":{"count":121}}
```

Si queremos consultar las transacciones directamente ejecutamos:

**INPUT:** token y id_site
<br>
**OUTPUT:** transactions

```
curl 'https://sync.paybook.com/v1/transactions?token=your_token&id_site=some_id_site'
```

Y nos regresará un arreglo de transacciones como la siguiente:

```
{"id_transaction":"573b8922234283ad738b45da","id_user":"573a91a90b212a0e3e8b4596","id_external":null,"id_site":"56cf5728784806f72b8b456f","id_site_organization":"56cf4ff5784806152c8b4568","id_site_organization_type":"56cf4f5b784806cf028b4569","id_account":"573b8921234283ad738b4567","id_account_type":"546d4904df527d1844a2e18d","is_disable":0,"description":"CREACIONES DE TECNOLOGIA AVANZADA DE MEXICO SA DE CV","amount":6834.93,"dt_transaction":1461960603,"dt_refresh":1463519574}
```

### Fin :)



























































































