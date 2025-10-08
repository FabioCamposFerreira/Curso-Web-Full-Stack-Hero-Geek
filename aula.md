---
title: Introdução ao Arduino
subtitle: Aula 1 - Fundamentos
author: Setta Digital Labs
date: 2025-10-07
slide-level: 1
---

# Introdução ao Arduino

- Plataforma open-source para prototipagem eletrônica.  
- Usa microcontroladores (ex.: ATmega328).  
- Permite interação entre hardware e software.

::: notes
Explicar que o Arduino foi criado na Itália e se popularizou pela facilidade de uso.
:::

---

# O que é o Arduino?

- Placa eletrônica programável.
- Conectada via USB ao computador.
- Controla sensores, motores e LEDs.

![Placa Arduino Uno](https://upload.wikimedia.org/wikipedia/commons/3/38/Arduino_Uno_-_R3.jpg){width=50%}

---

# Componentes Principais

| Componente | Função |
|-------------|---------|
| Microcontrolador | Cérebro do Arduino |
| Portas Digitais | Entrada/Saída de sinais |
| Portas Analógicas | Leitura de sensores |
| Conector USB | Comunicação e alimentação |

---

# Instalação do Arduino IDE

1. Baixe em: [https://www.arduino.cc/en/software](https://www.arduino.cc/en/software)  
2. Instale o driver USB.  
3. Selecione a placa e a porta correta.  
4. Teste o código de exemplo **Blink**.

---

# Primeiro Código: Blink

```c
void setup() {
  pinMode(13, OUTPUT); // Configura o pino 13 como saída
}

void loop() {
  digitalWrite(13, HIGH); // Liga o LED
  delay(1000);            // Espera 1 segundo
  digitalWrite(13, LOW);  // Desliga o LED
  delay(1000);            // Espera 1 segundo
}
