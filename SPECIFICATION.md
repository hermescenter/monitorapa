# monitorapa
Progetto per monitoraggio e notifica di non compliance GDPR alle PA con input da IndicePA.

Telegram: https://t.me/monitoraPA   
[Element/Matrix](https://element.io): https://matrix.to/#/%23MonitoraPA:matrix.opencloud.lu

## Project Description
This project is about to write several scripts that perform the following actions, each one individually:

1.    Download a database of organizations names along with website address and email address
 2.    Analyze each of the website in a technically advanced way to evaluate if certain resources are present, writing a short report
 3.    Enrich the database of point 1, in a machine readable format, for the organizations/websites pairs that match the analysis of point 2
 4.    Starting from the enriched database of 3, send a notification email to the corresponding email address according to a pre-defined template
 5.    Enrich the database of point 3, with the outcome/results of notification

## Software requirements
The software must be written in Python.

Each step must be an individual script to be executed manually from the command line.

The software must be provided with the setup instruction and with the uses instruction, in Markdown format, to be published as README.md of Github repository.

The software must be provided along with the results of the entire test and the results must be repeatable.

The software must be published on a dedicated Github Repository to enable anyone to repeat the process.

## The Database - Point 1
The database to be downloaded and imported is the list of Italian Public Agencies available as a tab separated file “amministrazioni.txt” from the URL https://indicepa.gov.it/ipa-dati/dataset/amministrazioni .

The database description is described as per manifest file at: https://indicepa.gov.it/ipa-dati/dataset/amministrazioni/resource/cdd614a1-875c-497a-8ce8-ba0c6b785cae .

## The Analysis - Point 2
The analysis to be done is to check with a web_test, reporting if it has a 0 or 1 result, the corresponding the test's metadata result, success or failure of the test, date and time of the test.

The web test, for this project, is to check if a website contain/include Google Analytics.

The website url to be used is the field sito_istituzionale of the database of Point 1.

The way to check the presence of Google Analysis must uses a full featured API that fully execute and load the website, including Javascript, emulating/using a full browser, checking if Google Analytics is loaded.

The Google Analytics UA number has to be extracted.

The request to the website must try up to 3 times, in case of failure.

The Analysis results has to be written in a short output file for diagnostic with all the relevant data of the Analytics process, including:
 -    URL of Website Analyzed
 -    Results of Connections / Requests (es: Connection Timeout, HTTP 503, etc)
 -    Presence or not of Web Test (Google Analytics presence)
-     Metadata of the Web Test (UA number of Google Analytics)
-     Date of Test
-     Time of Test (in UTC)

## The First Database Enrichment - Point 3

This process must take as a input the output of Point 2 and enrich the file of Point 1, creating a full database of Italian Public Agencies, extend with the information:

 -    web_test_result: Presence or not of Web Test - Google Analytics (0 or 1)
 -    web_test_metadata: UA number of Google Analytics
 -    web_test_date: Date of Test
 -    web_test_time:Time of Test

## The sending of email notification - Point 4

Taking as a input the enriched database of Point 3, this separated script must take care of sending email to the email address from the field mail1 .

The email notification is to be sent only to all the email addresses of the organizations that was found to have Google Analytics included into their website.

The email has to be sent using a configurable SMTP server with SMTP/TLS with Login+Password authentication.

The email has to be sent with a configurable delay between each email sent expressed in seconds (es: 1 email sent every 15 seconds).

The descriptive sender and sender email of the email must be configurable.

The email generated must pass the Spam Rating Checks being not considered as Spam as per:
 -    https://spamcheck.postmarkapp.com/
 -    https://www.mail-tester.com/

The format/template of the email has to be configurable, in the Subject and in the Body as follow, using a set of variables from the originating database.

TEMPLATE FOR SUBJECT:

Subject: Ammonizione per violazione del GDPR per utilizzo Google Analytics su $cod_amm

TEMPLATE FOR BODY:

Alla Att.ne del DPO (Responsabile Protezione Dati) dell’Ente.
Oggetto: Ammonizione per violazione del GDPR per utilizzo Google Analytics su sito istituzionale
La presente comunicazione come Ammonimento per segnalare violazione del GDPR avvenuta dal vs. Ente $des_amm con responsabile Dott. $nome_resp $cogn_resp derivante dall’utilizzo presso il sito $sito_*istituzionale del fornitore Google, secondo quanto confermato dalla decisione dell'EDPS nell'arrivare a sanzionare il Parlamento Europeo per l'uso dello strumento Google Analytics come indicato in seguito https://noyb.eu/en/edps-sanctions-parliament-over-eu-us-data-transfers-google-and-stripe .
La presente viene inviata in via informativa per consentire una rapida rimozione di Google Analytics, rimandando raccomandato dalla Agenzia per l'Italia Digitale Web Analytics Italia https://www.agid.gov.it/it/design-servizi/web-analytics-italia .
Il rendiconto delle Pubbliche Amministrazioni in violazione viene pubblicato come report e inviato come segnalazione al Garante per la Protezione dei Dati e al Difensore Civico Digitale.
END_TEMPLATE_FOR_BODY

The script sending the email must write a short summary report and state file of the email sent and the email that had errors.

It must be possible to interrupt the script and execute it again, so that the script will starts agains sending email back to the point it has been interrupted.

## The Second Database Enrichment - Point 5

This process must take as an input the output of Point 4 and enrich the file of Point 3, creating a full database of Italian Public Agencies, extending with the information:

 -    notification_success: Successful notification or Not (0 or 1)
 -    notification_date: Date of Notification
 -    notification_time: Time of Notification

The final results is the database downloaded at Point 1 with the additional field enriched at Point 3 and Point 5.
