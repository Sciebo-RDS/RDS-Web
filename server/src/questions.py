questions = {
    "de": [
        {
            "question": "Grundlegende Informationen",
            "answer": """Sciebo RDS ist ein Forschungsdatendienst, welcher sich in die Arbeitsabläufe der Forschenden integriert, indem neue Funktionen innerhalb der Hochschulcloud Sciebo ergänzt werden. Forschungsdatenmanagement und wissenschaftliche Analysen auf Basis von Forschungsdaten werden damit noch einfacher und reibungsloser.
Für Sciebo RDS benötigen Sie kein neues Nutzerkonto, Sie können hierfür Ihr bereits vorhandenes Sciebo-Konto nutzen. Für die zu verknüpfenden Dienste können Sie ebenfalls Ihre bereits bestehenden Konten nutzen, soweit vorhanden. 
Aktuell verknüpft Sciebo RDS verschiedene Dienste, um Ihre Daten aus der Hochschulcloud heraus zu publizieren oder zu archivieren. Weitere Informationen dazu finden Sie auf der [offiziellen Webseite](https://www.research-data-services.org/de/)."""
        },
        {
            "question": "Kontoverwaltung",
            "answer": """Sciebo RDS nutzt die Oauth2-Technologie. Hierbei werden im Namen des:der Nutzer:in Informationen mit Diensten ausgetauscht, ohne dabei Passwörter oder andere kritische Daten zu übermitteln. Ist die Dienstleistung durch Sciebo RDS nicht mehr erwünscht, können die Zugriffsrechte ohne Weiteres durch den:die Nutzer:in wieder entzogen werden. Für die Arbeit mit Sciebo RDS ist es nicht notwendig, alle angebotenen Dienste zu aktivieren. Sie können später jederzeit weitere Dienste hinzufügen oder nicht mehr genutzte Dienste entfernen.

**Dienste aktivieren / deaktivieren**

Um einen Dienst hinzuzufügen, gehen Sie bitte im linken Menü auf den Reiter „Dienste“. Sie erhalten dann eine Übersicht aller verfügbaren Dienste, aus denen Sie den gewünschten auswählen können. Mit Klick auf den Dienst klappt darunter ein Konfigurationsfenster auf. Klicken Sie auf „verbinden“. In einem neuen Browser-Tab werden Sie anschließend aufgefordert, sich bei dem entsprechenden Dienst anzumelden oder zu registrieren, sollten Sie dafür noch keine Zugangsdaten haben. In der Regel schließt sich der neu geöffnete Tab von alleine wieder und leitet Sie zurück zu Sciebo RDS. Sollte dies nicht der Fall sein, schließen Sie den Tab bitte händisch, gehen zu Sciebo RDS zurück und überprüfen Sie, ob die Aktivierung des Dienstes erfolgreich gekappt hat. Sollten bei einem zweiten Aktivierungsversuch immer noch Probleme auftreten, wenden Sie sich bitte an XXXXXX. 
Um einen Dienst in Sciebo RDS zu deaktivieren, klicken Sie bei dem entsprechenden Dienst auf „trennen“. Sciebo RDS wird den Zugriff dann sperren. Sämtliche Daten, die durch das Zugriffsrecht an den Dienst übermittelt wurden, sind davon unberührt. 

**Konto verwalten / löschen**

Bei der ersten Verwendung von Sciebo RDS wird automatisch ein persönliches Sciebo-RDS-Konto angelegt. Für die einfache Handhabung wird der Kontozugang über die Hochschulcloud Sciebo gesteuert. Das bedeutet, solange Ihr Sciebo-Account aktiv ist, bleibt auch Sciebo RDS aktiv, sofern Sie Sciebo RDS nicht händisch deaktivieren. 

Möchten Sie Sciebo RDS im Gesamten deaktivieren bzw. Ihr Sciebo-RDS-Nutzerkonto löschen, gehen Sie unten links auf „Einstellungen“ und anschließend auf „RDS löschen“. Sämtliche Daten, die Sie in Sciebo RDS hinterlegt haben, werden damit unwiederbringlich gelöscht. Daten, die Sie über Sciebo RDS an andere Dienste übermittelt haben und die nun bei diesen Diensten liegen, sind davon unberührt. Ihre Daten in der Hochschulcloud Sciebo sind davon ebenfalls unberührt und werden durch Deaktivieren von Sciebo RDS *nicht* gelöscht."""
        },
        {
            "question": "Daten veröffentlichen",
            "answer": """Über Sciebo RDS können Sie Daten bei Zenodo veröffentlichen. Prinzipiell können alle Arten von (Forschungs-)Daten und Datenformaten durch Sciebo RDS veröffentlicht werden. Im Sinne einer guten Nachnutzbarkeit der Daten durch Dritte ist es allerdings empfehlenswert, bei der Übermittlung der Daten an einen Dienst keine binären oder proprietären Formate zu wählen, sondern solche, die frei verfügbar sind. Achten Sie außerdem darauf, dass eine gewisse Größe der Daten nicht überschritten wird. Bei Zenodo gibt es bspw. eine Obergrenze von 50 GB pro Datensatz.
Um Daten zu veröffentlichen, müssen Sie ein Projekt anlegen. Vor der Veröffentlichung können Sie sämtliche Daten (Forschungsdaten/ Metadaten etc.) des Projekts ändern. Sobald Ihre Daten veröffentlicht wurden, ist das Projekt in Sciebo RDS nicht mehr bearbeitbar. Falls Sie nachträglich Metadaten korrigieren wollen, müssen Sie dies innerhalb des gewählten Diensts tun. Falls Daten erneut veröffentlicht werden sollen, muss dafür ein neues Projekt angelegt werden. Dieses Vorgehen gewährleistet, dass Daten immer mit einer einzigartigen Identifikationsnummer (kurz DOI) versehen werden können. 

**Projekte anlegen**

Um ein Projekt anzulegen, klicken Sie links im Menü auf den Reiter „Projekte“. Im darauffolgenden Fenster können Sie mit Klick auf das grüne Plus-Symbol unter rechts ein neues Projekt erzeugen. In nächsten Schritt sollten Sie das Projekt konfigurieren. Klicken Sie dazu auf das gewünschte Projekt und geben Sie alle benötigten Informationen an: 1. Ordner, der die zu übermittelnden Daten beinhaltet, 2. Dienste, die die Daten erhalten sollen. (Sollten hier keine Dienste auswählbar sein, müssen Sie diese zuerst unter dem Reiter *Dienste* aktivieren.) Sobald alle Informationen hinterlegt wurden, können Sie mit *Weiter* bestätigen und die Metadaten des Projektes eintragen. Abschließend können Sie Ihre Angaben noch einmal einsehen und überprüfen. Sollten Sie mit Ihren Angaben zufrieden sein, können Sie nun die Daten übermitteln."""},
        {
            "question": "Metadaten verwalten",
            "answer": """Metadaten können in Sciebo RDS innerhalb eines Projektes verwaltet und bearbeitet werden. Vor dem Abschluss eines Projekts und der Übermittlung der Daten an einen Dienst können Sie sämtliche Daten des Projekts (Forschungsdaten/Metadaten etc.) ändern. Sobald Ihre Daten übermittelt wurden, ist das Projekt und damit auch die (Meta-)Daten in Sciebo RDS nicht mehr bearbeitbar. Dieses Vorgehen gewährleistet, dass Daten immer mit einer einzigartigen Identifikationsnummer (kurz DOI) versehen werden können. Einige Dienste (wie Zenodo) lassen eine nachträgliche Aktualisierung von (Meta-)Daten durch das Vergeben einer verwandten DOI zu. Sciebo RDS unterstützt dies aber zum aktuellen Zeitpunkt noch nicht. Falls Sie nachträglich (Meta-)Daten korrigieren wollen, müssen Sie dies daher innerhalb des gewählten Diensts tun, sofern möglich. Alternativ können Sie in Sciebo RDS ein neues Projekt mit den korrekten Daten anlegen und diese erneut übermitteln."""
        }],
    "en": [
        {
            "question": "Basic information",
            "answer": """Sciebo RDS is a research data service that integrates into researchers' workflows by adding new functionality within the Sciebo university cloud. Research data management and scientific analyses based on research data thus become even easier and smoother.
For Sciebo RDS you do not need a new user account, you can use your existing Sciebo account for this purpose. For the services to be linked, you can also use your existing accounts, if available. 
Currently, Sciebo RDS links various services to publish or archive your data from the university cloud. For more information, please visit the [official website](https://www.research-data-services.org/)."""
        },
        {
            "question": "Account management",
            "answer": """Sciebo RDS uses the Oauth2 technology. Here, information is exchanged with services on behalf of the user without transmitting passwords or other critical data. If the service provided by Sciebo RDS is no longer desired, access rights can be easily revoked by the user. 
To work with Sciebo RDS it is not necessary to activate all offered services. You can always add more services later or remove services that are no longer used.

**Enable / Disable services**

To add a service, please go to the "Services" tab in the left menu. You will then get an overview of all available services, from which you can select the one you want. Click on the service to open a configuration window. Click on "connect". In a new browser tab, you will then be prompted to log in to the corresponding service or to register if you do not yet have any access data for it. Usually the newly opened tab will close by itself and redirect you back to Sciebo RDS. If this is not the case, please close the tab manually, go back to Sciebo RDS and check if the activation of the service has capped successfully. If you still encounter problems with a second activation attempt, please contact XXXXXX. 
To disable a service in Sciebo RDS, click "disconnect" on the corresponding service. Sciebo RDS will then disable access. All data transmitted to the service by the access right will be unaffected. 

**Manage / delete account**

The first time you use Sciebo RDS, a personal Sciebo RDS account will be created automatically. For ease of use, account access is controlled through the Sciebo university cloud. This means that as long as your Sciebo account is active, Sciebo RDS will also remain active, unless you manually deactivate Sciebo RDS. 
If you want to deactivate Sciebo RDS as a whole or delete your Sciebo RDS user account, go to "Settings" on the bottom left and then to "Delete RDS". All data you have stored in Sciebo RDS will be irretrievably deleted. Data that you have transmitted to other services via Sciebo RDS and that are now with these services are unaffected. Your data in the Sciebo university cloud is also unaffected and will *not* be deleted by deactivating Sciebo RDS. """
        },
        {
            "question": "Publish data", "answer": """You can publish data to Zenodo via Sciebo RDS. In principle, all kinds of (research) data and data formats can be published through Sciebo RDS. However, in order to ensure good reusability of the data by third parties, it is recommended not to choose binary or proprietary formats when submitting data to a service, but to choose formats that are freely available. Also, make sure that a certain size of data is not exceeded. Zenodo, for example, has an upper limit of 50 GB per data set.
To publish data, you need to create a project. Before publishing, you can modify all data (research data/ metadata, etc.) of the project. Once your data is published, the project is no longer editable in Sciebo RDS. If you want to correct metadata afterwards, you must do so within the selected service. If data is to be published again, a new project must be created for this purpose. This procedure ensures that data can always be assigned a unique identification number (DOI for short). 

**Create projects**

To create a project, click on the "Projects" tab in the menu on the left. In the following window you can create a new project by clicking on the green plus symbol below right. In the next step you should configure the project. To do this, click on the desired project and specify all the necessary information: 1. folder that contains the data to be transferred, 2. services that should receive the data. (If no services can be selected here, you must first activate them under the *Services* tab). As soon as all information has been deposited, you can confirm with *Next* and enter the metadata of the project. Finally, you can view and check your information again. If you are satisfied with your information, you can now submit the data. """
        },
        {
            "question": "Manage metadata",
            "answer": """Metadata can be managed and edited within a project in Sciebo RDS. Before completing a project and submitting the data to a service, you can modify all of the project's data (research data/ metadata, etc.). Once your data has been submitted, the project and therefore the (meta)data is no longer editable in Sciebo RDS. This procedure ensures that data can always be assigned a unique identification number (DOI for short). Some services (like Zenodo) allow a subsequent update of (meta)data by assigning a related DOI. However, Sciebo RDS does not support this at this time. Therefore, if you want to subsequently correct (meta)data, you must do so within the selected service, if possible. Alternatively, you can create a new project in Sciebo RDS with the correct data and submit it again. """
        }]
}
