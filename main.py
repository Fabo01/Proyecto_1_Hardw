# Este programa procesa un archivo WAV estéreo para obtener información básica sobre el audio.
# Además, extrae el canal derecho (que está invertido), lo reconstruye, lo convierte a mono,
# reduce la frecuencia de muestreo a 22050 Hz y guarda el resultado en out.wav.
# Solo se utiliza el módulo wave de la biblioteca estándar de Python.

import wave

# Nombre del archivo de audio de entrada y salida
archivo_entrada = 'song.wav'
archivo_salida = 'out.wav'

print('Abriendo archivo de entrada...\n')
# Abrir el archivo WAV de entrada en modo lectura binaria
with wave.open(archivo_entrada, 'rb') as wav_in:
    print('Leyendo parámetros del archivo WAV...\n')
    # Obtener parámetros del archivo de entrada
    num_canales = wav_in.getnchannels()  # Debe ser 2 (estéreo)
    frecuencia_muestreo = wav_in.getframerate()  # Debe ser 44100
    num_muestras = wav_in.getnframes()
    tamaño_bytes = wav_in.getsampwidth()  # Debe ser 2 bytes (16 bits)
    print(f'Canales: {num_canales}, \nFrecuencia: {frecuencia_muestreo} Hz, \nMuestras: {num_muestras}, \nTamaño muestra: {tamaño_bytes} bytes\n')
    print('Leyendo todos los frames del archivo...\n')
    # Leer todos los frames del archivo (cada frame contiene muestras de ambos canales)
    frames = wav_in.readframes(num_muestras)
    print(f'Tamaño total de los frames leídos: {len(frames)} bytes\n') # Total de bytes leídos

print('Extrayendo canal derecho...\n')
# Extraer el canal derecho:
# Cada frame tiene 4 bytes (2 bytes canal izquierdo, 2 bytes canal derecho)
# Vamos a extraer solo los bytes del canal derecho
canal_derecho = bytearray()
for i in range(0, len(frames), 4):
    # Tomar los dos bytes correspondientes al canal derecho
    canal_derecho += frames[i+2:i+4]
print(f'Total de muestras extraídas del canal derecho: {len(canal_derecho)//2}\n')

print('Invirtiendo el canal derecho para reconstruir el orden original...\n')
# El canal derecho está invertido, así que lo reconstruimos invirtiendo el orden de las muestras
# Cada muestra son 2 bytes, así que invertimos de a 2 bytes
muestras = [canal_derecho[i:i+2] for i in range(0, len(canal_derecho), 2)]
muestras_invertidas = muestras[::-1]

print('Realizando downsampling (reducción de frecuencia a 22050 Hz)...\n')
# Downsampling: reducir la frecuencia de muestreo a la mitad (de 44100 a 22050 Hz)
# Para esto, tomamos una de cada dos muestras
muestras_downsampled = muestras_invertidas[::2]
print(f'Total de muestras tras downsampling: {len(muestras_downsampled)}\n')

# Unimos las muestras en un solo bloque de bytes
datos_salida = b''.join(muestras_downsampled)

print('Guardando el resultado en out.wav (mono, 16 bits, 22050 Hz)...\n')
# Guardar el resultado en un nuevo archivo WAV mono, 16 bits, 22050 Hz
with wave.open(archivo_salida, 'wb') as wav_out:
    wav_out.setnchannels(1)  # Mono
    wav_out.setsampwidth(2)  # 16 bits
    wav_out.setframerate(22050)  # 22050 Hz
    wav_out.writeframes(datos_salida)

print('Procesamiento completado. Archivo out.wav generado correctamente.\n')