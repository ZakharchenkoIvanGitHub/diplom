import pytest
import yaml
from send_report_to_email import send_message_to_email

if __name__ == "__main__":
    with open("config.yaml", encoding="utf-8") as f:
        testdata = yaml.safe_load(f)
    pytest.main()
    send_message_to_email(testdata['fromaddr_report'],
                          testdata['toaddr_report'],
                          testdata['mail_password'],
                          "report.html")
