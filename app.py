import streamlit as st
from azure.storage.blob import BlobServiceClient
from datetime import datetime

# Configuración de Azure Blob Storage
STORAGE_ACCOUNT_NAME = "propositodevida"
STORAGE_ACCOUNT_KEY = "Oab9z2ETu3g+Btk4pghs52nP7iJj39MJHjIOBl2md72nuH8ojNE1vLENpF8BI"
CONTAINER_NAME = "propositodevida"

# Conecta a Azure Blob Storage
connection_string = f"DefaultEndpointsProtocol=https;AccountName={STORAGE_ACCOUNT_NAME};AccountKey={STORAGE_ACCOUNT_KEY};EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Título de la aplicación
st.title("Subida de Videos a Azure Blob Storage")

# Pedir nombre y apellido al usuario
first_name = st.text_input("Nombre:", placeholder="Ingresa tu nombre")
last_name = st.text_input("Apellido:", placeholder="Ingresa tu apellido")

# Verificar que el usuario haya ingresado su nombre y apellido
if first_name and last_name:
    user_name = f"{first_name}_{last_name}"  # Combina nombre y apellido

    # Subir archivo de video
    uploaded_file = st.file_uploader("Selecciona un archivo de video para cargar (formatos soportados: MP4, AVI, MOV)", type=["mp4", "avi", "mov"])

    if uploaded_file is not None:
        st.write(f"Archivo seleccionado: {uploaded_file.name}")

        # Leer contenido del archivo
        file_contents = uploaded_file.read()

        # Generar un timestamp para crear un nombre único
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        blob_name = f"{user_name}_{timestamp}_{uploaded_file.name}"

        # Botón para subir archivo
        if st.button("Subir archivo a Azure Blob Storage"):
            try:
                # Crear un blob cliente
                blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blob_name)

                # Subir el archivo al contenedor
                blob_client.upload_blob(file_contents, overwrite=True)

                st.success(f"El archivo '{blob_name}' se cargó correctamente a Azure Blob Storage.")
            except Exception as e:
                st.error(f"Error al cargar el archivo: {e}")
else:
    st.warning("Por favor, ingresa tu nombre y apellido antes de subir un archivo.")
