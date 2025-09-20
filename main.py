
import streamlit as st
import gspread
import json

# Leer el secreto desde Streamlit Cloud
service_account_info = json.loads(st.secrets["google"]["service_account_json"])
gc = gspread.service_account_from_dict(service_account_info)
sh = gc.open("MiBaseDeDatos")
worksheet = sh.sheet1


data = worksheet.get_all_records()

st.title("Rifa andrea - Asigna y quita nombres")

# ✅ Calcular totales
total_vendidos = sum(1 for row in data if row["nombre"])  # con nombre asignado
total_libres = sum(1 for row in data if not row["nombre"])  # sin nombre

# Mostrar totales
st.subheader("📊 Totales")
col1, col2 = st.columns(2)
col1.metric("Números vendidos", total_vendidos)
col2.metric("Números libres", total_libres)

# Filtro por estado
estado = st.radio("Filtrar por:", ["Todos", "Libres", "Asignados"])
if estado == "Libres":
    data_filtrada = [row for row in data if not row['nombre']]
elif estado == "Asignados":
    data_filtrada = [row for row in data if row['nombre']]
else:
    data_filtrada = data

# Mostrar tabla filtrada
st.write("Números y nombres:")
st.dataframe(data_filtrada, use_container_width=True)

# Seleccionar número (solo los filtrados)
numeros = [row['numero'] for row in data_filtrada]
if numeros:
    numero = st.selectbox("Selecciona un número", numeros)
    nombre_actual = next((row['nombre'] for row in data if row['numero'] == numero), "")

    st.write(f"Nombre actual: {nombre_actual if nombre_actual else 'Sin asignar'}")

    nuevo_nombre = st.text_input("Nuevo nombre para este número", value=nombre_actual)
    if st.button("Asignar nombre"):
        cell = worksheet.find(str(numero))
        worksheet.update_cell(cell.row, cell.col + 1, nuevo_nombre)
        st.success("Nombre asignado correctamente")
        st.rerun()  # <-- Recarga la app


    if st.button("Quitar nombre"):
        cell = worksheet.find(str(numero))
        worksheet.update_cell(cell.row, cell.col + 1, "")
        st.success("Nombre quitado correctamente")
        st.rerun()  # <-- Recarga la app

else:
    st.info("No hay números en este filtro.")
