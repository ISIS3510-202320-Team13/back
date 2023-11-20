import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils import key_mail

def send_email(receiver_email, uid_reservation, parking_name, start_time, duratiom, cost, name):

  sender_email = "losarquipanitas@gmail.com"
  password = key_mail.password

  message = MIMEMultipart("alternative")
  message["Subject"] = "Your reservation with ParkEz"
  message["From"] = sender_email
  message["To"] = receiver_email

  html = """\
  <!DOCTYPE html>
  <html>
  <head>
      <meta charset="UTF-8">
      <title>Parking Reservation Confirmation</title>
      <style>
          body {{
              font-family: Arial, sans-serif;
          }}
          .container {{
              max-width: 600px;
              margin: 0 auto;
              padding: 20px;
          }}
          .header {{
              background-color: #007BFF;
              color: #fff;
              text-align: center;
              padding: 20px;
          }}
          .confirmation {{
              text-align: center;
          }}
          .reservation-details {{
              border: 1px solid #ccc;
              padding: 20px;
          }}
      </style>
  </head>
  <body>
      <div class="container">
          <div class="header">
              <h1>Parking Reservation Confirmation</h1>
          </div>
          <div class="confirmation">
              <p>Dear {customer_name},</p>
              <p>Your parking reservation has been confirmed. Here are the details:</p>
          </div>
          <div class="reservation-details">
              <p><strong>Reservation ID:</strong> {reservation_id}</p>
              <p><strong>Reserved Parking Space:</strong> {parking_space}</p>
              <p><strong>Date and Time:</strong> {date_and_time}</p>
              <p><strong>Duration:</strong> {duration}</p>
              <p><strong>Total Cost:</strong> ${total_cost}</p>
          </div>
          <div class="confirmation">
              <p>Thank you for choosing our parking service. If you have any questions or need further assistance, please contact our customer support at {phone_number} or email us at {email_address}.</p>
              <p>Safe travels!</p>
          </div>
      </div>
  </body>
  </html>
  """

  reservation_info = {
      "customer_name": name,
      "reservation_id": uid_reservation,
      "parking_space": parking_name,
      "date_and_time": start_time,
      "duration": duratiom,
      "total_cost": cost,
      "phone_number": "01 8000 - ParkEz",
      "email_address": "help@parkez.com",
  }

  formatted_html = html.format(**reservation_info)
  part2 = MIMEText(formatted_html, "html")
  message.attach(part2)

  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
      server.login(sender_email, password)
      server.sendmail(
          sender_email, receiver_email, message.as_string()
      )