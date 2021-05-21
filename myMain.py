import pprint
import veryfi
import requests

import json

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QPushButton, QPlainTextEdit
from PyQt5.QtCore import Qt

client_id = "vrfUR8DYFLHXG3orIhUlLc0TD83UwvmzV4fjkTU"
client_secret = "BOoL0NjknVwbyykJUETv4DPImDKMfCMGMXBc9nOef8W4IglYd7XYcb9Obz80M3UllRMVesifNOy6ip4SJupEgTpBKZUyROi6M5N7ZGcNwEplal8MXXNeNofVXcUcVj5z"
username = "javalenz25"
api_key = "c107386d8bf3dc9cfe78dbb2845947f9"
ENVIRONMENT_URL = "https://api.veryfi.com/"

class ListBoxWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.resize(200, 200)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            links = []
            for url in event.mimeData().urls():

                if url.isLocalFile():
                    links.append(str(url.toLocalFile()))
                else:
                    links.append(str(url.toString()))
            self.addItems(links)
        else:
            event.ignore()


def create_json(response):
    list_lineitem_dictionaries = response.json()["line_items"]
    parsed_list = []

    for dictionary in list_lineitem_dictionaries:
        line_item = {
            "item_description": dictionary["description"],
            "item_price": dictionary["total"]
        }
        parsed_list.append(line_item)

    receipt = {}  # final json output
    receipt["items"] = parsed_list

    receipt["subtotal"] = response.json()["subtotal"]
    receipt["tax"] = response.json()["tax"]
    receipt["total"] = response.json()["total"]

    pprint.pprint(receipt)
    return json.dumps(receipt)


class AppDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1200, 600)

        self.listbox_view = ListBoxWidget(self)

        self.btn = QPushButton('Get Value', self)
        self.btn.setGeometry(200, 400, 200, 50)
        self.btn.clicked.connect(lambda: print(self.getSelectedItem()))

        # Add text field
        self.json_text_field = QPlainTextEdit(self)
        self.json_text_field.insertPlainText("json file will be printed here.\n")
        self.json_text_field.move(500, 10)
        self.json_text_field.resize(400, 580)
        self.json_text_field.setReadOnly(True)
        #self.json_label.setBackgroundRole(QPalette::Shadow)


    def getSelectedItem(self):
        if self.listbox_view.count():
            path = QListWidgetItem(self.listbox_view.currentItem())
            print("processing...")
            client = veryfi.Client(client_id, client_secret, username, api_key)
            categories = ["Description", "Price", "Total"]
            json_result = client.process_document( fr"{path.text()}", categories)
            print(type(json_result))
            print(json_result["id"])
            document_id = json_result["id"]
            print("...done")
            CLIENT_ID = client_id
            url = '{0}api/v7/partner/documents/{1}/'.format(ENVIRONMENT_URL, document_id)
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "CLIENT-ID": CLIENT_ID,
                "AUTHORIZATION": "apikey {0}:{1}".format(username, api_key)
            }
            response = requests.get(url=url, headers=headers)
            json_file = create_json(response)
            self.json_text_field.setPlainText(json_file)
        else:
            print("list is empty!")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = AppDemo()
    demo.show()

    sys.exit(app.exec_())