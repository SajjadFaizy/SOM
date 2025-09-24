# Bericht zum KI-Projekt: Türme von Hanoi

## 1. Einleitung
Die Aufgabe des Projekts war es, das klassische Rätsel der "Türme von Hanoi" zu implementieren und eine künstliche Intelligenz (KI) zu entwickeln, die dieses Problem mit Reinforcement Learning (RL) löst. Das Spiel besteht aus drei Türmen und einer variablen Anzahl von Scheiben, die von einem Startturm auf einen Zielturm bewegt werden müssen, wobei bestimmte Regeln eingehalten werden. Ziel war es, eine optimale Strategie zu erlernen, die das Problem mit möglichst wenigen Zügen löst. Neben der Implementierung des Spiels wurde eine grafische Darstellung entwickelt, um das Verhalten der KI zu visualisieren.

Die KI wurde mithilfe der OpenAI-Gym-Bibliothek trainiert, um das Rätsel effizient zu lösen. Ziel war es, eine Abstraktion der Spielsituation und der möglichen Züge vorzunehmen und das Modell durch wiederholtes Training zu optimieren. Eine Herausforderung bestand darin, eine geeignete Belohnungsstruktur zu entwerfen, die das Lernen effizient steuert. Abschließend wurde das gesamte System mit einer grafischen Benutzeroberfläche versehen, um eine visuelle Demonstration der KI zu ermöglichen. Die finale Vorführung beinhaltete eine Demonstration der KI-gestützten Lösung des Problems sowie eine Präsentation der gesammelten Erkenntnisse und Herausforderungen während der Entwicklung.

## 2. Beteiligte Personen und Aufgaben
- **Sajjad Ali Faizy**: Implementierung der Spielmechanik
- **Csongor Kiss**: Entwicklung des Q-Learning-Algorithmus
- **Marvin Rosseburg**: Erstellung der grafischen Benutzeroberfläche
- **Daniel Cortés-Caparrós**: Training und Optimierung der KI

## 3. Beschreibung des Projekts
### 3.1 Implementierung der grundlegenden Spielmechanik

Die grundlegende Spielmechanik der Türme von Hanoi wurde in der Klasse `Game` innerhalb der Datei `game_logic.py` realisiert. Diese Klasse verwaltet den Zustand des Spiels, überprüft die Einhaltung der Spielregeln und ermöglicht das Verschieben der Ringe zwischen den drei Türmen. Ein zentrales Element ist der Konstruktor, der das Spielfeld mit der gewählten Anzahl an Ringen initialisiert.

```python
class Game:
    def __init__(self, num_disks=3):
        self.num_disks = num_disks
        self.towers = [np.array([i for i in range(num_disks, 0, -1)]), np.array([]), np.array([])] # The bigger the disk, the smaller the index, 0 excluded in range()
        self.history = np.array([0])
```

Dabei werden die Türme als Listen dargestellt, wobei der erste Turm mit einer absteigenden Reihenfolge von Ringen gefüllt wird. Die beiden anderen Türme starten leer. Um das Spiel zu ermöglichen, wurde eine Methode `move_ring` implementiert, die für die Bewegung der Ringe zwischen den Türmen zuständig ist.

```python
def move_ring(self, source, target):

    # Chosen Towers valid?
    if not (0 <= source <= 2 and 0 <= target <= 2): # If source inexistent -> error
        raise ValueError("The peg's indexes must be between 0 and 2")
    if self.towers[source].size == 0: # If source empty -> error
        raise ValueError(f"The peg {source} is empty")

    # Moving Ring
    disk = self.towers[source][-1]

    # Valid Move?
    if self.towers[target].size > 0 and self.towers[target][-1] < disk: # If upper disk on target is smaller
        raise ValueError(f"It's not possible to lay the disk {disk} on a smaller disk")
    
    # Move
    self.towers[source] = self.towers[source][:-1] # Delete disk from source
    self.towers[target] = np.append(self.towers[target], disk) # Add disk to target

    # Update History
    self.history = np.append(self.history, self.get_state_index())
```

Hierbei werden zwei Bedingungen überprüft, bevor ein Ring bewegt wird. Zunächst wird geprüft, ob der Quellturm überhaupt einen Ring enthält. Falls dieser leer ist, wird eine Fehlermeldung ausgelöst. Anschließend wird sichergestellt, dass ein größerer Ring nicht auf einen kleineren abgelegt wird. Sollte diese Regel verletzt werden, wird ebenfalls eine Fehlermeldung generiert. Erst wenn beide Bedingungen erfüllt sind, wird der Ring entfernt und auf dem Zielstab platziert.

Ein weiteres wichtiges Element ist die Methode `is_solved`, die überprüft, ob das Spiel beendet ist. Dies geschieht, indem überprüft wird, ob alle Ringe auf dem dritten Turm liegen.

```python
def is_solved(self):
    return (self.towers[2].size == self.num_disks and 
            self.towers[0].size == 0 and
            self.towers[1].size == 0)
```

Diese Methoden garantieren, dass das Spiel nur mit gültigen Zügen gespielt wird. Da illegale Spielzüge direkt in `move_ring` abgefangen werden, ist es der KI nicht möglich, das Spiel in einen ungültigen Zustand zu versetzen. Dies stellt sicher, dass der Lernprozess effizient bleibt und sich auf die Lösung des Spiels konzentriert.

### 3.2 Q-Learning-Algorithmus

Nachdem die grundlegende Spielmechanik festgelegt war, wurde der Q-Learning-Algorithmus entwickelt, um das Problem der Türme von Hanoi effizient zu lösen. Der Algorithmus basiert auf der Verstärkungslernstrategie, wobei das Modell durch wiederholtes Spielen lernt, welche Züge es ausführen sollte, um das Ziel mit möglichst wenigen Schritten zu erreichen.

Ein wesentlicher Bestandteil dieser Methode ist das Belohnungssystem, das in `ai_training.py` definiert wurde. Die Belohnungen sind wie folgt strukturiert:

| **Situation**                           | **Belohnung/Bestrafung**       | **Erklärung** |
|-----------------------------------------|--------------------------------|------------------------------|
| Spiel erfolgreich abgeschlossen        | **+10 bis +20** (sehr hoch)    | Wird vergeben, wenn alle Ringe korrekt auf den Zielstab verschoben wurden. Die genaue Höhe hängt von der Effizienz der Lösung ab. |
| Neue maximale Anzahl an Ringen auf Stab 3   | **+3**                    | Wird gewährt, wenn erstmals eine größere Anzahl von Ringen auf dem Zielstab liegt als in einem vorherigen Zustand. |
| Gültiger Zug ohne Fortschritt           | **+0.2**                      | Gültiger, aber nicht optimaler Zug, der keine direkte Verbesserung bringt. |
| Redundante Bewegung                     | **-0.1**                      | Strafe für unnötige Wiederholungen von Zügen, um ineffiziente Strategien zu vermeiden. |
| Ungültiger Zug                          | **-0.05**                     | Wird verhängt, wenn gegen die Regeln verstoßen wird, z. B. ein größerer Ring auf einen kleineren gelegt wird. |
| Strafe für übermäßige Züge              | **-0.01 pro zusätzlichem Zug** | Wird für jeden zusätzlichen Zug über das theoretische Minimum hinaus abgezogen, um effizientes Spielen zu fördern. |

Durch diese Belohnungsstruktur wird die KI dazu gebracht, optimale Strategien zu erlernen, indem sie für effiziente Lösungen belohnt und für ineffiziente oder illegale Züge bestraft wird. Dadurch verbessert sich ihr Verhalten mit jeder Trainingsiteration.

Der Kern des Q-Learning-Algorithmus ist in der Klasse `SOMPiBrain` in `q_brain.py` implementiert. Die Methode zur Auswahl einer Aktion zeigt die Balance zwischen Exploration (Zufallsauswahl) und Exploitation (Wahl der besten bekannten Aktion):

```python
class SOMPiBrain:
    def __init__(self, state_num, action_num, q_table=False, alpha=0.1, gamma=0.7, epsilon=0.1):
        self.alpha = alpha      # Lernrate
        self.gamma = gamma      # Zukunftsorientierung
        self.epsilon = epsilon  # Explorationsrate
        self.action_num = action_num
        # [...]

    def get_action(self, state, explore=True):
        if explore and (random.uniform(0, 1) < self.epsilon):
            return random.randint(0, self.action_num - 1)
        else:
            return np.argmax(self.q_table[state])
    
    # [...]
```

Die Tabelle unten fasst die in der Implementierung verwendeten Hyperparameter zusammen und gibt eine kurze Erklärung zu deren Bedeutung:

| **Parameter**       | **Bedeutung** |
|---------------------|----------------------------------------------|
| **Lernrate (alpha)** | Bestimmt, wie stark neue Informationen in das bestehende Wissen integriert werden. Ein hoher Wert bedeutet schnelleres Lernen, kann aber auch Instabilität verursachen. |
| **Diskontfaktor (gamma)** | Gibt an, wie wichtig zukünftige Belohnungen im Vergleich zu unmittelbaren Belohnungen sind. Ein hoher Wert fördert langfristiges Denken. |
| **Explorationsrate (epsilon)** | Bestimmt, wie oft zufällige Züge ausgeführt werden, um neue Strategien zu entdecken. Zu Beginn des Trainings ist dieser Wert meist hoch und wird mit der Zeit reduziert. |
| **Anzahl Episoden (num_episodes)** | Die Anzahl an vollständigen Trainingsdurchläufen, die die KI durchführt. Ein höherer Wert bedeutet intensiveres Lernen. |
| **Maximale Schritte pro Episode (max_steps_per_episode)** | Die maximale Anzahl an Zügen, die die KI in einer Episode ausführen darf. |

Die Implementierung des Algorithmus sorgt dafür, dass das Modell kontinuierlich dazulernt und sich in Richtung einer effizienten Problemlösung optimiert. Das Zusammenspiel aus Belohnungssystem und Aktionswahl ermöglicht es der KI, durch eine Vielzahl an Trainingsdurchläufen ein nahezu perfektes Spielverhalten zu entwickeln.

### 3.3 Training der KI

Das Training der KI wurde mit `ai_training.py` durchgeführt. In diesem Prozess wurden verschiedene Hyperparameter angepasst, um die Lernleistung der KI zu maximieren. Die KI spielte eine große Anzahl an Durchläufen, um ihre Strategie schrittweise zu verbessern und letztendlich eine optimale Lösung für das Problem zu finden. Die wichtigsten Bestandteile der Trainingsimplementierung sind in der folgenden Codepassage dargestellt:

```python
def train_brain(training_index, num_disks, num_episodes, max_steps_per_episode, q_table, alpha, epsilon, gamma):
    #[...]
    q_brain = SOMPiBrain(state_num, action_num, epsilon=epsilon, alpha=alpha, gamma=gamma, q_table=q_table) # Instance Agent

    for episode in range(num_episodes):
        #[...]
        for _ in range(max_steps_per_episode):
            if game.is_solved():
                break
            # Get action from Q-Learning-Brain
            action = q_brain.get_action(state_index) # Choose action
            source, target = actions[action] # Extract source and target from chosen action

            # Execute action AND train model
            try: # to move ring
                game.move_ring(source, target)
                reward = 0.2
            except ValueError: # If chosen action is invalid move
                reward = -0.1

            # Reward solved game & penalty additional step
            reward += 7 * num_disks if game.is_solved() else -2

            # Reward for positioning more qty of disks on tower 3
            if len(game.towers[2]) > max_disks_on_tower_3:
                max_disks_on_tower_3 = len(game.towers[2])
                reward += 2

            # Redundance Penalty
            if np.any(game.history[:-1] == game.history[-1]): reward -= 10

            # Update Q-table
            #[...]

            # Update Status
            #[...]
        if not game.is_solved():
            print(f"\nEpisode {episode + 1}: Did not solve the game in {total_moves} moves.\n")
        else:
            total_moves_hist.append(total_moves)
    # [...]
    return total_moves_hist
```

Im Rahmen dieses Projekts wurde die KI über **1000 Trainingsdurchläufe** trainiert. Durch diesen iterativen Lernprozess konnte die KI eine effiziente Strategie entwickeln, um das Spiel mit einer minimalen Anzahl an Zügen zu lösen.

### 3.4 Visuelle Darstellung des Spiels

Parallel zur Entwicklung der KI wurde eine grafische Benutzeroberfläche implementiert, um das Verhalten der KI visuell nachvollziehbar zu machen. Die GUI wurde in `gui.py` mit `vpython` entwickelt und stellt das Spielfeld sowie die Bewegung der Ringe in einer animierten Umgebung dar.

Die grundlegende Struktur der Klasse `HanoiGUI` ist in folgendem gekürzten Code-Snippet dargestellt:

```python
class HanoiGUI:
    def __init__(self, ring_count, speed):
        self.ring_count = ring_count
        self.speed = speed
        self.stabs = []
        self.rings = [[], [], []]
        self.setupScene()

    def setupScene(self):
        # Szene konfigurieren
        # [...]

        # Ringe erstellen und auf den ersten Stab legen
        height = -0.9
        last_thickness = max_thickness
        for i in range(self.ring_count):
            current_thickness = max_thickness - i * step
            height += current_thickness + last_thickness if i > 0 else current_thickness
            last_thickness = current_thickness
            ring_color = colors[i % len(colors)]
            ring_obj = ring(pos=vector(-4, height, 0), axis=vector(0, 1, 0),
                            radius=1 - i * 0.1, thickness=current_thickness, color=ring_color)
            self.rings[0].append(ring_obj)  # Ringe dem ersten Stab zuweisen

    def moveRing(self, from_stab, to_stab):
        if not self.rings[from_stab]:
            print(f"Stab {from_stab} hat keine Ringe!")
            return
        
        # Ring vom Startstab entfernen
        ring = self.rings[from_stab].pop()
        
        # Zielhöhe & -postition berechnen
        # [...]
        
        # Animation
        while ring.pos.y < 3:  # Hebe den Ring auf eine Höhe über den Stäben
            rate(50 * self.speed)
            ring.pos.y += 0.05
        # [...]
        
        # Ring dem Zielstab hinzufügen
        self.rings[to_stab].append(ring)
```

Die GUI erzeugt eine dreidimensionale Darstellung mit Türmen und Ringen, die sich entsprechend der vom KI-Algorithmus getroffenen Entscheidungen bewegen.

Die folgende Tabelle listet die wesentlichen Parameter der `HanoiGUI`-Klasse und ihre Bedeutung auf:

| **Parameter**    | **Bedeutung** |
|-----------------|------------------------------------------------|
| **ring_count**  | Anzahl der Ringe im Spiel, bestimmt die Schwierigkeit. |
| **speed**       | Geschwindigkeit der Animation für die Bewegungen der Ringe. |
| **stabs**       | Liste der drei vertikalen Zylinder, die als Türme dienen. |
| **rings**       | 2D-Liste, die speichert, welche Ringe sich auf welchem Turm befinden. |

Durch diese Implementierung wird das Verhalten der KI nachvollziehbar dargestellt und bietet eine visuelle Kontrolle über den Lernprozess. Die Animationen helfen dabei, den Fortschritt des Algorithmus zu verdeutlichen und dessen Lösungsstrategie in Echtzeit zu beobachten.

### 4. Ergebnisse

Nach Abschluss des Trainings wurde die KI anhand der Q-Tables analysiert, um die Fortschritte in ihrer Entscheidungsfindung zu bewerten. Die Ergebnisse zeigen, dass die KI im Laufe des Trainings eine effizientere Strategie zur Lösung des Türme von Hanoi-Problems entwickelt hat. Dies wurde durch eine schrittweise Optimierung der Q-Table erreicht, die es der KI ermöglichte, bessere Entscheidungen zu treffen und sich auf effektive Spielzüge zu konzentrieren.

Durch die Anpassung der Belohnungsstruktur und die wiederholten Trainingsdurchläufe hat die KI gelernt, nicht nur zulässige Züge auszuführen, sondern auch den optimalen Weg zur Lösung zu priorisieren. Sie konnte redundante oder ineffiziente Bewegungen reduzieren und stattdessen Muster erkennen, die das Spiel in möglichst wenigen Zügen zum Abschluss bringen.

Ein wesentlicher Bestandteil des Lernprozesses war die Verbesserung der Aktionsbewertung, wodurch die KI in späteren Durchläufen zielgerichteter agierte. In den ersten Trainingsphasen wurden noch viele zufällige Entscheidungen getroffen, doch mit fortschreitender Optimierung wurden immer effizientere Sequenzen bevorzugt. Dies zeigt, dass der Reinforcement-Learning-Ansatz erfolgreich war und die KI eine stabile Strategie zur Lösung des Problems entwickelt hat.

Zusammenfassend hat die KI bewiesen, dass sie das Problem der Türme von Hanoi durch wiederholtes Lernen meistern kann. Die erzielten Fortschritte zeigen, dass das Training effektiv war und der Algorithmus nach mehreren Durchläufen in der Lage war, das Spiel mit einer minimalen Anzahl an Zügen zu lösen.

## 5. Fazit
Das Projekt hat erfolgreich gezeigt, wie Reinforcement Learning zur Lösung eines klassischen Problems eingesetzt werden kann. Die KI war in der Lage, sich eine effektive Strategie anzueignen und das Spiel optimal zu lösen. Während des Projekts wurden wertvolle Erkenntnisse über die Funktionsweise und Optimierung von Q-Learning-Algorithmen gewonnen. Zudem hat die Kombination aus theoretischem Wissen und praktischer Implementierung dazu beigetragen, ein tieferes Verständnis für die Herausforderungen und Möglichkeiten von Reinforcement Learning zu entwickeln.
