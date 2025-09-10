from collections import defaultdict, deque

# Definición de tareas y sus propiedades
tasks = {
    'A': {'desc': 'Identificar servidores afectados', 'duration': 15, 'deps': []},
    'B': {'desc': 'Priorizar datos críticos', 'duration': 20, 'deps': []},
    'C': {'desc': 'Activar protocolo de recuperación', 'duration': 10, 'deps': ['A', 'B']},
    'D': {'desc': 'Asignar técnicos a servidores', 'duration': 5, 'deps': ['C']},
    'E': {'desc': 'Recuperar datos de servidor 1', 'duration': 30, 'deps': ['D']},
    'F': {'desc': 'Recuperar datos de servidor 2', 'duration': 25, 'deps': ['D', 'E']},  # Solo uno a la vez
    'G': {'desc': 'Validar integridad de datos recuperados', 'duration': 15, 'deps': ['F']},
    'H': {'desc': 'Generar informe preliminar para dirección', 'duration': 10, 'deps': ['G']},
    'I': {'desc': 'Comunicar a clientes afectados', 'duration': 20, 'deps': ['G']},
    'J': {'desc': 'Coordinar con equipo legal', 'duration': 15, 'deps': ['G']},
    'K': {'desc': 'Preparar plan de contingencia', 'duration': 25, 'deps': ['G']},
}

# Recursos disponibles
NUM_TECHNICIANS = 3
TOTAL_TIME = 120  # minutos

# Representación de dependencias (grafo dirigido)
def build_dependency_graph(tasks):
    graph = defaultdict(list)
    indegree = defaultdict(int)
    for t, props in tasks.items():
        for dep in props['deps']:
            graph[dep].append(t)
            indegree[t] += 1
        if t not in indegree:
            indegree[t] = 0
    return graph, indegree

# Algoritmo para calcular el cronograma (simplificado)
def schedule_tasks(tasks):
    graph, indegree = build_dependency_graph(tasks)
    queue = deque([t for t in tasks if indegree[t] == 0])
    start_times = {}
    finish_times = {}
    technicians = [0] * NUM_TECHNICIANS  # tiempo libre de cada técnico

    while queue:
        task = queue.popleft()
        # Determinar el tiempo de inicio: máximo de los predecesores
        start = 0
        for dep in tasks[task]['deps']:
            start = max(start, finish_times[dep])
        # Asignar técnico disponible más pronto
        tech_available = min(technicians)
        start = max(start, tech_available)
        duration = tasks[task]['duration']
        finish = start + duration
        start_times[task] = start
        finish_times[task] = finish
        # Asignar técnico (solo para tareas que requieren técnicos)
        if task in ['D', 'E', 'F', 'G']:
            idx = technicians.index(tech_available)
            technicians[idx] = finish
        # Agregar tareas dependientes
        for neighbor in graph[task]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    return start_times, finish_times

def print_schedule(tasks, start_times, finish_times):
    print("Cronograma de Rescate de Datos Críticos:\n")
    for t in sorted(tasks, key=lambda x: start_times[x]):
        print(f"{t}: {tasks[t]['desc']}")
        print(f"   Inicio: {start_times[t]} min | Fin: {finish_times[t]} min | Duración: {tasks[t]['duration']} min\n")

if __name__ == "__main__":
    start_times, finish_times = schedule_tasks(tasks)
    print_schedule(tasks, start_times, finish_times)
    total = max(finish_times.values())
    print(f"Tiempo total estimado: {total} minutos (límite: {TOTAL_TIME} minutos)")
    if total > TOTAL_TIME:
        print("¡Advertencia! El plan excede el tiempo disponible.")