# Robotics for Good – Robot SDK 🤖🌍

This project is designed to run on the **Adeept RaspTank Robot**, a Raspberry Pi–based tracked robot commonly used in robotics education.
The Robot SDK in this repository **wraps and simplifies** the original Adeept hardware interfaces, making them easier and safer for students to use in the Robotics for Good Youth Challenge.

- 💻 **Original Adeept RaspTank GitHub repository**  
https://github.com/adeept/Adeept_RaspTank
- 📘 **Official Adeept RaspTank lessons & documentation**  
https://www.adeept.com/learn/detail-85.html

- 🚗 Robot movement (motors)
- 💡 LEDs and visual feedback
- 📏 Ultrasonic distance sensing
- 📷 Camera & OpenCV foundations
- 🧩 A beginner-friendly API designed for students

The goal is to **hide hardware complexity** and let students focus on **problem-solving, logic, and impact-driven robotics**.

---

## 📦 Project Structure


---

## 🛠️ Requirements

- Raspberry Pi (3B+, 4, or 5 recommended)
- Raspberry Pi OS (Bookworm recommended)
- Python **3.9+**
- Git installed
- Adeept Packages

---

## 🚀 Installation

### 1️⃣ Clone the repository
```bash
cd ~
git clone https://github.com/Skyrov01/robotics-for-good.git
cd robotics-for-good

```bash
pip3 uninstall robot-sdk -y --break-system-packages
```
```bash
pip3 install -e . --break-system-packages
```
```bash
python3 -c "import robot_sdk; print('robot-sdk installed successfully')"
```
