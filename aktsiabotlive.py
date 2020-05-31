import pandas as pd
from alpha_vantage.techindicators import TechIndicators
import datetime
import time


def email(tekst, aktsia):
    # email
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    fromEmail = 'toodmany@gmail.com'
    toEmail = 'kaarel.vesilind@gmail.com'

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Aktsia alert: " + aktsia
    msg["From"] = fromEmail
    msg["To"] = toEmail

    html = """
            <h4> %s </h4>
        """ % (tekst)

    mime = MIMEText(html, 'html')

    msg.attach(mime)

    try:
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login(fromEmail, "password")
        mail.sendmail(fromEmail, toEmail, msg.as_string())
        mail.quit()
        print('Email sent!')
    except Exception as e:
        print('Something went wrong... %s' % e)


i = 0
while True:
    try:
        if (datetime.datetime.now().hour >= 10 and datetime.datetime.now().hour < 16):
            api_key = 'api key'
            aktsiad = ['SAB1L.VS', 'TAL1T.TL', 'TSM1T.TL', 'TKM1T.TL', 'LHV1T.TL', 'TVEAT.TL', 'MRK1T.TL',
                       'CPA1T.TL', 'TEL1L.VS', 'EFT1T.TL', 'APG1L.VS', 'OLF1R.RG', 'NCN1T.TL', 'SFG1T.TL']
            aktsia = aktsiad[i % 14]
            print(aktsia)
            ti = TechIndicators(key=api_key, output_format='pandas')
            data, meta_data = ti.get_ema(
                symbol=aktsia, interval='15min', time_period=72, series_type='close')
            time.sleep(2)
            avg3 = data['EMA']
            data, meta_data = ti.get_ema(
                symbol=aktsia, interval='15min', time_period=216, series_type='close')
            time.sleep(2)
            avg10 = data['EMA']
            eelmine_avg3 = avg3[-2]
            eelmine_avg10 = avg10[-2]
            praegune_avg3 = avg3[-1]
            praegune_avg10 = avg10[-1]
            data, meta_data = ti.get_sma(
                symbol=aktsia, interval='1min', time_period=2, series_type='close')
            hind_palju = data['SMA']
            hind = hind_palju[-1]

            print('Eelmine lühikeskmine oli:', eelmine_avg3)
            print('Eelmine pikkkeskmine oli:', eelmine_avg10)
            print('Lühikeskmine on:', praegune_avg3)
            print('Pikkkeskmine on:', praegune_avg10)
            print('Hind praegu', hind)

            timestamp = 'Timestamp: '+meta_data['3: Last Refreshed'] +" "+ \
                meta_data['7: Time Zone']
            print(timestamp)
            tekst_põhi = 'Eelmine lühikeskmine oli: '+ str(eelmine_avg3) + '<br/>' + 'Eelmine pikkkeskmine oli: '+ str(eelmine_avg10) + '<br/>' + \
                'Lühikeskmine on: ' + str(praegune_avg3) + '<br/>' + 'Pikkkeskmine on: ' + str(praegune_avg10) + \
                    '<br/>' + 'Viimane hind: '+ str(hind) + '<br/>' + str(timestamp)

            if eelmine_avg3 <= eelmine_avg10 and praegune_avg3 > praegune_avg10:
                tekst = "Osta " + aktsia + '<br><br>' + tekst_põhi
                email(tekst,aktsia)
            elif eelmine_avg3 >= eelmine_avg10 and praegune_avg3 < praegune_avg10:
                tekst = "Müü " + aktsia + '<br><br>' + tekst_põhi
                email(tekst, aktsia)
    except Exception as e:
        print('Miski läks valesti... %s' % e)
    i += 1
    time.sleep(60)
