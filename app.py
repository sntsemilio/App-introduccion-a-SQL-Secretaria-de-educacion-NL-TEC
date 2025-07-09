import streamlit as st
import sqlite3
import pandas as pd
import io
import contextlib

# Configuración de la página
st.set_page_config(
    page_title="Aprende SQL - Tutorial Interactivo",
    page_icon="📚",
    layout="wide"
)

# Función para crear la base de datos de ejemplo
def crear_base_datos():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # Crear tabla de empleados
    cursor.execute('''
    CREATE TABLE empleados (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        departamento TEXT,
        salario REAL,
        fecha_contratacion DATE
    )
    ''')
    
    # Insertar datos de ejemplo
    empleados_data = [
        (1, 'Juan', 'Pérez', 'Ventas', 45000, '2020-01-15'),
        (2, 'María', 'González', 'Marketing', 50000, '2019-03-22'),
        (3, 'Carlos', 'López', 'IT', 60000, '2021-07-10'),
        (4, 'Ana', 'Martínez', 'Ventas', 48000, '2020-11-05'),
        (5, 'Luis', 'Rodríguez', 'IT', 65000, '2018-09-12'),
        (6, 'Elena', 'García', 'Marketing', 52000, '2021-02-28')
    ]
    
    cursor.executemany(
        'INSERT INTO empleados VALUES (?, ?, ?, ?, ?, ?)',
        empleados_data
    )
    
    # Crear tabla de departamentos
    cursor.execute('''
    CREATE TABLE departamentos (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        presupuesto REAL
    )
    ''')
    
    departamentos_data = [
        (1, 'Ventas', 100000),
        (2, 'Marketing', 80000),
        (3, 'IT', 150000)
    ]
    
    cursor.executemany(
        'INSERT INTO departamentos VALUES (?, ?, ?)',
        departamentos_data
    )
    
    conn.commit()
    return conn

# Función para ejecutar consultas SQL
def ejecutar_consulta(conn, query):
    try:
        df = pd.read_sql_query(query, conn)
        return df, None
    except Exception as e:
        return None, str(e)

# Función para capturar la salida de una función
@contextlib.contextmanager
def capturar_salida():
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        yield f
    return f.getvalue()

# Inicializar la base de datos
if 'conn' not in st.session_state:
    st.session_state.conn = crear_base_datos()

# Título principal
st.title("Aprende SQL - Tutorial Interactivo")
st.markdown("### Una guía paso a paso para aprender SQL sin conocimientos previos")

# Sidebar para navegación
st.sidebar.title("Navegación")
seccion = st.sidebar.selectbox(
    "Selecciona una lección:",
    [
        "1. Introducción a SQL",
        "2. SELECT - Consultas básicas",
        "3. WHERE - Filtrar datos",
        "4. ORDER BY - Ordenar resultados",
        "5. COUNT y GROUP BY - Contar y agrupar",
        "6. JOIN - Unir tablas",
        "7. Práctica libre"
    ]
)

# Mostrar datos de ejemplo
st.sidebar.markdown("### Datos de ejemplo")
if st.sidebar.button("Ver tabla empleados"):
    df_empleados = pd.read_sql_query("SELECT * FROM empleados", st.session_state.conn)
    st.sidebar.dataframe(df_empleados)

if st.sidebar.button("Ver tabla departamentos"):
    df_departamentos = pd.read_sql_query("SELECT * FROM departamentos", st.session_state.conn)
    st.sidebar.dataframe(df_departamentos)

# Contenido principal según la sección seleccionada
if seccion == "1. Introducción a SQL":
    st.header("¿Qué es SQL?")
    st.write("""
    **SQL** (Structured Query Language) es un lenguaje especial que se usa para comunicarse con bases de datos.
    
    Imagina que una base de datos es como un archivero gigante con muchos cajones (tablas), 
    y cada cajón contiene fichas (registros) con información organizada en columnas.
    
    SQL nos permite:
    - **Buscar** información específica
    - **Filtrar** datos que cumplan ciertas condiciones
    - **Ordenar** la información
    - **Contar** elementos
    - **Combinar** información de diferentes tablas
    """)
    
    st.subheader("Conceptos básicos")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Tabla**: Como una hoja de Excel con filas y columnas")
        st.write("**Fila/Registro**: Cada línea de datos")
        st.write("**Columna/Campo**: Cada tipo de información")
    
    with col2:
        st.write("**Base de datos**: Colección de tablas relacionadas")
        st.write("**Consulta**: Pregunta que le hacemos a la base de datos")
        st.write("**Resultado**: La respuesta que nos da la base de datos")

elif seccion == "2. SELECT - Consultas básicas":
    st.header("SELECT - Seleccionar datos")
    st.write("""
    La palabra clave **SELECT** es la más importante en SQL. Se usa para elegir qué información queremos ver.
    
    **Sintaxis básica:**
    ```sql
    SELECT columna1, columna2 FROM nombre_tabla;
    ```
    """)
    
    st.subheader("Ejemplos prácticos")
    
    # Ejemplo 1
    st.write("**Ejemplo 1: Ver todos los datos**")
    st.code("SELECT * FROM empleados;", language="sql")
    st.write("El asterisco (*) significa 'todas las columnas'")
    
    if st.button("Ejecutar ejemplo 1"):
        df, error = ejecutar_consulta(st.session_state.conn, "SELECT * FROM empleados")
        if error:
            st.error(f"Error: {error}")
        else:
            st.dataframe(df)
    
    # Ejemplo 2
    st.write("**Ejemplo 2: Ver solo nombres y apellidos**")
    st.code("SELECT nombre, apellido FROM empleados;", language="sql")
    
    if st.button("Ejecutar ejemplo 2"):
        df, error = ejecutar_consulta(st.session_state.conn, "SELECT nombre, apellido FROM empleados")
        if error:
            st.error(f"Error: {error}")
        else:
            st.dataframe(df)
    
    # Ejercicio
    st.subheader("¡Tu turno!")
    st.write("Escribe una consulta para ver solo los nombres y departamentos de todos los empleados:")
    consulta_usuario = st.text_area("Tu consulta SQL:", key="select_ejercicio")
    
    if st.button("Ejecutar mi consulta"):
        if consulta_usuario.strip():
            df, error = ejecutar_consulta(st.session_state.conn, consulta_usuario)
            if error:
                st.error(f"Error: {error}")
            else:
                st.success("¡Excelente!")
                st.dataframe(df)
        else:
            st.warning("Por favor, escribe una consulta SQL")

elif seccion == "3. WHERE - Filtrar datos":
    st.header("WHERE - Filtrar información")
    st.write("""
    La cláusula **WHERE** nos permite filtrar los datos, es decir, mostrar solo las filas que cumplan ciertas condiciones.
    
    **Sintaxis:**
    ```sql
    SELECT columnas FROM tabla WHERE condición;
    ```
    """)
    
    st.subheader("Operadores de comparación")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("- **=** : igual a")
        st.write("- **>** : mayor que")
        st.write("- **<** : menor que")
    
    with col2:
        st.write("- **>=** : mayor o igual que")
        st.write("- **<=** : menor o igual que")
        st.write("- **!=** : diferente de")
    
    st.subheader("Ejemplos prácticos")
    
    # Ejemplo 1
    st.write("**Ejemplo 1: Empleados del departamento de Ventas**")
    st.code("SELECT * FROM empleados WHERE departamento = 'Ventas';", language="sql")
    
    if st.button("Ejecutar ejemplo 1", key="where_ej1"):
        df, error = ejecutar_consulta(st.session_state.conn, "SELECT * FROM empleados WHERE departamento = 'Ventas'")
        if error:
            st.error(f"Error: {error}")
        else:
            st.dataframe(df)
    
    # Ejemplo 2
    st.write("**Ejemplo 2: Empleados con salario mayor a 50000**")
    st.code("SELECT nombre, apellido, salario FROM empleados WHERE salario > 50000;", language="sql")
    
    if st.button("Ejecutar ejemplo 2", key="where_ej2"):
        df, error = ejecutar_consulta(st.session_state.conn, "SELECT nombre, apellido, salario FROM empleados WHERE salario > 50000")
        if error:
            st.error(f"Error: {error}")
        else:
            st.dataframe(df)
    
    # Ejercicio
    st.subheader("¡Tu turno!")
    st.write("Encuentra todos los empleados del departamento de IT:")
    consulta_usuario = st.text_area("Tu consulta SQL:", key="where_ejercicio")
    
    if st.button("Ejecutar mi consulta", key="where_ejecutar"):
        if consulta_usuario.strip():
            df, error = ejecutar_consulta(st.session_state.conn, consulta_usuario)
            if error:
                st.error(f"Error: {error}")
            else:
                st.success("¡Muy bien!")
                st.dataframe(df)

elif seccion == "4. ORDER BY - Ordenar resultados":
    st.header("ORDER BY - Ordenar datos")
    st.write("""
    **ORDER BY** nos permite ordenar los resultados por una o más columnas.
    
    **Sintaxis:**
    ```sql
    SELECT columnas FROM tabla ORDER BY columna ASC/DESC;
    ```
    
    - **ASC**: orden ascendente (menor a mayor) - es el predeterminado
    - **DESC**: orden descendente (mayor a menor)
    """)
    
    st.subheader("Ejemplos prácticos")
    
    # Ejemplo 1
    st.write("**Ejemplo 1: Empleados ordenados por salario (menor a mayor)**")
    st.code("SELECT nombre, apellido, salario FROM empleados ORDER BY salario;", language="sql")
    
    if st.button("Ejecutar ejemplo 1", key="order_ej1"):
        df, error = ejecutar_consulta(st.session_state.conn, "SELECT nombre, apellido, salario FROM empleados ORDER BY salario")
        if error:
            st.error(f"Error: {error}")
        else:
            st.dataframe(df)
    
    # Ejemplo 2
    st.write("**Ejemplo 2: Empleados ordenados por salario (mayor a menor)**")
    st.code("SELECT nombre, apellido, salario FROM empleados ORDER BY salario DESC;", language="sql")
    
    if st.button("Ejecutar ejemplo 2", key="order_ej2"):
        df, error = ejecutar_consulta(st.session_state.conn, "SELECT nombre, apellido, salario FROM empleados ORDER BY salario DESC")
        if error:
            st.error(f"Error: {error}")
        else:
            st.dataframe(df)
    
    # Ejercicio
    st.subheader("¡Tu turno!")
    st.write("Ordena a los empleados alfabéticamente por apellido:")
    consulta_usuario = st.text_area("Tu consulta SQL:", key="order_ejercicio")
    
    if st.button("Ejecutar mi consulta", key="order_ejecutar"):
        if consulta_usuario.strip():
            df, error = ejecutar_consulta(st.session_state.conn, consulta_usuario)
            if error:
                st.error(f"Error: {error}")
            else:
                st.success("¡Perfecto!")
                st.dataframe(df)

elif seccion == "5. COUNT y GROUP BY - Contar y agrupar":
    st.header("COUNT y GROUP BY - Análisis de datos")
    st.write("""
    **COUNT** cuenta el número de filas, y **GROUP BY** agrupa los datos por categorías.
    
    **Sintaxis:**
    ```sql
    SELECT columna, COUNT(*) FROM tabla GROUP BY columna;
    ```
    """)
    
    st.subheader("Ejemplos prácticos")
    
    # Ejemplo 1
    st.write("**Ejemplo 1: Contar total de empleados**")
    st.code("SELECT COUNT(*) as total_empleados FROM empleados;", language="sql")
    
    if st.button("Ejecutar ejemplo 1", key="count_ej1"):
        df, error = ejecutar_consulta(st.session_state.conn, "SELECT COUNT(*) as total_empleados FROM empleados")
        if error:
            st.error(f"Error: {error}")
        else:
            st.dataframe(df)
    
    # Ejemplo 2
    st.write("**Ejemplo 2: Contar empleados por departamento**")
    st.code("SELECT departamento, COUNT(*) as cantidad FROM empleados GROUP BY departamento;", language="sql")
    
    if st.button("Ejecutar ejemplo 2", key="count_ej2"):
        df, error = ejecutar_consulta(st.session_state.conn, "SELECT departamento, COUNT(*) as cantidad FROM empleados GROUP BY departamento")
        if error:
            st.error(f"Error: {error}")
        else:
            st.dataframe(df)
    
    # Ejercicio
    st.subheader("¡Tu turno!")
    st.write("Calcula el salario promedio por departamento (usa AVG en lugar de COUNT):")
    consulta_usuario = st.text_area("Tu consulta SQL:", key="count_ejercicio")
    
    if st.button("Ejecutar mi consulta", key="count_ejecutar"):
        if consulta_usuario.strip():
            df, error = ejecutar_consulta(st.session_state.conn, consulta_usuario)
            if error:
                st.error(f"Error: {error}")
            else:
                st.success("¡Excelente análisis!")
                st.dataframe(df)

elif seccion == "6. JOIN - Unir tablas":
    st.header("JOIN - Combinar información de diferentes tablas")
    st.write("""
    **JOIN** nos permite combinar datos de dos o más tablas relacionadas.
    
    **Sintaxis básica:**
    ```sql
    SELECT columnas 
    FROM tabla1 
    JOIN tabla2 ON tabla1.columna = tabla2.columna;
    ```
    """)
    
    st.subheader("Ejemplo práctico")
    st.write("**Combinar empleados con información de departamentos:**")
    st.code("""
    SELECT e.nombre, e.apellido, e.departamento, d.presupuesto
    FROM empleados e
    JOIN departamentos d ON e.departamento = d.nombre;
    """, language="sql")
    
    if st.button("Ejecutar ejemplo JOIN"):
        query = """
        SELECT e.nombre, e.apellido, e.departamento, d.presupuesto
        FROM empleados e
        JOIN departamentos d ON e.departamento = d.nombre
        """
        df, error = ejecutar_consulta(st.session_state.conn, query)
        if error:
            st.error(f"Error: {error}")
        else:
            st.dataframe(df)
    
    st.write("""
    **Explicación:**
    - **e** y **d** son alias (nombres cortos) para las tablas
    - **ON** especifica cómo se relacionan las tablas
    - Podemos acceder a columnas de ambas tablas en el resultado
    """)

elif seccion == "7. Práctica libre":
    st.header("Zona de práctica libre")
    st.write("Aquí puedes experimentar con cualquier consulta SQL que quieras probar.")
    
    # Recordatorio de las tablas disponibles
    st.subheader("Tablas disponibles:")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**empleados:**")
        st.write("- id, nombre, apellido")
        st.write("- departamento, salario")
        st.write("- fecha_contratacion")
    
    with col2:
        st.write("**departamentos:**")
        st.write("- id, nombre")
        st.write("- presupuesto")
    
    # Sugerencias de consultas
    st.subheader("Sugerencias de consultas para probar:")
    sugerencias = [
        "SELECT * FROM empleados WHERE salario BETWEEN 45000 AND 55000;",
        "SELECT departamento, AVG(salario) as salario_promedio FROM empleados GROUP BY departamento;",
        "SELECT * FROM empleados ORDER BY fecha_contratacion DESC;",
        "SELECT COUNT(*) FROM empleados WHERE fecha_contratacion >= '2020-01-01';"
    ]
    
    for i, sugerencia in enumerate(sugerencias, 1):
        if st.button(f"Usar sugerencia {i}", key=f"sugerencia_{i}"):
            st.session_state.consulta_libre = sugerencia
    
    # Editor de consultas
    consulta_usuario = st.text_area(
        "Escribe tu consulta SQL:",
        value=st.session_state.get('consulta_libre', ''),
        height=100,
        key="practica_libre"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        ejecutar = st.button("Ejecutar consulta")
    with col2:
        if st.button("Limpiar"):
            st.session_state.consulta_libre = ""
            st.experimental_rerun()
    
    if ejecutar and consulta_usuario.strip():
        df, error = ejecutar_consulta(st.session_state.conn, consulta_usuario)
        if error:
            st.error(f"Error: {error}")
            st.write("**Consejos para corregir errores comunes:**")
            st.write("- Verifica que los nombres de columnas y tablas estén correctos")
            st.write("- Asegúrate de usar comillas simples para texto: 'texto'")
            st.write("- Revisa que la sintaxis sea correcta")
        else:
            st.success("Consulta ejecutada correctamente")
            st.dataframe(df)
            
            # Mostrar estadísticas del resultado
            st.write(f"**Resultado:** {len(df)} filas y {len(df.columns)} columnas")

# Footer
st.markdown("---")
st.markdown("### Consejos finales")
st.write("""
- **Practica regularmente**: La mejor forma de aprender SQL es practicando
- **Empieza simple**: Domina las consultas básicas antes de pasar a las complejas
- **Lee los errores**: Los mensajes de error te ayudan a entender qué está mal
- **Experimenta**: No tengas miedo de probar diferentes consultas
""")