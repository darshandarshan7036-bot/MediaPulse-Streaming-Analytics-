from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os


app = FastAPI(
    title="MediaPulse API",
    description="Real-time audience analytics API",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "host.docker.internal"),
    "database": os.getenv("DB_NAME", "mediapulse"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD"),
    "port": int(os.getenv("DB_PORT", "5432"))
}
def get_connection():
    return psycopg2.connect(**DB_CONFIG)


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "MediaPulse API is running"
    }


# --------------------------------------------------
# LIVE AUDIENCE
# --------------------------------------------------

@app.get("/api/audience/live")
def get_live_audience():

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            total_live_events,
            unique_active_users,
            active_content,
            total_watch_seconds,
            average_watch_seconds,
            completed_events,
            completion_rate
        FROM live_audience_kpis;
    """)

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return {
        "total_live_events": row[0],
        "unique_active_users": row[1],
        "active_content": row[2],
        "total_watch_seconds": row[3],
        "average_watch_seconds": float(row[4]),
        "completed_events": row[5],
        "completion_rate": float(row[6])
    }


# --------------------------------------------------
# CONTENT PERFORMANCE
# --------------------------------------------------

@app.get("/api/content/{content_id}/performance")
def get_content_performance(content_id: str):

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            content_id,
            genre,
            language,
            duration,
            total_views,
            total_watch_seconds,
            watch_hours,
            completed_views,
            completion_rate
        FROM public.content_performance
        WHERE content_id = %s;
    """, (content_id,))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail=f"Content {content_id} not found"
        )

    return {
        "content_id": row[0],
        "genre": row[1],
        "language": row[2],
        "duration": row[3],
        "total_views": row[4],
        "total_watch_seconds": row[5],
        "watch_hours": float(row[6]),
        "completed_views": row[7],
        "completion_rate": float(row[8])
    }
# --------------------------------------------------
# CAMPAIGN PERFORMANCE
# --------------------------------------------------

@app.get("/api/campaigns")
def get_campaigns():

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            campaign_id,
            ad_events,
            impressions,
            clicks,
            ctr_percent
        FROM public.campaign_performance
        ORDER BY ctr_percent DESC;
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "campaigns": [
            {
                "campaign_id": row[0],
                "ad_events": row[1],
                "impressions": row[2],
                "clicks": row[3],
                "ctr_percent": float(row[4])
            }
            for row in rows
        ]
    }
# --------------------------------------------------
# SUBSCRIBER HEALTH
# --------------------------------------------------

@app.get("/api/subscriber/{user_id}/health")
def get_subscriber_health(user_id: str):

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            u.user_id,
            u.subscription_type,
            u.region,
            u.device,
            s.plan,
            s.status,
            COUNT(t.ticket_id) AS support_tickets
        FROM public.dim_user u
        LEFT JOIN public.fact_subscription s
            ON u.user_key = s.user_key
        LEFT JOIN public.support t
            ON u.user_id = t.user_id
        WHERE u.user_id = %s
        GROUP BY
            u.user_id,
            u.subscription_type,
            u.region,
            u.device,
            s.plan,
            s.status;
    """, (user_id,))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail=f"Subscriber {user_id} not found"
        )

    return {
        "user_id": row[0],
        "subscription_type": row[1],
        "region": row[2],
        "device": row[3],
        "plan": row[4],
        "status": row[5],
        "support_tickets": row[6]
    }
# --------------------------------------------------
# CHURN RISK
# --------------------------------------------------

@app.get("/api/churn-risk")
def get_churn_risk():

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            user_id,
            subscription_type,
            region,
            device,
            plan,
            status,
            total_views,
            total_watch_seconds,
            support_tickets,
            risk_level
        FROM public.churn_risk
        ORDER BY
            CASE risk_level
                WHEN 'High' THEN 1
                WHEN 'Medium' THEN 2
                WHEN 'Low' THEN 3
            END,
            user_id;
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "total_users": len(rows),
        "high_risk_users": sum(
            1 for row in rows if row[9] == "High"
        ),
        "medium_risk_users": sum(
            1 for row in rows if row[9] == "Medium"
        ),
        "low_risk_users": sum(
            1 for row in rows if row[9] == "Low"
        ),
        "users": [
            {
                "user_id": row[0],
                "subscription_type": row[1],
                "region": row[2],
                "device": row[3],
                "plan": row[4],
                "status": row[5],
                "total_views": row[6],
                "total_watch_seconds": row[7],
                "support_tickets": row[8],
                "risk_level": row[9]
            }
            for row in rows
        ]
    }
# --------------------------------------------------
# DATA QUALITY
# --------------------------------------------------

@app.get("/api/data-quality")
def get_data_quality():

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    checks = []

    # ----------------------------------------------
    # USERS
    # ----------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE user_id IS NULL
           OR subscription_type IS NULL
           OR region IS NULL
           OR device IS NULL;
    """)

    null_users = cursor.fetchone()[0]

    checks.append({
        "check": "Users null values",
        "failed_records": null_users,
        "status": "PASS" if null_users == 0 else "FAIL"
    })

    # ----------------------------------------------
    # VIEWS
    # ----------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM views
        WHERE event_id IS NULL
           OR user_id IS NULL
           OR content_id IS NULL
           OR timestamp IS NULL;
    """)

    null_views = cursor.fetchone()[0]

    checks.append({
        "check": "Views null values",
        "failed_records": null_views,
        "status": "PASS" if null_views == 0 else "FAIL"
    })

    cursor.execute("""
        SELECT COUNT(*)
        FROM views
        WHERE watch_seconds < 0;
    """)

    negative_watch = cursor.fetchone()[0]

    checks.append({
        "check": "Negative watch seconds",
        "failed_records": negative_watch,
        "status": "PASS" if negative_watch == 0 else "FAIL"
    })

    # ----------------------------------------------
    # VIEW FOREIGN KEYS
    # ----------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM views v
        LEFT JOIN users u
            ON v.user_id = u.user_id
        LEFT JOIN content c
            ON v.content_id = c.content_id
        WHERE u.user_id IS NULL
           OR c.content_id IS NULL;
    """)

    invalid_view_fk = cursor.fetchone()[0]

    checks.append({
        "check": "Views foreign key integrity",
        "failed_records": invalid_view_fk,
        "status": "PASS" if invalid_view_fk == 0 else "FAIL"
    })

    # ----------------------------------------------
    # ADS
    # ----------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM ads
        WHERE impression NOT IN (0, 1)
           OR click NOT IN (0, 1);
    """)

    invalid_ads = cursor.fetchone()[0]

    checks.append({
        "check": "Invalid ad values",
        "failed_records": invalid_ads,
        "status": "PASS" if invalid_ads == 0 else "FAIL"
    })

    cursor.execute("""
        SELECT COUNT(*)
        FROM ads
        WHERE click = 1
          AND impression = 0;
    """)

    invalid_clicks = cursor.fetchone()[0]

    checks.append({
        "check": "Clicks without impressions",
        "failed_records": invalid_clicks,
        "status": "PASS" if invalid_clicks == 0 else "FAIL"
    })

    # ----------------------------------------------
    # SUBSCRIPTIONS
    # ----------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM subscriptions s
        LEFT JOIN users u
            ON s.user_id = u.user_id
        WHERE u.user_id IS NULL;
    """)

    invalid_subscription_fk = cursor.fetchone()[0]

    checks.append({
        "check": "Subscription foreign key integrity",
        "failed_records": invalid_subscription_fk,
        "status": "PASS" if invalid_subscription_fk == 0 else "FAIL"
    })

    # ----------------------------------------------
    # SUPPORT
    # ----------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM support s
        LEFT JOIN users u
            ON s.user_id = u.user_id
        WHERE u.user_id IS NULL;
    """)

    invalid_support_fk = cursor.fetchone()[0]

    checks.append({
        "check": "Support foreign key integrity",
        "failed_records": invalid_support_fk,
        "status": "PASS" if invalid_support_fk == 0 else "FAIL"
    })

    cursor.close()
    conn.close()

    failed_checks = sum(
        1 for check in checks
        if check["status"] == "FAIL"
    )

    return {
        "overall_status": "PASS" if failed_checks == 0 else "FAIL",
        "total_checks": len(checks),
        "passed_checks": len(checks) - failed_checks,
        "failed_checks": failed_checks,
        "checks": checks
    }

@app.get("/api/alerts")
def get_alerts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            alert_id,
            alert_type,
            severity,
            owner,
            status,
            reason,
            created_at,
            acknowledged_at
        FROM alerts
        ORDER BY created_at DESC
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "alert_id": row[0],
            "alert_type": row[1],
            "severity": row[2],
            "owner": row[3],
            "status": row[4],
            "reason": row[5],
            "created_at": row[6],
            "acknowledged_at": row[7]
        }
        for row in rows
    ]
    
# --------------------------------------------------
# ACKNOWLEDGE ALERT
# --------------------------------------------------

@app.post("/api/alerts/{alert_id}/acknowledge")
def acknowledge_alert(alert_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE alerts
        SET
            status = 'Acknowledged',
            acknowledged_at = CURRENT_TIMESTAMP
        WHERE alert_id = %s
        RETURNING
            alert_id,
            alert_type,
            severity,
            owner,
            status,
            reason,
            created_at,
            acknowledged_at;
    """, (alert_id,))

    row = cursor.fetchone()

    conn.commit()

    cursor.close()
    conn.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail=f"Alert {alert_id} not found"
        )

    return {
        "alert_id": row[0],
        "alert_type": row[1],
        "severity": row[2],
        "owner": row[3],
        "status": row[4],
        "reason": row[5],
        "created_at": row[6],
        "acknowledged_at": row[7]
    }
    
# --------------------------------------------------
# ALERT ACTIONS
# --------------------------------------------------

@app.get("/api/alert-actions")
def get_alert_actions():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            action_id,
            alert_id,
            action_type,
            recipient,
            action_status,
            message,
            created_at
        FROM alert_actions
        ORDER BY created_at DESC;
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "total_actions": len(rows),
        "actions": [
            {
                "action_id": row[0],
                "alert_id": row[1],
                "action_type": row[2],
                "recipient": row[3],
                "action_status": row[4],
                "message": row[5],
                "created_at": row[6]
            }
            for row in rows
        ]
    }

@app.get("/api/audience/forecast")
def get_audience_forecast():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            forecast_id,
            forecast_date,
            predicted_audience,
            mae,
            rmse,
            created_at
        FROM audience_forecasts
        ORDER BY forecast_date DESC
        LIMIT 1;
    """)

    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="No forecast available")

    return {
        "forecast_id": row[0],
        "forecast_date": row[1],
        "predicted_audience": row[2],
        "mae": float(row[3]),
        "rmse": float(row[4]),
        "created_at": row[5]
    }
    
@app.get("/api/health")
def health_check():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT 1;")
    db_status = cur.fetchone()[0] == 1

    cur.close()
    conn.close()

    return {
        "status": "healthy",
        "database": "connected" if db_status else "error",
        "service": "MediaPulse API"
    }
