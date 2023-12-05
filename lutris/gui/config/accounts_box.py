from gettext import gettext as _

from gi.repository import Gtk

from lutris import settings
from lutris.gui.config.base_config_box import BaseConfigBox
from lutris.util.steam.config import STEAM_ACCOUNT_SETTING, get_steam_users


class AccountsBox(BaseConfigBox):

    def __init__(self):
        super().__init__()
        self.add(self.get_section_label(_("Steam accounts")))
        self.add(self.get_description_label(
            _("Select which Steam account is used for Lutris integration and creating Steam shortcuts.")
        ))
        frame = Gtk.Frame(visible=True, shadow_type=Gtk.ShadowType.ETCHED_IN)
        self.pack_start(frame, False, False, 12)

        vbox = Gtk.VBox(visible=True)
        frame.add(vbox)

        main_radio_button = None
        active_steam_account = settings.read_setting(STEAM_ACCOUNT_SETTING)
        steam_users = get_steam_users()
        for account in steam_users:
            radio_button = Gtk.RadioButton.new_with_label_from_widget(
                main_radio_button,
                account["PersonaName"]
            )
            radio_button.set_margin_top(16)
            radio_button.set_margin_start(16)
            radio_button.set_margin_bottom(16)
            radio_button.show()
            radio_button.set_active(active_steam_account == account["steamid64"])
            radio_button.connect("toggled", self.on_steam_account_toggled, account["steamid64"])
            vbox.pack_start(radio_button, True, True, 0)
            if not main_radio_button:
                main_radio_button = radio_button
        if not steam_users:
            vbox.pack_start(Gtk.Label(_("No Steam account found"), visible=True), True, True, 0)

    def on_steam_account_toggled(self, radio_button, steamid64):
        """Handler for switching the active Steam account."""
        settings.write_setting(STEAM_ACCOUNT_SETTING, steamid64)
