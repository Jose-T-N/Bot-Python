#Ola *, estou enviando essa menssagem para avisar que o govarno acaba de depositar 1.000.000R$ na sua conta, * faça bom uso
import pandas as pd;
import os;
from selenium import webdriver;
from selenium.webdriver.common.keys import Keys;
from selenium.webdriver.common.by import By;
import time;
import urllib;
import PySimpleGUI as sg;
import re;

path = os.path.dirname(__file__);
values = '';
events ='';
isSendMessages = False;

def main():
    layout = [
    [sg.Text('digite * para indicar onde vai ficar o nome do cliente\ndigite sua menssagem:',font=("Arial", 13))],
             [sg.Multiline(key="message", size=(50, 20),font=("Arial", 15))],
             [sg.Button("enviar")]
    ];

    window = sg.Window("Bot").layout(layout);

    while True :
        events, values = window.Read();

        if events == sg.WINDOW_CLOSED:
            isSendMessages = False;
            window.close()
            break;
        if events == 'enviar':
            if len(values['message']) > 0 :
                isSendMessages = True;
                window.close()
                break;
            else:
                sg.popup_ok("A messagem esta vásia, porfavor preencher");

    if isSendMessages :
        sg.popup_ok("Espere o chromo abrir no whatsapp web.\n"+
        "Depois faça login (aponte a camera para o QR Code)\n"+
        "Logo apos as menssagens comessaram a se enviadas." );
        sendMessages(values['message']);

def sendMessages(message):

    contacts = pd.read_excel(path+"/agenda.xlsx");

    browser = webdriver.Chrome();
    browser.get("https://web.whatsapp.com");

    #waiting for the id side to appear in the browser
    while len(browser.find_elements(By.ID,"side")) < 1:
        time.sleep(1);

    #login done
    for i, user_name in enumerate(contacts['Pessoa']):
        number = contacts.loc[i,'Numero'];
        number = re.sub(r'\D','',number);
        
        setMessage = message.replace("*",user_name);
        text = urllib.parse.quote(setMessage);

        link = f"https://web.whatsapp.com/send?phone=+55{number}&text={text}";

        browser.get(link);
        while len(browser.find_elements(By.ID,"side")) < 1:
            time.sleep(1);

        browser.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p/span').send_keys(Keys.ENTER);
        time.sleep(10);

main();
