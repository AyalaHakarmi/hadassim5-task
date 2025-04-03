## Part C - Theory Questions

### Question 1:

**Rating:** 2

---

### Question 2:

#### a. What is the transmission method between the remote and the air conditioner?

The communication between the remote and the air conditioner is typically done using **infrared (IR) transmission**. The remote emits pulses of infrared light that encode information, which are received by an IR sensor on the air conditioner. Some modern systems may also use **radio frequency (RF)** or **Bluetooth**, but IR is by far the most common in standard remote-controlled AC systems.

#### b. What components are required on the remote and on the air conditioner side?

**On the remote control side:**

- Infrared LED to emit the signal.
- Microcontroller or chip to encode signals.
- Buttons connected to the microcontroller.
- Power supply (typically a battery).

**On the air conditioner side:**

- Infrared sensor/receiver to detect incoming signals.
- Microcontroller to decode the signal.
- Actuators or relays to execute the command (e.g., turn on, change temperature).

#### c. How does the air conditioner know which button was pressed?

Each button on the remote corresponds to a unique **digital code**. When a button is pressed:

- The remote encodes the corresponding command as a binary signal using a specific **protocol** (e.g., NEC, RC-5).
- The signal is transmitted as a series of modulated infrared pulses.
- The air conditioner's IR receiver demodulates and decodes the incoming signal.
- The microcontroller identifies the command based on the code received.

**Possible implementations to differentiate buttons:**

- Assign each button a unique binary command (e.g., power = 0x10EF, temperature up = 0x10E0).
- Use a start bit and parity to validate transmission.
- Use pulse-width modulation or different signal patterns.
- In advanced systems, use encryption or rolling codes to prevent signal spoofing.

---

