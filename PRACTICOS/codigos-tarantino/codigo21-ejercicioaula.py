class EscritorDeArchivos:
  def __init__(self, archivo, agregarAlFinal=False):
      modo = 'a' if agregarAlFinal else 'w'
      self.escritor = open(archivo, modo)

  def cerrar(self):
      self.escritor.close()

  def escribir(self, texto):
      datos_escritos = False
      if not self.escritor.closed:
          self.escritor.write(texto + "\n")
          datos_escritos = True
      return datos_escritos


# --------------------------
# 🧪 Programa principal
# --------------------------
def main():
  escritor = EscritorDeArchivos("Prueba.txt")  # Crea o sobreescribe el archivo
  exito = escritor.escribir("Hola mundo")

  if exito:
      print("✅ Texto escrito correctamente.")
  else:
      print("❌ No se pudo escribir en el archivo.")

  escritor.cerrar()


if __name__ == "__main__":
  main()