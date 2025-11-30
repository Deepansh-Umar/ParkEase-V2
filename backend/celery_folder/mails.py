import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


SMTP_SERVER = "localhost"
SMTP_PORT = 1025
SENDER_EMAIL = 'ParkEaseAdmin@example.com'


def send_email(to, subject, html):

    msg = MIMEMultipart("alternative")
    msg['To'] = to
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL

    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP(host=SMTP_SERVER, port=SMTP_PORT) as client:
        client.send_message(msg)
        client.quit()



def daily_reminder_template(username):
    return f"""
    <html>
    <body>
        <h2>Hello {username} 👋</h2>
        <p>This is your daily reminder to log in to ParkEase!</p>
        <p>Have a great day 😊</p>
    </body>
    </html>
    """

 
def monthly_report_template(username, reservations, total_cost, month, year):

    rows = ""
    for r in reservations:
        rows += f"""
            <tr>
                <td>{r.id}</td>
                <td>{r.lot.name}</td>
                <td>{r.spot_id}</td>
                <td>{r.start_time}</td>
                <td>{r.leave_time or '-'}</td>
                <td>{r.total_cost or 0}</td>
            </tr>
        """

    if not reservations:
        table_html = "<p>No reservations this month.</p>"
    else:
        table_html = f"""
        <table border="1" cellpadding="8" cellspacing="0">
            <tr>
                <th>ID</th>
                <th>Lot</th>
                <th>Spot</th>
                <th>Start</th>
                <th>End</th>
                <th>Cost</th>
            </tr>
            {rows}
        </table>
        <h3>Total Monthly Cost: ₹{total_cost}</h3>
        """

    return f"""
    <html>
    <body>
        <h2>Monthly Parking Report – {month} {year}</h2>
        <h3>Hello {username},</h3>
        <p>Here is your summary for this month:</p>
        {table_html}
        <br>
        <p>Thank you for using ParkEase 🚗</p>
    </body>
    </html>
    """
