# EcoBin Rewards

A Raspberry Pi–based smart recycling bin. Users register by face, insert a bottle, get it classified by type, and earn points redeemable at a canteen — end to end: sensors → GPIO control → computer vision → a Flask admin app.

## How it works

1. User presses the start button.
2. **Face recognition** (`services/auth.py`, OpenCV + `face_recognition`) verifies a returning user or walks a new one through registration via the I2C keypad/LCD.
3. The lid opens (servo), an **ultrasonic sensor** detects the bottle drop, and a second camera captures it for classification.
4. **`services/classify.py`** identifies the bottle type and maps it to a point value.
5. Points are written to the database (`services/db.py`) and the LCD/buzzer confirm the result.
6. A separate **Flask admin app** (`webApp/`) lists users and lets canteen staff redeem (deduct) points.

## Hardware

| Component | Interface | Module |
|---|---|---|
| Ultrasonic sensors (bottle + bin-full detection) | GPIO | `Components/ultrasonic.py` |
| Servo (lid) | PWM (GPIO) | `Components/servo.py` |
| Buzzer | GPIO | `Components/buzzer.py` |
| 4x4 keypad | I2C | `Components/keypad_i2c.py` |
| LCD | I2C | `Components/lcd_i2c.py` |
| Two cameras (user-facing, bottle-facing) | CSI/USB | `Components/camera.py` |

Pin assignments live in `config.py` / `Components/pins.py`. Each peripheral has a standalone smoke test under `test/` (`Servo_test.py`, `LCD_test.py`, `UltraSonic_test.py`, `camera_test.py`, etc.) for bringing hardware up one piece at a time.

## Software

- **Runtime loop** — `main.py` → `services/workflow.py` drives the bin's state machine: verify user → open lid → detect bottle → classify → award points → reset.
- **Bottle classification** — `services/classify.py` is wired for a CV/ML pipeline (OpenCV capture, PyTorch/TensorFlow in `requirements.txt`) but currently returns a fixed label via `DummyClassifier` — the hook is in place, the trained model isn't plugged in yet. That's the natural next step: collect labeled images from the bin's own camera and swap the dummy in for a real classifier (e.g. a fine-tuned MobileNetV2).
- **Admin app** — `webApp/app.py` (Flask) shows registered users, their point balances, and lets staff deduct points at redemption.
- **Persistence** — MySQL via `mysql-connector-python` (`services/db.py`): `users`, `transactions`, `events` tables.

## Setup

```bash
sudo raspi-config          # enable Camera, I2C, SSH

pip install -r requirements.txt
cp .env.example .env       # fill in DB credentials and a real FLASK_SECRET_KEY

python main.py             # runs the bin loop (needs the Pi's GPIO/camera hardware)
python webApp/app.py       # runs the admin dashboard on :8080
```

Credentials and the Flask secret are read from environment variables (`python-dotenv`) — nothing is hardcoded in source.

## Known limitations

- Bottle classification is a stub (`DummyClassifier`) pending a trained model and a labeled dataset from the physical bin.
- `webApp/templates/login.html` exists but the admin app has no auth wired up yet — it's currently open, not gated.
- No CI or automated tests yet; hardware verification is manual, per-peripheral, via the `test/` scripts.

## Why this project

This is my Stage 4 (Embedded AI / Edge AI) project on my [engineering roadmap](https://github.com/ItsDietrich/ItsDietrich) — the point of it was to get one project that actually spans the full stack I'm aiming for: firmware-level sensor/actuator control, a CV pipeline on real hardware, and the backend/web layer that makes the hardware useful to an actual user.
