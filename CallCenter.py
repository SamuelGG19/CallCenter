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

def separar_grupos(cola: PriorityQueue) -> PriorityQueue:
    if len(cola) == 0:
        raise EmptyQueueError()

    grupo = PriorityQueue()
    cola_aux = PriorityQueue()
    prioridades = {}
    while len(cola) != 0:
        mensaje = cola.dequeue()
        if mensaje.prioridad in prioridades:
            prioridades[mensaje.prioridad] += 1
        else:
            prioridades[mensaje.prioridad] = 1
        cola_aux.enqueue(mensaje)

    for peso, cont in prioridades.items():
        if cont == max(prioridades.values()):
            prioridad = peso

    while len(cola_aux) != 0:
        mensaje = cola_aux.dequeue()
        if mensaje.prioridad == prioridad:
            grupo.enqueue(mensaje)
        else:
            cola.enqueue(mensaje)

    return grupo

def obtener_primero_y_ultimo(cola: PriorityQueue) -> PriorityQueue:
    if len(cola) == 0:
        raise EmptyQueueError()

    grupo = separar_grupos(cola)
    if len(grupo) == 1:
        primero = PriorityQueue()
        primero.enqueue(grupo.dequeue())
        return primero

    primero_y_ultimo = PriorityQueue()
    primero_y_ultimo.enqueue(grupo.dequeue())
    while len(grupo) > 1:
        cola.enqueue(grupo.dequeue())

    primero_y_ultimo.enqueue(grupo.dequeue())
    return primero_y_ultimo

def largo_y_corto(cola: PriorityQueue) -> PriorityQueue:
    if len(cola) == 0:
        raise EmptyQueueError()

    grupo = separar_grupos(cola)
    if len(grupo) == 1:
        unico = PriorityQueue()
        unico.enqueue(grupo.dequeue())
        return unico
    
    largo_y_corto = PriorityQueue()

    for i in range(len(grupo)):
        anterior_m = None
        anterior_M = None
    
        if i != 0:
            if len(grupo.first().mensaje) < len(mas_corto.mensaje):
                anterior_m = mas_corto
                mas_corto = grupo.dequeue()
            
            elif len(grupo.first().mensaje) > len(mas_largo.mensaje):
                anterior_M = mas_largo
                mas_largo = grupo.dequeue()
            
            else:
                cola_aux.enqueue(grupo.dequeue())

        else:
            mas_corto = grupo.first()
            mas_largo = grupo.dequeue()
            cola_aux = PriorityQueue()
        
        if anterior_m != mas_largo and anterior_m is not None:
            cola_aux.enqueue(anterior_m)
        if anterior_M != mas_corto and anterior_M is not None:
            cola_aux.enqueue(anterior_M)
        

    for _ in range(len(cola_aux)):
        cola.enqueue(cola_aux.dequeue())

    largo_y_corto.enqueue(mas_largo)
    largo_y_corto.enqueue(mas_corto)
    return largo_y_corto
    

if __name__ == "__main__":
    cola_mensajes = PriorityQueue()

    agente1 = Agente("experto")
    agente2 = Agente("intermedio")
    agente3 = Agente("basico")

    ingresar_mensajes(cola_mensajes)
    if len(cola_mensajes) != 0:
        while True:
            opc = input("Ingrese 1 para atender todos los mensajes.\nIngrese 2 para atender el primero y el último.\nIngrese 3 para atender el más largo y el más corto.\nOpción: ")
            if opc == "1":
                thread1 = Thread(target=agente1.atender_mensaje, args=(cola_mensajes,))
                thread2 = Thread(target=agente2.atender_mensaje, args=(cola_mensajes,))
                thread3 = Thread(target=agente3.atender_mensaje, args=(cola_mensajes,))
                break
            if opc == "2":
                grupo = obtener_primero_y_ultimo(cola_mensajes)
                thread1 = Thread(target=agente1.atender_mensaje, args=(grupo,))
                thread2 = Thread(target=agente2.atender_mensaje, args=(grupo,))
                thread3 = Thread(target=agente3.atender_mensaje, args=(grupo,))
                break
            if opc == "3":
                grupo = largo_y_corto(cola_mensajes)
                thread1 = Thread(target=agente1.atender_mensaje, args=(grupo,))
                thread2 = Thread(target=agente2.atender_mensaje, args=(grupo,))
                thread3 = Thread(target=agente3.atender_mensaje, args=(grupo,))
                break
        

        while True:
            if len(cola_mensajes) == 0 or opc == 2 or opc == 3:
                opcion = input("Terminar? (Y/N): ")
                if opcion.upper() == "Y":
                    break
                if opcion.upper() == "N":
                    ingresar_mensajes(cola_mensajes)
                    while True:
                        opc = input("Ingrese 1 para atender todos los mensajes.\nIngrese 2 para atender el primero y el último.\nIngrese 3 para atender el más largo y el más corto.\nOpción: ")
                        if opc == "1":
                            thread1 = Thread(target=agente1.atender_mensaje, args=(cola_mensajes,))
                            thread2 = Thread(target=agente2.atender_mensaje, args=(cola_mensajes,))
                            thread3 = Thread(target=agente3.atender_mensaje, args=(cola_mensajes,))
                            break
                        if opc == "2":
                            grupo = obtener_primero_y_ultimo(cola_mensajes)
                            thread1 = Thread(target=agente1.atender_mensaje, args=(grupo,))
                            thread2 = Thread(target=agente2.atender_mensaje, args=(grupo,))
                            thread3 = Thread(target=agente3.atender_mensaje, args=(grupo,))
                            break
                        if opc == "3":
                            grupo = largo_y_corto(cola_mensajes)
                            thread1 = Thread(target=agente1.atender_mensaje, args=(grupo,))
                            thread2 = Thread(target=agente2.atender_mensaje, args=(grupo,))
                            thread3 = Thread(target=agente3.atender_mensaje, args=(grupo,))
                            break

                else:
                    continue

            opc = int(opc)

            thread1.start()
            thread2.start()
            thread3.start()

            thread1.join()
            thread2.join()
            thread3.join()
