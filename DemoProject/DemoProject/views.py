import joblib
import json
import pandas as pd
import pymysql

from django.conf import settings
from django.shortcuts import render, redirect
from datetime import date
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa



# ===========================
# Database Config (SECURE)
# ===========================
DB_CONFIG = {
    "host": "mysql-shambhavi-shambhaviasole9-python.h.aivencloud.com",
    "port": 10850,
    "user": "shambhavi",
    "password": "AVNS_HmvZ_bGZzAhYDISIpxY",
    "database": "shambhavidb",
    "ssl": {"ssl": {}}
}

# ===========================
# Homepage View
# ===========================
def home(request):
    return render(request, "index.html")


# ===========================
# Registration View
# ===========================
def registration(request):
    msg = ""
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('emailID')
        password = request.POST.get('password')

        try:
            con = pymysql.connect(
                host='mysql-shambhavi-shambhaviasole9-python.h.aivencloud.com',
                port=10850,
                user='shambhavi',
                password='AVNS_HmvZ_bGZzAhYDISIpxY',
                database='shambhavidb',
                ssl={'ssl': {}}
            )

            with con.cursor() as curs:
                curs.execute(
                    "SELECT * FROM StudentRegistration WHERE emailID=%s",
                    (email,)
                )

                if curs.fetchone():
                    msg = "Email already registered."
                else:
                    curs.execute("""
                        INSERT INTO StudentRegistration (fullname, emailID, password)
                        VALUES (%s, %s, %s)
                    """, (fullname, email, password))
                    con.commit()
                    msg = "Registration successful!"

        except Exception as e:
            msg = f"Error: {e}"

        finally:
            con.close()

    return render(request, 'registration.html', {'message': msg})


# ===========================
# Login View
# ===========================
def login(request):
    if request.method == "POST":
        email = request.POST.get('emailID').strip()
        psw = request.POST.get('password').strip()

        try:
            con = pymysql.connect(
                host='mysql-shambhavi-shambhaviasole9-python.h.aivencloud.com',
                port=10850,
                user='shambhavi',
                password='AVNS_HmvZ_bGZzAhYDISIpxY',
                database='shambhavidb',
                ssl={'ssl': {}}
            )

            with con.cursor() as curs:
                curs.execute("""
                    SELECT studID FROM StudentRegistration
                    WHERE emailID=%s AND password=%s
                """, (email, psw))

                result = curs.fetchone()

                if result:
                    request.session['studID'] = result[0]
                    return redirect('stdDashboard')
                else:
                    return render(request, 'loginfailed.html')

        except Exception as e:
            return render(request, 'login.html', {'error': str(e)})

        finally:
            con.close()

    return render(request, 'login.html')


# ===========================
# Dashboard View
# ===========================
# def stdDashboard(request):
#     if 'studID' not in request.session:
#         return redirect('login')
#     return render(request, 'stdDashboard.html')
def stdDashboard(request):
    if "studID" not in request.session:
        return redirect("login")

    con = pymysql.connect(**DB_CONFIG)
    with con.cursor() as curs:
        curs.execute("""
            SELECT fullname
            FROM StudentRegistration
            WHERE studID=%s
        """, (request.session["studID"],))
        row = curs.fetchone()
    con.close()

    return render(request, "stdDashboard.html", {
        "student_name": row[0] if row else "Student"
    })


# ===========================
# Logout View
# ===========================
def logout(request):
    request.session.flush()
    return render(request, "logout.html")


# ===========================
# Mental Health Prediction View
# ===========================
def mental_health_prediction(request):
    if request.method == 'POST':
        try:
            df = pd.DataFrame([{
                'Gender': int(request.POST['Gender']),
                'Age': int(request.POST['Age']),
                'Education': int(request.POST['Education']),
                'ScreenTime': float(request.POST['ScreenTime']),
                'Sleep': float(request.POST['Sleep']),
                'Physical': float(request.POST['Physical']),
                'Stress': int(request.POST['Stress']),
                'Anxious': int(request.POST['Anxious']),
                'AcademicPerf': int(request.POST['AcademicPerf'])
            }])

            FEATURE_ORDER = [
                'Gender', 'Age', 'Education', 'ScreenTime',
                'Sleep', 'Physical', 'Stress', 'Anxious',
                'AcademicPerf'
            ]
            df = df[FEATURE_ORDER]

            model = joblib.load(settings.ML_MODEL_PATH)
            pred = model.predict(df)

            prediction = "Mentally Fit" if pred[0] == 0 else "Mentally Unfit"

            # -------- Explanation --------

            # stress = int(df.at[0, 'Stress'])
            # anxious = int(df.at[0, 'Anxious'])
            # sleep = float(df.at[0, 'Sleep'])
            # screen = float(df.at[0, 'ScreenTime'])
            # physical = float(df.at[0, 'Physical'])

            reasons = []
            if df.at[0, 'Stress'] == 0:
                reasons.append("High stress level detected")
            if df.at[0, 'Anxious'] == 1:
                reasons.append("Symptoms of anxiety detected")
            if df.at[0, 'Sleep'] < 6:
                reasons.append("Insufficient sleep duration")
            if df.at[0, 'ScreenTime'] > 6:
                reasons.append("Excessive daily screen time")
            if df.at[0, 'Physical'] < 1:
                reasons.append("Low physical activity level")

            if not reasons:
                reasons.append("Healthy lifestyle and balanced mental indicators")

            # reasons = []

            # if stress == 2:  # High stress
            #     reasons.append("High stress level detected")

            # if anxious == 1:
            #     reasons.append("Symptoms of anxiety detected")

            # if sleep < 6:
            #     reasons.append("Insufficient sleep duration")

            # if screen > 6:
            #     reasons.append("Excessive daily screen time")

            # if physical < 1:
            #     reasons.append("Low physical activity level")

            # if not reasons:
            #     reasons.append("Healthy lifestyle and balanced mental indicators")


            # -------- Recommendations --------
            if prediction == "Mentally Unfit":
                recommendations = [
                    "🛌 Improve sleep (7–8 hours)",
                    "📵 Reduce screen time",
                    "🏃 Exercise 30 minutes daily",
                    "🧘 Practice stress management",
                    "📞 Contact campus counselor"
                ]
            else:
                recommendations = [
                    "✅ Maintain current routine",
                    "📈 Preventive wellness practices",
                    "🧠 Take regular breaks",
                    "🌿 Stay socially active",
                    "🛌 Maintain healthy sleep"
                ]

             # ---------- Save Inputs for PDF ----------
            # request.session["inputs"] = {
            #     "Stress Level": df.at[0, "Stress"],
            #     "Sleep Hours": df.at[0, "Sleep"],
            #     "Screen Time (hrs)": df.at[0, "ScreenTime"],
            #     "Physical Activity": df.at[0, "Physical"],
            #     "Anxiety": "Yes" if df.at[0, "Anxious"] == 1 else "No"
            # }


            request.session["inputs"] = {
                "stress": int(df.at[0, "Stress"]),
                "sleep": float(df.at[0, "Sleep"]),
                "screen": float(df.at[0, "ScreenTime"]),
                "physical": float(df.at[0, "Physical"]),
                "anxiety": "Yes" if int(df.at[0, "Anxious"]) == 1 else "No",
            }


            # -------- Save Analytics --------
            con = pymysql.connect(
                host='mysql-shambhavi-shambhaviasole9-python.h.aivencloud.com',
                port=10850,
                user='shambhavi',
                password='AVNS_HmvZ_bGZzAhYDISIpxY',
                database='shambhavidb',
                ssl={'ssl': {}}
            )

            with con.cursor() as curs:
                curs.execute("""
                    INSERT INTO MentalHealthRecords
                    (studID, stress, sleep, screen_time, prediction)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    request.session['studID'],
                    df.at[0, 'Stress'],
                    df.at[0, 'Sleep'],
                    df.at[0, 'ScreenTime'],
                    prediction
                ))
                con.commit()

            con.close()

            request.session['prediction_result'] = prediction
            request.session['explanation'] = reasons
            request.session['recommendations'] = recommendations

            return redirect('mental_health_result')

        except Exception as e:
            return render(request, "mental_health_form.html", {'error': str(e)})

    return render(request, "mental_health_form.html")


# ===========================
# Prediction Result View
# ===========================
def mental_health_result(request):
    return render(request, "mental_health_result.html", {
        'prediction': request.session.get('prediction_result'),
        'explanation': request.session.get('explanation', []),
        'recommendations': request.session.get('recommendations', [])
    })


# ===========================
# Analytics Dashboard View
# ===========================
def analytics_dashboard(request):
    con = pymysql.connect(
        host='mysql-shambhavi-shambhaviasole9-python.h.aivencloud.com',
        port=10850,
        user='shambhavi',
        password='AVNS_HmvZ_bGZzAhYDISIpxY',
        database='shambhavidb',
        ssl={'ssl': {}}
    )

    with con.cursor() as curs:
        curs.execute("SELECT stress, sleep FROM MentalHealthRecords")
        stress_sleep = curs.fetchall()

        curs.execute("SELECT screen_time, prediction FROM MentalHealthRecords")
        screen_pred = curs.fetchall()

        curs.execute("""
            SELECT MONTH(created_at), COUNT(*)
            FROM MentalHealthRecords
            GROUP BY MONTH(created_at)
        """)
        monthly = curs.fetchall()

    con.close()

    return render(request, "analytics_dashboard.html", {
        "stress_sleep": json.dumps(stress_sleep),
        "screen_pred": json.dumps(screen_pred),
        "monthly": json.dumps(monthly)
    })


def download_report(request):
    if "studID" not in request.session:
        return redirect("login")

    con = pymysql.connect(**DB_CONFIG)
    with con.cursor() as curs:
        curs.execute("""
            SELECT fullname, emailID
            FROM StudentRegistration
            WHERE studID=%s
        """, (request.session["studID"],))
        student_row = curs.fetchone()
    con.close()

    student = {
        "name": student_row[0],
        "email": student_row[1]
    }

    template = get_template("mental_health_report.html")
    html = template.render({
    "student": student,
    "inputs": request.session.get("inputs", {}),
    "prediction": request.session.get("prediction_result"),
    "explanation": request.session.get("explanation", []),  # ✅ ADD THIS
    "recommendations": request.session.get("recommendations", []),
    "date": date.today()
})


    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="Mental_Health_Report.pdf"'

    pdf = pisa.CreatePDF(html, dest=response)
    if pdf.err:
        return HttpResponse("Error generating PDF", status=500)

    return response




def resources(request):
    if "studID" not in request.session:
        return redirect("login")

    inputs = request.session.get("inputs")
    prediction = request.session.get("prediction_result")

    ai_resources = []

    # SAFETY CHECK
    if not inputs:
        ai_resources.append({
            "title": "Take Mental Health Assessment",
            "desc": "Please complete an assessment to get AI-based recommendations."
        })
    else:
        if inputs.get("Stress Level", 1) == 0:
            ai_resources.append({
                "title": "Managing Stress Effectively",
                "desc": "Evidence-based techniques to manage academic and emotional stress."
            })

        if inputs.get("Anxiety") == "Yes":
            ai_resources.append({
                "title": "5-Minute Breathing Exercise",
                "desc": "A simple breathing routine to reduce anxiety instantly."
            })

        if inputs.get("Sleep Hours", 7) < 6:
            ai_resources.append({
                "title": "Improve Sleep Quality",
                "desc": "Sleep hygiene techniques to improve mental well-being."
            })

        if inputs.get("Screen Time (hrs)", 0) > 6:
            ai_resources.append({
                "title": "Digital Detox Guide",
                "desc": "Reduce screen time and improve focus & sleep."
            })

        if prediction == "Mentally Fit":
            ai_resources.append({
                "title": "Preventive Mental Wellness",
                "desc": "Daily habits to maintain long-term emotional health."
            })

    return render(request, "resources.html", {
        "ai_resources": ai_resources
    })





# ===========================
# Login Failed View
# ===========================
def loginfailed(request):
    return render(request, "loginfailed.html")
