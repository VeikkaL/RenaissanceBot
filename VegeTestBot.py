# TODO
# - Symbolilistat
# - Nousijat/laskijat
# - Aamuviestit
# - Lähetys jos ei usernamea

# Osaketietojen hakemiseen
from yahoo_fin.stock_info import *

# Telegram-botin käyttöön
import telepot
from telepot.loop import MessageLoop
import time

aika = time.gmtime(time.time())

token = '860817945:AAGQLppRDE0mtBTps3C0-YO6HOCs5dfI_iw'
bot = telepot.Bot(token)

# Käsittelee botille tulevat viestit
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    text = msg.get('text').upper()
    user = msg['from']['username']
    
    ticker = text[7:]
    quote = round(get_live_price(ticker), 2)
    table = get_quote_table(ticker)
    close = round(table.get('Previous Close'), 2)
    change = round((quote / close - 1) * 100, 2)
    tableS = get_quote_table('^GSPC')
    tableH = get_quote_table('^OMXHPI')
    quoteS = round(get_live_price('^GSPC'), 2)
    quoteH = round(get_live_price('^OMXHPI'), 2)
    closeS = round(tableS.get('Previous Close'), 2)
    closeH = round(tableH.get('Previous Close'), 2)
    changeS = round((quoteS / closeS - 1) * 100, 2)
    changeH = round((quoteH / closeH - 1) * 100, 2)
    
    if aika.tm_wday <= 4 and aika.tm_hour == 7 and aika.tm_min == 0:
        bot.sendMessage('301161189', 'OMXHPI auki! {quoteH}, tänään {changeH}%'.format(quoteH=quoteH, changeH=changeH))
    if aika.tm_wday <= 4 and aika.tm_hour == 13 and aika.tm_min == 30:
        bot.sendMessage('301161189', 'S&P500 auki! {quoteS}, tänään {changeS}%'.format(quoteS=quoteS, changeS=changeS))
    
    print(content_type, chat_type, chat_id, user, text)
    
    try:
        if content_type == 'text' and 'KURSSI' in text:
            
            if '.' in ticker:
                if '.SS' in ticker:
                    bot.sendMessage(chat_id, '{ticker}: RMB {quote}, tänään {change}%'.format(ticker=ticker, quote=quote, change=change))
                elif '.HK' in ticker:
                    bot.sendMessage(chat_id, '{ticker}: HKD {quote}, tänään {change}%'.format(ticker=ticker, quote=quote, change=change))
                elif '.L' in ticker:
                    bot.sendMessage(chat_id, '{ticker}: £{quote}, tänään {change}%'.format(ticker=ticker, quote=quote, change=change))
                elif '.T' in ticker:
                    bot.sendMessage(chat_id, '{ticker}: ¥{quote}, tänään {change}%'.format(ticker=ticker, quote=quote, change=change))
                elif '.BO' in ticker:
                    bot.sendMessage(chat_id, '{ticker}: INR {quote}, tänään {change}%'.format(ticker=ticker, quote=quote, change=change))
                elif '.TO' in ticker:
                    bot.sendMessage(chat_id, '{ticker}: CAD {quote}, tänään {change}%'.format(ticker=ticker, quote=quote, change=change))
                elif '.KS' in ticker:
                    bot.sendMessage(chat_id, '{ticker}: ₩{quote}, tänään {change}%'.format(ticker=ticker, quote=quote, change=change))
                else:
                    bot.sendMessage(chat_id, '{ticker}: €{quote}, tänään {change}%'.format(ticker=ticker, quote=quote, change=change))
            elif '^' in ticker:
                bot.sendMessage(chat_id, '{ticker}: {quote}, tänään {change}%'.format(ticker=ticker, quote=quote, change=change))
            else:
                bot.sendMessage(chat_id, '{ticker}: ${quote}, tänään {change}%'.format(ticker=ticker, quote=quote, change=change))

        elif content_type == 'text' and 'INDEKSIT' in text:
       
            if aika.tm_wday <= 4 and aika.tm_hour >= 13 and aika.tm_hour <= 15:
                if aika.tm_hour == 13 and aika.tm_min >= 30:
                    bot.sendMessage(chat_id, 'S&P500: {quoteS}, tänään {changeS}%\nOMXHPI: {quoteH}, tänään {changeH}%'.format(quoteS=quoteS, changeS=changeS, quoteH=quoteH, changeH=changeH))
                elif aika.tm_hour == 14:
                    bot.sendMessage(chat_id, 'S&P500: {quoteS}, tänään {changeS}%\nOMXHPI: {quoteH}, tänään {changeH}%'.format(quoteS=quoteS, changeS=changeS, quoteH=quoteH, changeH=changeH))
                elif aika.tm_hour == 15 and aika.tm_min <= 30:
                    bot.sendMessage(chat_id, 'S&P500: {quoteS}, tänään {changeS}%\nOMXHPI: {quoteH}, tänään {changeH}%'.format(quoteS=quoteS, changeS=changeS, quoteH=quoteH, changeH=changeH))
                                
            elif aika.tm_wday <= 4 and aika.tm_hour >= 7 and aika.tm_hour <= 13:
                if aika.tm_hour == 13 and aika.tm_min < 30:
                    bot.sendMessage(chat_id, 'S&P500 kiinni, edellinen {changeS}%\nOMXHPI: {quoteH}, tänään {changeH}%'.format(quoteS=quoteS, changeS=changeS, quoteH=quoteH, changeH=changeH))                  
                elif aika.tm_hour == 13 and aika.tm_min >= 30:
                    bot.sendMessage(chat_id, 'S&P500: {quoteS}, tänään {changeS}%\nOMXHPI: {quoteH}, tänään {changeH}%'.format(quoteS=quoteS, changeS=changeS, quoteH=quoteH, changeH=changeH))
                else: bot.sendMessage(chat_id, 'S&P500 kiinni, edellinen {changeS}%\nOMXHPI: {quoteH}, tänään {changeH}%'.format(quoteS=quoteS, changeS=changeS, quoteH=quoteH, changeH=changeH))    
            
            elif aika.tm_wday <= 4 and aika.tm_hour >= 15 and aika.tm_hour <= 20:
                if aika.tm_hour == 15 and aika.tm_min > 30:    
                    bot.sendMessage(chat_id, 'S&P500: {quoteS}, tänään {changeS}%\nOMXH kiinni, edellinen {changeH}%'.format(quoteS=quoteS, changeS=changeS, quoteH=quoteH, changeH=changeH))
                elif aika.tm_hour == 15 and aika.tm_min <= 30:
                    bot.sendMessage(chat_id, 'S&P500: {quoteS}, tänään {changeS}%\nOMXHPI: {quoteH}, tänään {changeH}%'.format(quoteS=quoteS, changeS=changeS, quoteH=quoteH, changeH=changeH))
                else: bot.sendMessage(chat_id, 'S&P500: {quoteS}, tänään {changeS}%\nOMXH kiinni, edellinen {changeH}%'.format(quoteS=quoteS, changeS=changeS, quoteH=quoteH, changeH=changeH))
                
            else:
                bot.sendMessage(chat_id, 'S&P500 kiinni, edellinen {changeS}%\nOMXH kiinni, edellinen {changeH}%'.format(quoteS=quoteS, changeS=changeS, quoteH=quoteH, changeH=changeH))                
                


#       elif content_type == 'text' and 'NOUSIJAT' in text:
        
#       elif content_type == 'text' and 'LASKIJAT' in text:
        
        elif content_type == 'text' and '/HELP' in text:
            bot.sendMessage(chat_id, 'Komennot:\n\n"Kurssi [symboli]" - hae osakkeen tai indeksin reaaliaikainen kurssi sekä muutos eiliseen. Symbolit ovat mallia Yahoo Finance. Esimerkki: kurssi sampo.he\n\n"Indeksit" - Näytä S&P500 ja OMX Helsinki PI:n tämänhetkinen kurssi sekä muutos eiliseen.')
        
        elif content_type == 'text' and '/START' in text:
            bot.sendMessage(chat_id, 'Tervetuloa! Kirjoita /help aloittaaksesi.')
        
        else:
            bot.sendMessage(chat_id, 'En ymmärrä :( Jos yritit hakea osakekurssia, varmista että symboli oli oikein. Myös kirjoittamalla /help saat apua!')
           

    except RuntimeError:
        return
MessageLoop(bot, handle).run_as_thread()


