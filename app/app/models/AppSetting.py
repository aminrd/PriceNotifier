from django.db import models


class Settings(models.Model):
    # key=SECTION::KEY
    key = models.CharField(primary_key=True, max_length=128)
    value = models.CharField(max_length=512)

    def get_section(self):
        return self.key.split("::")[0].split(":")[0]

    def get_key_name(self):
        return self.key.split("::")[0].split(":")[1]

    def get_icon(self):
        section = self.get_section()
        if section == "notif":
            return '<i class="fa-solid fa-bell" style="color: #74C0FC;"></i>'
        elif section == "app":
            return '<i class="fa-solid fa-gears" style="color: #74C0FC;"></i>'
        else:
            return ''

    def get_name(self):
        return self.key.split("::")[1]