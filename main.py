import streamlit as st
import pandas as pd
import database

st.title("Empleados")
st.sidebar.title("Navegación")

database.ejecutar_query("""
    CREATE TABLE IF NOT EXISTS empleados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        apellido TEXT,
        edad INTEGER,
        sexo TEXT,
        correo TEXT,
        puesto TEXT,
        area TEXT,
        salario REAL,
        turno TEXT,
        fecha_ingreso TEXT,
        tipo_contrato TEXT,
        estatus TEXT
    )
""")
empleados = database.ejecutar_query("SELECT * FROM empleados")

opciones = ["Todos", "Crear", "Editar", "Borrar"]
opcion_seleccionada = st.sidebar.radio("Opciones:", opciones)

st.subheader(opcion_seleccionada)

if opcion_seleccionada == opciones[0]:
    df = pd.DataFrame(empleados, columns=["ID","nombre", "apellido", "edad", "sexo", "correo", "puesto", "area", "salario", "turno" ,"fecha_ingreso", "tipo_contrato", "estatus"])
    st.dataframe(df)

if opcion_seleccionada == opciones[1]:
    with st.form("formulario_crear_empleados", clear_on_submit=True):
        
        nombre = st.text_input("Nombre")
        apellido = st.text_input("Apellido")
        edad = st.number_input("Edad", min_value=18, max_value=80, step=1)
        sexo = st.selectbox("Sexo", ["M", "F", "Otro"])
        correo = st.text_input("Correo electronico")
        puesto = st.text_input("Puesto")
        area = st.text_input("Area / Departamento")
        salario = st.number_input("Salario", min_value=0.0, step=500.0)
        turno = st.selectbox("Turno", ["Matutino", "Vespertino", "Nocturno"])
        fecha_ingreso = st.date_input("Fecha de ingreso")
        tipo_contrato = st.selectbox("Tipo de contrato", ["Indefinido", "Temporal", "Practicas", "Honorarios"])
        estatus = st.selectbox("Estatus", ["Activo", "Inactivo", "Baja"])

        
        submit = st.form_submit_button("Crear")

        if submit:
            if nombre and apellido and correo and puesto and area:
                database.ejecutar_query("""
                    INSERT INTO empleados (
                        nombre, 
                        apellido, 
                        edad, 
                        sexo, 
                        correo, 
                        puesto, 
                        area, 
                        salario, 
                        turno, 
                        fecha_ingreso, 
                        tipo_contrato,
                        estatus
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                    """, 
                (nombre, apellido, edad, sexo, correo, puesto, area, salario, turno ,fecha_ingreso, tipo_contrato, estatus)
                )
            else:
                st.error("Todos los campos son obligatorios")

if opcion_seleccionada == opciones[2]:
    empleado_selc = st.selectbox("Nombre", empleados, format_func=lambda e: f"{e[1]} {e[2]}")
    with st.form("formulario_crear_empleados", clear_on_submit=True):
        print(empleado_selc)
        nombre = st.text_input("Nombre", value=empleado_selc[1])
        apellido = st.text_input("Apellido", value=empleado_selc[2])
        edad = st.number_input("Edad", min_value=18, max_value=80, step=1,value=empleado_selc[3])
        
        x = ["M", "F", "Otro"]
        sexo = st.selectbox("Sexo", x, index=x.index(empleado_selc[4]))
        
        correo = st.text_input("Correo electronico", value=empleado_selc[5])
        puesto = st.text_input("Puesto", value=empleado_selc[6])
        area = st.text_input("Area / Departamento", value=empleado_selc[7])
        salario = st.number_input("Salario", min_value=0.0, step=500.0, value=empleado_selc[8])
        
        x = ["Matutino", "Vespertino", "Nocturno"]
        turno = st.selectbox("Turno", x, index=x.index(empleado_selc[9]))
        fecha_ingreso = st.date_input("Fecha de ingreso", value=empleado_selc[10])
        
        x = ["Indefinido", "Temporal", "Practicas", "Honorarios"]
        tipo_contrato = st.selectbox("Tipo de contrato", x, index=x.index(empleado_selc[11]))
        
        x= ["Activo", "Inactivo", "Baja"]
        estatus = st.selectbox("Estatus", x, index=x.index(empleado_selc[12]))

        
        submit = st.form_submit_button("Editar")

        if submit:
            if nombre and apellido and correo and puesto and area:
                database.ejecutar_query("""
                    UPDATE empleados
                        SET 
                            nombre = ?, 
                            apellido = ?, 
                            edad = ?, 
                            sexo = ?, 
                            correo = ?, 
                            puesto = ?, 
                            area = ?, 
                            salario = ?, 
                            turno = ?, 
                            fecha_ingreso = ?, 
                            tipo_contrato = ?, 
                            estatus = ?
                        WHERE id = ?;
                    """, 
                (nombre, apellido, edad, sexo, correo, puesto, area, salario, turno ,fecha_ingreso, tipo_contrato, estatus, empleado_selc[0])
                )
                st.rerun()
            else:
                st.error("Todos los campos son obligatorios")
            
if opcion_seleccionada == opciones[3]:
    with st.form("formulario_borrar_empleado"):
        empleado = st.selectbox("Nombre", empleados, format_func=lambda e: f"{e[1]} {e[2]}")
        submit = st.form_submit_button("Borrar")
        if submit:
            database.ejecutar_query("DELETE FROM empleados WHERE id = ?", (str(empleado[0])))
            st.rerun()