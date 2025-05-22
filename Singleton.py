from abc import ABC, ABCMeta, abstractmethod
from threading import Lock

# Esta es una interfaz. Define qué debe hacer un logger, sin decir cómo.
class ILogger(ABC):
    @abstractmethod
    def log(self, message: str) -> None:
        pass

# Esta clase hace que cualquier clase que la use tenga una única instancia.
class SingletonMeta(ABCMeta):
    _instances = {}       # Aquí se guardan las instancias
    _lock: Lock = Lock()  # Esto asegura que no se creen 2 instancias al mismo tiempo

    def __call__(cls, *args, **kwargs):
        with cls._lock:  # Protege el acceso
            if cls not in cls._instances:
                print("[SingletonMeta] Creando nueva instancia de", cls.__name__)
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
            else:
                print("[SingletonMeta] Usando instancia existente de", cls.__name__)
        return cls._instances[cls]

# Este es el logger real que usaremos. Solo existirá una instancia gracias a SingletonMeta.
class Logger(ILogger, metaclass=SingletonMeta):
    def __init__(self):
        self.logs = []

    def log(self, message: str) -> None:
        self.logs.append(message)
        print(f"[Logger] {message}")  # Aquí muestra el mensaje en la consola

# Esta clase se encarga de "procesar" eventos y avisar al logger.
class EventProcessor:
    def __init__(self, logger: ILogger):
        self.logger = logger  # Recibe el logger como parámetro

    def process_event(self, event_name: str) -> None:
        self.logger.log(f"Procesando evento: {event_name}")  # Registra el evento

# Esta clase mejora la anterior, agregando mensajes antes y después del evento.
class DetailedEventProcessor(EventProcessor):
    def process_event(self, event_name: str) -> None:
        self.logger.log(f"[Inicio del evento] {event_name}")  # Antes de procesar
        super().process_event(event_name)                    # Procesa normal
        self.logger.log(f"[Fin del evento] {event_name}")    # Después de procesar

# Aquí empieza el programa
if __name__ == "__main__":
    print("🚀 Iniciando el sistema de registro de eventos...")

    # Creamos el logger (aunque si se crea otro más tarde, será el mismo)
    logger = Logger()

    # Creamos el procesador que usará ese logger
    processor = DetailedEventProcessor(logger)

    # Simulamos que ocurren algunos eventos
    print("\n📌 Simulando eventos...\n")
    processor.process_event("Inicio de sesión del usuario")
    processor.process_event("Subida de archivo por el usuario")

    # Verificamos que el logger es singleton
    print("\n🔁 Probando que el logger es único (Singleton)...")
    another_logger = Logger()
    if logger is another_logger:
        print("✅ Ambos loggers son el mismo objeto. ¡Funciona el Singleton!")
    else:
        print("❌ Hay más de un logger. Algo salió mal.")
