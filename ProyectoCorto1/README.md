# Explicación del Proyecto en C# (`ProyectoCorto1`)

Para poder ejecutar una aplicación con interfaz gráfica de usuario (**GUI**) en un entorno Linux Ubuntu utilizando C#, se requieren ciertos archivos de configuración y paquetes específicos dentro de la estructura del proyecto, por lo tanto utilizamos ciertos comandos para poder realizar nuestra interfaz en ubuntu

## 1. Archivos Generados por .NET

Cuando creamos el proyecto con `dotnet new console`, el framework genera automáticamente los archivos base necesarios para la compilación:

* **`ProyectoCorto1.csproj`**: Es el archivo principal de configuración del proyecto, este define que versión de .NET se está utilizando, las propiedades de compilación y registra las dependencias externas (librerías/paquetes NuGet) que requiere la aplicación para funcionar.
* **`Program.cs`**: Contiene el código fuente principal escrito en C#. Aquí es donde se construye la interfaz gráfica, se manejan los eventos de los botones y se ejecuta la lógica del programa, ya que como no tenemos en si lo que seria como la visualizacion de C# normal, todo es mediante codigo definiendo cada label, cada buttom etc.
* **Carpetas `bin/` y `obj/`**: Son creadas durante el proceso de compilación y restauración de paquetes y este contienen los archivos binarios ejecutables e intermediarios generados por el compilador de .NET.

---

## 2. Librería Grafica: `GtkSharp`

Por defecto, la plantilla de consola en .NET en Linux no incluye componentes visuales (como ventanas, botones o cuadros de texto). Para añadir la GUI sin salir de C#, se instaló la librería **GtkSharp**:

* **GtkSharp para que nos sirvio**: es como una vinculación de C# para **GTK+**, el kit de herramientas de interfaz gráfica estándar utilizado por entornos de escritorio en Linux como lo es en nuestro caso Ubuntu.
* **Porque lo utilizamos**: porque perrmite instanciar objetos visuales nativos desde código C# puro para que la aplicación muestre una ventana interactiva en la pantalla en lugar de solo texto en la terminal.

---

## 3. Manejo de Archivos y Eventos

El proyecto incluye paquetes internos de .NET para cumplir con los requerimientos de la interfaz, por lo tanto tiene muchisimos archivos con codigo, pero como explicabamos anteriormente era por los paquetes que instalamos para nuestra interfaz grafica

