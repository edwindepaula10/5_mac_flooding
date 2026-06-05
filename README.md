# Laboratorio 5: Ataque y Mitigación de MAC Flooding

## 1. Información General

* **Institución:** Instituto Tecnológico de las Américas (ITLA)
* **Materia:** Seguridad de Redes
* **Estudiante:** Edwin De Paula
* **Matrícula:** 2024-2415
* **Enlace del Video:** [Lista de Reproducción de YouTube - Demostración](https://www.google.com/search?q=AQU%C3%8D_PEGAS_EL_LINK_DE_TU_PLAYLIST_O_VIDEO)

---

## 2. Objetivos del Laboratorio

* **Objetivo General:** Evaluar el impacto de la saturación de la memoria CAM (Content Addressable Memory) en un switch de capa 2 y validar la efectividad de los mecanismos de mitigación perimetral.
* **Objetivo del Script:** Generar e inyectar de forma masiva y a alta velocidad tramas Ethernet con direcciones MAC de origen aleatorias para desbordar los recursos del switch.

---

## 3. Requisitos y Parámetros del Script

### Requisitos del Sistema:

* Entorno de ejecución Linux (Parrot OS / Kali Linux).
* Privilegios de superusuario (`sudo`).
* Python 3 instalado junto con la librería de manipulación de paquetes **Scapy**.
```bash
sudo apt install python3-scapy -y

```



### Parámetros utilizados en la herramienta:

* **Interfaz de red:** Determina la tarjeta de red por donde se inyectará el tráfico malicioso.
* **Dirección MAC origen (`src`):** Generada de forma aleatoria mediante funciones de aleatoriedad hexadecimal en cada ciclo del bucle.
* **Dirección MAC destino (`dst`):** Fijada en Broadcast (`ff:ff:ff:ff:ff:ff`) para asegurar que el switch procese la trama inmediatamente.

---

## 4. Documentación del Funcionamiento del Script

El script utiliza un bucle continuo (`while True`) que ensambla tramas de Capa 2 personalizadas. En cada iteración, la librería Scapy construye un paquete Ethernet donde el campo de dirección de origen se genera aleatoriamente empleando la función `RandMAC()`.

Estas tramas son enviadas en ráfaga a través del socket crudo de la interfaz seleccionada. Debido a que el switch analiza la MAC de origen de cada trama entrante para actualizar su tabla de reenvío, el script lo obliga a registrar miles de direcciones falsas en milisegundos, agotando el espacio de almacenamiento físico asignado para este fin.

---

## 5. Documentación de la Red y Topología

### Detalles de Infraestructura:

* **Entorno de Simulación:** PNetLab
* **Switch Principal:** SW1-CISCO (Cisco vIOS L2 / IOL)
* **Interfaz de Conexión del Atacante:** `Ethernet0/1`
* **Segmento de Red:** VLAN 10 (Datos)
* **Direccionamiento IP de Prueba:** `192.168.10.0/24`

---

## 6. Documentación de la Contra-medida (Mitigación)

Para mitigar de raíz esta vulnerabilidad en la capa de enlace de datos, se implementó la tecnología de **Port-Security** en el puerto correspondiente del switch.

### Comandos de Configuración Aplicados:

```cisconet
SW1-CISCO# configure terminal
SW1-CISCO(config)# interface Ethernet0/1
SW1-CISCO(config-if)# switchport mode access
SW1-CISCO(config-if)# switchport port-security
SW1-CISCO(config-if)# switchport port-security maximum 1
SW1-CISCO(config-if)# switchport port-security violation shutdown
SW1-CISCO(config-if)# end

```

### Justificación Técnica de la Defensa:

1. **`switchport port-security`**: Habilita el análisis dinámico de direcciones MAC en la interfaz física.
2. **`maximum 1`**: Restringe el puerto para que solo admita una única dirección MAC legítima (la del dispositivo del usuario).
3. **`violation shutdown`**: Define que al detectar una segunda dirección MAC (intento de inundación), el switch proteja la red de forma proactiva apagando el puerto inmediatamente e ingresándolo en estado `err-disable`.
