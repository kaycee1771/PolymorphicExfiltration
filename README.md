
# Polymorphic Protocol Exfiltration System
## A Dynamic Adversarial Data Exfiltration System

### Overview
This project simulates an adversary attempting to exfiltrate data past advanced network monitoring systems. The system uses a **polymorphic protocol** that dynamically adapts its behavior to avoid detection. It implements **secure data transmission** through at least **three different camouflage protocols**, and switches between them based on real-time network conditions (packet loss, latency, bandwidth).

This system features **DNS traffic simulation**, **HTTPS behavior mimicking**, **custom UDP protocol**, and additional enhancements for resilience and performance, designed to evade detection from sophisticated network monitoring tools.

---

## Table of Contents

1. System Overview
2. Key Features
3. Protocols and Camouflage Modes
   - DNS Traffic Simulation
   - HTTPS Behavior Mimicking
   - Custom UDP Protocol
   - ICMP Shell (Optional)
4. Dynamic Mode Switching
5. Traffic Patterns and Security
6. Error Handling and Resilience
7. Detection Avoidance Techniques
8. System Requirements
9. Installation and Setup
10. Usage Instructions
11. Conclusion
12. License

---

## 1. System Overview

This system enables secure message transmission between a **client** and a **server** using four camouflage protocols:
- **DNS Exfiltration**
- **HTTPS Exfiltration**
- **UDP Exfiltration**
- **ICMP-based Exfiltration** (Optional)

It allows dynamic switching between these modes based on the network conditions (RTT, packet loss, bandwidth) to evade detection, while ensuring encrypted, covert data transmission. The client sends encrypted commands and receives execution results back via one of these modes, while the server dynamically adapts to network changes.

---

## 2. Key Features

- **Secure Data Transmission**: 
   - Encryption is implemented with **AES** (for UDP) and **SSL/TLS** (for HTTPS) to ensure the integrity and confidentiality of exfiltrated data.

- **Multiple Camouflage Modes**: 
   - **DNS** traffic simulation, **HTTPS** behavior mimicking, and **UDP** exfiltration allow the adversary to blend data exfiltration with common network traffic.

- **Dynamic Mode Switching**: 
   - The system automatically switches between camouflage modes based on network conditions to evade detection when one protocol is blocked or throttled.

- **Interactive Command Execution**: 
   - Through the **DNS Shell** and **ICMP Shell**, the client can send commands interactively and receive real-time outputs.

- **Robust Error Handling**:
   - The system ensures resilience against network interruptions by adapting its behavior and employing retries.

---

## 3. Protocols and Camouflage Modes

### DNS Traffic Simulation (DNS Exfiltration)

The **DNS exfiltration mode** mimics legitimate DNS queries to send encoded commands from the client to the server. The server then processes the command and returns the output encoded within a DNS response.

#### Key Concepts:
- **DNS Query**: Commands are base64 encoded and sent as part of DNS queries to the server.
- **DNS Response**: The server sends back the command output as part of the DNS reply, which is also base64 encoded.

This technique blends with normal DNS traffic, making it hard to detect without deep packet inspection.

### HTTPS Behavior Mimicking (SSL/TLS Exfiltration)

In **HTTPS mode**, the client and server use **SSL/TLS** to encrypt their communication, making the data flow appear like normal web traffic.

#### Key Concepts:
- **SSL/TLS Encryption**: Data is securely transmitted over an encrypted channel, simulating regular HTTPS traffic.
- **Command Execution**: The server receives base64-encoded commands over HTTPS, executes them, and returns the result.

This mode helps hide exfiltrated data within HTTPS traffic, which is a common protocol for legitimate internet communication.

### Custom UDP Protocol (UDP Exfiltration)

For **UDP exfiltration**, the client sends encrypted UDP packets containing commands. The server decrypts the packets, executes the command, and returns the result encrypted in UDP packets.

#### Key Concepts:
- **UDP Packet**: The client sends encrypted UDP packets containing the command data.
- **AES Encryption**: Data is encrypted using AES to ensure confidentiality and prevent detection of the exfiltration data.

This mode mimics regular UDP traffic and allows for faster transmission of data with low latency.

### ICMP Shell (Optional)

In **ICMP mode**, commands are encoded into **ICMP Echo Request** packets. The server receives these requests, executes the commands, and sends the results back as part of an **ICMP Echo Reply**.

#### Key Concepts:
- **ICMP Echo Request**: Command data is embedded in the ICMP packet sent from the client to the server.
- **ICMP Echo Reply**: The server returns the command output encoded in the ICMP reply.

ICMP provides another layer of camouflage, as ping requests are often overlooked by network monitoring tools.

---

## 4. Dynamic Mode Switching

The system can automatically switch between modes based on network conditions such as **RTT (Round-Trip Time)**, **packet loss**, and **available bandwidth**. The **ModeSwitchingAI** class in the client analyzes these parameters in real-time and dynamically selects the most appropriate camouflage mode. If a mode gets blocked or detected, the system seamlessly switches to another mode, ensuring continuous data exfiltration.

---

## 5. Traffic Patterns and Security

The traffic patterns in the system are designed to mimic real network traffic:
- **Timing-based Communication**: The system can be configured to simulate realistic delays between packets, making the communication patterns appear natural.
- **Network Traffic Shaping**: The client adjusts the data rate, packet size, and frequency of transmissions to further blend with legitimate traffic patterns.

The use of **encryption (AES for UDP, SSL/TLS for HTTPS)** ensures that the exfiltrated data remains confidential and resistant to detection by deep packet inspection tools.

---

## 6. Error Handling and Resilience

The system is designed to be resilient in case of network failures or interruptions. It automatically adjusts:
- **Retry Mechanisms**: If packets are lost or dropped, the system will retry transmission.
- **Adaptive Protocol Switching**: The system dynamically switches between camouflage modes if one mode is blocked or throttled due to network interference.

These features ensure that the exfiltration process remains robust and reliable under challenging network conditions.

---

## 7. Detection Avoidance Techniques

- **Protocol Camouflage**: The system uses DNS, HTTPS, and UDP to make the exfiltration traffic blend with normal network activity, avoiding detection by most network monitoring tools.
- **Payload Encryption**: Data is encrypted using **AES** (for UDP) and **SSL/TLS** (for HTTPS), making it unreadable to anyone intercepting the traffic.
- **Dynamic Mode Switching**: The system intelligently switches modes based on real-time network conditions, ensuring that if one protocol is detected or blocked, another can be used.
- **Traffic Shaping and Timing Obfuscation**: The system uses configurable delays and packet size adjustments to further avoid detection by monitoring systems that look for unusual patterns.

---

## 8. System Requirements

- **Python 3.x**: The project is built with Python 3.
- **Required Libraries**:
  - `ssl` (for HTTPS)
  - `dnslib` (for DNS simulation)
  - `subprocess` (for command execution)
  - `cryptography` (for AES encryption)
  - `socket` (for raw socket handling)
