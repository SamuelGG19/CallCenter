from threading import Thread
import time

palabras_clave = {"emergencia": 10,
                  "fallo critico": 9,
                  "urgente": 8,
                  "problema": 5,
                  "consulta": 2,
                  "duda": 1}

class EmptyQueueError(Exception):
    def __init__(self, message="La cola está vacía."):
        self.message = message

        super().__init__(self.message)

class NivelAgenteError(Exception):
    def __init__(self, message="El nivel del agente debe ser: basico, intermedio o experto."):
        self.message = message

        super().__init__(self.message)

class Mensaje:
    def __init__(self, mensaje: str):
        self.mensaje = mensaje
        self.prioridad = 0
        for palabra_clave, peso in palabras_clave.items():
            if palabra_clave in mensaje.lower():
                self.prioridad += peso

    def __lt__(self, other) -> bool:
        return self.prioridad < other.prioridad

    def __repr__(self) -> str:
        return self.mensaje

class PriorityQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, mensaje: Mensaje):
        self.queue.append(mensaje)
        self.queue.sort(reverse=True)

    def dequeue(self) -> Mensaje:
        if len(self.queue) == 0:
            raise EmptyQueueError()
        return self.queue.pop(0)

    def first(self) -> Mensaje:
        if len(self.queue) == 0:
            raise EmptyQueueError()
        return self.queue[0]

    def __len__(self) -> int:
        return len(self.queue)

    def __repr__(self) -> str:
        return str(self.queue)

class Agente:
    def __init__(self, nivel_experiencia: str):
        niveles = {"basico": 0, "intermedio": 1, "experto": 2}
        if nivel_experiencia not in niveles:
            raise NivelAgenteError()

        self.id = nivel_experiencia
        self.nivel_experiencia = niveles[nivel_experiencia]
        self.disponible = True

    def tiempo_atencion(self, mensaje: Mensaje) -> float:
        factores = [1, 0.75, 0.5]
        factor_nivel = factores[self.nivel_experiencia]

        tiempo_estimado = (len(mensaje.mensaje.split()) / 10) + (mensaje.prioridad / 2)
        return tiempo_estimado * factor_nivel

    def atender_mensaje(self, cola: PriorityQueue):
        while True:
            try:
                mensaje = cola.dequeue()
            except EmptyQueueError:
                return
            else:
                self.disponible = False
                tiempo_estimado = self.tiempo_atencion(mensaje)
                print(f"Agente {self.id} atendiendo mensaje: {mensaje}")
                time.sleep(tiempo_estimado)
                print(f"Agente {self.id} ha terminado de atender el mensaje: {mensaje.mensaje}")
                self.disponible = True

    def __repr__(self) -> str:
        return f"Agente {self.id}"


def ingresar_mensajes(cola: PriorityQueue):
    while True:
        opc = input("Ingresar mensaje? (Y/N): ")
        if opc.upper() == "Y":
            mensaje = input("Ingrese el mensaje: ")
            cola.enqueue(Mensaje(mensaje))
        elif opc.upper() == "N":
            return
        else:
            ...

def separar_grupos(cola: PriorityQueue):
    cola_aux = cola
    prioridades = {}
    while True:
        



if __name__ == "__main__":
    cola_mensajes = PriorityQueue()

    agente1 = Agente("experto")
    agente2 = Agente("intermedio")
    agente3 = Agente("basico")

    ingresar_mensajes(cola_mensajes)

    thread1 = Thread(target=agente1.atender_mensaje, args=(cola_mensajes,))
    thread2 = Thread(target=agente2.atender_mensaje, args=(cola_mensajes,))
    thread3 = Thread(target=agente3.atender_mensaje, args=(cola_mensajes,))

    while True:
        if len(cola_mensajes) == 0:
            opcion = input("Terminar? (Y/N): ")
            if opcion.upper() == "Y":
                break
            elif opcion.upper() == "N":
                ingresar_mensajes(cola_mensajes)
                thread1 = Thread(target=agente1.atender_mensaje, args=(cola_mensajes,))
                thread2 = Thread(target=agente2.atender_mensaje, args=(cola_mensajes,))
                thread3 = Thread(target=agente3.atender_mensaje, args=(cola_mensajes,))
            else:
                continue

        thread1.start()
        thread2.start()
        thread3.start()

        thread1.join()
        thread2.join()
        thread3.join()
