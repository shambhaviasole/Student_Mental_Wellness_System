# 🧠 Student Mental Health Assessment & Wellness System

An intelligent web-based system that predicts student mental health status using machine learning and provides personalized recommendations, analytics, downloadable reports, and AI-curated resources to promote mental well-being.

---

## 📌 Project Overview

Mental health issues among students are increasing due to academic pressure, screen overuse, lack of sleep, and stress. Early identification and preventive care are crucial.

This project uses a **Decision Tree Machine Learning model** integrated into a **Django web application** to:

* Predict mental health condition
* Provide personalized recommendations
* Visualize mental wellness analytics
* Generate professional PDF reports
* Suggest AI-based learning and wellness resources
* Manage counselor appointments

---

## 🎯 Objectives

* Predict mental health status based on user inputs
* Assist students with personalized wellness guidance
* Provide data-driven insights using visual analytics
* Generate downloadable medical-style reports
* Create an interactive, modern dashboard
* Support institutions in early mental health screening

---

## 🛠️ Technologies Used

### 🔹 Frontend

* HTML5
* CSS3 (Glassmorphism & Dark UI)
* Bootstrap 5
* JavaScript
* Chart.js

### 🔹 Backend

* Python 3.13
* Django 5.2

### 🔹 Machine Learning

* Scikit-learn
* Decision Tree Classifier
* Pandas & NumPy
* Joblib (model loading)

### 🔹 Database

* MySQL (via PyMySQL)

### 🔹 PDF Generation

* xhtml2pdf (pisa)

---

## 📂 Project Features

### 1️⃣ Mental Health Prediction (AI-Powered)

* Inputs:

  * Stress level
  * Sleep duration
  * Screen time
  * Physical activity
  * Anxiety symptoms
* ML model predicts:

  * **Mentally Fit**
  * **Mentally Unfit**

---

### 2️⃣ AI Explanation (Explainable AI)

The system generates **reasons** behind the prediction, such as:

* High stress detected
* Insufficient sleep
* Excessive screen time
* Low physical activity
* Anxiety symptoms

This improves **trust and transparency** of AI predictions.

---

### 3️⃣ Personalized Recommendations

Based on prediction result:

#### If Mentally Unfit:

* Improve sleep (7–8 hours)
* Reduce screen exposure
* Daily physical exercise
* Stress management techniques
* Counselor support suggestion

#### If Mentally Fit:

* Maintain current routine
* Preventive wellness tips
* Mindfulness practices

---

### 4️⃣ Interactive Student Dashboard

Features:

* Recent assessment summary
* AI wellness insights
* Weekly stress trend chart
* Wellness progress bar
* Feedback submission
* Quick navigation sidebar

Built using **Bootstrap + Chart.js** with animations and responsive design.

---

### 5️⃣ Mental Health Analytics

Visual analytics include:

* Stress vs Sleep trend
* Weekly stress variation
* Wellness progress indicators

These charts help students understand patterns and improve habits.

---

### 6️⃣ Downloadable PDF Report

After assessment, students can download a **professional mental health report** containing:

* Student details
* Input summary
* Prediction result
* AI explanation
* Personalized recommendations
* Date of assessment
* Medical disclaimer
* University-level layout
* Watermark & student ID

---

### 7️⃣ AI-Recommended Resources

Personalized resources based on prediction:

* 🎥 YouTube videos (meditation, stress relief)
* 📄 Articles & PDFs
* 🧘 Mental wellness practices
* 🧠 Self-help content

Resources are **clickable** and dynamically generated.

---

### 8️⃣ Appointment Management

Students can:

* Request counselor appointments
* View appointment status
* Schedule future sessions

(Admin/Counselor module can be extended)

---

## 🔐 Authentication & Security

* Student login system
* Session-based authentication
* Secure access to reports and dashboards
* Input validation

---

## 📊 System Architecture

```
User → Django Views → ML Model → Prediction
           ↓
     Database (MySQL)
           ↓
   Dashboard / PDF / Analytics
```

---

## 🚀 How to Run the Project

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/student-mental-health-ai.git
cd student-mental-health-ai
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv env
env\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Database

Update MySQL credentials in `settings.py`.

### 5️⃣ Run Server

```bash
python manage.py runserver
```

---

## 📁 Folder Structure (Simplified)

```
DemoProject/
│── templates/
│── static/
│── ml_model/
│── views.py
│── urls.py
│── settings.py
│── db.sqlite3 / MySQL
```

---

## 📌 Future Enhancements

* Deep learning model (LSTM)
* Real-time emotion detection
* Counselor/admin dashboard
* Email notifications
* Mobile app version
* Cloud deployment (AWS / Azure)

---

## 🎓 Academic Relevance

* Suitable for **Final Year Project**
* Covers:

  * Machine Learning
  * Web Development
  * Data Analytics
  * AI Explainability
* Aligns with **Industry 4.0 & AI in Healthcare**

---

## 🧾 Disclaimer

> This system is intended for educational and preliminary assessment purposes only.
> It does **not replace professional medical diagnosis or treatment**.

---

## 👩‍💻 Developed By

**Name:** *Shambhavi Asole*

Just tell me 😊
