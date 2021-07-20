questions = {
    "de": [
        {
            "question": "Grundlegende Informationen",
            "answer": """Sciebo RDS ist ein Forschungsdatendienst, welcher sich in die Arbeitsabläufe der Forschenden integriert, indem neue Funktionen innerhalb der Hochschulcloud Sciebo integriert werden.
                
Es ist demnach nicht notwendig, neue Benutzerkonten oder weiteres anzulegen. Sie verwenden Ihr bereits vorhandenes Sciebokonto für die Authentifizierung gegenüber Sciebo RDS. Für die zu verknüpfenden Dienste, nutzen Sie auch ihre bereits bestehenden Konten, soweit vorhanden.

Aktuell verknüpft Sciebo RDS verschiedene Dienste, um Ihre Daten aus der Hochschulcloud aus zu publizieren oder zu archivieren. Sie benötigen keine aufwendigen Umwandlungen oder Transfers per Hand durchführen: Das übernimmt Sciebo RDS für Sie.

Für weitere Informationen, sehen Sie sich gerne auf der [offiziellen Webseite](https://www.research-data-services.org/de/) um.""",
        },
        {
            "question": "Kontoverwaltung",
            "answer": """Sciebo RDS nutzt die Oauth2-Technologie, um Informationen mit Diensten auszutauschen im Namen des/der Nutzer:in ohne das Passwörter oder andere kritische Daten ausgetauscht werden müssen.
Durch diese Technologie wird dem Nutzenden alle Berechtigungen durch Sciebo RDS transparent gemacht. Ist die Dienstleistung durch Sciebo RDS nicht mehr erwünscht, können die Zugriffsrechte ohne weiteres durch den Nutzenden wieder entzogen werden.

Es ist nicht notwendig, dass sie alle Dienste aktivieren. Wählen Sie lediglich alle Dienste aus mit denen sie bereits arbeiten. Später können sie weiterhin Dienste hinzufügen oder entfernen.

**Services aktivieren / Deaktivieren**

Um einen Dienst hinzuzufügen, klicken Sie bitte im linken Menü auf Dienste. Anschließend erhalten Sie eine Übersicht über alle verfügbaren Dienste. Wählen Sie den gewünschten Dienst aus. Anschließend fährt die Konfiguration für den gewählten Dienst darunter aus.
Nun klicken Sie auf den Knopf *verbinden*: Es öffnet sich ein neuer Tab und sie können dort nun sehen, was der Dienst von Ihnen benötigt, um Sciebo RDS die Zugriffsrechte geben zu können. Bei den meisten Dienstleistungen wird dies ein Konto für den entsprechenden Dienst sein.

Sobald Sie Sciebo RDS die Zugriffsrechte für ihren Account für den Dienst gegeben haben, wird alles im Hintergrund für Sie erledigt. Somit können Sie anschließend die Konfiguration für ein Projekt aufrufen und den eben angelegten Dienst hinterlegen.

Sollten Sie ein Dienst deaktivieren wollen, so gehen sie wie bei aktivieren vor, klicken jedoch auf ein bereits aktivierten Dienst und dann auf *trennen*. Sciebo RDS wird den Zugriff zurückgeben. Sämtliche Daten, welche durch das Zugriffsrecht beim Dienst hochgeladen wurden, sind davon unberührt.
Falls Sie sich sicher sein möchten, dass sämtliche Rechte Sciebo RDS entzogen werden, so müssen sie manuell im ehemals aktivierten Dienst diese Berechtigung entziehen. Es ist Sciebo RDS nicht bei allen Diensten möglich, dies automatisch zu tun.

**Konto verwalten / löschen**

Bei der ersten Verwendung von Sciebo RDS, haben sie ein Konto angelegt, worunter alle Dienstzugriffe verwaltet werden. Sie müssen dieses Konto nicht stetig verlängern. Solange Ihr Sciebo Account valide ist, wird auch Sciebo RDS aktiv sein.
Sie können diesen Account löschen, womit sämtliche Daten von Sciebo RDS gelöscht werden. Daten, welche zuvor veröffentlicht wurden, sind davon unberührt. Auch alle Daten, welche in Sciebo liegen, werden dabei nicht angefasst.

Sie können den Sciebo RDS Account löschen, indem sie unten links auf *Einstellungen* drücken und auf das erscheinende Fenster unten auf *RDS löschen* drücken. Dort werden die Konsequenzen noch einmal aufgezählt. Sobald das bestätigt wird, ist der Sciebo RDS unwiderbringlich gelöscht.""",
        },
        {
            "question": "Daten veröffentlichen",
            "answer": """Prinzipiell können alle Daten und -formate durch Sciebo RDS veröffentlicht werden, da keinerlei Einsicht in diese von nöten ist. Aber der Nachnutzbarkeit durch Dritte ist es natürlich förderlich, wenn Sie keine binären noch proprietäre, sondern frei verfügbare, Format bei dem Transferprozess angeben.
Außerdem sollten die Daten eine gewisse Größe nicht überschreiten, da sonst der Transferprozess von Seiten des Dienstleisters abgebrochen werden könnte. Zum Beispiel besitzt Zenodo eine Obergrenze von 50 GB.

Um Daten zu veröffentlichen, benötigen Sie ein Projekt, welches Sie durch die Konfiguration und die Angabe von Metadaten leitet. Sie können sämtliche Daten noch vor der Veröffentlichung ändern.
Sobald Ihre Daten jedoch veröffentlich wurden, können Sie das dazugehörige Projekt nicht mehr bearbeiten.
Falls Daten erneut veröffentlicht werden, so muss ein neues Projekt angelegt werden.

Dies gewährleistet, dass Daten immer mit einer einzigartigen Identifikationsnummer (kurz DOI) versehen werden können.

**Projekte anlegen**

Um ein Projekt anzulegen, klicken Sie links im Menü auf Projekte. Im darauffolgenden Fenster sehen Sie unten rechts ein grünes Plus. Sobald Sie darauf klicken, wird ein neues Projekt erzeugt.
In diesem Projekt ist nichts konfiguriert. Klicken Sie nun auf das eben erzeugte Projekt, um die Konfiguration aufzurufen. Die Konfiguration finden Sie nach dem Klick auf das entsprechende Projekt direkt darunter.

Geben Sie nun alle benötigten Informationen an. Zuerst muss ein Ordner ausgewählt werden, welcher die zu veröffentlichenden Daten beinhaltet. Anschließend müssen die Dienste ausgewählt werden, welche die Daten erhalten sollen. Sollten hier keine Dienste auswählbar sein, müssen Sie erst welche unter *Dienste* hinterlegen. Wie sie das tun, steht in einem anderen Hilfekästchen.
Sobald nun alle Informationen hinterlegt wurden, können Sie auf *Weiter* drücken. Nun sehen Sie ein weiteres Fenster, worin Sie ihre Metadaten eintragen können. Wie dies zu verwenden ist, steht ebenfalls in einem weiteren Hilfekästchen. Im letzten Fenster können Sie nun nocheinmal Ihre Angaben einsehen und ggfs. zurückgehen, um die Informationen anzupassen.
Sollten Sie mit Ihren Angaben zufrieden sein, so können Sie nun die Daten veröffentlichen. Herzlichen Glückwunsch: Ihre Daten sind nun auf den angegeben Diensten veröffentlicht worden und stehen der Allgemeinheit zur Verfügung.

Sollten Sie falsche Angaben gemacht haben bei den Metadaten oder der Konfiguration, so müssen sie diese per Hand, falls möglich, im entsprechenden Dienst anpassen. Sciebo RDS bietet dafür noch keine Funktionalität.
"""
        }, {
            "question": "Metadaten verwalten",
            "answer": """Falls Sie falsche oder unvollständige (Meta)daten veröffentlicht haben, können diese nicht über Sciebo RDS bearbeitet werden. Falls der gewählte Dienst es zulässt, können die Daten dort manuell bearbeitet werden. Andernfalls erzeugen sie eine neue Veröffentlichung und machen dort die gewollten Änderungen publik.

Aktuell lässt Sciebo RDS keine Aktualisierung von veröffentlichten Projekten zu. Dies liegt u.a. daran, dass viele Dienste einen speziellen Identifier (DOI) den Daten vergeben. Der Sinn dahinter ist, dass in Veröffentlichungen eine Referenz auf diese DOI gegeben werden kann und der Verfassende kann sich darauf verlassen, dass sich hinter der DOI der Inhalt verbirgt, welcher zur Veröffentlichung dort zu finden war.
Könnten sich Inhalte hinter der DOI durch Aktualisierungen ändern, wäre der Sinn hinter diesen verfehlt. Einige Dienst (wie Zenodo) lassen jedoch eine Aktualisierung durch das Vergeben einer verwandten DOI zu. Sciebo RDS unterstützt dies aber zum aktuellen Zeitpunkt nicht.
Dies könnte sich in Zukunft jedoch ändern.
            """
        }
    ],
    "en": [
        {
            "question": "This is the first question.",
            "answer": "This is the first answer.",
        },
        {
            "question": "This is the second question.",
            "answer": "This is the second answer.",
        },
    ],
}
