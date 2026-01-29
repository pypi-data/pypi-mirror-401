# ==============================================
# CODE TO SAVE DATA IN ORIGIN
# ==============================================

print("\n" + "="*50)
print("GUARDANDO DATOS EN ARCHIVOS")
print("="*50)

# Determine how many files we need to create
num_archivos = len(F_ph_array)
print(f"Se crearán {num_archivos} archivo(s) de datos")

# For each F_ph value, create a file with the corresponding data
for idx, fph_valor in enumerate(F_ph_array):

    # Obtain the data of Sigma and Source for this specific F_ph
    # (Note: In the original code, the lists are reset in each iteration)
    # For this example, we assume we want to save the data from the last calculation
    # But if you need to save all calculations, you should store them in a list

    # Create filename based on the F_ph value
    nombre_archivo = f"photo_stimulation_Fph_{fph_valor:.1f}nm.txt"

    # Verify that we have the necessary data
    if len(longitud_array) == len(Sigma1_array) == len(Sigma2_array) == len(Sigma3_array) == len(Fuente_Luz_array):

        # Create array with the data to save
        # Make sure to take the real part of complex arrays
        datos_fph = np.column_stack((
            longitud_array.real,     # Columna 1: LONG (longitud de onda)
            Sigma1_array.real,       # Columna 2: SIGMA1
            Sigma2_array.real,       # Columna 3: SIGMA2
            Sigma3_array.real,       # Columna 4: SIGMA3
            Fuente_Luz_array.real    # Columna 5: FUENTE
        ))

        # Save in text file with format suitable for Origin
        np.savetxt(nombre_archivo, datos_fph,
                   delimiter='\t',
                   fmt=['%.2f', '%.6e', '%.6e', '%.6e', '%.6f'],
                   header='LONG\tSIGMA1\tSIGMA2\tSIGMA3\tFUENTE',
                   comments='')

        print(f"✅ File '{nombre_archivo}' created")
        print(f"   Values: LONG({len(longitud_array)}), F_ph={fph_valor:.1f}nm")

    else:
        print(f"⚠️  Error: Data arrays do not have the same length")

print("\n" + "="*50)
print(f"TOTAL: {num_archivos} file(s) created")
print("="*50)

# If there are multiple F_ph values, we can also save a summary file
if len(F_ph_array) > 1:
    print("\n" + "="*50)
    print("CREATING PARAMETER SUMMARY FILE")
    print("="*50)

    # Create summary file with pf values for each F_ph
    datos_resumen = np.column_stack((
        F_ph_array,              # Columna 1: F_ph
        np.array(pf1_v),         # Columna 2: pf1
        np.array(pf2_v),         # Columna 3: pf2
        np.array(pf3_v)          # Columna 4: pf3
    ))

    np.savetxt("resumen_parametros.txt", datos_resumen,
               delimiter='\t',
               fmt=['%.2f', '%.6e', '%.6e', '%.6e'],
               header='F_ph\tpf1\tpf2\tpf3',
               comments='')

    print("✅ File 'summary_parameters.txt' created")
    print("\nSummary content:")
    print("F_ph\t\tpf1\t\t\tpf2\t\t\tpf3")
    print("-"*70)
    for i in range(len(F_ph_array)):
        print(f"{F_ph_array[i]:.2f}\t{pf1_v[i]:.6e}\t{pf2_v[i]:.6e}\t{pf3_v[i]:.6e}")

# ==============================================
# CÓDIGO PARA DESCARGAR ARCHIVOS (Google Colab)
# ==============================================

print("\n" + "="*50)
print("DESCARGANDO ARCHIVOS")
print("="*50)

try:
    # Intentar importar para Google Colab
    from google.colab import files

    # Descargar cada archivo individual creado
    for idx, fph_valor in enumerate(F_ph_array):
        nombre_archivo = f"foto_estimulacion_Fph_{fph_valor:.1f}nm.txt"
        files.download(nombre_archivo)
        print(f"📥 Descargado: {nombre_archivo}")

    # Si existe, descargar también el archivo resumen
    if len(F_ph_array) > 1:
        files.download("resumen_parametros.txt")
        print("📥 Descargado: resumen_parametros.txt")

except ImportError:
    print("⚠️  No se encuentra Google Colab - los archivos se guardaron localmente")
    print("   Archivos creados:")
    for idx, fph_valor in enumerate(F_ph_array):
        nombre_archivo = f"foto_estimulacion_Fph_{fph_valor:.1f}nm.txt"
        print(f"   • {nombre_archivo}")
    if len(F_ph_array) > 1:
        print("   • resumen_parametros.txt")

print("\n" + "="*50)
print("PROCESO COMPLETADO")
print("="*50)
